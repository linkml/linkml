import csv
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from linkml.validator.cli import cli

VALID_PERSON_1 = {"id": "id:1", "name": "John Doe", "age": 35}
VALID_PERSON_2 = {"id": "id:2", "name": "Jane Smith", "age": 25, "telephone": "555-555-5550"}
PERSONINFO_SCHEMA = str(Path(__file__).parent / "input/personinfo.yaml")


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def csv_data_file(tmp_path):
    def create(data, filename="data.csv"):
        data_path = tmp_path / filename
        with open(data_path, "w") as data_file:
            writer = csv.DictWriter(data_file, ["id", "name", "age", "telephone"])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return str(data_path)

    return create


@pytest.fixture
def json_data_file(tmp_path):
    def create(data, filename="data.json"):
        data_path = tmp_path / filename
        with open(data_path, "w") as data_file:
            json.dump(data, data_file)
        return str(data_path)

    return create


def test_valid_csv_file(cli_runner, csv_data_file):
    """Verify that two rows of a CSV file successfully validate against an appropriate target class"""

    data_path = csv_data_file([VALID_PERSON_1, VALID_PERSON_2])
    result = cli_runner.invoke(cli, ["-s", PERSONINFO_SCHEMA, "-C", "Person", data_path])
    assert "No issues found" in result.output
    assert result.exception is None
    assert result.exit_code == 0


def test_valid_json_file_object(tmp_path, cli_runner, json_data_file):
    """Verify that a root-level object successfully validates against the tree_root class of the schema"""

    data_path = json_data_file({"persons": [VALID_PERSON_1, VALID_PERSON_2]})
    result = cli_runner.invoke(cli, ["-s", PERSONINFO_SCHEMA, data_path])
    assert result.exception is None
    assert "No issues found" in result.output
    assert result.exit_code == 0


def test_valid_json_file_list(cli_runner, json_data_file):
    """Verify that a root-level list successfully validates against an appropriate target class"""

    data_path = json_data_file([VALID_PERSON_1, VALID_PERSON_2])

    result = cli_runner.invoke(cli, ["-s", PERSONINFO_SCHEMA, "-C", "Person", data_path])
    assert result.exception is None
    assert "No issues found" in result.output
    assert result.exit_code == 0


def test_no_files_provided(cli_runner):
    """Verify a useful message is emitted when no files are specified."""

    result = cli_runner.invoke(cli, [])
    assert "No files specified" in result.output
    assert result.exit_code == 1


def test_schema_against_metamodel_valid(cli_runner):
    """Valid schema passes metamodel validation when no -s flag is given."""

    result = cli_runner.invoke(cli, [PERSONINFO_SCHEMA])
    assert result.exit_code == 0
    assert "No issues found" in result.output


def test_schema_against_metamodel_invalid(cli_runner, tmp_path):
    """Invalid schema reports errors when no -s flag is given."""

    schema_path = tmp_path / "bad_schema.yaml"
    schema_path.write_text(
        """
id: not_a_uri
classes:
  Thing:
    attributes:
      foo:
        description: test
"""
    )
    result = cli_runner.invoke(cli, [str(schema_path)])
    assert result.exit_code == 1
    assert "[ERROR]" in result.output


def test_fix_coerces_types(cli_runner, tmp_path):
    """--fix normalizes data types and validates the result."""

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
id: https://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
default_range: string
classes:
  Thing:
    tree_root: true
    description: Test class.
    attributes:
      name:
        identifier: true
        description: The name.
      count:
        range: integer
        description: A count.
"""
    )
    data_path = tmp_path / "data.yaml"
    data_path.write_text('name: foo\ncount: "5"\n')

    # Without --fix: type error
    result = cli_runner.invoke(cli, ["-s", str(schema_path), str(data_path)])
    assert result.exit_code == 1
    assert "[ERROR]" in result.output

    # With --fix: coerced and valid
    result = cli_runner.invoke(cli, ["-s", str(schema_path), "--fix", str(data_path)])
    assert result.exit_code == 0
    assert "count: 5" in result.output
    assert "[ERROR]" not in result.output


def test_fix_output_is_clean_yaml(cli_runner, tmp_path):
    """--fix stdout is valid YAML with no diagnostic pollution."""

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
id: https://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
default_range: string
classes:
  Thing:
    tree_root: true
    description: Test class.
    attributes:
      name:
        identifier: true
        description: The name.
      count:
        range: integer
        description: A count.
"""
    )
    data_path = tmp_path / "data.yaml"
    data_path.write_text("name: foo\ncount: 5\n")

    result = cli_runner.invoke(cli, ["-s", str(schema_path), "--fix", str(data_path)])
    assert result.exit_code == 0
    # stdout should be parseable YAML with no "No issues found" appended
    parsed = yaml.safe_load(result.output)
    assert isinstance(parsed, dict)
    assert parsed["name"] == "foo"
    assert parsed["count"] == 5
    assert "No issues found" not in result.output


def test_fix_rejects_unsupported_extension(cli_runner, tmp_path):
    """--fix errors clearly on non-YAML/JSON files."""

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(
        """
id: https://example.org/test
name: test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
classes:
  Thing:
    tree_root: true
    description: Test.
    attributes:
      name:
        description: Test.
"""
    )
    data_path = tmp_path / "data.csv"
    data_path.write_text("name\nfoo\n")

    result = cli_runner.invoke(cli, ["-s", str(schema_path), "--fix", str(data_path)])
    assert result.exit_code == 1
    assert ".csv" in result.output
    assert "--fix only supports" in result.output


def test_invalid_json(cli_runner, json_data_file):
    """Verify that validation messages are emitted for invalid data"""

    invalid_data = {**VALID_PERSON_1, "telephone": "asdf"}
    data_path = json_data_file({"persons": [invalid_data]})

    result = cli_runner.invoke(cli, ["-s", PERSONINFO_SCHEMA, data_path])
    assert "[ERROR]" in result.output
    assert "'asdf' does not match" in result.output
    assert "/persons/0/telephone" in result.output
    assert result.exit_code == 1


def test_custom_plugin_config(tmp_path, cli_runner, csv_data_file):
    """Verify that a custom plugin set can be specified via a config file"""

    config_yaml = f"""
schema: {PERSONINFO_SCHEMA}
target_class: Person
plugins:
  RecommendedSlotsPlugin:
"""

    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as config_file:
        config_file.write(config_yaml)

    # This would cause validation error if using the JsonschemaValidationPlugin.
    # But since our config does _not_ include that plugin, we want to verify that
    # we don't see such an error.
    person2 = {**VALID_PERSON_2, "age": "asdf"}
    data_path = csv_data_file([VALID_PERSON_1, person2])
    result = cli_runner.invoke(cli, ["--config", str(config_path), data_path])
    assert result.exception is None
    assert "[WARN]" in result.output
    assert "'telephone' is recommended" in result.output
    assert "[ERROR]" not in result.output
    assert result.exit_code == 0


def test_custom_loader_config(tmp_path, cli_runner, csv_data_file, json_data_file):
    """Verify that a custom loader can be specified via a config file"""

    # With no file extension, attempting to automatically choose a loader would fail. The
    # custom config also sets the `index_slot_name` option so that the data is loaded
    # as an object (instead of individual rows) and validated against the schema's container
    # class.
    csv_data_path = csv_data_file([VALID_PERSON_1, VALID_PERSON_1], filename="data")
    json_data_path = json_data_file({"persons": [VALID_PERSON_1, VALID_PERSON_2]})
    config_yaml = f"""
schema: {PERSONINFO_SCHEMA}
data_sources:
  - {json_data_path}
  - CsvLoader:
      source: {csv_data_path}
      index_slot_name: persons
"""

    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as config_file:
        config_file.write(config_yaml)

    result = cli_runner.invoke(cli, ["--config", str(config_path)])
    print(str(result.exception))
    assert result.exception is None
    assert "No issues found" in result.output
    assert result.exit_code == 0


# --- tests for --allow-null-for-optional-enums  ---
# Uses the existing personinfo.yaml schema which has:
#   - gender slot: range=GenderType enum, required=false (optional) ← perfect for our test


def test_allow_null_for_optional_enums_without_flag(cli_runner, json_data_file):
    """
    Without the flag, empty string in an optional enum slot should be ERROR.
    Uses personinfo.yaml: gender slot is optional with GenderType enum range.
    Verifies backward compatibility — default behavior is unchanged.
    """
    data = [
        {"id": "P:001", "name": "Alice", "gender": "cisgender woman"},
        {"id": "P:002", "name": "Bob", "gender": ""},  # empty — ERROR without flag
    ]
    data_path = json_data_file(data)
    result = cli_runner.invoke(cli, ["-s", PERSONINFO_SCHEMA, "-C", "Person", data_path])

    assert "[ERROR]" in result.output
    assert "'' is not one of" in result.output
    assert result.exit_code == 1


def test_allow_null_for_optional_enums_empty_string(cli_runner, json_data_file):
    """
    With the flag, empty string in an optional enum slot is downgraded to WARN.
    Uses personinfo.yaml: gender slot is optional with GenderType enum range.
    """
    data = [
        {"id": "P:001", "name": "Alice", "gender": "cisgender woman"},
        {"id": "P:002", "name": "Bob", "gender": ""},  # empty string — WARN with flag
    ]
    data_path = json_data_file(data)
    result = cli_runner.invoke(
        cli,
        ["-s", PERSONINFO_SCHEMA, "-C", "Person", "--allow-null-for-optional-enums", data_path],
    )

    assert result.exception is None
    assert "[WARN]" in result.output
    assert "[ERROR]" not in result.output
    assert result.exit_code == 0


def test_allow_null_for_optional_enums_none_value(cli_runner, json_data_file):
    """
    None (JSON null) in an optional enum slot passes cleanly — the JSON Schema
    validator does not raise an error for null on an optional slot, so no
    downgrade is needed.
    """
    data = [
        {"id": "P:001", "name": "Alice", "gender": "cisgender woman"},
        {"id": "P:002", "name": "Bob", "gender": None},  # null — passes cleanly
    ]
    data_path = json_data_file(data)
    result = cli_runner.invoke(
        cli,
        ["-s", PERSONINFO_SCHEMA, "-C", "Person", "--allow-null-for-optional-enums", data_path],
    )

    assert result.exception is None
    assert "No issues found" in result.output
    assert result.exit_code == 0


def test_allow_null_for_optional_enums_valid_value_unaffected(cli_runner, json_data_file):
    """
    With the flag, valid enum values should still pass with no issues.
    Ensures the flag does not suppress legitimate validation.
    """
    data = [
        {"id": "P:001", "name": "Alice", "gender": "cisgender woman"},
        {"id": "P:002", "name": "Bob", "gender": "cisgender man"},
    ]
    data_path = json_data_file(data)
    result = cli_runner.invoke(
        cli,
        ["-s", PERSONINFO_SCHEMA, "-C", "Person", "--allow-null-for-optional-enums", data_path],
    )

    assert result.exception is None
    assert "No issues found" in result.output
    assert result.exit_code == 0
