import csv
import re
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path

from linkml.validator.loaders.loader import Loader

_NUMERIC_TYPE_NAMES = frozenset({"integer", "float", "double", "decimal"})


def _parse_numeric(value: str):
    """Attempt to coerce a string value to int or float."""
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


def _get_numeric_slots(schema_path: str | Path, target_class: str) -> set[str]:
    """Return column names whose schema range is a numeric type.

    Only these columns should be passed through ``_parse_numeric``. All others
    (string, enum, uri, date, custom string-derived types, etc.) are returned
    as-is to avoid breaking validation.

    Uses ``SchemaView.type_ancestors()`` to walk ``typeof`` chains, so custom
    types like ``typeof: string`` are handled correctly.
    """
    from linkml_runtime import SchemaView

    sv = SchemaView(str(schema_path))
    numeric_slots: set[str] = set()
    all_types = sv.all_types()
    for slot in sv.class_induced_slots(target_class):
        if slot.range in all_types:
            ancestors = sv.type_ancestors(slot.range)
            if any(a in _NUMERIC_TYPE_NAMES for a in ancestors):
                numeric_slots.add(slot.name)
                if slot.alias:
                    numeric_slots.add(slot.alias)
    return numeric_slots


class _DelimitedFileLoader(Loader, ABC):
    """Base class for TSV and CSV loaders.

    When *schema_path* and *target_class* are provided, the loader uses schema
    information to decide whether a cell value should be kept as a string rather
    than auto-converted to a number.  Without schema information the loader
    falls back to the original heuristic (convert anything that looks numeric).
    """

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
        # None means "no schema provided" → coerce everything (backward compat)
        # An empty set means "schema provided but no numeric slots" → coerce nothing
        self._numeric_slots: set[str] | None = (
            _get_numeric_slots(schema_path, target_class)
            if schema_path is not None and target_class is not None
            else None
        )

    def set_schema_context(self, schema_path: str | Path, target_class: str) -> None:
        """Configure schema-aware type coercion after construction.

        This is used by the :class:`~linkml.validator.Validator` to inject
        schema information into loaders that were created without it (e.g.
        by the CLI or ``default_loader_for_file``).
        """
        self._numeric_slots = _get_numeric_slots(schema_path, target_class)

    def _coerce_value(self, key: str, value: str):
        """Return *value* coerced to the appropriate Python type.

        When schema info is available, only columns with numeric ranges go
        through ``_parse_numeric``; everything else is returned as-is.
        Without schema info (``_numeric_slots is None``), all columns are
        coerced for backward compatibility.
        """
        if self._numeric_slots is not None and key not in self._numeric_slots:
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
    """A loader for instances serialized as CSV.

    :param skip_empty_rows: If ``True``, skip empty rows instead of yielding empty dicts. Defaults
        to ``False``.
    :param index_slot_name: If provided, ``iter_instances`` will yield one dict where all rows of
        the CSV file are collected into a list with ``index_slot_name`` as the key. If ``None``,
        ``iter_instances`` will yield each row as a dict individually. Defaults to ``None``.
    :param schema_path: Optional path to a LinkML schema for schema-aware type coercion.
    :param target_class: Name of the target class within the schema.
    """

    @property
    def delimiter(self):
        return ","


class TsvLoader(_DelimitedFileLoader):
    """A loader for instances serialized as TSV.

    :param skip_empty_rows: If ``True``, skip empty rows instead of yielding empty dicts. Defaults
        to ``False``.
    :param index_slot_name: If provided, ``iter_instances`` will yield one dict where all rows of
        the TSV file are collected into a list with ``index_slot_name`` as the key. If ``None``,
        ``iter_instances`` will yield each row as a dict individually. Defaults to ``None``.
    :param schema_path: Optional path to a LinkML schema for schema-aware type coercion.
    :param target_class: Name of the target class within the schema.
    """

    @property
    def delimiter(self):
        return "\t"
