from typing import TYPE_CHECKING

from .dependency_sorter import DependencySorter

if TYPE_CHECKING:
    from .dataframe_generator import DataframeGenerator


class ClassHandlerBase:
    def __init__(self, generator: "DataframeGenerator"):
        self.generator = generator

    def enum_or_class(self, cn):
        schemaview = self.generator.schemaview

        if cn in schemaview.all_enums():
            return self.generator.schemaview.get_enum(cn, strict=True)

        if cn in schemaview.all_classes():
            return schemaview.get_class(cn, strict=True)

        raise Exception(f"Unknown class or enum {cn}")

    def ordered_classes(self):
        # Tolerate cycles: even with the parent/child association cycle skip
        # in `add_dependencies_by_association`, the LinkML metamodel imports
        # still contain peer cycles between mutually-recursive classes (e.g.
        # path_expression ↔ schema_definition ↔ slot_definition ↔
        # anonymous_class_expression). The three-pass polars template lets us
        # emit those classes in arbitrary order, so we silently break any
        # remaining cycles instead of raising.
        sorter = DependencySorter(allow_cycles=True)

        self.add_dependencies_by_association(sorter)
        self.add_dependencies_for_hierarchy(sorter)
        sorted_class_names = sorter.sort_dependencies()

        ordered = [self.enum_or_class(cn) for cn in sorted_class_names]

        return ordered

    def add_dependencies_for_hierarchy(self, sorter: DependencySorter) -> None:
        """
        Add dependencies based on class hierarchy.
        """
        sv = self.generator.schemaview

        for cn in sv.all_classes():
            sorter.add_dependency(cn, None)
            parents = sv.class_parents(cn)

            for p in parents:
                sorter.add_dependency(cn, p)

    def add_dependencies_by_association(self, sorter: DependencySorter) -> None:
        """
        Add dependencies based on associations.
        """
        sv = self.generator.schemaview

        for cn in sv.all_classes():
            for slot_name in sv.class_slots(cn):
                slot = sv.induced_slot(slot_name, cn)
                if slot.range and slot.range in sv.all_classes() and slot.range not in sv.all_enums():
                    ## Skip if the range is cn itself or a descendant of cn.
                    ## The hierarchy already orders parent before child, so adding
                    ## cn --> slot.range here would create a cycle with child --> cn.
                    if cn in sv.class_ancestors(slot.range, reflexive=True):
                        continue
                    # Only add dependency if slot is inlined or range has no identifier
                    if slot.inlined or slot.inlined_as_list or sv.get_identifier_slot(slot.range) is None:
                        sorter.add_dependency(cn, slot.range)
                    else:
                        sorter.add_dependency(cn, None)
