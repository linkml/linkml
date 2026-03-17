import csv
import re
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path

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


def _get_string_slots(schema_path: str | Path, target_class: str) -> set[str]:
    """Return column names whose schema range is ``string`` or an enum.

    These columns should *not* be passed through ``_parse_numeric`` because the
    schema expects string values even when the cell looks numeric (e.g. a
    zipcode ``"90210"`` or an enum permissible value ``"4"``).
    """
    from linkml_runtime import SchemaView

    sv = SchemaView(str(schema_path))
    string_slots: set[str] = set()
    all_enums = set(sv.all_enums())
    for slot in sv.class_induced_slots(target_class):
        if slot.range == "string" or slot.range in all_enums:
            string_slots.add(slot.name)
    return string_slots


class _DelimitedFileLoader(Loader, ABC):
    """Base class for TSV and CSV loaders"""

    @property
    @abstractmethod
    def delimiter(self):
        pass

    def __init__(
        self,
        source,
        *,
        skip_empty_rows: bool = False,
        index_slot_name: str | None = None,
        schema_path: str | Path | None = None,
        target_class: str | None = None,
    ) -> None:
        super().__init__(source)
        self.skip_empty_rows = skip_empty_rows
        self.index_slot_name = index_slot_name
        self._string_slots: set[str] = (
            _get_string_slots(schema_path, target_class)
            if schema_path is not None and target_class is not None
            else set()
        )

    def _coerce_value(self, key: str, value: str):
        """Return *value* coerced to the appropriate Python type.

        Columns listed in ``_string_slots`` are returned as-is; all others go
        through ``_parse_numeric``.
        """
        if key in self._string_slots:
            return value
        return _parse_numeric(value)

    def _rows(self) -> Iterator[dict]:
        with open(self.source) as file:
            reader: csv.DictReader = csv.DictReader(file, delimiter=self.delimiter, skipinitialspace=True)
            for row in reader:
                if self.skip_empty_rows and not any(row.values()):
                    continue
                yield {k: self._coerce_value(k, v) for k, v in row.items() if k is not None and v != ""}

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
