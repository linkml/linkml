from typing import Callable, Iterable, List

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import (ClassDefinition, ClassDefinitionName,
                                         SchemaDefinition, SlotDefinition)

from ..config.datamodel.config import TreeRootClassRuleConfig
from ..linter import LinterProblem, LinterRule


class TreeRootClassRule(LinterRule):
    id = "tree_root_class"

    def __init__(self, config: TreeRootClassRuleConfig) -> None:
        super().__init__(config)

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        tree_roots = [
            c for c in schema_view.all_classes(imports=False).values() if c.tree_root
        ]
        if len(tree_roots) > 0:
            if self.config.validate_existing_class_name:
                for tree_root in tree_roots:
                    if str(tree_root.name) != self.config.root_class_name:
                        yield LinterProblem(
                            message=f"Tree root class has name '{tree_root.name}'"
                        )
        else:
            if fix:
                container = ClassDefinition(self.config.root_class_name, tree_root=True)
                schema_view.add_class(container)
                self.add_index_slots(schema_view, container.name)
            else:
                yield LinterProblem("Schema does not have class with `tree_root: true`")

    def add_index_slots(
        self,
        schema_view: SchemaView,
        container_name: ClassDefinitionName,
        inlined_as_list=False,
        must_have_identifier=False,
        slot_name_func: Callable = None,
        convert_camel_case=False,
    ) -> List[SlotDefinition]:
        """
        Adds index slots to a container pointing at all top-level classes

        :param schema: input schema, will be modified in place
        :param container_name:
        :param inlined_as_list:
        :param must_have_identifier:
        :param slot_name_func: function to determine the name of the slot from the class
        :return: new slots
        """
        container = schema_view.get_class(container_name)
        ranges = set()
        for cn in schema_view.all_classes():
            for s in schema_view.class_induced_slots(cn):
                ranges.add(s.range)
        top_level_classes = [
            c
            for c in schema_view.all_classes().values()
            if not c.tree_root and c.name not in ranges
        ]
        if must_have_identifier:
            top_level_classes = [
                c
                for c in top_level_classes
                if schema_view.get_identifier_slot(c.name) is not None
            ]
        index_slots = []
        for c in top_level_classes:
            has_identifier = schema_view.get_identifier_slot(c.name)
            if slot_name_func:
                sn = slot_name_func(c)
            else:
                cn = c.name
                if convert_camel_case:
                    cn = self.uncamel(cn).lower()
                cn = cn.replace(" ", "_")
                sn = f"{cn}_index"
            index_slot = SlotDefinition(
                sn,
                range=c.name,
                multivalued=True,
                inlined_as_list=not has_identifier or inlined_as_list,
            )
            index_slots.append(index_slot)
            schema_view.add_slot(index_slot)
            container.slots.append(index_slot.name)
        return index_slots
