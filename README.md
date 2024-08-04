# MainAPI

Responsible for providing the base functionality for all plugins. Base functionality includes:

1. Authentication and authorization
2. Database connection
3. Communication with other plugins
4. Plugin discovery and management
5. Logging

## Process

1. List all plugins available in the main repository via GitHub API
2. Upon click on the installation button, clone the repo in `plugins` directory
3. Maintain a file called `plugins.txt` in the main repository, which will contain the list of path to the plugins
4. Have a file watcher in the dockerfile to watch the `plugins.txt` file for changes
5. Upon change in the `plugins.txt`, restart the container
6. At the startup of the container, install all the plugins listed in `plugins.txt`
7. Have a plugin discovery method in the main application
8. Upon startup, mount all the routes from the installed plugins
9. Check the scopes, resources and construct permissions in the DB
