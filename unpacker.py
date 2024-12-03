class Unpacker:
    def __init__(self, compression_manager):
        """
        :param compression_manager: Instanz des CompressionManager zur Verwaltung von Plugins.
        """
        self.manager = compression_manager

    def unpack_file(self, file_path, output_folder):
        """
        Entpackt die Datei basierend auf dem Plugin, das den Dateityp unterstützt.
        :param file_path: Pfad zur Eingabedatei.
        :param output_folder: Ordner, in dem die entpackten Dateien gespeichert werden.
        """
        try:
            print(f"Attempting to unpack file: {file_path}")
            extension = os.path.splitext(file_path)[-1].lower()
            print(f"Detected file extension: {extension}")

            plugin_name = self.detect_plugin_by_extension(extension)
            print(f"Identified plugin: {plugin_name}")

            if not plugin_name:
                print(f"No plugin available for extension: {extension}")
                return

            plugin = self.manager.get_plugin(plugin_name)
            if not plugin:
                print(f"Plugin '{plugin_name}' could not be loaded.")
                return

            print(f"Using plugin '{plugin_name}' to unpack the file...")
            plugin.decompress(file_path, output_folder)
            print("Unpacking completed.")
        except Exception as e:
            print(f"Error during unpacking: {e}")


    def detect_plugin_by_extension(self, extension):
        """
        Erkennt das passende Plugin basierend auf der Dateierweiterung.
        :param extension: Dateierweiterung der Eingabedatei.
        :return: Name des Plugins, das die Erweiterung unterstützt.
        """
        extension_map = {
            '.zip': 'zip',
            # Weitere Erweiterungen wie '.rar', '.7z' können hier ergänzt werden.
        }
        return extension_map.get(extension, None)
