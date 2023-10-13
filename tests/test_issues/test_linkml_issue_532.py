import pytest
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator


def test_issue_532(input_path):
    """
    Tests: https://github.com/linkml/linkml/issues/532
    """
    schemafile = input_path("linkml_issue_532.yaml")
    sv = SchemaView(schemafile)
    datafile = input_path("linkml_issue_532_data.jsonld")
    python_module = PythonGenerator(schemafile).compile_module()
    target_class = python_module.__dict__["PhysicalSampleRecord"]
    obj = rdflib_loader.load(datafile, fmt="json-ld", target_class=target_class, schemaview=sv)
    validator = JsonSchemaDataValidator(sv.schema)
    # throws an error if invalid
    validator.validate_object(obj)

    # test deliberately invalid data
    with pytest.raises(Exception):
        bad_obj = rdflib_loader.load(
            input_path("linkml_issue_532_data_fail.jsonld"),
            fmt="json-ld",
            target_class=target_class,
            schemaview=sv,
        )
        validator.validate_object(bad_obj)
