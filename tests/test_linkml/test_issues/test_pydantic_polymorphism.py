import re

import pytest
from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError

from linkml.generators.pydanticgen import PydanticGenerator


def test_pydantic_obey_range(schema_str):
    gen = PydanticGenerator(schema_str)
    output = gen.serialize()

    assert re.match(r"Union\[[a-zA-Z0-9]*\]", output) is None, "a python Union should always have more than one option"

    output_subset = [line for line in output.splitlines() if "thingtype" in line]
    assert len(output_subset) > 0

    assert len([x for x in output_subset if "x:Person" in x]) == 1

    gen = PydanticGenerator(schema_str.replace("uriorcurie", "uri"))
    output = gen.serialize()
    output_subset = [line for line in output.splitlines() if "thingtype" in line]
    assert len(output_subset) > 0
    assert len([x for x in output_subset if "http://example.org/Person" in x]) == 1


def test_type_hierarchy(type_hierarchy_schema_str):
    gen_range_not_specified = PydanticGenerator(type_hierarchy_schema_str)
    output = gen_range_not_specified.serialize()
    mod = compile_python(output, "testschema")
    id = "TEST:1"
    _ = mod.Person(id=id)
    _ = mod.Person(id=id, category=["http://example.org/Person"])
    _ = mod.Person(id=id, category=["x:Person"])
    with pytest.raises(ValidationError):
        mod.Person(category=["x:NamedThing"])


def test_pydantic_load_poly_data(schema_str, data_str):
    gen = PydanticGenerator(schema_str)
    output = gen.serialize()
    mod = compile_python(output, "testschema")
    data = mod.Container.model_validate_json(data_str)

    assert len([x for x in data.things if isinstance(x, mod.Person)]) == 1
    assert len([x for x in data.things if isinstance(x, mod.Organisation)]) == 1
