import json

from linkml.generators.jsonschemagen import JsonSchemaGenerator


def test_per_class_additional_properties_honor_not_closed(input_path):
    """additionalProperties on a class should depend on the global not_closed setting."""
    schema = input_path("personinfo.yaml")
    classes = ["NamedThing", "Person", "Organization", "Address", "Event", "Concept"]

    for not_closed in [True, False]:
        generated_schema = json.loads(JsonSchemaGenerator(schema, not_closed=not_closed).serialize())
        for klass in classes:
            assert generated_schema["$defs"][klass]["additionalProperties"] == not_closed
