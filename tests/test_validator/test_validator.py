import unittest
from typing import Iterable

from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition

from linkml.validator import Validator
from linkml.validator.loaders import Loader
from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext

SCHEMA = SchemaDefinition(
    id="testschema",
    name="testschema",
    classes=[
        ClassDefinition(name="TreeRoot", tree_root=True),
        ClassDefinition(name="OtherClass"),
    ],
)


class AcceptAnythingValidationPlugin(ValidationPlugin):
    def process(self, instance: dict, context: ValidationContext) -> Iterable[ValidationResult]:
        return []


class AcceptNothingValidationPlugin(ValidationPlugin):
    def __init__(self, num_results: int) -> None:
        super().__init__()
        self.num_results = num_results

    def process(self, instance: dict, context: ValidationContext) -> Iterable[ValidationResult]:
        for i in range(self.num_results):
            yield ValidationResult(
                type="accept nothing",
                severity=Severity.ERROR,
                message=f"Error number {i}",
                instance=instance,
                instantiates=context.target_class,
            )


class TestDataLoader(Loader):
    def __init__(self, source, how_many) -> None:
        super().__init__(source)
        self.how_many = how_many

    def iter_instances(self) -> Iterable[dict]:
        for i in range(self.how_many):
            yield {"id": i}


class TestValidator(unittest.TestCase):
    def test_validate_valid_instance(self):
        plugins = [AcceptAnythingValidationPlugin()]
        validator = Validator(SCHEMA, plugins)
        report = validator.validate({"foo": "bar"})
        self.assertEqual(len(report.results), 0)

    def test_validate_invalid_instance(self):
        plugins = [AcceptNothingValidationPlugin(10)]
        validator = Validator(SCHEMA, plugins)
        report = validator.validate({"foo": "bar"})
        self.assertEqual(len(report.results), 10)

    def test_validate_multiple_plugins(self):
        plugins = [
            AcceptAnythingValidationPlugin(),
            AcceptNothingValidationPlugin(5),
            AcceptNothingValidationPlugin(10),
        ]
        validator = Validator(SCHEMA, plugins)
        report = validator.validate({"foo": "bar"})
        self.assertEqual(len(report.results), 15)

    def test_iter_results_valid_instance(self):
        plugins = [AcceptAnythingValidationPlugin()]
        validator = Validator(SCHEMA, plugins)
        results = validator.iter_results({"foo": "bar"})
        self.assertRaises(StopIteration, lambda: next(results))

    def test_iter_results_invalid_instance(self):
        plugins = [AcceptNothingValidationPlugin(2)]
        validator = Validator(SCHEMA, plugins)
        results = validator.iter_results({"foo": "bar"})
        self.assertIn("0", next(results).message)
        self.assertIn("1", next(results).message)
        self.assertRaises(StopIteration, lambda: next(results))

    def test_provides_default_target_class_in_context(self):
        plugins = [AcceptNothingValidationPlugin(1)]
        validator = Validator(SCHEMA, plugins)
        results = validator.iter_results({"foo": "bar"})
        result = next(results)
        self.assertEqual(result.instantiates, "TreeRoot")

    def test_provides_custom_target_class_in_context(self):
        plugins = [AcceptNothingValidationPlugin(1)]
        validator = Validator(SCHEMA, plugins)
        target_class = "OtherClass"
        results = validator.iter_results({"foo": "bar"}, target_class)
        result = next(results)
        self.assertEqual(result.instantiates, target_class)

    def test_error_on_missing_target_class(self):
        plugins = [AcceptNothingValidationPlugin(1)]
        validator = Validator(SCHEMA, plugins)
        self.assertRaises(ValueError, lambda: validator.validate({"foo": "bar"}, "NonExistentClass"))

    def test_validate_source(self):
        plugins = [AcceptNothingValidationPlugin(3)]
        validator = Validator(SCHEMA, plugins)
        loader = TestDataLoader(None, 4)
        report = validator.validate_source(loader)
        self.assertEqual(len(report.results), 12)

    def test_iter_results_from_source(self):
        plugins = [AcceptNothingValidationPlugin(2)]
        validator = Validator(SCHEMA, plugins)
        loader = TestDataLoader(None, 5)
        results = list(validator.iter_results_from_source(loader))
        self.assertEqual(len(results), 10)

    def test_no_plugins(self):
        validator = Validator(SCHEMA)
        report = validator.validate({"foo": "bar"})
        self.assertEqual(report.results, [])
