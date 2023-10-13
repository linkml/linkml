from types import ModuleType

from linkml_runtime.loaders import json_loader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


def make_python(infile) -> ModuleType:
    pstr = str(PythonGenerator(infile, mergeimports=True).serialize())
    kitchen_module = compile_python(pstr)
    return kitchen_module


def test_pythongen(kitchen_sink_path):
    """python"""
    kitchen_module = make_python(kitchen_sink_path)
    c = kitchen_module.Company("ROR:1")
    assert str(c) == "Company(id='ROR:1', name=None, aliases=[], ceo=None)"
    h = kitchen_module.EmploymentEvent(employed_at=c.id)
    assert str(h) == (
        "EmploymentEvent(started_at_time=None, ended_at_time=None, is_current=None, "
        "metadata=None, employed_at='ROR:1', type=None)"
    )
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
    assert str(p) == (
        "Person(id='P:1', name=None, has_employment_history=[EmploymentEvent(started_at_time=None, "
        "ended_at_time=None, is_current=None, metadata=None, employed_at='ROR:1', type=None)], "
        "has_familial_relationships=[], has_medical_history=[], age_in_years=None, addresses=[], "
        "has_birth_event=None, species_name=None, stomach_count=None, is_living=None, aliases=[])"
    )

    f = kitchen_module.FamilialRelationship(related_to="me", type="SIBLING_OF", cordialness="heartfelt")
    assert str(f) == (
        "FamilialRelationship(started_at_time=None, ended_at_time=None, related_to='me', "
        "type='SIBLING_OF', cordialness=(text='heartfelt', description='warm and hearty friendliness'))"
    )

    diagnosis = kitchen_module.DiagnosisConcept(id="CODE:D0001", name="headache")
    event = kitchen_module.MedicalEvent(in_location="GEO:1234", diagnosis=diagnosis)
    assert str(event) == (
        "MedicalEvent(started_at_time=None, ended_at_time=None, is_current=None, "
        "metadata=None, in_location='GEO:1234', diagnosis=DiagnosisConcept(id='CODE:D0001', "
        "name='headache', in_code_system=None), procedure=None)"
    )


def test_multiline_stuff(input_path):
    multi_line_module = make_python(input_path("kitchen_sink_mlm.yaml"))

    assert (
        multi_line_module.EmploymentEventType.PROMOTION.description
        == 'This refers to some sort of promotion event.")\n\n\nimport os\n'
        "print('DELETING ALL YOUR STUFF. HA HA HA.')"
    )
