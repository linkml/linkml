import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader

from tests.test_issues.environment import env
from tests.test_issues.models.model_817 import Container, Person, VitalStatusEnum, PersonNoId


class Issue817TestCase(unittest.TestCase):
    env = env

    def _roundtrip(self, c: Container):
        s = yaml_dumper.dumps(c)
        c2 = yaml_loader.loads(s, Container)
        self.assertCountEqual(c2.persons_as_list, c.persons_as_list)
        self.assertCountEqual(c2.persons_as_dict.values(), c.persons_as_dict.values())
        self.assertCountEqual(c2.noidobj_as_list, c.noidobj_as_list)

    def test_issue_817(self):
        person = Person(id='x', name='x', vital_status=VitalStatusEnum('LIVING'))
        person2 = Person(id='y', name='y', vital_status=VitalStatusEnum('DEAD'))
        thing = PersonNoId(name='z', vital_status=VitalStatusEnum('LIVING'))
        c = Container(persons_as_list=[person, person2],
                      persons_as_dict={person.id: person, person2.id: person2},
                      single_person_inlined=person,
                      noidobj_as_list=[thing],
                      single_noidobj_inlined=thing)
        self._roundtrip(c)




if __name__ == '__main__':
    unittest.main()
