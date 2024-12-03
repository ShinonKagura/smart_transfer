import zipfile
from compression_plugin_base import CompressionPlugin

class ZipCompressionPlugin(CompressionPlugin):
    def compress(self, data):
        raise NotImplementedError("ZIP compression not yet implemented for raw data.")

    def decompress(self, file_path, output_folder):
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(output_folder)
            print(f"ZIP file extracted to {output_folder}")
        except Exception as e:
            print(f"Error extracting ZIP file: {e}")

    @staticmethod
    def get_name():
        return "zip"
