import unittest
from typing import Type

from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition, ClassDefinition
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.test_issues.environment import env


def override(cls: Type[YAMLRoot]):
    orig = cls.MissingRequiredField
    def mrf(self, field_name: str) -> None:
        if isinstance(self, SchemaDefinition) and field_name == "name" and self.id:
            id_parts = self.id.replace('#', '/').rsplit('/')
            self.name = id_parts[-1]
        elif isinstance(self, SlotDefinition) and field_name == "name":
            self.name = "id"
        elif isinstance(self, ClassDefinition) and field_name == "name":
            self.name = "core"
        else:
            orig(self, f"{type(self).__name__}.{field_name}")
    cls.MissingRequiredField = mrf
    return orig


msgs = set()


def override2():
    def mrf(self, field_name: str) -> None:
        msgs.add(f"{type(self).__name__}.{field_name} is not supplied")
    orig = YAMLRoot.MissingRequiredField
    YAMLRoot.MissingRequiredField = mrf
    return orig


class TestErrorIntercept(unittest.TestCase):

    def test_legitimate_error(self):
        """ Test that legitimate errors are emitted correctly """
        test_file = env.input_path('issue_8a.yaml')
        with self.assertRaises(ValueError) as e:
            yaml_loader.load(test_file, SchemaDefinition)
        self.assertEqual('name must be supplied', str(e.exception), "ValueError should be raised")
        orig = override(SchemaDefinition)
        try:
            with self.assertRaises(ValueError) as e:
                yaml_loader.load(test_file, SchemaDefinition)
            self.assertEqual('SchemaDefinition.name must be supplied', str(e.exception))
        finally:
            # SchemaDefinition.MissingRequiredField = orig
            delattr(SchemaDefinition, "MissingRequiredField")

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
            delattr(SchemaDefinition, "MissingRequiredField")
            delattr(SlotDefinition, "MissingRequiredField")
            delattr(ClassDefinition, "MissingRequiredField")
            # SchemaDefinition.MissingRequiredField = origschd
            # SlotDefinition.MissingRequiredField = origslotd
            # ClassDefinition.MissingRequiredField = origcd


if __name__ == '__main__':
    unittest.main()
