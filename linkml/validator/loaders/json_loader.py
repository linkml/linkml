from typing import Any, Iterable

from linkml_runtime.loaders import json_loader

from linkml.validator.loaders.loader import Loader


class JsonLoader(Loader):
    """A loader for instances serialized as JSON"""

    def __init__(self, source) -> None:
        """Constructor method

        :param source: Path or URL to JSON source
        """
        super().__init__(source)

    def iter_instances(self) -> Iterable[Any]:
        """Lazily yield instance from JSON source.

        If the root of the JSON is an array, yield each element of the array. Otherwise
        yield the root element itself.

        :return: Iterator over data instances
        :rtype: Iterable[Any]
        """
        data = json_loader.load_as_dict(self.source)
        if isinstance(data, list):
            yield from data
        else:
            yield data