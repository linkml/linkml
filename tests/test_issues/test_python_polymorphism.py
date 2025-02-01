import json

import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


def test_pythongenerator_loads_poly(schema_str, data_str):
    gen = PythonGenerator(schema_str)
    output = gen.serialize()
    print(output)
    mod = compile_python(output, "testschema")
    json_data = json.loads(data_str)
    print(json_data)
    cont = mod.Container(**json_data)
    assert 1 == len([x for x in cont.things if type(x) is mod.Person])
    assert 1 == len([x for x in cont.things if type(x) is mod.Organisation])


def test_type_hierarchy(type_hierarchy_schema_str):
    gen_range_not_specified = PythonGenerator(type_hierarchy_schema_str)
    output = gen_range_not_specified.serialize()
    mod = compile_python(output, "testschema")
    _ = mod.Person(id=1)
    # TODO: support URI vs CURIE polymorphism
    # _ = mod.Person(id=2,category='http://example.org/Person')
    _ = mod.Person(id=3, category="x:Person")
    pytest.raises(ValueError, lambda: mod.Person(id=4, category="x:NamedThing"))


def test_class_instantiation_without_designator(schema_str):
    gen = PythonGenerator(schema_str)
    output = gen.serialize()
    mod = compile_python(output, "testschema")
    person = mod.Person(height=80, full_name="Frank", id=1)
    organisation = mod.Organisation(number_of_employees=70, id=2)
    named = mod.NamedThing(full_name="banana", id=3)
    assert person.height == 80
    assert organisation.number_of_employees == 70
    assert type(named) is mod.NamedThing
    assert named.thingtype == "x:NamedThing"
    # TODO
    # assert person.thingtype == "http://testbreaker/not-the-uri-you-expect"
    assert organisation.thingtype == "x:Organisation"
    forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="x:ForProfit")
    assert isinstance(forProfit, mod.ForProfit)
    # TODO
    # forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="http://example.org/ForProfit")
    # assert isinstance(forProfit, mod.ForProfit)


def test_type_designator_ranges(schema_str):
    gen = PythonGenerator(schema_str)
    output = gen.serialize()
    mod = compile_python(output, "testschema")
    forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="x:ForProfit")
    assert isinstance(forProfit, mod.ForProfit)
    # TODO
    # forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="http://example.org/ForProfit")
    # assert isinstance(forProfit, mod.ForProfit)
    # gen = PythonGenerator(schema_str)
    # output = gen.serialize()
    # mod = compile_python(output, "testschema")
    # forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="ForProfit")
    # assert isinstance(forProfit, mod.ForProfit)
