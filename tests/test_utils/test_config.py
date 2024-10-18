"""
Test configuration settings
"""

from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Callable, Dict

import pytest
import tomli_w
import yaml
from click.testing import CliRunner
from pydantic import ValidationError

from linkml.cli.config import get as cli_get
from linkml.cli.config import set as cli_set
from linkml.utils.config import GlobalConfig, LogConfig, _dirs


def _flatten(d, parent_key="", separator="__") -> dict:
    """https://stackoverflow.com/a/6027615/13113166"""
    items = []
    for key, value in d.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(_flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


@pytest.fixture(scope="module", autouse=True)
def dodge_existing_global_config(tmp_path_factory):
    """
    Suspend any existing global config file during config tests
    """
    tmp_path = tmp_path_factory.mktemp("config_backup")
    default_global_config_path = Path(_dirs.user_config_dir) / "linkml_config.yaml"
    backup_global_config_path = tmp_path / "linkml_config.yaml.bak"

    configured_global_config_path = GlobalConfig().config_file
    backup_configured_global_path = tmp_path / "linkml_config_custom.yaml.bak"

    if default_global_config_path.exists():
        default_global_config_path.rename(backup_global_config_path)
    if configured_global_config_path.exists():
        default_global_config_path.rename(backup_configured_global_path)

    yield

    if backup_global_config_path.exists():
        default_global_config_path.unlink(missing_ok=True)
        backup_global_config_path.rename(default_global_config_path)
    if backup_configured_global_path.exists():
        configured_global_config_path.unlink(missing_ok=True)
        backup_configured_global_path.rename(configured_global_config_path)


@pytest.fixture()
def tmp_cwd(tmp_path, monkeypatch) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture()
def set_env(monkeypatch) -> Callable[[Dict[str, Any]], None]:
    """
    Function fixture to set environment variables using a nested dict
    matching a GlobalConfig.model_dump()
    """

    def _set_env(config: Dict[str, Any]) -> None:
        for key, value in _flatten(config).items():
            key = "LINKML_" + key.upper()
            monkeypatch.setenv(key, str(value))

    return _set_env


@pytest.fixture()
def set_dotenv(tmp_cwd) -> Callable[[Dict[str, Any]], Path]:
    """
    Function fixture to set config variables in a .env file
    """
    dotenv_path = tmp_cwd / ".env"

    def _set_dotenv(config: Dict[str, Any]) -> Path:
        with open(dotenv_path, "w") as dfile:
            for key, value in _flatten(config).items():
                key = "LINKML_" + key.upper()
                dfile.write(f"{key}={value}\n")
        return dotenv_path

    return _set_dotenv


@pytest.fixture()
def set_pyproject(tmp_cwd) -> Callable[[Dict[str, Any]], Path]:
    """
    Function fixture to set config variables in a pyproject.toml file
    """
    toml_path = tmp_cwd / "pyproject.toml"

    def _set_pyproject(config: Dict[str, Any]) -> Path:
        config = {"tool": {"linkml": {"config": config}}}

        with open(toml_path, "wb") as tfile:
            tomli_w.dump(config, tfile)

        return toml_path

    return _set_pyproject


@pytest.fixture()
def set_local_yaml(tmp_cwd) -> Callable[[Dict[str, Any]], Path]:
    """
    Function fixture to set config variables in a local linkml_config.yaml file
    """
    yaml_path = tmp_cwd / "linkml_config.yaml"

    def _set_local_yaml(config: Dict[str, Any]) -> Path:
        with open(yaml_path, "w") as yfile:
            yaml.safe_dump(config, yfile)
        return yaml_path

    return _set_local_yaml


@pytest.fixture()
def set_global_yaml() -> Callable[[Dict[str, Any]], Path]:
    """
    Function fixture to reversibly set config variables in a global linkml_config.yaml file
    """
    global_config_path = Path(_dirs.user_config_dir) / "linkml_config.yaml"
    backup_path = Path(_dirs.user_config_dir) / "linkml_config.yaml.bak"
    restore_backup = global_config_path.exists()

    try:
        if restore_backup:
            global_config_path.rename(backup_path)

        def _set_global_yaml(config: Dict[str, Any]) -> Path:
            with open(global_config_path, "w") as gfile:
                yaml.safe_dump(config, gfile)
            return global_config_path

        yield _set_global_yaml

    finally:
        global_config_path.unlink(missing_ok=True)
        if restore_backup:
            backup_path.rename(global_config_path)


def test_log_level_propagates():
    """
    the level field should propagate to the individual `level_file` etc settings
    when they aren't set
    """
    log_config = LogConfig(level="WARNING", level_file=None, level_stream=None)
    assert log_config.level == "WARNING"
    assert log_config.level_file == "WARNING"
    assert log_config.level_stream == "WARNING"


@pytest.mark.parametrize(
    "setter",
    ["set_env", "set_dotenv", "set_pyproject", "set_local_yaml", "set_global_yaml"],
)
def test_config_sources(setter, request):
    """
    Base test that each of the settings sources in isolation can set values
    """
    assert GlobalConfig().log.level != "WARNING"

    setting = {"log": {"level": "WARNING"}}
    fixture_fn = request.getfixturevalue(setter)
    fixture_fn(setting)
    config = GlobalConfig()
    assert config.log.level == "WARNING"


def test_config_sources_overrides(set_env, set_dotenv, set_pyproject, set_local_yaml, set_global_yaml):
    """Test that the different config sources are overridden in the correct order"""
    set_global_yaml({"log": {"file_n": 0}})
    assert GlobalConfig().log.file_n == 0
    set_pyproject({"log": {"file_n": 1}})
    assert GlobalConfig().log.file_n == 1
    set_local_yaml({"log": {"file_n": 2}})
    assert GlobalConfig().log.file_n == 2
    set_dotenv({"log": {"file_n": 3}})
    assert GlobalConfig().log.file_n == 3
    set_env({"log": {"file_n": 5}})
    assert GlobalConfig().log.file_n == 5
    assert GlobalConfig(**{"log": {"file_n": 6}}).log.file_n == 6


def test_cli_get_config():
    """
    linkml config get <key> can get config values
    """

    config = GlobalConfig()

    # get all values in yaml-serializable form
    runner = CliRunner()
    result = runner.invoke(cli_get)
    printed_value = yaml.safe_load(result.stdout)
    assert GlobalConfig(**printed_value) == config

    # get single value in base model
    runner = CliRunner()
    result = runner.invoke(cli_get, ["user_dir"])
    assert result.stdout.strip() == str(config.user_dir)

    # and a single value in a nested model
    runner = CliRunner()
    result = runner.invoke(cli_get, ["log.level"])
    assert result.stdout.strip() == str(config.log.level)


def test_cli_set_config(set_global_yaml, set_dotenv):
    """
    linkml config set <key> <value> can set config values
    """

    set_global_yaml({"log": {"level": "INFO"}})

    config = GlobalConfig()
    global_config_file = config.config_file

    with open(global_config_file, "r") as gfile:
        assert yaml.safe_load(gfile)["log"]["level"] == "INFO"

    # Setting a value in a nested model
    runner = CliRunner()
    result = runner.invoke(cli_set, ["log.level", "WARNING"])
    with open(global_config_file, "r") as gfile:
        assert yaml.safe_load(gfile)["log"]["level"] == "WARNING"

    # Ensure we validate models

    runner = CliRunner()
    result = runner.invoke(cli_set, ["log.level", "INVALID_VALUE"])
    assert result.exit_code == 1
    assert isinstance(result.exception, ValidationError)

    # Key with no value sets to null, even if `NULL` is not an allowable value
    runner = CliRunner()
    result = runner.invoke(cli_set, ["log.level"])
    assert result.exit_code == 0
    with open(global_config_file, "r") as gfile:
        assert "level" not in yaml.safe_load(gfile)["log"]

    # Can delete multiple times without choking
    runner = CliRunner()
    result = runner.invoke(cli_set, ["log.level"])
    assert result.exit_code == 0
    with open(global_config_file, "r") as gfile:
        assert "level" not in yaml.safe_load(gfile)["log"]
