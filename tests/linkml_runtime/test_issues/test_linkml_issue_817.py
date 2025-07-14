from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from tests.test_issues.models.model_817 import Container, Person, PersonNoId, VitalStatusEnum


def test_issue_817() -> None:
    person = Person(id="x", name="x", vital_status=VitalStatusEnum("LIVING"))
    person2 = Person(id="y", name="y", vital_status=VitalStatusEnum("DEAD"))
    thing = PersonNoId(name="z", vital_status=VitalStatusEnum("LIVING"))
    c = Container(
        persons_as_list=[person, person2],
        persons_as_dict={person.id: person, person2.id: person2},
        single_person_inlined=person,
        noidobj_as_list=[thing],
        single_noidobj_inlined=thing,
    )
    s = yaml_dumper.dumps(c)
    c2 = yaml_loader.loads(s, Container)
    assert len(c2.persons_as_list) == len(c.persons_as_list)
    assert len(c2.persons_as_dict.values()) == len(c.persons_as_dict.values())
    assert len(c2.noidobj_as_list) == len(c.noidobj_as_list)
