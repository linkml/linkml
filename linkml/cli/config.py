"""
CLI for global config

See docs/config/index.md for documentation
"""

import json

import click
import yaml
from pydantic import BaseModel

from linkml.utils.config import GlobalConfig


@click.group("config")
def config():
    """
    LinkML Global Configuration
    """


@config.command(name="get")
@click.argument("key", required=False)
def get(key=None):
    """
    Get a configuration value. If no setting name is passed, show entire config

    Examples:
    ---------

    .. code-block:: shell

        $ linkml config get

    .. code-block:: yaml

        \b
        user_dir: /Users/jonny/Library/Application Support/linkml
        config_file: /Users/jonny/Library/Application Support/linkml/linkml_config.yaml
        log:
          dir: /Users/jonny/Library/Logs/linkml
          file_name: linkml.log
          level: WARNING
          # ...

    .. code-block:: shell

        $ linkml config get log

    .. code-block:: yaml

        \b
        dir: /Users/jonny/Library/Logs/linkml
        file_name: linkml.log
        level: WARNING
        # ...

    .. code-block:: shell

        $ linkml config get log.level

    .. code-block::

        WARNING


    """
    config = GlobalConfig()
    if key is not None:
        subkeys = key.split(".")
        for subkey in subkeys:
            config = getattr(config, subkey)

    if isinstance(config, BaseModel):
        config = config.model_dump_json()
        config = json.loads(config)
        print(yaml.safe_dump(config, sort_keys=False))
    else:
        print(config)


@config.command(name="set")
@click.argument("key")
@click.argument("value", required=False)
def set(key, value=None):
    """
    Set a configuration value in the global `linkml_config.yaml` file.

    If a ``value`` is absent, the key is deleted from the global yaml config.
    """
    config = GlobalConfig()
    global_config_file = config.config_file
    if global_config_file.exists():
        with open(global_config_file, "r") as f:
            global_config = yaml.safe_load(f)
    else:
        global_config = {}

    subkeys = key.split(".")
    if len(subkeys) == 1:
        if value is None and subkeys[0] in global_config:
            del global_config[subkeys[0]]
        elif value is not None:
            global_config[subkeys[0]] = value

    else:
        config = global_config
        for subkey in subkeys[:-1]:
            config = config.setdefault(subkey, {})
        if value is None and subkeys[-1] in config:
            del config[subkeys[-1]]
        elif value is not None:
            config[subkeys[-1]] = value

    # validate model

    _ = GlobalConfig.model_validate(global_config)

    with open(global_config_file, "w") as f:
        yaml.safe_dump(global_config, f)

    print(f"Updated linkml config:\nkey: {key}\nvalue: {value}\nconfig file: {str(global_config_file)}")
