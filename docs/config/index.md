# Configuration

Global configuration in linkml uses [`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)


## Sources

Config values can be set (in order of priority from high to low, where higher
priorities override lower priorities)

* in the arguments passed to the class constructor (not user configurable)
* in environment variables like `export LINKML_LOG_DIR=~/`
* in a `.env` file in the working directory
* in a `linkml_config.yaml` file in the working directory
* in the `tool.linkml.config` table in a `pyproject.toml` file in the working directory
* in the global `linkml_config.yaml` file in the platform-specific data directory
  (use `linkml config get global_config` to find its location)
* the default values in the :class:`.Config` model

Parent directories are _not_ checked.

## Keys

### Prefix

Keys for environment variables (i.e. set in a shell with e.g. `export` or in a `.env` file)
are prefixed with `LINKML_` to not shadow other environment variables.
Keys in `toml` or `yaml` files are not prefixed with `LINKML_` .

### Nesting

Keys for nested models are separated by a `__` double underscore in `.env`
files or environment variables (eg. `LINKML_LOG__DIR`)

Keys in `toml` or `yaml` files do not have a dunder separator because
they can represent the nesting directly (see examples below)

When setting values from the cli, keys for nested models are separated with a `.`.

### Case

Keys are case-insensitive, i.e. these are equivalent::

    export LINKML_LOG__DIR=~/
    export linkml_log__dir=~/

## CLI

Global settings can be gotten and set via the CLI, for example:

### Getting values

```{command-output} linkml config get
---
ellipsis: 5
---
``` 

Index nested config models with `.`

```{command-output} linkml config get log.level
```

### Setting values

Values are set in the global `linkml_config.yaml` file with a similar syntax

```{note}
Values set via the CLI are set in the global `linkml_config.yaml`
file, which is the lowest priority source of settings, and will thus be
overridden by any local configs in `.env` files or otherwise.
```

```{command-output} linkml config set log.level WARNING
```

```{command-output} linkml config get log.level
```




## Examples


`````{tab-set}
````{tab-item} linkml_config.yaml
```{code-block} yaml
user_dir: ~/.config/linkml
config_file: linkml_config.yaml
log:
  dir: /var/log/linkml
  level_file: INFO
  level_stream: WARNING
  file_n: 5
``` 
````
````{tab-item} env vars
```{code-block} bash
export LINKML_USER_DIR='~/.config/linkml'
export LINKML_CONFIG_FILE='linkml_config.yaml'
export LINKML_LOG__DIR='/var/log/linkml'
export LINKML_LOG__LEVEL_FILE='INFO'
export LINKML_LOG__LEVEL_STREAM='WARNING'
export LINKML_LOG__FILE_N=5
```
````
````{tab-item} .env file
```{code-block} python
LINKML_USER_DIR='~/.config/linkml'
LINKML_CONFIG_FILE='linkml_config.yaml'
LINKML_LOG__DIR='/var/log/linkml'
LINKML_LOG__LEVEL_FILE='INFO'
LINKML_LOG__LEVEL_STREAM='WARNING'
LINKML_LOG__FILE_N=5
```
````
````{tab-item} pyproject.toml
```{code-block} toml
[tool.linkml.config]
user_dir = "~/.config/linkml"
config_file = "linkml_config.yaml"

[tool.linkml.config.log]
dir = "/var/log/linkml"
level_file = "INFO"
level_stream = "WARNING"
file_n = 5

``` 
````
````{tab-item} cli
```{code-block} bash
linkml config set user_dir '~/.config/linkml'
linkml config set config_file 'linkml_config.yaml'
linkml config set log.dir '/var/log/linkml'
linkml config set log.level_file 'info'
linkml config set log.level_stream 'warning'
linkml config set log.file_n 5
``` 
````
`````


## API

```{eval-rst}
.. automodule:: linkml.utils.config
    :members:
    
```