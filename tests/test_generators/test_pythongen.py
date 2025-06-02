import re
from types import ModuleType

import pytest
from linkml_runtime.loaders import json_loader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator

pytestmark = pytest.mark.pythongen


def make_python(infile) -> ModuleType:
    pstr = str(PythonGenerator(infile, mergeimports=True).serialize())
    kitchen_module = compile_python(pstr)
    return kitchen_module


def test_pythongen(kitchen_sink_path):
    """python"""
    kitchen_module = make_python(kitchen_sink_path)
    c = kitchen_module.Company("ROR:1")
    assert str(c) == "Company({'id': 'ROR:1'})"
    h = kitchen_module.EmploymentEvent(employed_at=c.id)
    assert str(h) == "EmploymentEvent({'employed_at': 'ROR:1'})"
    p = kitchen_module.Person("P:1", has_employment_history=[h])
    assert p.id == "P:1"
    assert p.has_employment_history[0] is not None
    assert p.has_employment_history[0].employed_at == c.id

    # Inline lists work:
    p2dict = {
        "id": "P:2",
        "addresses": [{"street": "1 foo street", "city": "foo city"}],
    }
    json_loader.loads(p2dict, kitchen_module.Person)

    # however, inline in a non-list context does not
    p2dict = {"id": "P:2", "has_birth_event": {"started_at_time": "1981-01-01"}}
    json_loader.loads(p2dict, kitchen_module.Person)
    assert str(p) == "Person({'id': 'P:1', 'has_employment_history': [EmploymentEvent({'employed_at': 'ROR:1'})]})"

    f = kitchen_module.FamilialRelationship(related_to="me", type="SIBLING_OF", cordialness="heartfelt")
    assert (
        str(f)
        == """FamilialRelationship({
  'related_to': 'me',
  'type': 'SIBLING_OF',
  'cordialness': CordialnessEnum(text='heartfelt', description='warm and hearty friendliness')
})"""
    )

    diagnosis = kitchen_module.DiagnosisConcept(id="CODE:D0001", name="headache")
    event = kitchen_module.MedicalEvent(in_location="GEO:1234", diagnosis=diagnosis)
    assert (
        str(event)
        == """MedicalEvent({
  'in_location': 'GEO:1234',
  'diagnosis': DiagnosisConcept({'id': 'CODE:D0001', 'name': 'headache'})
})"""
    )


def test_multiline_stuff(input_path):
    multi_line_module = make_python(input_path("kitchen_sink_mlm.yaml"))

    assert (
        multi_line_module.EmploymentEventType.PROMOTION.description
        == 'This refers to some sort of promotion event.")\n\n\nimport os\n'
        "print('DELETING ALL YOUR STUFF. HA HA HA.')"
    )


def test_enum_permissiblevalue_ifabsent(input_path):
    # this would fail if generated python code is not compilable
    ksm = make_python(input_path("kitchen_sink_ifabsent.yaml"))
    # ensure that the right permissible value is taken if other value absent
    assert ksm.IfAbsent().ifabsent_not_literal is ksm.CordialnessEnum.heartfelt


def test_head():
    """Validate the head/nohead parameter"""
    yaml = """id: "https://w3id.org/biolink/metamodel"
description: Metamodel for biolink schema
license: https://creativecommons.org/publicdomain/zero/1.0/
version: 0.4.0
default_range: string
prefixes:
    xsd: http://www.w3.org/2001/XMLSchema#
types:
   string:
      base: str
      uri: xsd:string"""

    output = PythonGenerator(
        yaml,
        format="py",
        metadata=True,
        source_file_date="August 10, 2020",
        source_file_size=173,
    ).serialize()
    assert output.startswith(
        f"# Auto generated from None by pythongen.py version: " f"{PythonGenerator.generatorversion}"
    )

    output = PythonGenerator(yaml, format="py", metadata=False).serialize()
    assert output.startswith("\n# id: https://w3id.org/biolink/metamodel")


def test_repr(kitchen_sink_path):
    """
    Be default, don't create __repr__ for dataclasses, but do if requested!
    """
    parentclass = """
class ParentClass:
    def __repr__(self):
        return "overridden"

    def __post_init__(self, *args, **kwargs):
        pass
"""

    pstr = str(PythonGenerator(kitchen_sink_path).serialize())
    pstr = parentclass + pstr
    pstr = re.sub(r"\(YAMLRoot\)", "(ParentClass)", pstr)
    kitchen_module = compile_python(pstr)

    # if a dataclass has `repr=False`, it shouldn't override the parent class's
    friend = kitchen_module.Friend(name="bestie")
    assert repr(friend) == "overridden"

    # but we should be able to make pythongenerator do `repr=True`, where the dataclasses _do_ override
    pstr = str(PythonGenerator(kitchen_sink_path, dataclass_repr=True).serialize())
    pstr = parentclass + pstr
    pstr = re.sub(r"\(YAMLRoot\)", "(ParentClass)", pstr)
    kitchen_module = compile_python(pstr)
    friend = kitchen_module.Friend(name="bestie")
    assert repr(friend) != "overridden"
