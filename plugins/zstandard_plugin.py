import zstandard as zstd
from compression_plugin_base import CompressionPlugin

class ZstdCompressionPlugin(CompressionPlugin):
    def compress(self, data):
        compressor = zstd.ZstdCompressor()
        return compressor.compress(data)

    def decompress(self, data):
        decompressor = zstd.ZstdDecompressor()
        return decompressor.decompress(data)

    @staticmethod
    def get_name():
        return "zstandard"