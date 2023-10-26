from typing import Any, Iterator

from linkml.validator.loaders.loader import Loader


class PassthroughLoader(Loader):
    """A loader that passes through from an existing Iterator

    :param source: An Iterator
    """

    def __init__(self, source: Iterator) -> None:
        super().__init__(source)

    def iter_instances(self) -> Iterator[Any]:
        """Pass through instances from an Iterator

        :return: Iterator over data instances
        :rtype: Iterator[Any]
        """
        yield from self.source
