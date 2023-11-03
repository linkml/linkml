from typing import Any, Iterator

import yaml

from linkml.validator.loaders.loader import Loader


class YamlLoader(Loader):
    """A loader for instances serialized as YAML

    :param source: Path to YAML source
    """

    def __init__(self, source) -> None:
        super().__init__(source)

    def iter_instances(self) -> Iterator[Any]:
        """Lazily yield instances from YAML source.

        If the root of the document is an array, yield each element of the array. Otherwise,
        yield the root element itself. Repeat for each document in the YAML file.

        :return: Iterator over data instances
        :rtype: Iterator[Any]
        """
        with open(self.source) as source_file:
            for document in yaml.safe_load_all(source_file):
                if isinstance(document, list):
                    yield from document
                else:
                    yield document
