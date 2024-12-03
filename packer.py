import os

class Packer:
    def __init__(self, plugin):
        self.plugin = plugin

    def pack_file(self, file_path, output_path):
        try:
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

            # Speichere den Header
            header_path = output_path + ".hdr"
            with open(header_path, 'w') as header_file:
                for key, value in header.items():
                    header_file.write(f"{key}:{value}\n")

            # Speichere die komprimierten Daten
            bin_path = output_path  # Keine zusätzliche ".bin" anhängen
            with open(bin_path, 'wb') as bin_file:
                for block in blocks:
                    bin_file.write(block)

            print(f"File packed and saved to {bin_path}.")
        except Exception as e:
            print(f"Error packing the file: {e}")
