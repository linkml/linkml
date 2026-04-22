"""
Test example runner using a simulated setup.

 - input/personinfo.yaml
 - input/examples
 - input/counter_examples
"""

import pytest
from prefixmaps.io.parser import load_multi_context

from linkml.workspaces.example_runner import ExampleRunner
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition

pytestmark = pytest.mark.xdist_group("workspaces")


@pytest.fixture
def example_runner(input_path, tmp_path):
    schemaview = SchemaView(input_path("personinfo.yaml"))
    ctxt = load_multi_context(["obo", "linked_data", "prefixcc"])
    return ExampleRunner(
        schemaview=schemaview,
        input_directory=input_path("examples"),
        counter_example_input_directory=input_path("counter_examples"),
        output_directory=tmp_path,
        prefix_map=ctxt.as_dict(),
    )


def test_load_from_dict(example_runner):
    """test loading from a dict object, including using type designators."""
    obj = example_runner._load_from_dict({"persons": [{"id": "p1", "name": "John"}]})
    assert obj is not None


def test_load_from_dict_hyphenated_keys(example_runner):
    """Hyphenated YAML keys must be translated to underscored Python kwargs."""
    example_runner.schemaview.schema.classes["Survey"] = ClassDefinition(
        name="Survey",
        tree_root=True,
        attributes={
            "how-many": SlotDefinition(name="how-many", range="integer"),
            "full-name": SlotDefinition(name="full-name", range="string"),
        },
    )
    example_runner.schemaview.schema.source_file = None
    obj = example_runner._load_from_dict(
        {"how-many": 3, "full-name": "Alice"},
        target_class="Survey",
    )
    assert obj is not None
    assert obj.how_many == 3
    assert obj.full_name == "Alice"


def test_load_from_dict_any_range(example_runner):
    """Slots with range: linkml:Any must pass the value through unchanged."""
    example_runner.schemaview.schema.classes["AnyValue"] = ClassDefinition(
        name="AnyValue",
        class_uri="linkml:Any",
    )
    example_runner.schemaview.schema.classes["AnyContainer"] = ClassDefinition(
        name="AnyContainer",
        attributes={
            "payload": SlotDefinition(name="payload", range="AnyValue"),
        },
    )
    example_runner.schemaview.schema.source_file = None

    # scalar value must pass through unchanged
    obj = example_runner._load_from_dict({"payload": 42}, target_class="AnyContainer")
    assert obj.payload == 42

    # dict value must not attempt typing.Any(**kwargs); Container's __init__
    # may wrap the raw dict in a JsonObj, so check attribute access instead.
    obj = example_runner._load_from_dict({"payload": {"x": 1, "y": 2}}, target_class="AnyContainer")
    assert obj.payload is not None
    assert obj.payload["x"] == 1
    assert obj.payload["y"] == 2


def test_example_runner(example_runner):
    """Process all YAML examples in input folder."""
    example_runner.process_examples()
    md = str(example_runner.summary)
    assert "Container-001" in example_runner.summary.inputs
    assert "Container-001.yaml" in example_runner.summary.outputs
    assert "Container-001.json" in example_runner.summary.outputs
    assert "Container-001.ttl" in example_runner.summary.outputs
    assert "Container-001" in md
    assert "Container-002" not in md


def test_example_runner_non_defaults(example_runner):
    """
    Process all JSON examples in input folder,
    using only ttl writing.
    :return:
    """
    example_runner.input_formats = ["json"]
    example_runner.output_formats = ["ttl"]
    example_runner.process_examples()
    md = str(example_runner.summary)
    assert "Container-002" in example_runner.summary.inputs
    assert "Container-002.yaml" not in example_runner.summary.outputs
    assert "Container-002.json" not in example_runner.summary.outputs
    assert "Container-002.ttl" in example_runner.summary.outputs
    assert "Container-001" not in md
    assert "Container-002" in md
