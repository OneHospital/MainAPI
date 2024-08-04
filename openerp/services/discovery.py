from openerp.config import Config


class Doscovery:
    def __init__(self):
        self.plugins = []
        self.discover()

    def discover(self):
        content = self.read_file()
        # Remove item containing '' from the list
        self.plugins = list(filter(None, content))
        print(self.plugins)

    @staticmethod
    def read_file() -> list:
        with open(Config.PLUGINS_LIST) as f:
            return f.read().splitlines()
