import zstandard as zstd
from compression_plugin_base import CompressionPlugin

class ZstdCompressionPlugin(CompressionPlugin):
    def compress(self, data):
        """
        Komprimiert die Rohdaten mit Zstandard.
        :param data: Rohdaten als Bytes.
        :return: Komprimierte Daten als Bytes.
        """
        compressor = zstd.ZstdCompressor()
        return compressor.compress(data)

    def decompress(self, file_path, output_folder):
        """
        Dekomprimiert eine Datei, die mit Zstandard komprimiert wurde.
        :param file_path: Pfad zur komprimierten Datei.
        :param output_folder: Ordner, in dem die dekomprimierten Daten gespeichert werden.
        """
        try:
            with open(file_path, 'rb') as f:
                compressed_data = f.read()

            decompressor = zstd.ZstdDecompressor()
            decompressed_data = decompressor.decompress(compressed_data)

            # Speichere die dekomprimierten Daten in einer Datei
            output_file = os.path.join(output_folder, "decompressed_output")
            with open(output_file, 'wb') as f:
                f.write(decompressed_data)

            print(f"Decompressed data saved to {output_file}.")
        except Exception as e:
            print(f"Error during decompression: {e}")

    @staticmethod
    def get_name():
        return "zstandard"
