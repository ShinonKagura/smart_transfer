import importlib
import os
import pkgutil

from compression_plugin_base import CompressionPlugin

class CompressionManager:
    def __init__(self):
        self.plugins = {}

    def load_plugins(self):
        plugins_path = os.path.join(os.path.dirname(__file__), 'plugins')
        for finder, name, ispkg in pkgutil.iter_modules([plugins_path]):
            module_name = f'plugins.{name}'
            module = importlib.import_module(module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, CompressionPlugin) and attr is not CompressionPlugin:
                    self.plugins[attr.get_name()] = attr()

    def list_plugins(self):
        return list(self.plugins.keys())

    def get_plugin(self, name):
        return self.plugins.get(name, None)