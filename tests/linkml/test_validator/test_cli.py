import csv
import json
from pathlib import Path

import pytest
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
    assert result.output == "No issues found\n"
    assert result.exception is None
    assert result.exit_code == 0


def test_valid_json_file_object(tmp_path, cli_runner, json_data_file):
    """Verify that a root-level object successfully validates against the tree_root class of the schema"""

    data_path = json_data_file({"persons": [VALID_PERSON_1, VALID_PERSON_2]})
    result = cli_runner.invoke(cli, ["-s", PERSONINFO_SCHEMA, data_path])
    assert result.exception is None
    assert result.output == "No issues found\n"
    assert result.exit_code == 0


def test_valid_json_file_list(cli_runner, json_data_file):
    """Verify that a root-level list successfully validates against an appropriate target class"""

    data_path = json_data_file([VALID_PERSON_1, VALID_PERSON_2])

    result = cli_runner.invoke(cli, ["-s", PERSONINFO_SCHEMA, "-C", "Person", data_path])
    assert result.exception is None
    assert result.output == "No issues found\n"
    assert result.exit_code == 0


def test_no_schema_provided(cli_runner):
    """Verify a useful message is emitted when a schema is not specified via options or config"""

    result = cli_runner.invoke(cli, [])
    assert "No schema specified" in result.output
    assert result.exit_code == 1


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
    assert result.output == "No issues found\n"
    assert result.exit_code == 0


def test_legacy_mode(csv_data_file, cli_runner):
    """Test that validation is delegated to the old module when the --legacy-mode flag is passed"""
    data_path = csv_data_file([VALID_PERSON_1, VALID_PERSON_2])
    result = cli_runner.invoke(
        cli, ["--legacy-mode", "--index-slot", "persons", "-s", PERSONINFO_SCHEMA, "-C", "Container", data_path]
    )
    assert result.exception is None
    assert result.output == "✓ No problems found\n"
    assert result.exit_code == 0


def test_deprecated_arguments(csv_data_file, cli_runner):
    """Test that a warning is issued when deprecated args are used without --legacy-mode"""
    data_path = csv_data_file([VALID_PERSON_1, VALID_PERSON_2])
    result = cli_runner.invoke(cli, ["--index-slot", "persons", "-s", PERSONINFO_SCHEMA, "-C", "Person", data_path])
    assert result.exception is None
    assert "Warning" in result.output
    assert "-S/--index-slot" in result.output

    result = cli_runner.invoke(cli, ["--module", "foo", "-s", PERSONINFO_SCHEMA, "-C", "Person", data_path])
    assert result.exception is None
    assert "Warning" in result.output
    assert "-m/--module" in result.output

    result = cli_runner.invoke(cli, ["--input-format", "yaml", "-s", PERSONINFO_SCHEMA, "-C", "Person", data_path])
    assert result.exception is None
    assert "Warning" in result.output
    assert "-f/--input-format" in result.output

    result = cli_runner.invoke(
        cli, ["--include-range-class-descendants", "-s", PERSONINFO_SCHEMA, "-C", "Person", data_path]
    )
    assert result.exception is None
    assert "Warning" in result.output
    assert "--include-range-class-descendants" in result.output
