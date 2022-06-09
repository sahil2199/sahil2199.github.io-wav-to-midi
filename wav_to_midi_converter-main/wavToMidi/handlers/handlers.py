from converter.converter import Converter


# handler to call the convert logic
class ConvertHandler:

    # caller method for conversion logic
    @staticmethod
    def convert_file(source_fname, target_fname):
        Converter.convert_file(source_fname, target_fname)
