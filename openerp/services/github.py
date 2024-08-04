import os

import httpx
from git import Repo, GitCommandError
from typing import Optional

from openerp.config import Config


class GithubService:
    plugins: list[dict[str, str]] = []

    def __init__(self, repo_url: str, access_token: Optional[str] = None):
        self.repo_url = repo_url
        self.root_dir = Config.PLUGINS_PATH
        self.access_token = access_token
        self.repo_name = self.get_repo_name()
        self.repo_dir = os.path.join(self.root_dir, self.repo_name)

    def get_repo_name(self) -> str:
        """Extracts the repository name from the URL."""
        return self.repo_url.split('/')[-1].replace('.git', '')

    def clone_repo(self) -> None:
        """Clones the repository to the specified directory."""
        if os.path.exists(self.repo_dir):
            print(f"Repository directory {self.repo_dir} already exists.")
            return

        clone_url = self._get_clone_url()
        try:
            print(f"Cloning repository from {clone_url} to {self.repo_dir}...")
            Repo.clone_from(clone_url, self.repo_dir)
            print("Repository cloned successfully.")
        except GitCommandError as e:
            print(f"Error cloning repository: {e}")

    def update_repo(self) -> None:
        """Updates the existing repository by pulling the latest changes."""
        if not os.path.exists(self.repo_dir):
            print(f"Repository directory {self.repo_dir} does not exist.")
            return

        try:
            print(f"Updating repository at {self.repo_dir}...")
            repo = Repo(self.repo_dir)
            origin = repo.remotes.origin
            origin.pull()
            print("Repository updated successfully.")
        except GitCommandError as e:
            print(f"Error updating repository: {e}")

    def replace_repo(self) -> None:
        """Replaces the existing repository by removing the old one and cloning a new one."""
        if os.path.exists(self.repo_dir):
            print(f"Removing existing repository directory {self.repo_dir}...")
            try:
                for root, dirs, files in os.walk(self.repo_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(self.repo_dir)
                print("Existing repository removed successfully.")
            except Exception as e:
                print(f"Error removing repository: {e}")
                return

        self.clone_repo()

    @classmethod
    def list_plugins(cls):
        if cls.plugins:
            return cls.plugins

        cls.plugins = []
        url = "https://api.github.com/orgs/OpenERPs/repos?type=public&sort=full_name&per_page=100"
        res = httpx.get(url)
        json = res.json()
        for repo in json:
            repo_name: str = repo['name']
            if repo_name.startswith('openerp_') and repo_name.endswith('_plugin'):
                repo = {
                    'name': repo_name,
                    'url': repo['clone_url']
                }
                cls.plugins.append(repo)

        return cls.plugins

    @classmethod
    def get_plugin(cls, plugin_id: str) -> str | None:
        if not cls.plugins:
            cls.list_plugins()

        for plugin in cls.plugins:
            if plugin.get('name') == plugin_id:
                return plugin.get('url')

    def _get_clone_url(self) -> str:
        """Returns the clone URL, including the access token if provided."""
        if self.access_token:
            # Handle token in the URL for authentication
            return self.repo_url.replace("https://", f"https://{self.access_token}@")
        return self.repo_url
