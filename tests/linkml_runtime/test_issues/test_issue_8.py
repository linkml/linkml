import pytest

from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.test_issues.environment import env

# https://github.com/linkml/linkml/issues/8


def override(cls: type[YAMLRoot]):
    orig = cls.MissingRequiredField

    def mrf(self, field_name: str) -> None:
        if isinstance(self, SchemaDefinition) and field_name == "name" and self.id:
            id_parts = self.id.replace("#", "/").rsplit("/")
            self.name = id_parts[-1]
        elif isinstance(self, SlotDefinition) and field_name == "name":
            self.name = "id"
        elif isinstance(self, ClassDefinition) and field_name == "name":
            self.name = "core"
        else:
            orig(self, f"{type(self).__name__}.{field_name}")

    cls.MissingRequiredField = mrf
    return orig


def test_legitimate_error() -> None:
    """Test that legitimate errors are emitted correctly."""
    test_file = env.input_path("issue_8a.yaml")
    with pytest.raises(ValueError, match="name must be supplied"):
        yaml_loader.load(test_file, SchemaDefinition)

    override(SchemaDefinition)
    try:
        with pytest.raises(ValueError, match="SchemaDefinition.name must be supplied"):
            yaml_loader.load(test_file, SchemaDefinition)
    finally:
        delattr(SchemaDefinition, "MissingRequiredField")


def test_missing_intercept() -> None:
    msgs = set()

    def override2():
        def mrf(self, field_name: str) -> None:
            msgs.add(f"{type(self).__name__}.{field_name} is not supplied")

        YAMLRoot.MissingRequiredField = mrf
        return YAMLRoot.MissingRequiredField

    test_file = env.input_path("issue_8.yaml")
    with pytest.raises(ValueError, match="name must be supplied"):
        yaml_loader.load(test_file, SchemaDefinition)

    try:
        orig = override2()
        yaml_loader.load(test_file, SchemaDefinition)
    finally:
        YAMLRoot.MissingRequiredField = orig

    assert msgs == {
        "ClassDefinition.name is not supplied",
        "SlotDefinition.name is not supplied",
        "SchemaDefinition.name is not supplied",
    }
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
