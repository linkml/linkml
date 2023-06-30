from abc import ABC, abstractmethod
from typing import Any, Iterable


class Loader(ABC):
    """Abstract base class for instance data loaders.

    Subclasses must implement the iter_instances method.
    """

    def __init__(self, source) -> None:
        """Constructor method

        :param source: Path or URL to load instances from
        """
        self.source = source

    @abstractmethod
    def iter_instances(self) -> Iterable[Any]:
        """Lazily load data instances from the source

        :return: Iterator over data instances
        :rtype: Iterable[Any]
        """
        pass
