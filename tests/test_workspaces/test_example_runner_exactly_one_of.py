"""
Test example runner using a simulated setup and in particular, test "exactly_one_of" constraint
"""

from linkml_runtime import SchemaView
from linkml.validator import validate
from prefixmaps.io.parser import load_multi_context
from linkml.workspaces.example_runner import ExampleRunner, cli
import pytest
from click.testing import CliRunner

@pytest.fixture
def runner():
    return CliRunner()

schema_slots = """
    id: https://example.org/issue
    prefixes:
        linkml: https://w3id.org/linkml/
    imports:
        - linkml:types
    classes:
        Class1:
            slots:
                - attr2
        Class2:
            slots:
                - attr2
                - attr3
        TopClass:
            tree_root: true
            slots:
                - attr1
    slots:
        attr2:
            range: string
        attr3:
            required: true
        attr1:
            exactly_one_of:
                - range: Class1
                - range: Class2
"""

schema_attrs = """
    id: https://example.org/issue
    prefixes:
        linkml: https://w3id.org/linkml/
    imports:
        - linkml:types
    classes:
        Class1:
            attributes:
                attr2:
                    range: string
        Class2:
            attributes:
                attr2: 
                    range: string
                attr3:
                    required: true
        TopClass:
            tree_root: true
            attributes:
                attr1:
                    exactly_one_of:
                        - range: Class1
                        - range: Class2
    """

@pytest.fixture
def example_runner_attrs(input_path, tmp_path):
    schemaview = SchemaView(schema_attrs)
    print("schema", schema_attrs)
    ctxt = load_multi_context(["obo", "linked_data", "prefixcc"])
    return ExampleRunner(
        schemaview=schemaview,
        prefix_map=ctxt.as_dict(),
    )

@pytest.fixture
def example_runner_slots(input_path, tmp_path):
    schemaview = SchemaView(schema_slots)
    print("schema", schema_slots)
    ctxt = load_multi_context(["obo", "linked_data", "prefixcc"])
    return ExampleRunner(
        schemaview=schemaview,
        prefix_map=ctxt.as_dict(),
    )

def test_process_examples_from_list_valid_attrs(example_runner_attrs, tmp_path):
    """
    Process all examples in input folder.
    """
    test_slot_topclass = {"attr1": {"attr2": "somestring"}}
    report = validate(test_slot_topclass, schema_attrs)
    if not report.results:
        print('The instance is valid!')
    else:
        for result in report.results:
            print(result.message)

    obj = example_runner_attrs._load_from_dict(test_slot_topclass)
    print(obj)
    assert obj is not None
    example_runner_attrs.process_examples()
    md = str(example_runner_attrs.summary)
    print("example runner summary", example_runner_attrs.summary.inputs)
    print("md example", md)

def test_process_examples_from_list_valid_slots(example_runner_slots, tmp_path):
    """
    Process all examples in input folder.
    """
    test_slot_topclass = {"attr1": {"attr2": "somestring"}}
    report = validate(test_slot_topclass, schema_slots)
    if not report.results:
        print('The instance is valid!')
    else:
        for result in report.results:
            print(result.message)

    obj = example_runner_slots._load_from_dict(test_slot_topclass)
    print(obj)
    assert obj is not None
    example_runner_slots.process_examples()
    md = str(example_runner_slots.summary)
    print("example runner summary", example_runner_slots.summary.inputs)
    print("md example", md)

