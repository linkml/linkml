from typing import Iterator

from linkml_runtime import SchemaView

from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


class RecommendedSlotsPlugin(ValidationPlugin):
    def pre_process(self, context: ValidationContext) -> None:
        pass

    def process(self, instance: dict, context: ValidationContext) -> Iterator[ValidationResult]:
        yield from self._do_process(instance, context.target_class, context.schema_view)

    def _do_process(
        self, instance: dict, class_name: str, schema_view: SchemaView
    ) -> Iterator[ValidationResult]:
        if not isinstance(instance, dict):
            return
        for slot_def in schema_view.class_induced_slots(class_name):
            if slot_def.recommended and slot_def.name not in instance:
                yield ValidationResult(
                    type="recommended slots",
                    severity=Severity.WARN,
                    instance=instance,
                    instantiates=class_name,
                    message=f"Slot '{slot_def.name}' is recommended on class '{class_name}'",
                )
            slot_range_class = schema_view.get_class(slot_def.range)
            if slot_range_class is not None and slot_def.name in instance:
                yield from self._do_process(
                    instance[slot_def.name], slot_range_class.name, schema_view
                )
