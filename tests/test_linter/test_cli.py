from pathlib import Path

import pytest
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


@pytest.fixture
def runner():
    """Click test runner fixture."""
    return CliRunner()


def test_no_config(runner):
    with runner.isolated_filesystem():
        write_schema_file()

        result = runner.invoke(main, [SCHEMA_FILE])
        assert result.exit_code == 2
        assert "warning  Class 'Adult' does not have recommended slot 'description'  (recommended)" in result.stdout
        assert "error    Slot 'age_in_yeas' not found on class 'Adult'  (no_invalid_slot_usage)" in result.stdout
        assert "warning  Class has name 'person'  (standard_naming)" in result.stdout


def test_implicit_config_file(runner):
    with runner.isolated_filesystem():
        write_schema_file()
        write_config_file(".linkmllint.yaml")

        result = runner.invoke(main, [SCHEMA_FILE])
        assert result.exit_code == 2
        assert "error    Schema does not have class with `tree_root: true`  (tree_root_class)" in result.stdout
        assert "Class has name 'person'" not in result.stdout


def test_explicit_config_file(runner):
    config_file = "config.yaml"
    with runner.isolated_filesystem():
        write_schema_file()
        write_config_file(config_file)

        result = runner.invoke(main, ["--config", config_file, SCHEMA_FILE])
        assert result.exit_code == 2
        assert "error    Schema does not have class with `tree_root: true`  (tree_root_class)" in result.stdout
        assert "Class has name 'person'" not in result.stdout


def test_config_extends_recommended(runner):
    config_file = "config.yaml"
    with runner.isolated_filesystem():
        write_schema_file()
        write_config_file(config_file, extends_recommended=True)

        result = runner.invoke(main, ["--config", config_file, SCHEMA_FILE])
        assert result.exit_code == 2
        assert "error    Schema does not have class with `tree_root: true`  (tree_root_class)" in result.stdout
        assert "warning  Class has name 'person'  (standard_naming)" in result.stdout


def test_warning_exit_code(runner):
    config_file = "config.yaml"
    with runner.isolated_filesystem():
        write_schema_file()
        write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

        result = runner.invoke(main, ["--config", config_file, SCHEMA_FILE])
        assert result.exit_code == 1
        assert "warning  Schema does not have class with `tree_root: true`  (tree_root_class)" in result.stdout


def test_ignore_warnings_flag(runner):
    config_file = "config.yaml"
    with runner.isolated_filesystem():
        write_schema_file()
        write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

        result = runner.invoke(main, ["--config", config_file, "--ignore-warnings", SCHEMA_FILE])
        assert result.exit_code == 0
        assert "warning  Schema does not have class with `tree_root: true`  (tree_root_class)" in result.stdout


def test_max_warnings_flag(runner):
    config_file = "config.yaml"
    with runner.isolated_filesystem():
        write_schema_file()
        write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

        result = runner.invoke(main, ["--config", config_file, "--max-warnings", 1, SCHEMA_FILE])
        assert result.exit_code == 0
        assert "warning  Schema does not have class with `tree_root: true`  (tree_root_class)" in result.stdout


def test_exceeded_max_warnings_flag(runner):
    config_file = "config.yaml"
    with runner.isolated_filesystem():
        write_schema_file()
        write_config_file(config_file, extends_recommended=False, tree_root_level="warning")

        result = runner.invoke(main, ["--config", config_file, "--max-warnings", 0, SCHEMA_FILE])
        assert result.exit_code == 1
        assert "warning  Schema does not have class with `tree_root: true`  (tree_root_class)" in result.stdout


def test_no_schema_errors(runner):
    with runner.isolated_filesystem():
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

        result = runner.invoke(main, [SCHEMA_FILE])
        assert result.exit_code == 0


def test_directory_of_files(runner):
    schema_dir = Path("schemas")
    schema_a = schema_dir / "schema_a.yaml"
    schema_b = schema_dir / "schema_b.yaml"
    with runner.isolated_filesystem():
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

        result = runner.invoke(main, [str(schema_dir)])
        assert result.exit_code == 1
        assert str(schema_a) in result.stdout
        assert "Class has name 'person'" in result.stdout
        assert str(schema_b) in result.stdout
        assert "Slot has name 'a slot'" in result.stdout


def test_ignores_dot_file_in_directory_when_all_option_omitted(runner):
    schema_dir = Path("schemas")
    schema_a = schema_dir / "schema_a.yaml"
    schema_b = schema_dir / ".schema_b.yaml"
    with runner.isolated_filesystem():
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

        result = runner.invoke(main, [str(schema_dir)])
        assert result.exit_code == 1
        assert str(schema_a) in result.stdout
        assert "Class has name 'person'" in result.stdout
        assert str(schema_b) not in result.stdout
        assert "Slot has name 'a slot'" not in result.stdout


def test_processes_dot_files_in_directory_when_a_option_provided(runner):
    schema_dir = Path("schemas")
    schema_a = schema_dir / "schema_a.yaml"
    schema_b = schema_dir / ".schema_b.yaml"
    with runner.isolated_filesystem():
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

        result = runner.invoke(main, ["-a", str(schema_dir)])
        assert result.exit_code == 1
        assert str(schema_a) in result.stdout
        assert "Class has name 'person'" in result.stdout
        assert str(schema_b) in result.stdout
        assert "Slot has name 'a slot'" in result.stdout


def test_processes_dot_files_in_directory_when_all_option_provided(runner):
    schema_dir = Path("schemas")
    schema_a = schema_dir / "schema_a.yaml"
    schema_b = schema_dir / ".schema_b.yaml"
    with runner.isolated_filesystem():
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

        result = runner.invoke(main, ["--all", str(schema_dir)])
        assert result.exit_code == 1
        assert str(schema_a) in result.stdout
        assert "Class has name 'person'" in result.stdout
        assert str(schema_b) in result.stdout
        assert "Slot has name 'a slot'" in result.stdout


def test_validate_schema(runner):
    with runner.isolated_filesystem():
        with open(SCHEMA_FILE, "w") as f:
            f.write(
                """
id: http://example.org/test
classes:
    person:
        description: a person
"""
            )

        result = runner.invoke(main, ["--validate", SCHEMA_FILE])
        assert result.exit_code == 2
        assert "error    In <root>: 'name' is a required property  (valid-schema)" in result.stdout
        assert "warning  Class has name 'person'  (standard_naming)" in result.stdout


def test_validate_schema_only(runner):
    with runner.isolated_filesystem():
        with open(SCHEMA_FILE, "w") as f:
            f.write(
                """
id: http://example.org/test
classes:
    person:
        description: a person
"""
            )

        result = runner.invoke(main, ["--validate-only", SCHEMA_FILE])
        assert result.exit_code == 2
        assert "error    In <root>: 'name' is a required property  (valid-schema)" in result.stdout
        assert "(standard_naming)" not in result.stdout
