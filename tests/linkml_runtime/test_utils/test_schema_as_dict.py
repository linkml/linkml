import logging
import os

import pytest

from linkml_runtime.linkml_model.meta import ClassDefinition
from linkml_runtime.utils.schema_as_dict import schema_as_dict, schema_as_yaml_dump
from linkml_runtime.utils.schema_builder import ClassDefinition, SchemaBuilder, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_utils import INPUT_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)


@pytest.fixture
def schema_no_imports_path():
    """Path to kitchen sink schema without imports."""
    return os.path.join(INPUT_DIR, "kitchen_sink_noimports.yaml")


@pytest.fixture
def clean_output_path():
    """Path for clean output schema file."""
    return os.path.join(OUTPUT_DIR, "kitchen_sink.clean.yaml")


def test_as_dict(schema_no_imports_path, clean_output_path):
    """
    tests schema_as_dict, see https://github.com/linkml/linkml/issues/100
    """
    view = SchemaView(schema_no_imports_path)
    all_slots = view.all_slots()
    assert "name" in all_slots
    logger.debug(view.schema.id)
    ystr = schema_as_yaml_dump(view.schema)
    with open(clean_output_path, "w") as stream:
        stream.write(ystr)
    view2 = SchemaView(ystr)
    obj = schema_as_dict(view.schema)
    # ensure that prefixes are compacted
    assert obj["prefixes"]["pav"] == "http://purl.org/pav/"
    assert "@type" not in obj
    for k in ["slots", "classes", "enums", "subsets"]:
        elt_dict = obj[k]
        for e_name, e in elt_dict.items():
            assert "name" not in e
        if k == "enums":
            for e in elt_dict.values():
                for pv in e.get("permissible_values", {}).values():
                    assert "text" not in pv
    assert "name" in obj["slots"]


def test_as_dict_with_attributes():
    """
    tests schema_as_dict, see https://github.com/linkml/linkml/issues/100
    """

    # Create a class with an attribute named 'name'
    cls = ClassDefinition(name="Patient")
    slots = [
        SlotDefinition(name="id", range="string"),
        SlotDefinition(name="name", range="string"),
    ]
    builder = SchemaBuilder()
    builder.add_class(cls=cls, slots=slots, use_attributes=True)

    # Verify that the 'name' slot exists in the schema
    view = SchemaView(builder.schema)
    assert "name" in view.all_slots()

    # Convert the schema to a dict
    obj = schema_as_dict(view.schema)

    # Verify that the 'name' slot still exists, as an attribute
    assert "name" in obj["classes"]["Patient"]["attributes"]
