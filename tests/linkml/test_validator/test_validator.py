from collections.abc import Iterable

import pytest
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
    __test__ = False

    def __init__(self, source, how_many) -> None:
        super().__init__(source)
        self.how_many = how_many

    def iter_instances(self) -> Iterable[dict]:
        for i in range(self.how_many):
            yield {"id": i}


def test_validate_valid_instance():
    plugins = [AcceptAnythingValidationPlugin()]
    validator = Validator(SCHEMA, plugins)
    report = validator.validate({"foo": "bar"})
    assert len(report.results) == 0


def test_validate_invalid_instance():
    plugins = [AcceptNothingValidationPlugin(10)]
    validator = Validator(SCHEMA, plugins)
    report = validator.validate({"foo": "bar"})
    assert len(report.results) == 10


def test_validate_multiple_plugins():
    plugins = [
        AcceptAnythingValidationPlugin(),
        AcceptNothingValidationPlugin(5),
        AcceptNothingValidationPlugin(10),
    ]
    validator = Validator(SCHEMA, plugins)
    report = validator.validate({"foo": "bar"})
    assert len(report.results) == 15


def test_iter_results_valid_instance():
    plugins = [AcceptAnythingValidationPlugin()]
    validator = Validator(SCHEMA, plugins)
    results = validator.iter_results({"foo": "bar"})
    with pytest.raises(StopIteration):
        next(results)


def test_iter_results_invalid_instance():
    plugins = [AcceptNothingValidationPlugin(2)]
    validator = Validator(SCHEMA, plugins)
    results = validator.iter_results({"foo": "bar"})
    assert "0" in next(results).message
    assert "1" in next(results).message
    with pytest.raises(StopIteration):
        next(results)


def test_provides_default_target_class_in_context():
    plugins = [AcceptNothingValidationPlugin(1)]
    validator = Validator(SCHEMA, plugins)
    results = validator.iter_results({"foo": "bar"})
    result = next(results)
    assert result.instantiates == "TreeRoot"


def test_provides_custom_target_class_in_context():
    plugins = [AcceptNothingValidationPlugin(1)]
    validator = Validator(SCHEMA, plugins)
    target_class = "OtherClass"
    results = validator.iter_results({"foo": "bar"}, target_class)
    result = next(results)
    assert result.instantiates == target_class


def test_error_on_missing_target_class():
    plugins = [AcceptNothingValidationPlugin(1)]
    validator = Validator(SCHEMA, plugins)
    with pytest.raises(ValueError):
        validator.validate({"foo": "bar"}, "NonExistentClass")


def test_validate_source():
    plugins = [AcceptNothingValidationPlugin(3)]
    validator = Validator(SCHEMA, plugins)
    loader = TestDataLoader(None, 4)
    report = validator.validate_source(loader)
    assert len(report.results) == 12


def test_iter_results_from_source():
    plugins = [AcceptNothingValidationPlugin(2)]
    validator = Validator(SCHEMA, plugins)
    loader = TestDataLoader(None, 5)
    results = list(validator.iter_results_from_source(loader))
    assert len(results) == 10


def test_no_plugins():
    validator = Validator(SCHEMA)
    report = validator.validate({"foo": "bar"})
    assert report.results == []


def test_load_schema_from_path(tmp_file_factory):
    # https://github.com/linkml/linkml/issues/1694
    main_path = tmp_file_factory(
        "main.yaml",
        """id: http://example.org/test_load_schema_from_path/main
prefixes:
  linkml: https://w3id.org/linkml/
default_range: string
imports:
  - base
""",
    )
    tmp_file_factory(
        "base.yaml",
        """id: http://example.org/base
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  AClass:
    attributes:
      an_attribute:
""",
    )

    validator = Validator(main_path, [AcceptAnythingValidationPlugin()])
    assert validator._schema.source_file == main_path

    report = validator.validate({"an_attribute": "something"})
    assert report.results == []
