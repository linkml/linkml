from linkml_runtime import SchemaView

from linkml import LOCAL_METAMODEL_YAML_FILE

from ..config.datamodel.config import RecommendedRuleConfig
from ..linter import LinterProblem, LinterRule


class RecommendedRule(LinterRule):

    id = "recommended"

    def __init__(self, config: RecommendedRuleConfig) -> None:
        super().__init__(config)
        meta_schema_view = SchemaView(LOCAL_METAMODEL_YAML_FILE)
        self.recommended_meta_slots = []
        for class_name in meta_schema_view.all_class(imports=False).keys():
            class_slots = meta_schema_view.class_induced_slots(class_name)
            for slot in class_slots:
                if slot.recommended:
                    self.recommended_meta_slots.append(f"{class_name}__{slot.name}")

    def check(self, schema_view: SchemaView, fix: bool = False):
        for element_name, element_definition in schema_view.all_elements(
            imports=False
        ).items():
            if self.config.include and element_name not in self.config.include:
                continue
            if element_name in self.config.exclude:
                continue
            for meta_slot_name, meta_slot_value in vars(element_definition).items():
                meta_class_name = type(element_definition).class_name
                key = f"{meta_class_name}__{meta_slot_name}"
                if key in self.recommended_meta_slots and not meta_slot_value:
                    yield LinterProblem(
                        f"{meta_class_name} '{element_name}' does not have recommended slot '{meta_slot_name}'"
                    )
