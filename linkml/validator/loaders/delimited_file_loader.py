import csv
import re
from abc import ABC, abstractmethod
from typing import Iterator, Optional

from linkml.validator.loaders.loader import Loader


def _parse_numeric(value: str):
    if not isinstance(value, str) or not re.search(r"[0-9]", value):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        pass
    try:
        return float(value)
    except (TypeError, ValueError, OverflowError):
        return value


class _DelimitedFileLoader(Loader, ABC):
    """Base class for TSV and CSV loaders"""

    @property
    @abstractmethod
    def delimiter(self):
        pass

    def __init__(self, source, *, skip_empty_rows: bool = False, index_slot_name: Optional[str] = None) -> None:
        super().__init__(source)
        self.skip_empty_rows = skip_empty_rows
        self.index_slot_name = index_slot_name

    def _rows(self) -> Iterator[dict]:
        with open(self.source) as file:
            reader: csv.DictReader = csv.DictReader(file, delimiter=self.delimiter, skipinitialspace=True)
            for row in reader:
                if self.skip_empty_rows and not any(row.values()):
                    continue
                yield {k: _parse_numeric(v) for k, v in row.items() if k is not None and v != ""}

    def iter_instances(self) -> Iterator[dict]:
        if self.index_slot_name is not None:
            yield {self.index_slot_name: list(self._rows())}
        else:
            yield from self._rows()


class CsvLoader(_DelimitedFileLoader):
    """A loader for instances serialized as CSV

    :param skip_empty_rows: If ``True``, skip empty rows instead of yielding empty dicts. Defaults
        to ``False``.
    :param index_slot_name: If provided, ``iter_instances`` will yield one dict where all rows of
        the CSV file are collected into a list with ``index_slot_name`` as the key. If ``None``,
        ``iter_instances`` will yield each row as a dict individually. Defaults to ``None``.
    """

    @property
    def delimiter(self):
        return ","


class TsvLoader(_DelimitedFileLoader):
    """A loader for instances serialized as TSV

    :param skip_empty_rows: If ``True``, skip empty rows instead of yielding empty dicts. Defaults
        to ``False``.
    :param index_slot_name: If provided, ``iter_instances`` will yield one dict where all rows of
        the TSV file are collected into a list with ``index_slot_name`` as the key. If ``None``,
        ``iter_instances`` will yield each row as a dict individually. Defaults to ``None``.
    """

    @property
    def delimiter(self):
        return "\t"
