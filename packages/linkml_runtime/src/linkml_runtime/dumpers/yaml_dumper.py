from datetime import date, datetime

import yaml
from pydantic import BaseModel

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.yamlutils import YAMLRoot


class _ISODateSafeDumper(yaml.SafeDumper):
    """SafeDumper that writes dates and datetimes as xsd:date and xsd:dateTime strings, not YAML timestamps."""


def _represent_iso_date(dumper: yaml.SafeDumper, value: date) -> yaml.ScalarNode:
    """Represent a date or datetime as its ISO 8601 string."""
    return dumper.represent_str(value.isoformat())


# SafeRepresenter registers both types exactly, so both need overriding.
_ISODateSafeDumper.add_representer(date, _represent_iso_date)
_ISODateSafeDumper.add_representer(datetime, _represent_iso_date)


class YAMLDumper(Dumper):
    def dumps(self, element: BaseModel | YAMLRoot, **kwargs) -> str:
        """Return element formatted as a YAML string"""
        # Internal note: remove_empty_items will also convert Decimals to int/float;
        # this is necessary until https://github.com/yaml/pyyaml/pull/372 is merged

        dumper_safe_element = element.model_dump() if isinstance(element, BaseModel) else element
        return yaml.dump(
            remove_empty_items(dumper_safe_element, hide_protected_keys=True),
            Dumper=_ISODateSafeDumper,
            sort_keys=False,
            allow_unicode=True,
            **kwargs,
        )
