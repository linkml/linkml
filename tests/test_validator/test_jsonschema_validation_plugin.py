import unittest
from pathlib import Path

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.validation_context import ValidationContext

PERSONINFO_SCHEMA = str(Path(__file__).parent / "input/personinfo.yaml")


class TestJsonschemaValidationPlugin(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        schema = yaml_loader.load(PERSONINFO_SCHEMA, SchemaDefinition)
        cls._context = ValidationContext(schema, "Person")

    def test_valid_instance(self):
        plugin = JsonschemaValidationPlugin()
        instance = {"id": "1", "full_name": "Person One"}
        result_iter = plugin.process(instance, self._context)
        self.assertRaises(StopIteration, lambda: next(result_iter))

    def test_invalid_instance(self):
        plugin = JsonschemaValidationPlugin()
        instance = {"id": "1", "full_name": "Person One", "phone": "555-CALL-NOW"}
        result_iter = plugin.process(instance, self._context)
        self.assertIn("'555-CALL-NOW' does not match", next(result_iter).message)
        self.assertRaises(StopIteration, lambda: next(result_iter))

    def test_invalid_instance_closed(self):
        plugin = JsonschemaValidationPlugin(closed=True)
        instance = {
            "id": "1",
            "full_name": "Person One",
            "whoops": "my bad",
        }
        result_iter = plugin.process(instance, self._context)
        message = next(result_iter).message
        self.assertIn("Additional properties", message)
        self.assertIn("whoops", message)
        self.assertRaises(StopIteration, lambda: next(result_iter))
