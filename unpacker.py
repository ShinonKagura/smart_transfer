import os

class Unpacker:
    def __init__(self, compression_manager):
        self.manager = compression_manager

    def unpack_file(self, file_path, output_folder):
        print("Unpacking the file...")

        # Header lesen
        header_path = file_path + ".hdr"
        if not os.path.exists(header_path):
            print(f"Header file not found: {header_path}")
            return

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
            with open(file_path, 'rb') as input_file:
                compressed_data = input_file.read()

            decompressed_data = plugin.decompress(compressed_data)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(decompressed_data)

            print(f"File unpacked and saved to {output_file_path}.")
        except Exception as e:
            print(f"Error during unpacking: {e}")
