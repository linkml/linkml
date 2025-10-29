from linkml_runtime.utils.pattern import PatternResolver, generate_patterns
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_utils.environment import env


def test_generate_patterns():
    """Test method that consolidates composite patterns."""
    sv = SchemaView(env.input_path("pattern-example.yaml"))

    # actual result returned from call to generate_patterns()
    actual_dict = generate_patterns(sv)

    expected_dict = {
        "{float} {unit.length}": "\\d+[\\.\\d+] (centimeter|meter|inch)",
        "{float} {unit.weight}": "\\d+[\\.\\d+] (kg|g|lbs|stone)",
    }

    assert actual_dict == expected_dict


def test_pattern_resolver():
    sv = SchemaView(env.input_path("pattern-example.yaml"))

    resolver = PatternResolver(sv)

    assert resolver.resolve("{float} {unit.length}") == "\\d+[\\.\\d+] (centimeter|meter|inch)"
    assert resolver.resolve("{float} {unit.weight}") == "\\d+[\\.\\d+] (kg|g|lbs|stone)"
