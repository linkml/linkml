import unittest
from pathlib import Path

from click.testing import CliRunner

from linkml.linter.cli import main

SCHEMA_FILE = "schema.yaml"


def write_schema_file() -> None:
    with open(SCHEMA_FILE, "w") as f:
        f.write(
            """
id: http://example.org/test
name: test

slots:
  age_in_years:
    range: integer
    minimum_value: 0
    maximum_value: 999

classes:
  person:
    description: a person
    slots:
      - age_in_years

  Adult:
    is_a: person
    slot_usage:
      age_in_yeas:
        minimum_value: 18
"""
        )


def write_config_file(name: str, extends_recommended: bool = False, tree_root_level: str = "error") -> None:
    with open(name, "w") as f:
        if extends_recommended:
            f.write(
                """
extends: recommended
"""
            )
        f.write(
            f"""
rules:
  tree_root_class:
    level: {tree_root_level}
"""
        )


class TestLinterCli(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_no_config(self):
        with self.runner.isolated_filesystem():
            write_schema_file()

            result = self.runner.invoke(main, [SCHEMA_FILE])
            self.assertEqual(result.exit_code, 2)
            self.assertIn(
                "warning  Class 'Adult' does not have recommended slot 'description'  (recommended)",
                result.stdout,
            )
            self.assertIn(
                "error    Slot 'age_in_yeas' not found on class 'Adult'  (no_invalid_slot_usage)",
                result.stdout,
            )
            self.assertIn("warning  Class has name 'person'  (standard_naming)", result.stdout)

    def test_implicit_config_file(self):
        with self.runner.isolated_filesystem():
            write_schema_file()
            write_config_file(".linkmllint.yaml")

            result = self.runner.invoke(main, [SCHEMA_FILE])
            self.assertEqual(result.exit_code, 2)
            self.assertIn(
                "error    Schema does not have class with `tree_root: true`  (tree_root_class)",
                result.stdout,
            )
            self.assertNotIn("Class has name 'person'", result.stdout)

    def test_explicit_config_file(self):
        config_file = "config.yaml"
        with self.runner.isolated_filesystem():
            write_schema_file()
            write_config_file(config_file)

            result = self.runner.invoke(main, ["--config", config_file, SCHEMA_FILE])
            self.assertEqual(result.exit_code, 2)
            self.assertIn(
                "error    Schema does not have class with `tree_root: true`  (tree_root_class)",
                result.stdout,
            )
            self.assertNotIn("Class has name 'person'", result.stdout)

    def test_config_extends_recommended(self):
        config_file = "config.yaml"
        with self.runner.isolated_filesystem():
            write_schema_file()
            write_config_file(config_file, extends_recommended=True)

            result = self.runner.invoke(main, ["--config", config_file, SCHEMA_FILE])
            self.assertEqual(result.exit_code, 2)
            self.assertIn(
                "error    Schema does not have class with `tree_root: true`  (tree_root_class)",
                result.stdout,
            )
            self.assertIn("warning  Class has name 'person'  (standard_naming)", result.stdout)

    def test_warning_exit_code(self):
        config_file = "config.yaml"
        with self.runner.isolated_filesystem():
            write_schema_file()
            write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

            result = self.runner.invoke(main, ["--config", config_file, SCHEMA_FILE])
            self.assertEqual(result.exit_code, 1)
            self.assertIn(
                "warning  Schema does not have class with `tree_root: true`  (tree_root_class)",
                result.stdout,
            )

    def test_ignore_warnings_flag(self):
        config_file = "config.yaml"
        with self.runner.isolated_filesystem():
            write_schema_file()
            write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

            result = self.runner.invoke(main, ["--config", config_file, "--ignore-warnings", SCHEMA_FILE])
            self.assertEqual(result.exit_code, 0)
            self.assertIn(
                "warning  Schema does not have class with `tree_root: true`  (tree_root_class)",
                result.stdout,
            )

    def test_max_warnings_flag(self):
        config_file = "config.yaml"
        with self.runner.isolated_filesystem():
            write_schema_file()
            write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

            result = self.runner.invoke(main, ["--config", config_file, "--max-warnings", 1, SCHEMA_FILE])
            self.assertEqual(result.exit_code, 0)
            self.assertIn(
                "warning  Schema does not have class with `tree_root: true`  (tree_root_class)",
                result.stdout,
            )

    def test_exceeded_max_warnings_flag(self):
        config_file = "config.yaml"
        with self.runner.isolated_filesystem():
            write_schema_file()
            write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

            result = self.runner.invoke(main, ["--config", config_file, "--max-warnings", 0, SCHEMA_FILE])
            self.assertEqual(result.exit_code, 1)
            self.assertIn(
                "warning  Schema does not have class with `tree_root: true`  (tree_root_class)",
                result.stdout,
            )

    def test_no_schema_errors(self):
        with self.runner.isolated_filesystem():
            with open(SCHEMA_FILE, "w") as f:
                f.write(
                    """
id: http://example.org/test
name: test

classes:
  Person:
    description: An individual human
"""
                )

            result = self.runner.invoke(main, [SCHEMA_FILE])
            self.assertEqual(result.exit_code, 0)

    def test_directory_of_files(self):
        schema_dir = Path("schemas")
        schema_a = schema_dir / "schema_a.yaml"
        schema_b = schema_dir / "schema_b.yaml"
        with self.runner.isolated_filesystem():
            schema_dir.mkdir()
            schema_a.write_text(
                """
id: http://example.org/test_a
name: test_a

classes:
  person:
    description: An individual human
"""
            )
            schema_b.write_text(
                """
id: http://example.org/test_b
name: test_b

slots:
  a slot:
    description: A slot to hold thing
"""
            )

            result = self.runner.invoke(main, [str(schema_dir)])
            self.assertEqual(result.exit_code, 1)
            self.assertIn(str(schema_a), result.stdout)
            self.assertIn("Class has name 'person'", result.stdout)
            self.assertIn(str(schema_b), result.stdout)
            self.assertIn("Slot has name 'a slot'", result.stdout)

    def test_ignores_dot_file_in_directory_when_all_option_omitted(self):
        schema_dir = Path("schemas")
        schema_a = schema_dir / "schema_a.yaml"
        schema_b = schema_dir / ".schema_b.yaml"
        with self.runner.isolated_filesystem():
            schema_dir.mkdir()
            schema_a.write_text(
                """
id: http://example.org/test_a
name: test_a

classes:
  person:
    description: An individual human
"""
            )
            schema_b.write_text(
                """
id: http://example.org/test_b
name: test_b

slots:
  a slot:
    description: A slot to hold thing
"""
            )

            result = self.runner.invoke(main, [str(schema_dir)])
            self.assertEqual(result.exit_code, 1)
            self.assertIn(str(schema_a), result.stdout)
            self.assertIn("Class has name 'person'", result.stdout)
            self.assertNotIn(str(schema_b), result.stdout)
            self.assertNotIn("Slot has name 'a slot'", result.stdout)

    def test_processes_dot_files_in_directory_when_a_option_provided(self):
        schema_dir = Path("schemas")
        schema_a = schema_dir / "schema_a.yaml"
        schema_b = schema_dir / ".schema_b.yaml"
        with self.runner.isolated_filesystem():
            schema_dir.mkdir()
            schema_a.write_text(
                """
id: http://example.org/test_a
name: test_a

classes:
  person:
    description: An individual human
"""
            )
            schema_b.write_text(
                """
id: http://example.org/test_b
name: test_b

slots:
  a slot:
    description: A slot to hold thing
"""
            )

            result = self.runner.invoke(main, ["-a", str(schema_dir)])
            self.assertEqual(result.exit_code, 1)
            self.assertIn(str(schema_a), result.stdout)
            self.assertIn("Class has name 'person'", result.stdout)
            self.assertIn(str(schema_b), result.stdout)
            self.assertIn("Slot has name 'a slot'", result.stdout)

    def test_processes_dot_files_in_directory_when_all_option_provided(self):
        schema_dir = Path("schemas")
        schema_a = schema_dir / "schema_a.yaml"
        schema_b = schema_dir / ".schema_b.yaml"
        with self.runner.isolated_filesystem():
            schema_dir.mkdir()
            schema_a.write_text(
                """
id: http://example.org/test_a
name: test_a

classes:
  person:
    description: An individual human
"""
            )
            schema_b.write_text(
                """
id: http://example.org/test_b
name: test_b

slots:
  a slot:
    description: A slot to hold thing
"""
            )

            result = self.runner.invoke(main, ["--all", str(schema_dir)])
            self.assertEqual(result.exit_code, 1)
            self.assertIn(str(schema_a), result.stdout)
            self.assertIn("Class has name 'person'", result.stdout)
            self.assertIn(str(schema_b), result.stdout)
            self.assertIn("Slot has name 'a slot'", result.stdout)

    def test_validate_schema(self):
        with self.runner.isolated_filesystem():
            with open(SCHEMA_FILE, "w") as f:
                f.write(
                    """
id: http://example.org/test
classes:
    person:
        description: a person
"""
                )

            result = self.runner.invoke(main, ["--validate", SCHEMA_FILE])
            self.assertEqual(result.exit_code, 2)
            self.assertIn(
                "error    In <root>: 'name' is a required property  (valid-schema)",
                result.stdout,
            )
            self.assertIn(
                "warning  Class has name 'person'  (standard_naming)",
                result.stdout,
            )

    def test_validate_schema_only(self):
        with self.runner.isolated_filesystem():
            with open(SCHEMA_FILE, "w") as f:
                f.write(
                    """
id: http://example.org/test
classes:
    person:
        description: a person
"""
                )

            result = self.runner.invoke(main, ["--validate-only", SCHEMA_FILE])
            self.assertEqual(result.exit_code, 2)
            self.assertIn(
                "error    In <root>: 'name' is a required property  (valid-schema)",
                result.stdout,
            )
            self.assertNotIn("(standard_naming)", result.stdout)
