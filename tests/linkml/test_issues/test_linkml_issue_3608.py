from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.linkml_model.meta import ExtraSlotsExpression


def test_honor_extra_slots_allowed_on_root_class():
    """extra_slots.allowed should work even on the root class."""
    schema = SchemaDefinition(
        id="test_honor_extra_slots_allowed_on_root_class",
        name="test_honor_extra_slots_allowed_on_root_class",
        classes=[
            ClassDefinition(
                name="Foo",
                attributes=[SlotDefinition(name="bar", range="Bar")],
                tree_root=True,
                extra_slots=ExtraSlotsExpression(allowed=True),
            ),
            ClassDefinition(name="Bar", attributes=[SlotDefinition(name="name", range="string")]),
        ],
    )
    validation_context = ValidationContext(schema)
    plugin = JsonschemaValidationPlugin(closed=True)
    results = list(plugin.process({"bar": {"name": "name of the bar"}, "extra": "extra slot"}, validation_context))
    assert results == []
