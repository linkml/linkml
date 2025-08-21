import pytest
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition

from linkml.linter.config.datamodel.config import RuleLevel, TreeRootClassRuleConfig
from linkml.linter.rules import TreeRootClassRule
from linkml.utils.schema_builder import SchemaBuilder

MY_CLASS = "MyClass"
MY_ENUM = "MyEnum"
FULL_NAME = "full_name"
DESC = "description"
CONTAINER = "ContainerClass"


@pytest.fixture
def schema_view():
    """Fixture to create a SchemaView with a predefined class and slots."""
    builder = SchemaBuilder()
    slots = [FULL_NAME, DESC]
    builder.add_class(MY_CLASS, slots)
    return SchemaView(builder.schema)


def test_single_tree_root():
    sb = SchemaBuilder()
    cd_org = ClassDefinition("Organization", slots=[SlotDefinition("name", range="string")], tree_root=True)
    cd_dept = ClassDefinition("Department", slots=["name"], tree_root=True)
    sb.add_class(cd_org)
    sb.add_class(cd_dept)
    config = TreeRootClassRuleConfig(
        level=RuleLevel.error.text,
        root_class_name=CONTAINER,
        validate_existing_class_name=False,
    )
    schema_view = SchemaView(sb.schema)
    rule = TreeRootClassRule(config)
    problems = list(rule.check(schema_view))
    print(problems)
    assert len(problems) == 1


def test_single_tree_root_with_valid_name():
    sb = SchemaBuilder()
    cd_org = ClassDefinition("Organization", slots=[SlotDefinition("name", range="string")], tree_root=True)
    cd_dept = ClassDefinition("Department", slots=["name"], tree_root=True)
    sb.add_class(cd_org)
    sb.add_class(cd_dept)
    config = TreeRootClassRuleConfig(
        level=RuleLevel.error.text,
        root_class_name=CONTAINER,
        validate_existing_class_name=True,
    )
    schema_view = SchemaView(sb.schema)
    rule = TreeRootClassRule(config)
    problems = list(rule.check(schema_view))
    assert len(problems) == 3


def test_no_tree_root_class(schema_view):
    config = TreeRootClassRuleConfig(
        level=RuleLevel.error.text,
        root_class_name=CONTAINER,
        validate_existing_class_name=False,
    )

    rule = TreeRootClassRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 1
    assert problems[0].message == "Schema does not have class with `tree_root: true`"


def test_fix_no_tree_root_class(schema_view):
    config = TreeRootClassRuleConfig(
        level=RuleLevel.error.text,
        root_class_name=CONTAINER,
        validate_existing_class_name=False,
    )

    rule = TreeRootClassRule(config)
    problems = list(rule.check(schema_view, fix=True))

    # Verify that no problems were reported and the fix was made
    assert len(problems) == 0
    container_class = schema_view.get_class(CONTAINER)
    assert container_class is not None
    assert container_class.tree_root

    # Verify that the schema view can be rechecked (no fix) without problems
    problems = list(rule.check(schema_view))
    assert len(problems) == 0


def test_existing_tree_root_class_name_matches(schema_view):
    config = TreeRootClassRuleConfig(
        level=RuleLevel.error.text,
        root_class_name=MY_CLASS,
        validate_existing_class_name=True,
    )

    rule = TreeRootClassRule(config)
    problems = list(rule.check(schema_view, fix=True))

    assert len(problems) == 0


def test_existing_tree_root_class_name_mismatch_fix(schema_view):
    config = TreeRootClassRuleConfig(
        level=RuleLevel.error.text,
        root_class_name=CONTAINER,
        validate_existing_class_name=True,
    )

    rule = TreeRootClassRule(config)
    problems = list(rule.check(schema_view, fix=True))

    assert len(problems) == 0


def test_existing_tree_root_class_name_mismatch(schema_view):
    config = TreeRootClassRuleConfig(
        level=RuleLevel.error.text,
        root_class_name=MY_CLASS,
        validate_existing_class_name=True,
    )

    rule = TreeRootClassRule(config)
    problems = list(rule.check(schema_view, fix=False))
    assert len(problems) == 1
