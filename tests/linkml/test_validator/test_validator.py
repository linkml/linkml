from collections.abc import Iterable

import pytest
import yaml

from linkml.utils.exceptions import ValidationError
from linkml.validator import Validator
from linkml.validator.loaders import Loader
from linkml.validator.plugins import JsonschemaValidationPlugin, ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition

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

    with pytest.raises(ValidationError, match=r"Error\(s\) validating data.*"):
        report.raise_for_results()


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


# Schema with a custom import URI that resolves (via importmap) to a base schema
# defining abstract MyClass/DataFile. Mirrors the issue #3349 reproduction: the
# equals_string constraint on SpecificFile.label must be enforced, which requires
# the imported definitions to be merged through the importmap rather than cleared.
_BASE_SCHEMA_YAML = """\
id: https://example.org/base_schema/0.1.0
name: base_schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  MyClass:
    abstract: true
    attributes:
      name: {range: string, required: true}
  DataFile:
    abstract: true
    attributes:
      file: {range: string, required: true}
      label: {range: string, required: true}
"""

_USER_SCHEMA_YAML = """\
id: https://example.org/user_schema
name: user_schema
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
  - https://example.org/base_schema/0.1.0
classes:
  MyRoot:
    is_a: MyClass
    tree_root: true
    attributes:
      files:
        range: DataFile
        multivalued: true
        required: true
        minimum_cardinality: 1
  SpecificFile:
    is_a: DataFile
    attributes:
      label:
        equals_string: specific
"""

_BAD_INSTANCE = {"name": "test", "files": [{"file": "/data/file.txt", "label": "wrong_label"}]}
_GOOD_INSTANCE = {"name": "test", "files": [{"file": "/data/file.txt", "label": "specific"}]}


@pytest.fixture
def importmap_factory(tmp_file_factory):
    """Return (user_schema_dict, importmap) for a given importmap style.

    ``kind="path"`` writes the base schema to disk and maps the import URI to that
    path (without the ``.yaml`` suffix). ``kind="dict"`` maps the URI to the base
    schema as an in-memory dict (the pattern used by database-backed callers).
    """

    def factory(kind: str):
        user_schema = yaml.safe_load(_USER_SCHEMA_YAML)
        uri = "https://example.org/base_schema/0.1.0"
        if kind == "path":
            base_path = tmp_file_factory("base_schema.yaml", _BASE_SCHEMA_YAML)
            importmap = {uri: base_path.removesuffix(".yaml")}
        elif kind == "dict":
            importmap = {uri: yaml.safe_load(_BASE_SCHEMA_YAML)}
        else:
            raise ValueError(kind)
        return user_schema, importmap

    return factory


@pytest.mark.parametrize("kind", ["path", "dict"])
def test_importmap_enforces_imported_constraints(importmap_factory, kind):
    """A schema with a custom import URI validates correctly when an importmap is
    supplied: imports are resolved and merged, so the imported equals_string
    constraint is enforced. Regression guard for https://github.com/linkml/linkml/issues/3349.
    """
    user_schema, importmap = importmap_factory(kind)
    validator = Validator(user_schema, [JsonschemaValidationPlugin(closed=True)], importmap=importmap)

    bad_report = validator.validate(_BAD_INSTANCE)
    assert [r.message for r in bad_report.results] == ["'specific' was expected in /files/0/label"]

    good_report = validator.validate(_GOOD_INSTANCE)
    assert good_report.results == []


def test_importmap_stored_on_validator(importmap_factory):
    user_schema, importmap = importmap_factory("dict")
    validator = Validator(user_schema, [JsonschemaValidationPlugin(closed=True)], importmap=importmap)
    assert validator._importmap is importmap


def test_importmap_reused_schema_object_does_not_collide():
    """One SchemaDefinition object validated under two importmaps that map the same
    import URI to different content must produce independent results. The shared JSON
    Schema cache is keyed on id(schema) and omits the importmap, so contexts with an
    importmap bypass it to avoid serving a stale cross-importmap result."""
    uri = "https://example.org/base/0.1.0"
    user = SchemaDefinition(
        id="https://example.org/user",
        name="user",
        prefixes=[{"prefix_prefix": "linkml", "prefix_reference": "https://w3id.org/linkml/"}],
        imports=["linkml:types", uri],
        classes=[ClassDefinition(name="Root", tree_root=True, is_a="Base")],
    )

    def base(expected: str) -> dict:
        return {
            "id": uri,
            "name": "base",
            "prefixes": {"linkml": "https://w3id.org/linkml/"},
            "imports": ["linkml:types"],
            "classes": {"Base": {"attributes": {"code": {"equals_string": expected}}}},
        }

    data = {"code": "AAA"}  # valid only when the imported constraint expects "AAA"

    report_aaa = Validator(user, [JsonschemaValidationPlugin(closed=True)], importmap={uri: base("AAA")}).validate(data)
    report_bbb = Validator(user, [JsonschemaValidationPlugin(closed=True)], importmap={uri: base("BBB")}).validate(data)

    assert report_aaa.results == []
    assert [r.message for r in report_bbb.results] == ["'BBB' was expected in /code"]


def test_no_importmap_defaults_to_none():
    validator = Validator(SCHEMA)
    assert validator._importmap is None
