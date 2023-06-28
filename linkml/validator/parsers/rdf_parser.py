import gzip
from typing import Any

from linkml.validator.parsers.base import BaseParser

class RdfParser(BaseParser):

    def __init__(self, **kwargs):
        super().__init__()

    def parse(self, filename: str, format: str, compressed: bool = False, **kwargs) -> Any:
        if compressed:
            handle = gzip.open(filename, 'rb')
        else:
            handle = open(filename, 'r')
        # TODO
