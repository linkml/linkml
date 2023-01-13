import importlib
import unittest

from linkml_runtime import SchemaView
from linkml_runtime.loaders import yaml_loader

from linkml.generators.pythongen import PythonGenerator
from linkml.validators import JsonSchemaDataValidator
from tests.test_data.environment import env

SCHEMA = env.input_path("issue_1213_schema.yaml")
DATA_VALID = env.input_path("issue_1213_data_valid.yaml")
DATA_DUPE_IDS = env.input_path("issue_1213_data_dupeids.yaml")
DATA_DUPE_NAMES = env.input_path("issue_1213_data_dupenames.yaml")
CLASSES = env.input_path("issue_1213_classes.py")


class UniqueKeyTestCase(unittest.TestCase):
    def test_range_in_external_yaml(self):
        asserted_person_range = "Person"
        scrutinized_slot = "person_set"
        view = SchemaView(SCHEMA)
        person_set_range = view.get_slot(scrutinized_slot).range
        self.assertEqual(person_set_range, asserted_person_range)

    # todo how do I reuse something from one test in a subsequent test?
    #   fixtures?

    def test_make_view(self):
        view = SchemaView(SCHEMA)
        expected_class_name = "SchemaView"
        # todo check by classname or class path?
        #   self.assertEqual(type(view), SchemaView)
        self.assertEqual(type(view).__name__, expected_class_name)

    def test_serialize_dataclasses(self):
        view = SchemaView(SCHEMA)
        python_dataclasses = PythonGenerator(view.schema).serialize()
        self.assertTrue(len(python_dataclasses) > 0)

    def test_dymanic_class(self):
        classname = "Database"
        view = SchemaView(SCHEMA)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        # todo how to convert the DATA file path into the module path below?
        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)

        # if the classname attribute was retrieved, dynamic_class will have the type <type>
        self.assertEqual(type(dynamic_class), type)

    def test_instantiate_dynamically(self):
        classname = "Database"
        view = SchemaView(SCHEMA)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)
        dynamic_data = yaml_loader.load(DATA_VALID, dynamic_class)

        self.assertEqual(type(dynamic_data).__name__, classname)

    def test_instantiate_dupe_ids(self):
        classname = "Database"
        view = SchemaView(SCHEMA)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)

        dynamic_data = None

        try:
            dynamic_data = yaml_loader.load(DATA_DUPE_IDS, dynamic_class)
        except Exception as e:
            # todo use logger instead?
            print("\n")
            print(e)

        self.assertIsNone(dynamic_data,
                          "Data contain duplicated ids but could still be instantiated against the schema.")

    def test_instantiated_values(self):
        classname = "Database"
        view = SchemaView(SCHEMA)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)
        dynamic_data = yaml_loader.load(DATA_VALID, dynamic_class)

        self.assertEqual(type(dynamic_data).__name__, classname)

        person_set = dynamic_data.person_set
        person_0 = person_set[0]
        person_0_name = person_0.name
        self.assertEqual(person_0_name, "John")

    def test_instantiate_dupe_names(self):
        classname = "Database"
        view = SchemaView(SCHEMA)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)

        dynamic_data = None

        try:
            dynamic_data = yaml_loader.load(DATA_DUPE_NAMES, dynamic_class)
        except Exception as e:
            # todo use logger instead?
            print("\n")
            print(e)

        self.assertIsNone(dynamic_data,
                          "Data contain duplicated names but could still be instantiated against the schema.")

    def test_create_validator(self):
        view = SchemaView(SCHEMA)
        validator = JsonSchemaDataValidator(schema=view.schema)
        self.assertIsNotNone(validator)

    def test_jsonschema_vs_valid(self):
        classname = "Database"

        view = SchemaView(SCHEMA)
        validator = JsonSchemaDataValidator(schema=view.schema)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)

        dynamic_data = yaml_loader.load(DATA_VALID, dynamic_class)
        errs = False
        try:
            validator.validate_object(dynamic_data)
        except Exception as e:
            # todo use logger instead?
            print("\n")
            print(e)
            errs = True
        self.assertTrue(not errs)

    def test_jsonschema_vs_dupe_ids(self):
        classname = "Database"

        view = SchemaView(SCHEMA)
        validator = JsonSchemaDataValidator(schema=view.schema)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)

        errs = False
        try:
            dynamic_data = yaml_loader.load(DATA_DUPE_IDS, dynamic_class)
            validator.validate_object(dynamic_data)
        except Exception as e:
            # todo use logger instead?
            print("\n")
            print(e)
            errs = True

        self.assertTrue(errs)

    def test_jsonschema_vs_dupe_names(self):
        classname = "Database"

        view = SchemaView(SCHEMA)
        validator = JsonSchemaDataValidator(schema=view.schema)

        python_dataclasses = PythonGenerator(view.schema).serialize()
        with open(CLASSES, "w") as f:
            f.writelines(python_dataclasses)

        dynamic_class = getattr(importlib.import_module("tests.test_data.input.issue_1213_classes"), classname)

        errs = False
        try:
            dynamic_data = yaml_loader.load(DATA_DUPE_NAMES, dynamic_class)
            validator.validate_object(dynamic_data)
        except Exception as e:
            print("\n")
            print(e)
            errs = True

        self.assertTrue(errs)
