from linkml_runtime.linkml_model import ClassDefinitionName


class ClassGeneratorMixin:
    def ordered_classes(self):
        return [self.schemaview.get_class(cn, strict=True) for cn in self.order_classes_by_hierarchy()]

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
