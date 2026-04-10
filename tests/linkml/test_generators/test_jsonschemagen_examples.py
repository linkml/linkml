import json
from textwrap import dedent

import pytest

from linkml.generators.jsonschemagen import JsonSchemaGenerator


@pytest.mark.parametrize(
    "range_type, yaml_value, expected_json_value",
    [
        pytest.param("integer", "42", 42, id="integer"),
        pytest.param("integer", "-7", -7, id="negative_integer"),
        pytest.param("float", "3.14", 3.14, id="float"),
        # "true"/"false" are in the BooleanConfig default truthy/falsy sets.
        pytest.param("boolean", "true", True, id="boolean_true_lowercase"),
        pytest.param("boolean", "false", False, id="boolean_false_lowercase"),
        # YAML unquoted booleans get str()-coerced to "True"/"False" by the metamodel;
        # "True"/"False" lower() → "true"/"false" which are in the default sets.
        pytest.param("boolean", "True", True, id="boolean_true_titlecase"),
        pytest.param("boolean", "False", False, id="boolean_false_titlecase"),
        # String range: value must remain a string.
        pytest.param("string", "hello", "hello", id="string_unchanged"),
    ],
)
def test_jsonschemagen_coerces_primitive_value_types(range_type, yaml_value, expected_json_value):
    """Scalar Example.value entries are type-coerced to match the slot's range type.

    Example.value is always stored as str in the metamodel (non-string YAML values
    like 42 or true are coerced to "42" / "True"). The generator must convert them
    back to the correct JSON type so that generated examples validate correctly.

    Boolean coercion uses get_boolean_config() so schema-level boolean_truthy /
    boolean_falsy annotations are respected.
    """
    schema = dedent(f"""
        id: http://example.org/examples
        name: examples
        imports:
          - linkml:types
        classes:
          Thing:
            tree_root: true
            attributes:
              my_slot:
                range: {range_type}
                examples:
                  - value: "{yaml_value}"
        """)
    js = json.loads(JsonSchemaGenerator(schema).serialize())
    examples = js["$defs"]["Thing"]["properties"]["my_slot"].get("examples")
    assert examples is not None
    assert expected_json_value in examples


@pytest.mark.parametrize(
    "range_type, yaml_values, expected_combined",
    [
        pytest.param("integer", ["1", "2", "3"], [1, 2, 3], id="multivalued_integers"),
        pytest.param("float", ["1.1", "2.2"], [1.1, 2.2], id="multivalued_floats"),
        pytest.param("boolean", ["true", "false"], [True, False], id="multivalued_booleans"),
    ],
)
def test_jsonschemagen_coerces_multivalued_primitive_types(range_type, yaml_values, expected_combined):
    """Scalar element examples on multivalued slots are also type-coerced."""
    examples_yaml = "\n".join(f'                  - value: "{v}"' for v in yaml_values)
    schema = dedent(f"""
        id: http://example.org/examples
        name: examples
        imports:
          - linkml:types
        classes:
          Thing:
            tree_root: true
            attributes:
              items:
                range: {range_type}
                multivalued: true
                examples:
                """)
    schema += examples_yaml

    js = json.loads(JsonSchemaGenerator(schema).serialize())
    exs = js["$defs"]["Thing"]["properties"]["items"].get("examples")
    assert exs == [expected_combined]


def test_jsonschemagen_includes_slot_examples():
    """Single-valued slot examples are emitted as independent entries."""

    schema = dedent("""
        id: http://example.org/examples
        name: examples
        classes:
          Person:
            tree_root: true
            attributes:
              name:
                examples:
                  - value: "Alice"
                  - object:
                      age: 30
        """)
    js = json.loads(JsonSchemaGenerator(schema).serialize())
    examples = js["$defs"]["Person"]["properties"]["name"].get("examples")
    assert examples is not None
    assert "Alice" in examples
    assert {"age": 30} in examples


@pytest.mark.parametrize(
    "example_yaml, expected_examples",
    [
        pytest.param(
            # Two scalar element examples → combined into one array-level example.
            # Matches the LinkML convention used in e.g. biolink-model's
            # "object label closure" slot.
            dedent("""\
                - value: "breast cancer"
                - value: "cancer"
                """),
            [["breast cancer", "cancer"]],
            id="two_scalars_combined",
        ),
        pytest.param(
            # One object element example → combined into one single-element array.
            # Matches the user's biological_processes case.
            dedent("""\
                - object:
                    id: "GO:0140999"
                    label: "histone H3K4 trimethyltransferase activity"
                """),
            [[{"id": "GO:0140999", "label": "histone H3K4 trimethyltransferase activity"}]],
            id="one_object_combined",
        ),
        pytest.param(
            # One explicit list-valued example → kept as a single complete-array example.
            # Now valid because Example.value accepts any YAML type.
            dedent("""\
                - value: ["BRACA1"]
                """),
            [["BRACA1"]],
            id="explicit_list_preserved",
        ),
        pytest.param(
            # Two explicit list-valued examples → two independent complete-array examples.
            dedent("""\
                - value: ["a", "b"]
                - value: ["c", "d"]
                """),
            [["a", "b"], ["c", "d"]],
            id="two_explicit_lists_independent",
        ),
        pytest.param(
            # Mixed: one scalar element + one explicit list.
            # Scalar is combined into its own single-element array; list is independent.
            dedent("""\
                - value: "ally"
                - value: ["bob", "robert"]
                """),
            [["ally"], ["bob", "robert"]],
            id="mixed_scalar_and_list",
        ),
    ],
)
def test_jsonschemagen_multivalued_slot_examples(example_yaml, expected_examples):
    """Examples on multivalued slots are emitted as strictly-valid array-level examples.

    - Scalar / object ``Example`` entries are combined into a single array.
    - List-valued ``Example`` entries are kept as independent complete-array examples.
    """
    examples_yaml = "\n".join(f"          {v}" for v in example_yaml.splitlines())

    schema = dedent("""
        id: http://example.org/examples
        name: examples
        classes:
          Thing:
            tree_root: true
            attributes:
              items:
                multivalued: true
                range: string
                examples:
                """)
    schema += examples_yaml
    js = json.loads(JsonSchemaGenerator(schema).serialize())
    exs = js["$defs"]["Thing"]["properties"]["items"].get("examples")
    assert exs == expected_examples


def test_jsonschemagen_multivalued_inlined_class_examples():
    """Object examples on a multivalued inlined-class slot are combined into one
    array-level example (the biological_processes use case)."""

    schema = dedent("""
        id: http://example.org/examples
        name: examples
        classes:
          Term:
            attributes:
              id: {}
              label: {}

          Dataset:
            tree_root: true
            attributes:
              biological_processes:
                range: Term
                multivalued: true
                inlined: true
                inlined_as_list: true
                examples:
                  - object:
                      id: "GO:0140999"
                      label: "histone H3K4 trimethyltransferase activity"
        """)
    js = json.loads(JsonSchemaGenerator(schema).serialize())
    exs = js["$defs"]["Dataset"]["properties"]["biological_processes"].get("examples")
    assert exs == [[{"id": "GO:0140999", "label": "histone H3K4 trimethyltransferase activity"}]]


def test_jsonschemagen_includes_single_valued_inlined_class_examples():
    """Examples on a single-valued inlined-class slot are plain objects (no wrapping)."""

    schema = dedent("""
        id: http://example.org/examples
        name: examples
        classes:
          Address:
            attributes:
              street: {}
              number: {}

          Person:
            tree_root: true
            attributes:
              address:
                range: Address
                inlined: true
                examples:
                  - object:
                      street: "Main"
                      number: 1
        """)
    js = json.loads(JsonSchemaGenerator(schema).serialize())
    exs = js["$defs"]["Person"]["properties"]["address"].get("examples")
    assert exs == [{"street": "Main", "number": 1}]


def test_jsonschemagen_includes_class_examples():
    """Class-level examples are emitted as independent full-instance examples."""

    schema = dedent("""
        id: http://example.org/examples
        name: examples
        classes:
          Person:
            tree_root: true
            examples:
              - object:
                  name: "Bob"
                  age: 40
            attributes:
              name: {}
              age: { range: integer }
        """)
    js = json.loads(JsonSchemaGenerator(schema).serialize())
    exs = js["$defs"]["Person"].get("examples")
    assert exs == [{"name": "Bob", "age": 40}]
