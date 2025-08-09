from linkml_runtime.linkml_model import ClassDefinitionName

from .dependency_sorter import DependencySorter


class ClassGeneratorMixin:
    def ordered_classes(self):
        oc = [self.schemaview.get_class(cn, strict=True) for cn in self.order_classes_by_associations()]

        return oc

    def order_classes_by_hierarchy(self) -> list[ClassDefinitionName]:
        sv = self.schemaview
        olist = sv.class_roots()
        unprocessed = [cn for cn in sv.all_classes() if cn not in olist]

        while len(unprocessed) > 0:
            ext_list = [cn for cn in unprocessed if not any(p for p in sv.class_parents(cn) if p not in olist)]
            if len(ext_list) == 0:
                raise ValueError(f"Cycle in hierarchy, cannot process: {unprocessed}")
            olist += ext_list
            unprocessed = [cn for cn in unprocessed if cn not in olist]

        return olist

    def order_classes_by_associations(self) -> list[ClassDefinitionName]:
        sv = self.schemaview
        dependency_dict = {}

        # Initialize dependency dict for all classes
        for class_name in sv.all_classes():
            dependency_dict[class_name] = []

        # Build dependencies based on slot ranges
        for class_name in sv.all_classes():
            for slot_name in sv.class_slots(class_name):
                slot = sv.induced_slot(slot_name, class_name)
                if slot.range and slot.range in sv.all_classes() and slot.range not in sv.all_enums():
                    # Only add dependency if slot is inlined or range has no identifier
                    if slot.inlined or slot.inlined_as_list or sv.get_identifier_slot(slot.range) is None:
                        dependency_dict[class_name].append(slot.range)

        # Sort dependencies
        # print(dependency_dict)
        sorter = DependencySorter(dependency_dict)
        return sorter.sort_dependencies()
