from unpacker import Unpacker
import os

class SmartTransferReceiver:
    def __init__(self, plugin):
        self.unpacker = Unpacker(plugin)

    def receive(self, packed_file_path, output_folder):
        # Empfangsvorgang für 'packed_file_path'
        self.unpacker.unpack_file(packed_file_path, output_folder)

    def receive_block(self, index, block):
        self.received_blocks[index] = block
        print(f"Block {index + 1} received.")

    def verify_blocks(self):
        self.missing_blocks = [i for i, block in enumerate(self.received_blocks) if block is None]
        if self.missing_blocks:
            print(f"Missing blocks: {self.missing_blocks}")
            return False
        return True

    def request_missing_blocks(self, sender):
        for index in self.missing_blocks:
            print(f"Requesting retransmission for block {index + 1}...")
            sender.retransmit_block(index, self)

    def reconstruct_file(self, output_folder, decompression_plugin):
        print("Reconstructing the file...")
        try:
            # Header-Daten auslesen (Dateiname)
            header_file_path = self.file_path + ".hdr"
            with open(header_file_path, 'r') as header_file:
                header = {}
                for line in header_file:
                    key, value = line.strip().split(":")
                    header[key] = value

            original_filename = header.get("original_filename", "output_file")

            # Dekodierte Datei im richtigen Ordner speichern
            output_file_path = os.path.join(output_folder, original_filename)
            
            with open(output_file_path, 'wb') as output_file:
                for block in self.received_blocks:
                    if block is not None:
                        decompressed_data = decompression_plugin.decompress(block)
                        output_file.write(decompressed_data)

            print(f"File reconstructed and saved to {output_file_path}.")
        except Exception as e:
            print(f"Error during file reconstruction: {e}")