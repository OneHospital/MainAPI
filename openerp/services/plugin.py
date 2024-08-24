from os import path

from openerp.config import Config


class Plugin:

    def __init__(self, name_list: list[str] = None):
        if not name_list:
            name_list = []

        self.name_list = name_list

    def update_installed(self):
        filename = 'plugins.txt'
        plugins = self._read_file(filename)
        for name in self.name_list:
            my_plugin = f'plugins/{name}'
            plugins.append(my_plugin)
        self._write_file(plugins, filename)

    def check_installed(self) -> list[str]:
        filename = '.plugins'
        plugins = self._read_file(filename)
        return plugins

    def trigger_reboot(self):
        plugins = self._read_file()
        for name in self.name_list:
            plugins.append(name)
        self._write_file(plugins)

    @staticmethod
    def _read_file(file_name='.plugins') -> list:
        file_path = path.join(Config.ROOT_PATH, 'plugins', file_name)
        if not path.exists(file_path):
            return []

        with open(file_path) as f:
            return f.read().splitlines()

    @staticmethod
    def _write_file(plugins: list, file_name='.plugins'):
        plugins.sort()

        file_path = path.join(Config.ROOT_PATH, 'plugins', file_name)
        with open(file_path, 'w') as f:
            f.write('\n'.join(plugins))
