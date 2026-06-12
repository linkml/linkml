"""
Parity tests for dataclassgen, the template-based successor to pythongen.

The gate is semantic, not byte-identical: generated modules must compile and
behave equivalently to pythongen's output when constructing and dumping data.
"""

import pytest
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.dataclassgen import DataclassGenerator
from linkml.generators.pythongen import PythonGenerator

pytestmark = pytest.mark.pythongen

KITCHEN_SINK_DATA = {
    "persons": [
        {
            "id": "P:1",
            "name": "Alice",
            "age_in_years": 33,
            "is_living": "LIVING",
            "aliases": ["Al"],
            "has_employment_history": [
                {"started_at_time": "2020-01-01", "is_current": True, "employed_at": "ROR:1"}
            ],
            "has_familial_relationships": [{"type": "SIBLING_OF", "related_to": "P:2"}],
            "has_medical_history": [
                {"in_location": "GEO:1234", "diagnosis": {"id": "CODE:D0001", "name": "headache"}}
            ],
            "addresses": [{"street": "1 Main St", "city": "Springfield"}],
        },
        {"id": "P:2", "name": "Bob"},
    ],
    "companies": [{"id": "ROR:1", "name": "Acme", "ceo": "P:1"}],
    "activities": [{"id": "A:1", "started_at_time": "2021-01-01", "was_associated_with": "AG:1"}],
}

ORGANIZATION_DATA = {
    "id": "ORG:1",
    "name": "Acme",
    "has_boss": {
        "id": "E:2",
        "last_name": "Boss",
        "first_name": "Big",
        "has_employees": [{"id": "E:1", "last_name": "Worker", "aliases": "Ace", "age_in_years": 40}],
    },
}


@pytest.fixture(scope="module")
def modules(input_path):
    """(schema key -> (dataclassgen module, pythongen module)) for the parity corpus."""
    out = {}
    for key in ("organization", "kitchen_sink"):
        path = str(input_path(f"{key}.yaml"))
        out[key] = (
            compile_python(DataclassGenerator(path).serialize(), f"dcgen_{key}"),
            compile_python(PythonGenerator(path).serialize(), f"pygen_{key}"),
        )
    return out


@pytest.mark.parametrize(
    "schema_key,root_class,data",
    [
        ("organization", "Organization", ORGANIZATION_DATA),
        ("kitchen_sink", "Dataset", KITCHEN_SINK_DATA),
    ],
)
def test_instance_parity_with_pythongen(modules, schema_key, root_class, data):
    """Constructing and dumping the same data through both modules is identical."""
    dc_mod, py_mod = modules[schema_key]
    dc_instance = getattr(dc_mod, root_class)(**data)
    py_instance = getattr(py_mod, root_class)(**data)
    assert yaml_dumper.dumps(dc_instance) == yaml_dumper.dumps(py_instance)


def test_coercion_behaviors(modules):
    """Key YAMLRoot behaviors: identifier coercion, inlined normalization, enum coercion."""
    dc_mod, _ = modules["kitchen_sink"]
    dataset = dc_mod.Dataset(**KITCHEN_SINK_DATA)
    alice = dataset.persons["P:1"] if isinstance(dataset.persons, dict) else dataset.persons[0]
    assert type(alice.id).__name__ == "PersonId"
    assert type(alice.is_living).__name__ == "LifeStatusEnum"
    assert type(alice.has_medical_history[0]).__name__ == "MedicalEvent"
    assert type(alice.has_medical_history[0].diagnosis).__name__ == "DiagnosisConcept"


def test_enum_addvals_and_meanings(modules):
    """Non-identifier permissible values land via _addvals; meanings resolve as namespace members."""
    dc_mod, py_mod = modules["kitchen_sink"]
    assert dc_mod.OtherCodes["a b"].text == py_mod.OtherCodes["a b"].text == "a b"
    assert str(dc_mod.EmploymentEventType.FIRE.meaning) == str(py_mod.EmploymentEventType.FIRE.meaning)


def test_metamodel_self_generation_gate():
    """The Phase 4 parity gate: dataclassgen(meta.yaml) compiles, loads meta.yaml,
    and is schema_as_dict-equal to the vendored pythongen metamodel."""
    import linkml_runtime.linkml_model.meta as vendored
    from linkml_runtime.loaders import yaml_loader
    from linkml_runtime.utils.schema_as_dict import schema_as_dict

    from linkml import LOCAL_METAMODEL_YAML_FILE

    module = compile_python(DataclassGenerator(LOCAL_METAMODEL_YAML_FILE).serialize(), "dcgen_meta")
    generated = yaml_loader.load(str(LOCAL_METAMODEL_YAML_FILE), module.SchemaDefinition)
    reference = yaml_loader.load(str(LOCAL_METAMODEL_YAML_FILE), vendored.SchemaDefinition)
    assert schema_as_dict(generated) == schema_as_dict(reference)


def test_required_field_enforced(modules):
    """Missing required fields raise like pythongen modules do."""
    dc_mod, _ = modules["organization"]
    with pytest.raises(ValueError, match="id must be supplied"):
        dc_mod.Organization(name="No Id")
