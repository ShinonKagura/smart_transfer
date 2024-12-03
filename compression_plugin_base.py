class CompressionPlugin:
    def compress(self, data):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def decompress(self, data):
        raise NotImplementedError("This method should be implemented by subclasses.")

    @staticmethod
    def get_name():
        raise NotImplementedError("This method should be implemented by subclasses.")
