""" Unit tests for issues encountered in the TCCM model generation """
import logging

import pytest

from linkml.generators.pythongen import PythonGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.utils.generator import Generator
from linkml.utils.schemaloader import SchemaLoader


def test_references_typeerror(input_path):
    """TypeError: sequence item 0: expected str instance, NoneType found is generated from schemasynopsis"""
    SchemaLoader(input_path("issue_tccm/resourcedescription.yaml"), mergeimports=False).resolve()


def test_slot_usage_only(input_path, snapshot):
    """Slot_usages without parents don't generate slots period."""
    output = PythonGenerator(
        input_path("issue_tccm/resourcedescription.yaml"),
        mergeimports=True,
    ).serialize()
    assert output == snapshot("issue_ttcm_1.py")


def test_mapping_prefix(caplog, input_path):
    """Prefix validation fails in"""
    YAMLGenerator(input_path("issue_tccm/illegal_mapping_prefix.yaml"), mergeimports=False).serialize(validateonly=True)

    assert "Unrecognized prefix: DO" in caplog.text, "Basic slot mapping validation failure"
    assert "Unrecognized prefix: RE" in caplog.text, "Basic class mapping validation failure"
    assert "Unrecognized prefix: MI" in caplog.text, "Solo slot usage mapping validation failure"
    assert "Unrecognized prefix: FA" in caplog.text, "Slot usage specialization validation failure"
    assert "Unrecognized prefix: SO" in caplog.text, "Slot usage variant validation failure"
    assert "Unrecognized prefix: LA" in caplog.text, "Inherited slot mapping validation failure"
    assert "Unrecognized prefix: TI" in caplog.text, "Inherited class mapping mapping validation failure"


def test_local_imports(input_path, snapshot):
    """Make sure there is a '.' on a local import in python"""
    output = PythonGenerator(
        input_path("issue_tccm/importee.yaml"),
        mergeimports=False,
    ).serialize()
    assert output == snapshot("issue_tccm/importee.py")

    output = PythonGenerator(
        input_path("issue_tccm/importer.yaml"),
        mergeimports=False,
    ).serialize()
    assert output == snapshot("issue_tccm/importer.py")


def test_minimal_model(input_path, snapshot, tmp_path):
    """Test to make the absolute minimal model work"""
    YAMLGenerator(
        input_path("issue_tccm/minimalmodel.yaml"),
        mergeimports=False,
        log_level=logging.INFO,
    ).serialize(validateonly=True)

    for generator in Generator.__subclasses__():
        if (
            not generator.__module__.startswith("linkml.generators")
            or generator.__name__ == "SQLDDLGenerator"
            or getattr(generator.serialize, "__isabstractmethod__", True)
        ):
            pass
        elif not generator.directory_output:
            output = generator(
                input_path("issue_tccm/minimalmodel.yaml"),
                mergeimports=False,
                emit_metadata=False,
            ).serialize()
            assert output == snapshot(f"issue_tccm/minimalmodel.{generator.valid_formats[0]}")
        else:
            output_dir = str(tmp_path / "issue_tccm" / generator.__name__)
            generator(
                input_path("issue_tccm/minimalmodel.yaml"),
                mergeimports=False,
                emit_metadata=False,
            ).serialize(directory=output_dir)
            assert output_dir == snapshot(f"issue_tccm/{generator.__name__}")


@pytest.mark.skip("Outstanding issue")
def test_dictionary_name(input_path, snapshot):
    """Allow dictionaries w/ explicit keys or identifiers through as long as they match"""
    output = (
        YAMLGenerator(
            input_path("issue_tccm/explicit_key_id.yaml"),
            mergeimports=False,
            emit_metadata=False,
        ).serialize(),
    )
    assert output == snapshot("issue_tccm/explicit_key_id.yaml")
