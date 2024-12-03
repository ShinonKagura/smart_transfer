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
            # Dateierweiterung ermitteln
            extension = os.path.splitext(file_path)[-1].lower()
            plugin_name = self.detect_plugin_by_extension(extension)
            plugin = self.manager.get_plugin(plugin_name)

            if not plugin:
                print(f"No plugin available for extension: {extension}")
                return

            # Plugin zum Entpacken verwenden
            print(f"Using plugin '{plugin_name}' to unpack the file...")
            plugin.decompress(file_path, output_folder)
            print("Unpacking completed.")
        except Exception as e:
            # Fehler protokollieren
            print(f"Error unpacking the file: {e}")

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
