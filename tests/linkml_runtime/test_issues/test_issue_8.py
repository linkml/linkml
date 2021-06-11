import unittest
from typing import Type

from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition, ClassDefinition
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.test_issues.environment import env


def override(cls: Type[YAMLRoot]):
    def mrf(self, field_name: str) -> None:
        if isinstance(self, SchemaDefinition) and field_name == "name":
            self.name = self.id.rsplit('/', 1)[1]
        elif isinstance(self, SlotDefinition) and field_name == "name":
            self.name = "id"
        elif isinstance(self, ClassDefinition) and field_name == "name":
            self.name = "core"
        else:
            cls.MissingRequiredField(f"{self.__class__.__name}.{field_name}")
    orig = cls.MissingRequiredField
    cls.MissingRequiredField = mrf
    return orig


msgs = set()


def override2():
    def mrf(self, field_name: str) -> None:
        msgs.add(f"{self.__class__.__name__}.{field_name} is not supplied")
    orig = YAMLRoot.MissingRequiredField
    YAMLRoot.MissingRequiredField = mrf
    return orig


class TestErrorIntercept(unittest.TestCase):

    def test_missing_intercept(self):
        test_file = env.input_path('issue_8.yaml')
        with self.assertRaises(ValueError) as e:
            yaml_loader.load(test_file, SchemaDefinition)
        self.assertEqual('name must be supplied', str(e.exception), "ValueError should be raised")

        try:
            orig = override2()
            yaml_loader.load(test_file, SchemaDefinition)
        finally:
            YAMLRoot.MissingRequiredField = orig
        self.assertEqual({'ClassDefinition.name is not supplied',
                          'SlotDefinition.name is not supplied',
                          'SchemaDefinition.name is not supplied'}, msgs)

        try:
            origschd = override(SchemaDefinition)
            origslotd = override(SlotDefinition)
            origcd = override(ClassDefinition)
            yaml_loader.load(test_file, SchemaDefinition)
        finally:
            SchemaDefinition.MissingRequiredField = origschd
            SlotDefinition.MissingRequiredField = origslotd
            ClassDefinition.MissingRequiredField = origcd


if __name__ == '__main__':
    unittest.main()
