from packer import Packer
import os

class SmartTransferSender:
    def __init__(self, file_path, plugin):
        self.packer = Packer(plugin)
        self.file_path = file_path

    def send(self, receiver):
        packed_file_path = self.file_path + ".bin"
        self.packer.pack_file(self.file_path, packed_file_path)
        # Sendevorgang für 'packed_file_path'


    def analyze_and_compress(self):
        print("Analyzing and compressing the file...")
        block_metadata = []

        with open(self.file_path, 'rb') as file:
            while chunk := file.read(self.block_size):
                compressed_chunk = self.plugin.compress(chunk)
                self.blocks.append(compressed_chunk)
                block_metadata.append(len(compressed_chunk))

        self.header = {
            "original_size": os.path.getsize(self.file_path),
            "block_count": len(self.blocks),
            "block_sizes": block_metadata,
            "compression_method": self.plugin.get_name(),
        }
        print(f"File split into {len(self.blocks)} compressed blocks.")

    def save_compression_data(self, output_path):
        """
        Saves the compressed data blocks, header, and debug information.
        """
        # Speichere die komprimierten Blöcke in einer .bin-Datei
        bin_path = output_path + ".bin"
        with open(bin_path, 'wb') as bin_file:
            for block in self.blocks:
                bin_file.write(block)
        print(f"Compressed data saved to {bin_path}.")

        # Speichere die Header-Datei
        header_path = output_path + ".hdr"
        with open(header_path, 'w') as header_file:
            for key, value in self.header.items():
                header_file.write(f"{key}:{value}\n")
        print(f"Header saved to {header_path}.")

        # Speichere Debug-Informationen
        debug_path = output_path + ".debug"
        total_compressed_size = sum(len(block) for block in self.blocks)
        with open(debug_path, 'w') as debug_file:
            debug_file.write(f"Original filename: {os.path.basename(self.file_path)}\n")
            debug_file.write(f"Original file size: {self.header['original_size']} bytes\n")
            debug_file.write(f"Compressed file size: {total_compressed_size} bytes\n")
            debug_file.write(f"Number of blocks: {self.header['block_count']}\\n")
            debug_file.write(f"Block sizes: {self.header['block_sizes']}\\n")
            debug_file.write(f"Compression method: {self.header['compression_method']}\\n")
        print(f"Debug information saved to {debug_path}.")


    def send(self, receiver):
        print("Sending blocks to receiver...")
        for index, block in enumerate(self.blocks):
            receiver.receive_block(index, block)