import pytest
from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError

from linkml.generators.pydanticgen import PydanticGenerator


def test_pydanticgen_required_slots(input_path):
    """
    Test for https://github.com/linkml/linkml/issues/1429

    Ensures that required slots are required in the generated pydantic class
    """
    SCHEMA = input_path("linkml_issue_1429.yaml")
    id = "ORCID:1234"
    full_name = "a b"
    gen = PydanticGenerator(SCHEMA)
    output = gen.serialize()
    mod = compile_python(output, "testschema")
    with pytest.raises(ValidationError):
        p = mod.Person()
    with pytest.raises(ValidationError):
        p = mod.Person(id=id)
    with pytest.raises(ValidationError):
        p = mod.Person(full_name=full_name)
    p = mod.Person(id=id, full_name=full_name)
    assert id == p.id
    assert full_name == p.full_name
