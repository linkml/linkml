import gzip
import ijson

from linkml.validator.parsers.base import BaseParser

class JsonParser(BaseParser):
    """
    Parser for parsing delimited file formats. 
    """

    def __init__(self, **kwargs):
        super().__init__()

    def parse(self, filename: str, format: str, compressed: bool = False, **kwargs):
        """
        Parse a JSON file and stream records.

        Args:
            filename: The filename
            format: The file format
            compressed: Whether or not the file is gzip compressed
            kwargs: Additional arguments

        """
        if compressed:
            handle = gzip.open(filename, 'rb')
        else:
            handle = open(filename, 'r')
        reader = ijson.items(handle, 'item')
        for obj in reader:
            yield obj
