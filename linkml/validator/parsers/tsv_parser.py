import csv
import gzip
from typing import Any

from linkml.validator.parsers.base import BaseParser

class TsvParser(BaseParser):
    """
    Parser for parsing delimited file formats. 
    """

    def __init__(self, **kwargs):
        super().__init__()

    def parse(self, filename: str, format: str, delimiter: str, compressed: bool = False, **kwargs) -> Any:
        """
        Parse a given file and stream records.

        Args:
            filename: The filename
            format: The file format
            delimiter: The delimiter used in the file
            compressed: Whether or not the file is gzip compressed
            kwargs: Additional arguments

        """
        if compressed:
            handle = gzip.open(filename, 'rt')
        else:
            handle = open(filename, 'r')
        reader = csv.DictReader(handle, delimiter=delimiter)
        for row in reader:
            print(row)
            yield row
