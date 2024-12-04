import os

class Packer:
    def __init__(self, plugin):
        self.plugin = plugin

    def pack_file(self, file_path, output_path):
        """
        Packt die Datei und speichert die Daten in Blöcken, Header und Debug-Informationen.
        :param file_path: Pfad zur Eingabedatei.
        :param output_path: Zielpfad für die komprimierten Daten.
        """
        print("Packing the file...")
        block_metadata = []
        blocks = []

        with open(file_path, 'rb') as file:
            while chunk := file.read(1024 * 1024):  # Blockgröße: 1 MB
                compressed_chunk = self.plugin.compress(chunk)
                blocks.append(compressed_chunk)
                block_metadata.append(len(compressed_chunk))

        header = {
            "original_size": os.path.getsize(file_path),
            "block_count": len(blocks),
            "block_sizes": block_metadata,
            "compression_method": self.plugin.get_name(),
            "original_filename": os.path.basename(file_path),
        }

        # Header speichern
        header_path = bin_path + ".hdr"
        with open(header_path, 'w') as header_file:
            for key, value in header.items():
                header_file.write(f"{key}:{value}\n")

        # Komprimierte Daten speichern
        bin_path = output_path if output_path.endswith(".bin") else output_path + ".bin"
        with open(bin_path, 'wb') as bin_file:
            for block in blocks:
                bin_file.write(block)

        # Debug-Informationen speichern
        debug_path = bin_path + ".debug"
        total_compressed_size = sum(len(block) for block in blocks)
        with open(debug_path, 'w') as debug_file:
            debug_file.write(f"Original filename: {header['original_filename']}\n")
            debug_file.write(f"Original file size: {header['original_size']} bytes\n")
            debug_file.write(f"Compressed file size: {total_compressed_size} bytes\n")
            debug_file.write(f"Number of blocks: {header['block_count']}\n")
            debug_file.write(f"Block sizes: {header['block_sizes']}\n")
            debug_file.write(f"Compression method: {header['compression_method']}\n")

        print(f"File packed and saved to {bin_path}.")