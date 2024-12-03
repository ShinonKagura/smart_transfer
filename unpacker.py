import os

class Unpacker:
    def __init__(self, plugin):
        self.plugin = plugin

    def unpack_file(self, input_file_path, output_folder):
        try:
            print("Unpacking the file...")

            # Header-Datei suchen
            header_path = input_file_path + ".hdr"  # Kein zusätzliches ".bin" erwartet
            if not os.path.exists(header_path):
                print(f"Header file not found: {header_path}")
                return

            # Header-Daten auslesen
            with open(header_path, 'r') as header_file:
                header = {}
                for line in header_file:
                    key, value = line.strip().split(":")
                    header[key] = value

            # Ursprünglichen Dateinamen aus dem Header rekonstruieren
            original_filename = header.get("original_filename", "output_file")
            output_file_path = os.path.join(output_folder, original_filename)

            # Komprimierte Daten dekomprimieren und speichern
            with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
                while chunk := input_file.read(8192):  # Blockgröße: 8 KB
                    decompressed_chunk = self.plugin.decompress(chunk)
                    output_file.write(decompressed_chunk)

            print(f"File unpacked and saved to {output_file_path}.")
        except Exception as e:
            print(f"Error unpacking the file: {e}")
