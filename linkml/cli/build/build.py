"""
CLI command for building based on a project-level configuration

TODO: This is in a very draft-y state!!!!! in progress!!!!!
"""

import inspect
import io
import warnings
from contextlib import redirect_stdout
from pathlib import Path
from typing import Dict, List, Optional, Type

import click
import tomllib
from jinja2 import Template
from linkml_runtime.utils.schemaview import load_schema_wrap
from tqdm import tqdm

from linkml.cli.build.models import AnonymousGeneratorConfig, FlatSchemaBuildConfig, LinkmlConfig
from linkml.utils.generator import Generator


@click.command(name="build")
@click.option(
    "-C",
    help="Execute build for a project in a specific directory " "(or for a specific pyproject.toml config)",
    type=click.Path(exists=True, dir_okay=True),
    required=False,
)
def build(c: Optional[Path] = None):
    """
    Build linkml schemas according to a pyproject.toml build configuration
    """
    build_configs = get_build_config(c)
    pbar = tqdm(total=len(build_configs))
    try:
        for build_config in build_configs:
            description = f"{build_config.schema_name} - {build_config.generator_name}"
            pbar.set_description(description)
            build_from_config(build_config)
            pbar.update()
    finally:
        pbar.close()


def build_from_config(config: FlatSchemaBuildConfig):
    if config.generator_config.pre_build or config.generator_config.post_build:
        raise NotImplementedError("build hooks are not implemented yet!")

    base_dir = Path(config.config_file).parent

    schema = load_schema_wrap(str(base_dir / config.schema_path))
    # expand output_path template string
    output_path = Template(config.generator_config.output).render(schema=schema)
    # relative to the config file
    output_path = base_dir / output_path

    generator_class = get_all_generators()[config.generator_name]
    generator = generator_class(schema, **config.generator_config.__pydantic_extra__)
    serialize_signature = inspect.signature(generator.serialize)

    if "output" in serialize_signature.parameters:
        generator.serialize(output=output_path)
    else:
        # we have to write the string ourselves, potentially even capturing it from stdout
        stdout_string = io.StringIO()
        with redirect_stdout(stdout_string):
            return_string = generator.serialize()
        write_string = return_string if return_string is not None else stdout_string.getvalue()
        if write_string is None:
            raise RuntimeError("Generator returned nothing and printed nothing to stdout!")
        with open(output_path, "w") as ofile:
            ofile.write(write_string)


def find_config(base_path: Optional[Path] = None) -> Optional[Path]:
    if base_path is None:
        base_path = Path.cwd()

    if base_path.is_file() and base_path.name == "pyproject.toml" and base_path.exists():
        return base_path

    for check_path in (base_path, *base_path.parents):
        if (pyproject_file := check_path / "pyproject.toml").exists():
            return pyproject_file


def load_config(pyproject_path: Path) -> LinkmlConfig:
    with open(pyproject_path, "rb") as tfile:
        pyproject = tomllib.load(tfile)

    tool = pyproject.get("tool", {})
    if "linkml" not in tool:
        raise RuntimeError(f"No [tool.linkml] table found in {pyproject_path}")

    linkml_config = tool["linkml"]
    linkml_config["config_file"] = str(pyproject_path)

    config = LinkmlConfig(**tool["linkml"])
    return config


def flatten_config(config: LinkmlConfig) -> List[FlatSchemaBuildConfig]:
    """
    Flatten all configurations, from global to local

    # FIXME: I hate this implementation
    - generate.global
    - generate.{generator}
    - build.{schema}
    - build.{schema}.{generator}
    """
    generator_global_configs = {}  # generator: config (for all schema using this generator)

    # --------------------------------------------------
    # Gather global configurations for generators
    # --------------------------------------------------
    if config.generate is not None:
        global_config = config.generate.global_.model_dump() if config.generate.global_ is not None else {}
        # we shouldn't support generating all generators for all schema - too many busted generators
        if global_config.get("enable", False):
            warnings.warn(
                "Cant use enable=true in tool.linkml.generate.global - enable individual generators specifically"
            )

        # update with all global generator-level configs
        for generator, gen_config in config.generate.__pydantic_extra__.items():
            generator_global_configs[generator] = global_config.copy()
            generator_global_configs[generator].update({k: v for k, v in gen_config.items() if v is not None})

    # --------------------------------------------------
    # Gather configurations per generator for schema
    # --------------------------------------------------
    # apply global generator settings per schema (we'll filter later)
    configs = {schema: generator_global_configs.copy() for schema in config.schema_}

    if config.build is not None:
        for schema_name, schema_build_config in config.build.items():
            schema_global = schema_build_config.global_.model_dump() if schema_build_config.global_ is not None else {}
            # all generator/schema configs
            schema_generator_configs = schema_build_config.__pydantic_extra__
            # set of all generators in global and schema-specific config
            schema_generators = set(list(generator_global_configs.keys()) + list(schema_generator_configs.keys()))
            for generator in schema_generators:
                if generator not in configs[schema_name]:
                    configs[schema_name][generator] = {}
                # first update with the schema-global config
                configs[schema_name][generator].update(schema_global)
                # then the schema-generator config
                configs[schema_name][generator].update(schema_generator_configs.get(generator, {}))

    # --------------------------------------------------
    # Flatten, filter, and cast configs
    # --------------------------------------------------
    cast_configs = []
    for schema_name, schema_build_config in configs.items():
        for generator, generator_config in schema_build_config.items():
            if not generator_config.get("enable", False):
                continue
            if generator_config.get("output", None) is None:
                warnings.warn(
                    f"schema: {schema_name} and generator: {generator} have no output "
                    "path configured and can't be built"
                )
                continue
            cast_configs.append(
                FlatSchemaBuildConfig(
                    schema_name=schema_name,
                    schema_path=config.schema_[schema_name],
                    generator_name=generator,
                    config_file=config.config_file,
                    generator_config=AnonymousGeneratorConfig(**generator_config),
                )
            )
    return cast_configs


def get_build_config(path: Optional[Path] = None) -> List[FlatSchemaBuildConfig]:
    config_file = find_config(path)
    linkml_config = load_config(config_file)
    configs = flatten_config(linkml_config)
    return configs


def get_all_generators() -> Dict[str, Type[Generator]]:
    subclasses = _get_generator_subclasses(Generator)
    subclasses = {gen.generatorname.rstrip(".py"): gen for gen in subclasses if gen.generatorname is not None}
    return subclasses


def _get_generator_subclasses(cls: Type[Generator]) -> List[Type[Generator]]:
    generators = [gen for gen in cls.__subclasses__()]
    for sub_generator in generators:
        if sub_generator.__subclasses__():
            generators.extend(_get_generator_subclasses(sub_generator))
    return generators
