# Configuration

Global configuration in linkml uses [`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)


## Sources

Config values can be set (in order of priority from high to low, where higher
priorities override lower priorities)

* in the arguments passed to the class constructor (not user configurable)
* in environment variables like `export LINKML_LOG__DIR="$HOME/.local/state/linkml/log"`
* in a `.env` file in the working directory
* in a `linkml_config.yaml` file in the working directory
* in the `tool.linkml.config` table in a `pyproject.toml` file in the working directory
* in the global `linkml_config.yaml` file in the platform-specific data directory[^platformdirs]
  (use `linkml config get config_file` to find its location)
* the default values in the {class}`~linkml.utils.config.GlobalConfig` model

Parent directories are _not_ checked.

[^platformdirs]: These directories come from [platformdirs](https://platformdirs.readthedocs.io/en/latest/index.html),
  see [their documentation](https://platformdirs.readthedocs.io/en/latest/platforms.html) for more info.
  The default configuration directories for linkml are:
    - Linux: `~/.config/linkml/`
    - Mac: `~/Library/Application Support/linkml/`
    - Windows: `~\AppData\Local\linkml\linkml\`

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

    export LINKML_LOG__DIR="$HOME/.local/state/linkml/log"
    export linkml_log__dir="$HOME/.local/state/linkml/log"

## Paths

LinkML does not automatically expand `~` in configuration paths. In YAML, TOML,
and `.env` files, `~/.config/linkml` is a literal relative path. Using it for
`user_dir` creates a directory named `~` under the working directory instead of
using your home directory. A quoted CLI argument such as `'~/.config/linkml'`
also remains literal.

In Bash, an unquoted `~` can be expanded by the shell. The shell examples here
use `"$HOME/..."` so that Bash expands the home directory before passing the
value to LinkML, including when the path contains spaces. In configuration files,
write the resulting absolute path directly.

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

These examples assume a Unix-like system where the home directory is
`/home/alex`. Replace the file examples' paths with absolute, writable paths on
your system. The shell examples use `$HOME` to select the current user's home
directory. Each tab shows an alternative configuration source; higher-priority
sources override lower-priority ones.

The CLI tab selects the global configuration file with `LINKML_USER_DIR` and
`LINKML_CONFIG_FILE` before setting values. Keep these environment variables set
when reading or updating that file later so that commands use the same location.

`````{tab-set}
````{tab-item} linkml_config.yaml
```{code-block} yaml
user_dir: /home/alex/.config/linkml
config_file: linkml_config.yaml
log:
  dir: /home/alex/.local/state/linkml/log
  level_file: INFO
  level_stream: WARNING
  file_n: 5
```
````
````{tab-item} env vars
```{code-block} bash
export LINKML_USER_DIR="$HOME/.config/linkml"
export LINKML_CONFIG_FILE='linkml_config.yaml'
export LINKML_LOG__DIR="$HOME/.local/state/linkml/log"
export LINKML_LOG__LEVEL_FILE='INFO'
export LINKML_LOG__LEVEL_STREAM='WARNING'
export LINKML_LOG__FILE_N=5
```
````
````{tab-item} .env file
```{code-block} text
LINKML_USER_DIR='/home/alex/.config/linkml'
LINKML_CONFIG_FILE='linkml_config.yaml'
LINKML_LOG__DIR='/home/alex/.local/state/linkml/log'
LINKML_LOG__LEVEL_FILE='INFO'
LINKML_LOG__LEVEL_STREAM='WARNING'
LINKML_LOG__FILE_N=5
```
````
````{tab-item} pyproject.toml
```{code-block} toml
[tool.linkml.config]
user_dir = "/home/alex/.config/linkml"
config_file = "linkml_config.yaml"

[tool.linkml.config.log]
dir = "/home/alex/.local/state/linkml/log"
level_file = "INFO"
level_stream = "WARNING"
file_n = 5

```
````
````{tab-item} cli
```{code-block} bash
export LINKML_USER_DIR="$HOME/.config/linkml"
export LINKML_CONFIG_FILE='linkml_config.yaml'
linkml config set log.dir "$HOME/.local/state/linkml/log"
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
