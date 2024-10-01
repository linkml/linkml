"""
Session-global configuration (see docs/config/index.md for documentation)
"""

from pathlib import Path
from typing import Any, Dict, Literal, Optional

from platformdirs import PlatformDirs
from pydantic import BaseModel, Field, TypeAdapter, field_validator, model_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

LOG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR"]
_dirs = PlatformDirs("linkml", "linkml")


class _GlobalYamlConfigSource(YamlConfigSettingsSource):
    """Yaml config source that gets the location of the global settings file from the prior sources"""

    def __init__(self, *args, **kwargs):
        self._global_config = None
        super().__init__(*args, **kwargs)

    @property
    def global_config_path(self) -> Path:
        """
        Location of the global ``linkml_config.yaml`` file,
        given the current state of prior config sources
        """
        current_state = self.current_state
        config_file = Path(current_state.get("config_file", "linkml_config.yaml"))
        user_dir = Path(current_state.get("user_dir", _dirs.user_config_dir))
        if not config_file.is_absolute():
            config_file = (user_dir / config_file).resolve()
        return config_file

    @property
    def global_config(self) -> Dict[str, Any]:
        """
        Contents of the global config file
        """
        if self._global_config is None:
            if self.global_config_path.exists():
                self._global_config = self._read_files(self.global_config_path)
            else:
                self._global_config = {}
        return self._global_config

    def __call__(self) -> Dict[str, Any]:
        return (
            TypeAdapter(Dict[str, Any]).dump_python(self.global_config)
            if self.nested_model_default_partial_update
            else self.global_config
        )


class LogConfig(BaseModel):
    """
    Config params for logging
    """

    dir: Path = Field(default=_dirs.user_log_dir, description="Directory where logs are stored")
    file_name: str = Field("linkml.log", description="Base name to use for rotating file logs")
    level: LOG_LEVELS = Field(
        "INFO",
        description="Base level to use for loggers. "
        "If more specific settings are not present (ie. level_file), use this as a default.",
    )
    level_file: Optional[LOG_LEVELS] = Field(None, description="Log level for file logging")
    level_stream: Optional[LOG_LEVELS] = Field(None, description="Log level for stdout/stderr stream logging")
    file_n: int = Field(5, description="Number of log files to rotate through")
    file_size: int = Field(2**22, description="Maximum size of log files (bytes)")

    @field_validator("level", "level_file", "level_stream", mode="before")
    @classmethod
    def uppercase_levels(cls, value: Optional[str] = None) -> Optional[str]:
        """
        Ensure log level strings are uppercased
        """
        if value is not None:
            value = value.upper()
        return value

    @model_validator(mode="after")
    def inherit_base_level(self) -> "LogConfig":
        """
        If loglevels for specific output streams are unset, set from base :attr:`.level`
        """
        levels = ("level_file", "level_stream")
        for level_name in levels:
            if getattr(self, level_name) is None:
                setattr(self, level_name, self.level)
        return self


class GlobalConfig(BaseSettings):
    """
    Global LinkML configuration that determines the behavior of linkml in a given shell session.

    Distinct from generator and project configs,
    which control the behavior of specific generators and projects, respectively.
    """

    user_dir: Path = Field(_dirs.user_config_dir, description="Directory containing linkml config files")
    config_file: Path = Field(
        Path("linkml_config.yaml"),
        description="Location of global linkml config file. "
        "If a relative path, interpreted as a relative to ``user_dir``",
    )
    log: LogConfig = LogConfig()

    model_config = SettingsConfigDict(
        env_prefix="linkml_",
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
        nested_model_default_partial_update=True,
        yaml_file="linkml_config.yaml",
        pyproject_toml_table_header=("tool", "linkml", "config"),
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Read config settings from, in order of priority from high to low, where
        high priorities override lower priorities:

        * in the arguments passed to the class constructor (not user configurable)
        * in environment variables like ``export LINKML_LOG_DIR=~/``
        * in a ``.env`` file in the working directory
        * in a ``linkml_config.yaml`` file in the working directory
        * in the ``tool.linkml.config`` table in a ``pyproject.toml`` file in the working directory
        * in the global ``linkml_config.yaml`` file in the platform-specific data directory
          (use ``linkml config get config_file`` to find its location)
        * the default values in the :class:`.GlobalConfig` model
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            PyprojectTomlConfigSettingsSource(settings_cls),
            _GlobalYamlConfigSource(settings_cls),
        )

    @field_validator("user_dir", mode="after")
    @classmethod
    def user_dir_exists(cls, v: Path) -> Path:
        """Ensure user_dir exists, make it otherwise"""
        v = Path(v)
        v.mkdir(exist_ok=True, parents=True)
        assert v.exists(), f"{v} does not exist!"
        return v

    @model_validator(mode="after")
    def config_file_is_absolute(self) -> "GlobalConfig":
        """
        If ``config_file`` is relative, make it absolute underneath user_dir
        """
        if not self.config_file.is_absolute():
            self.config_file = self.user_dir / self.config_file
        return self
