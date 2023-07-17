import unittest

from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleLevel, TreeRootClassRuleConfig
from linkml.linter.rules import TreeRootClassRule
from linkml.utils.schema_builder import SchemaBuilder

MY_CLASS = "MyClass"
MY_ENUM = "MyEnum"
FULL_NAME = "full_name"
DESC = "description"
CONTAINER = "ContainerClass"


class TestTreeRootClassRule(unittest.TestCase):
    def test_no_tree_root_class(self):
        builder = SchemaBuilder()
        slots = [FULL_NAME, DESC]
        builder.add_class(MY_CLASS, slots)

        schema_view = SchemaView(builder.schema)
        config = TreeRootClassRuleConfig(
            level=RuleLevel.error.text,
            root_class_name=CONTAINER,
            validate_existing_class_name=False,
        )

        rule = TreeRootClassRule(config)
        problems = list(rule.check(schema_view))

        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].message, "Schema does not have class with `tree_root: true`")

    def test_fix_no_tree_root_class(self):
        builder = SchemaBuilder()
        slots = [FULL_NAME, DESC]
        builder.add_class(MY_CLASS, slots)

        schema_view = SchemaView(builder.schema)
        config = TreeRootClassRuleConfig(
            level=RuleLevel.error.text,
            root_class_name=CONTAINER,
            validate_existing_class_name=False,
        )

        rule = TreeRootClassRule(config)
        problems = list(rule.check(schema_view, fix=True))

        # verify that no problems were reported and the fix was made
        self.assertEqual(len(problems), 0)
        container_class = schema_view.get_class(CONTAINER)
        self.assertIsNotNone(container_class)
        self.assertTrue(container_class.tree_root)

        # verify that the schema view can be rechecked (no fix) without problems
        problems = list(rule.check(schema_view))
        self.assertEqual(len(problems), 0)

    def test_existing_tree_root_class_name_matches(self):
        builder = SchemaBuilder()
        slots = [FULL_NAME, DESC]
        builder.add_class(MY_CLASS, slots, tree_root=True)

        schema_view = SchemaView(builder.schema)
        config = TreeRootClassRuleConfig(
            level=RuleLevel.error.text,
            root_class_name=MY_CLASS,
            validate_existing_class_name=True,
        )

        rule = TreeRootClassRule(config)
        problems = list(rule.check(schema_view, fix=True))

        self.assertEqual(len(problems), 0)

    def test_existing_tree_root_class_name_mismatch(self):
        builder = SchemaBuilder()
        slots = [FULL_NAME, DESC]
        builder.add_class(MY_CLASS, slots, tree_root=True)

        schema_view = SchemaView(builder.schema)
        config = TreeRootClassRuleConfig(
            level=RuleLevel.error.text,
            root_class_name=CONTAINER,
            validate_existing_class_name=True,
        )

        rule = TreeRootClassRule(config)
        problems = list(rule.check(schema_view, fix=True))

        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].message, f"Tree root class has name '{MY_CLASS}'")
