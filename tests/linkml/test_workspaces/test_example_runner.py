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


def test_load_from_dict_underscored_input_keys(example_runner):
    """Pre-underscored keys must be accepted by _load_from_dict.

    The personinfo schema includes slots such as ``founding location``. Callers
    may provide pre-underscored keys (e.g. ``founding_location``) as produced by
    JSON Schema / Python generators.
    """
    obj = example_runner._load_from_dict(
        {
            "organizations": [
                {
                    "id": "ROR:1",
                    "name": "Acme Corp",
                    "founding_location": "GEO:001",
                }
            ]
        }
    )
    assert obj is not None
    assert obj.organizations[0].founding_location == "GEO:001"


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
