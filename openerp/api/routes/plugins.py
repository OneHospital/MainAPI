from fastapi import APIRouter, HTTPException

from openerp.services.github import GithubService
from openerp.services.plugin import Plugin

router = APIRouter()


@router.get("/")
async def read_plugins():
    """
    List all the supported plugins from the official GitHub repository
    """
    plugins = GithubService.list_plugins()
    return plugins


@router.get("/{plugin_id}/install/")
async def install_plugin(plugin_id: str, reboot: bool = False):
    """
    Install a plugin from the official GitHub repository. After installation, a server reboot is required
    :param plugin_id: ID of the plugin, get from the plugin list
    :param reboot: If true reboot the server
    :return:
    """
    plugin_url = GithubService.get_plugin(plugin_id)
    if not plugin_url:
        raise HTTPException(status_code=404, detail="Plugin not found")

    git = GithubService(plugin_url)
    git.clone_repo()

    plugins = Plugin([plugin_id])
    plugins.update_installed()
    if reboot:
        plugins.trigger_reboot()

    return {"message": "Plugin installed"}
