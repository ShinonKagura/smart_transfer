import os

class Unpacker:
    def __init__(self, compression_manager):
        self.manager = compression_manager

    def unpack_file(self, input_file_path, output_folder):
        """
        Entpackt die Datei basierend auf dem Plugin, das den Dateityp unterstützt.
        :param input_file_path: Pfad zur komprimierten Datei.
        :param output_folder: Zielordner für die entpackten Dateien.
        """
        print("Unpacking the file...")

        # Header lesen
        header_path = input_file_path + ".hdr"
        if not os.path.exists(header_path):
            print(f"Header file not found: {header_path}")
            return

        # Header-Daten einlesen
        header = {}
        with open(header_path, 'r') as header_file:
            for line in header_file:
                key, value = line.strip().split(":")
                header[key] = value

        # Ursprünglichen Dateinamen aus dem Header verwenden
        original_filename = header.get("original_filename", "output_file")
        output_file_path = os.path.join(output_folder, original_filename)

        # Plugin ermitteln
        compression_method = header.get("compression_method")
        if not compression_method:
            print("Compression method not specified in the header.")
            return

        plugin = self.manager.get_plugin(compression_method)
        if not plugin:
            print(f"Plugin for compression method '{compression_method}' not found.")
            return

        # Datei dekomprimieren
        try:
            temp_decompressed_file = os.path.join(output_folder, os.path.basename(input_file_path) + '_decompressed')
            plugin.decompress(input_file_path, output_folder)

            # Umbenennen der Datei
            if os.path.exists(temp_decompressed_file):
                os.rename(temp_decompressed_file, output_file_path)
                print(f"File unpacked and saved to {output_file_path}.")
            else:
                print("Decompressed file not found. Unpacking failed.")

        except Exception as e:
            print(f"Error during unpacking: {e}")
