import os
import zstandard as zstd
from compression_plugin_base import CompressionPlugin

class ZstdCompressionPlugin(CompressionPlugin):
    def compress(self, data):
        compressor = zstd.ZstdCompressor()
        return compressor.compress(data)

    def decompress(self, input_file_path, output_folder):
        try:
            print(f"Decompressing file: {input_file_path}")
            if not os.path.exists(input_file_path):
                print(f"Input file does not exist: {input_file_path}")
                return

            if not os.path.exists(output_folder):
                print(f"Output folder does not exist. Creating: {output_folder}")
                os.makedirs(output_folder)

            output_file_path = os.path.join(output_folder, os.path.basename(input_file_path) + '_decompressed')

            with open(input_file_path, 'rb') as compressed_file, open(output_file_path, 'wb') as output_file:
                decompressor = zstd.ZstdDecompressor()
                with decompressor.stream_reader(compressed_file) as reader:
                    while True:
                        chunk = reader.read(8192)
                        if not chunk:
                            break
                        output_file.write(chunk)

            print(f"Decompressed data saved to: {output_file_path}")
        except Exception as e:
            print(f"Error during decompression: {e}")

    @staticmethod
    def get_name():
        return "zstandard"
