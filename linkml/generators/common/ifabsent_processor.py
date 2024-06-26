import abc
import re
from abc import ABC
from typing import Any, Optional

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition


class IfAbsentProcessor(ABC):
    """
    Processes value of ifabsent slot.

    See `<https://w3id.org/linkml/ifabsent>`_.
    """

    ifabsent_regex = re.compile("""(?:(?P<type>\w+)\()?[\"\']?(?P<default_value>[^\(\)\"\')]*)[\"\']?\)?""")

    def __init__(self, schema_view: SchemaView):
        self.schema_view = schema_view

    def process_slot(self, slot: SlotDefinition, cls: ClassDefinition) -> Optional[str]:
        if slot.ifabsent:
            ifabsent_match = self.ifabsent_regex.search(slot.ifabsent)
            ifabsent_default_value = ifabsent_match.group("default_value")

            return self._map_to_default_value(slot, ifabsent_default_value, cls)

        return None

    @abc.abstractmethod
    def _map_to_default_value(
        self, slot: SlotDefinition, ifabsent_default_value: Any, cls: ClassDefinition
    ) -> Optional[str]:
        return None
