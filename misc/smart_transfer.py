import os
import zstandard as zstd
import threading
from tkinter import Tk, filedialog

# Sender module to handle file compression and preparation for transfer
class SmartTransferSender:
    def __init__(self, file_path, block_size=1024 * 1024):  # Default block size is 1 MB
        self.file_path = file_path
        self.block_size = block_size
        self.blocks = []
        self.header = None

    def analyze_and_compress(self):
        """
        Reads the input file, splits it into blocks, compresses each block, 
        and stores the compressed blocks with metadata for later use.
        """
        print("Analyzing and compressing the file...")
        compressor = zstd.ZstdCompressor()

        block_metadata = []  # To store block-specific metadata like compressed size

        with open(self.file_path, 'rb') as file:
            while chunk := file.read(self.block_size):  # Read file in chunks of block_size
                compressed_chunk = compressor.compress(chunk)  # Compress each chunk
                self.blocks.append(compressed_chunk)  # Store the compressed block
                block_metadata.append(len(compressed_chunk))  # Record the size of the block

        # Create a header containing metadata for reconstruction
        self.header = {
            "original_size": os.path.getsize(self.file_path),
            "block_count": len(self.blocks),
            "block_sizes": block_metadata
        }

        print(f"File split into {len(self.blocks)} compressed blocks.")

    def save_header(self, output_path):
        """
        Writes the metadata header to a separate .hdr file for use during reconstruction.
        """
        header_path = output_path + ".hdr"
        with open(header_path, 'w') as header_file:
            for key, value in self.header.items():
                header_file.write(f"{key}:{value}\n")
        print(f"Header saved to {header_path}.")

    def save_debug_info(self, output_path):
        """
        Generates a .debug file containing information about the compression process,
        including file sizes and block details.
        """
        debug_path = output_path + ".debug"
        total_compressed_size = sum(len(block) for block in self.blocks)
        with open(debug_path, 'w') as debug_file:
            debug_file.write(f"Original file size: {self.header['original_size']} bytes\n")
            debug_file.write(f"Compressed file size: {total_compressed_size} bytes\n")
            debug_file.write(f"Number of blocks: {self.header['block_count']}\n")
            debug_file.write(f"Block sizes: {self.header['block_sizes']}\n")
        print(f"Debug information saved to {debug_path}.")

    def send(self, receiver):
        """
        Simulates sending compressed blocks to the receiver using threading. 
        Each block is sent in a separate thread for parallelism.
        """
        print("Sending blocks to receiver...")
        for index, block in enumerate(self.blocks):
            threading.Thread(target=receiver.receive_block, args=(index, block)).start()


# Receiver module to handle file reconstruction from compressed blocks
class SmartTransferReceiver:
    def __init__(self, total_blocks):
        self.received_blocks = [None] * total_blocks  # Placeholder for received blocks
        self.lock = threading.Lock()  # Ensures thread-safe access to shared resources
        self.missing_blocks = []  # Tracks missing blocks for retransmission

    def receive_block(self, index, block):
        """
        Simulates the receipt of a block and stores it in the correct order.
        Thread-safe to handle simultaneous reception of multiple blocks.
        """
        with self.lock:
            self.received_blocks[index] = block
            print(f"Block {index + 1} received.")

    def verify_blocks(self):
        """
        Verifies that all blocks have been received. 
        Returns True if all blocks are present, False otherwise.
        """
        self.missing_blocks = [i for i, block in enumerate(self.received_blocks) if block is None]
        if self.missing_blocks:
            print(f"Missing blocks detected: {self.missing_blocks}")
            return False
        return True

    def request_missing_blocks(self, sender):
        """
        Requests retransmission of missing blocks from the sender.
        """
        if self.missing_blocks:
            print(f"Requesting retransmission for blocks: {self.missing_blocks}")
            for index in self.missing_blocks:
                threading.Thread(target=sender.retransmit_block, args=(index, self)).start()

    def reconstruct_file(self, output_path):
        """
        Reconstructs the original file by decompressing and combining all received blocks.
        Writes the final output to the specified path.
        """
        print("Verifying blocks...")
        if not self.verify_blocks():
            print("Cannot reconstruct file. Missing blocks.")
            return

        print("Reconstructing the file...")
        decompressor = zstd.ZstdDecompressor()

        with open(output_path, 'wb') as output_file:
            for block in self.received_blocks:
                if block is not None:
                    decompressed_data = decompressor.decompress(block)  # Decompress block
                    output_file.write(decompressed_data)  # Write decompressed data to file

        print(f"File reconstructed and saved to {output_path}.")

        # Save debug information about the reconstructed file
        reconstructed_size = os.path.getsize(output_path)
        debug_path = output_path + ".debug"
        with open(debug_path, 'a') as debug_file:
            debug_file.write(f"Reconstructed file size: {reconstructed_size} bytes\n")
        print(f"Reconstructed file size added to debug information.")

# Sender retransmission capability
class SmartTransferSenderWithRetransmit(SmartTransferSender):
    def retransmit_block(self, index, receiver):
        """
        Simulates retransmission of a specific block to the receiver.
        """
        print(f"Retransmitting block {index + 1}...")
        threading.Thread(target=receiver.receive_block, args=(index, self.blocks[index])).start()


# Main application entry point
if __name__ == "__main__":
    # GUI setup for selecting input and output files
    Tk().withdraw()  # Hide the root Tkinter window

    # Select the input file for processing
    print("Please select the file to process:")
    input_file_path = filedialog.askopenfilename(title="Select File")

    if not input_file_path:
        print("No file selected. Exiting.")
        exit()

    # Suggest the original filename with a suffix for the output file
    default_output_name = os.path.splitext(os.path.basename(input_file_path))[0] + "_compressed"

    # Select the output file location and name
    print("Please select where to save the reconstructed file:")
    output_file_path = filedialog.asksaveasfilename(title="Save File As", defaultextension=".bin", initialfile=default_output_name)

    if not output_file_path:
        print("No output location selected. Exiting.")
        exit()

    # Initialize sender and receiver modules
    sender = SmartTransferSenderWithRetransmit(input_file_path)
    sender.analyze_and_compress()  # Analyze and compress the input file
    sender.save_header(output_file_path)  # Save metadata header
    sender.save_debug_info(output_file_path)  # Save debug information

    receiver = SmartTransferReceiver(total_blocks=len(sender.blocks))
    sender.send(receiver)  # Simulate sending the compressed blocks

    # Wait for all blocks to be received (simplified synchronization)
    threading.Event().wait(1)  # Allow threads to finish

    # Request retransmission for missing blocks
    receiver.request_missing_blocks(sender)

    # Wait for retransmitted blocks
    threading.Event().wait(1)

    # Reconstruct the file from the received blocks
    receiver.reconstruct_file(output_file_path)

    # Verify the result by comparing the reconstructed file with the original
    if os.path.exists(output_file_path):
        if open(input_file_path, 'rb').read() == open(output_file_path, 'rb').read():
            print("File transfer and reconstruction successful!")
        else:
            print("File reconstruction failed: Content mismatch.")
