
from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    Base parser class that all parsers should inherit from.
    """

    def __init__(self, **kwargs):
        ...

    @abstractmethod
    def parse(self, filename: str, **kwargs):
        """
        Parse a given file
        """
        ...
