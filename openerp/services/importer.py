import importlib


class Importer:
    def __init__(self, plugins: list[str]):
        self.app_list = []
        self.plugins = plugins
        self.import_plugins()

    def import_plugins(self):
        """
        Loop through the list of plugins and import
            - Variables `title`, `description`, `author`, `version`
            - FastAPI app `app` which can be mounted in the main app
            - The List of `available_resources`
            - List of requested scopes `data_scopes`
        """
        for plugin_name in self.plugins:
            print(f"Importing plugin: {plugin_name}")
            plugin = importlib.import_module(plugin_name)
            app_dict = {
                "name": plugin_name,
                "title": plugin.title,
                "description": plugin.description,
                "author": plugin.author,
                "version": plugin.version,
                "app": plugin.app,
                "available_resources": plugin.available_resources,
                "data_scopes": plugin.data_scopes,
            }

            self.app_list.append(app_dict)
