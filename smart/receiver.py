import os

class SmartTransferReceiver:
    def __init__(self, total_blocks):
        self.received_blocks = [None] * total_blocks
        self.missing_blocks = []

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

    def reconstruct_file(self, output_path, decompression_plugin):
        print("Reconstructing the file...")

        with open(output_path, 'wb') as output_file:
            for block in self.received_blocks:
                if block is not None:
                    decompressed_data = decompression_plugin.decompress(block)
                    output_file.write(decompressed_data)

        print(f"File reconstructed and saved to {output_path}.")