import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueInlinedWithEnumsTestCase(TestEnvironmentTestCase):
    """
    Tests https://github.com/linkml/linkml/issues/817
    """

    env = env

    def _roundtrip(self, obj, tc):
        v = yaml_dumper.dumps(obj)
        obj2 = yaml_loader.loads(v, target_class=tc)
        self.assertEqual(obj, obj2)
        return obj2

    def test_inline(self):
        name = "linkml_issue_817"
        infile = env.input_path(f"{name}.yaml")
        pygen = PythonGenerator(infile)
        mod = pygen.compile_module()
        p = mod.Person(id="x", name="x", vital_status=mod.VitalStatusEnum("LIVING"))
        c = mod.Container()
        c.persons_as_list = [p]
        # c.persons_as_dict = {p.id: p}
        self._roundtrip(c, mod.Container)
        c = mod.Container(persons_as_list=[p], persons_as_dict=[p])
        self.assertEqual(c.persons_as_dict[p.id].name, p.name)
        c2 = self._roundtrip(c, mod.Container)
        self.assertEqual(c2.persons_as_dict[p.id].name, p.name)


if __name__ == "__main__":
    unittest.main()
