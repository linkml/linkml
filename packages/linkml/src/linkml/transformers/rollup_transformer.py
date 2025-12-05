"""
flatten_transformer.py

This module provides a FlattenTransformer that transforms a LinkML schema into a flattened version.
The transformer takes a target class name and rolls up all slots from its descendants into that class.
This is useful for implementing single table inheritance or simplifying inheritance for systems like KGX.
"""

import copy
from dataclasses import dataclass
from typing import Optional

from linkml_runtime.linkml_model.meta import (
    ClassDefinitionName,
    SchemaDefinition,
)
from linkml_runtime.utils.schemaview import SchemaView

from linkml.transformers.model_transformer import ModelTransformer


@dataclass
class FlattenTransformerConfiguration:
    """
    Configuration options for the FlattenTransformer.

    Attributes:
        preserve_class_designator: If True, preserves the original class name in the specified
            class designator slot (e.g., 'category').
        class_designator_slot: The name of the slot that designates the original class (e.g., 'category').
        include_all_classes: If True, keeps all classes in the schema; otherwise, only the target class
            and non-descendants are kept.
        include_mixins: If True, includes properties from mixins in the flattened class.
    """

    preserve_class_designator: bool = True
    class_designator_slot: Optional[str] = "category"
    include_all_classes: bool = False
    include_mixins: bool = True


class RollupTransformer(ModelTransformer):
    """
    Transforms a LinkML schema by flattening an inheritance hierarchy into a single class.

    This transformer takes a schema and a target class name, and produces a new schema where
    all descendant classes of the target class are removed and their slots are rolled up into the
    target class.
    """

    def __init__(
        self,
        target_class: str,
        config: Optional[FlattenTransformerConfiguration] = None,
    ):
        super().__init__()
        self.target_class = target_class
        self.config = config or FlattenTransformerConfiguration()
        self._descendant_classes: set[str] = set()
        self._class_to_slot_map: dict[str, set[str]] = {}

    def transform(self, tgt_schema_name: str = None, top_class: ClassDefinitionName = None) -> SchemaDefinition:
        """
        Transform the schema by flattening the inheritance hierarchy.

        Args:
            tgt_schema_name: Optional target schema name (not used in this transformer)
            top_class: Optional top class name (not used in this transformer)

        Returns:
            A transformed SchemaDefinition with the target class having all slots from its descendants.
        """
        if not self.schemaview:
            raise ValueError("SchemaView not set. Ensure schema is set by calling set_schema().")

        schema_copy = copy.deepcopy(self.source_schema)
        view = SchemaView(schema_copy)
        descendants = view.class_descendants(self.target_class, imports=True, mixins=True, reflexive=False, is_a=True)
        self._descendant_classes = set(descendants)

        # Collect all slots from the target class and its descendant classes, and
        # populate a mapping of class name to the set of its slot names.
        for descendant in self._descendant_classes:
            slots = view.class_induced_slots(descendant)
            self._class_to_slot_map[descendant] = {s.name for s in slots}

        # flatten the schema
        return self._create_flattened_schema(schema_copy)

    def _create_flattened_schema(self, schema: SchemaDefinition) -> SchemaDefinition:
        """
        Create a new flattened version of the schema based on collected slots.
        """
        target_class_def = schema.classes[self.target_class]
        existing_slot_names = set(target_class_def.slots or [])
        all_slots = set()

        for descendant in self._descendant_classes:
            if descendant in schema.classes:
                for slot_name in self._class_to_slot_map.get(descendant, set()):
                    if slot_name not in existing_slot_names:
                        all_slots.add(slot_name)

        if not target_class_def.slots:
            target_class_def.slots = []

        target_class_def.slots.extend(list(all_slots))

        # Optionally remove descendant classes.
        if not self.config.include_all_classes:
            for descendant in self._descendant_classes:
                if descendant in schema.classes:
                    del schema.classes[descendant]

        return schema
