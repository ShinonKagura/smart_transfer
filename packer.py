class Packer:
    def __init__(self, plugin):
        """
        :param plugin: Kompressionsplugin, das für das Packen verwendet wird.
        """
        self.plugin = plugin

    def pack_file(self, input_file, output_file):
        """
        Packt die Datei mit dem Plugin und speichert sie im Zielpfad.
        :param input_file: Pfad zur Eingabedatei.
        :param output_file: Pfad zur Ausgabedatei.
        """
        try:
            print("Packing the file...")
            with open(input_file, 'rb') as f:
                data = f.read()

            compressed_data = self.plugin.compress(data)
            if compressed_data is None:
                print("Packing failed: Compression plugin returned no data.")
                return

            with open(output_file, 'wb') as f:
                f.write(compressed_data)

            print(f"File packed and saved to {output_file}.")
        except Exception as e:
            print(f"Error packing the file: {e}")
