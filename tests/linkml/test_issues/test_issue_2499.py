import json

import pytest

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.deprecation import EMITTED
from tests import DEFAULT_LOG_LEVEL


def test_json_schema_resolves_structured_patterns_automatically(input_path, snapshot):
    """Resolve structured patterns without modifying the source schema."""
    generator = JsonSchemaGenerator(input_path("issue_2499.yaml"), log_level=DEFAULT_LOG_LEVEL)
    identifier = generator.schemaview.get_slot("identifier")

    assert identifier.pattern is None

    json_schema = generator.serialize()

    assert json_schema == snapshot("issue_2499.json")
    assert identifier.pattern is None


@pytest.mark.parametrize("legacy_value", [True, False])
def test_json_schema_materialize_patterns_option_is_deprecated(input_path, legacy_value: bool) -> None:
    """Register either legacy value without allowing it to disable resolution."""
    EMITTED.discard("materialize-patterns-generator-option")

    generator = JsonSchemaGenerator(input_path("issue_2499.yaml"), materialize_patterns=legacy_value)

    assert "materialize-patterns-generator-option" in EMITTED

    generated_schema = json.loads(generator.serialize())
    identifier = generated_schema["$defs"]["Thing"]["properties"]["identifier"]
    assert identifier["pattern"] == r"^(?:^(https?://|(mailto|tel):)\w+$)$"
