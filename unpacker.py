class Unpacker:
    def __init__(self, compression_manager):
        self.manager = compression_manager

    def unpack_file(self, file_path, output_folder):
        extension = os.path.splitext(file_path)[-1].lower()
        plugin_name = self.detect_plugin_by_extension(extension)
        plugin = self.manager.get_plugin(plugin_name)
        if plugin:
            plugin.decompress(file_path, output_folder)
        else:
            print(f"No plugin available for extension: {extension}")

    def detect_plugin_by_extension(self, extension):
        extension_map = {
            '.zip': 'zip',
            # Weitere Erweiterungen wie '.rar', '.7z' können hier hinzugefügt werden
        }
        return extension_map.get(extension, None)
