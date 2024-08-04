from dataclasses import dataclass
from os import path

# Get the path to the root
_FILE_ROOT_PATH = path.dirname(path.dirname(path.abspath(__file__)))


@dataclass
class Config:
    ROOT_PATH: str = _FILE_ROOT_PATH
    PLUGINS_PATH: str = path.join(ROOT_PATH, "plugins")
    PLUGINS_LIST: str = path.join(PLUGINS_PATH, ".plugins")
