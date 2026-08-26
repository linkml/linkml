import logging
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, NamedTuple

import click
import yaml

from linkml._version import __version__
from linkml.cli.logging import log_level_option
from linkml.generators.excelgen import ExcelGenerator
from linkml.generators.graphqlgen import GraphqlGenerator
from linkml.generators.javagen import JavaGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.prefixmapgen import PrefixGenerator
from linkml.generators.protogen import ProtoGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.sqltablegen import SQLTableGenerator
from linkml.utils.generator import Generator

logger = logging.getLogger(__name__)

PATH_FSTRING = str
GENERATOR_NAME = str
ARG_DICT = dict[str, Any]


class GeneratorConfig(NamedTuple):
    """How gen-project drives one generator.

    A NamedTuple rather than a plain tuple so that ``serialize_only`` can be left
    off the entries that don't need it, and so fields can be read by name; entries
    still unpack positionally.
    """

    generator: type[Generator]
    """The generator class to instantiate."""

    path_fstring: PATH_FSTRING
    """Output path template for the generated artefact, e.g. ``"owl/{name}.owl.ttl"``."""

    default_args: ARG_DICT
    """Arguments applied before any user-supplied ``generator_args``."""

    serialize_only: frozenset[str] = frozenset()
    """Keys to pass to ``serialize()`` but NOT to the constructor.

    Scoped per generator so that a name which is serialize-only here (JavaGenerator's
    ``directory``) is not dropped from a different generator's constructor call, where
    the same name is a genuine constructor argument (dotgen, docgen and plantumlgen all
    take ``directory`` that way).
    """


# Retained as the previous name for this entry type.
CONFIG_TUPLE = GeneratorConfig

GEN_MAP: dict[GENERATOR_NAME, GeneratorConfig]
GEN_MAP = {
    "graphql": GeneratorConfig(GraphqlGenerator, "graphql/{name}.graphql", {}),
    "jsonldcontext": GeneratorConfig(ContextGenerator, "jsonld/{name}.context.jsonld", {}),
    "jsonld": GeneratorConfig(
        JSONLDGenerator,
        "jsonld/{name}.jsonld",
        {"context": "{parent}/{name}.context.jsonld"},
    ),
    "jsonschema": GeneratorConfig(JsonSchemaGenerator, "jsonschema/{name}.schema.json", {}),
    "owl": GeneratorConfig(OwlSchemaGenerator, "owl/{name}.owl.ttl", {}),
    "prefixmap": GeneratorConfig(PrefixGenerator, "prefixmap/{name}.yaml", {}),
    "proto": GeneratorConfig(ProtoGenerator, "protobuf/{name}.proto", {}),
    "python": GeneratorConfig(PythonGenerator, "{name}.py", {}),
    #    'rdf': GeneratorConfig(RDFGenerator, 'rdf/{name}.ttl', {}),
    #    'rdf': GeneratorConfig(
    #        RDFGenerator, 'rdf/{name}.ttl', {'context': '{parent}/../jsonld/{name}.context.jsonld'}
    #    ),
    "shex": GeneratorConfig(ShExGenerator, "shex/{name}.shex", {}),
    "shacl": GeneratorConfig(ShaclGenerator, "shacl/{name}.shacl.ttl", {}),
    "sqltable": GeneratorConfig(SQLTableGenerator, "sqlschema/{name}.sql", {}),
    # JavaGenerator writes one file per class directly into `directory`
    # (a serialize()-time argument, not a constructor argument) and its
    # serialize() always returns None.
    "java": GeneratorConfig(
        JavaGenerator,
        "java/{name}.java",
        {"directory": "{parent}"},
        serialize_only=frozenset({"directory"}),
    ),
    "excel": GeneratorConfig(ExcelGenerator, "excel/{name}.xlsx", {"output": "{parent}/{name}.xlsx"}),
}


@lru_cache
def get_local_imports(schema_path: Path, dir: Path):
    logger.info(f"GETTING IMPORTS = {schema_path}")
    all_imports = [schema_path]
    with open(schema_path, encoding="utf-8") as stream:
        schema = yaml.safe_load(stream)
        for imp in schema.get("imports", []):
            imp_path = dir / f"{imp}.yaml"
            logger.info(f" IMP={imp} //  path={imp_path}")
            if imp_path.is_file():
                all_imports += get_local_imports(imp_path, dir)
    return all_imports


@dataclass
class ProjectConfiguration:
    """
    Global project configuration, and per-generator configurations
    """

    directory: str = "tmp"
    generator_args: dict[GENERATOR_NAME, ARG_DICT] = field(default_factory=lambda: defaultdict(dict))
    includes: list[str] = None
    excludes: list[str] = None
    mergeimports: bool = None


class ProjectGenerator:
    """
    Generates complete project folders

    Note this doesn't conform to overall generator framework, as it is a meta-generator
    """

    @staticmethod
    def generate(schema_path: str, config: ProjectConfiguration = ProjectConfiguration()):
        if config.directory is None:
            raise Exception("Must pass directory")

        # Resolve which generators run and with what merged arguments, rejecting
        # any bad `generator_args` value before anything at all is generated or
        # written -- a typo in the config for the last generator must not leave
        # behind a half-built project. This is the only place a `generator_args`
        # value gets checked; a ValueError raised later while actually
        # constructing a generator is therefore a genuine failure (e.g. an
        # unloadable schema) and is left to propagate with its own traceback,
        # rather than being caught and mistaken for a bad config value.
        selected: list[tuple[GENERATOR_NAME, GeneratorConfig, ARG_DICT]] = []
        for gen_name, gen_config in GEN_MAP.items():
            if config.includes is not None and config.includes != [] and gen_name not in config.includes:
                logger.info(f"Skipping {gen_name} as not in inclusion list: {config.includes}")
                continue
            if config.excludes is not None and gen_name in config.excludes:
                logger.info(f"Skipping {gen_name} as it is in exclusion list")
                continue
            all_gen_args = {
                **gen_config.default_args,
                **config.generator_args.get(gen_name, {}),
            }
            gen_config.generator.validate_generator_args(all_gen_args)
            selected.append((gen_name, gen_config, all_gen_args))

        output_dir = Path(config.directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        if config.mergeimports:
            all_schemas = [schema_path]
        else:
            all_schemas = get_local_imports(schema_path, Path(schema_path).parent)
        logger.debug(f"ALL_SCHEMAS = {all_schemas}")
        for gen_name, gen_config, all_gen_args in selected:
            logger.info(f"Generating: {gen_name}")
            for local_path in all_schemas:
                logger.info(f" SCHEMA: {local_path}")
                name = Path(local_path).stem
                gen_path = gen_config.path_fstring.format(name=name)
                gen_path_full = output_dir / gen_path
                parent_dir = gen_path_full.parent
                logger.info(f" PARENT={parent_dir}")
                parent_dir.mkdir(parents=True, exist_ok=True)
                gen: Generator

                # Per-schema copy: the `output` value is interpolated per schema
                # below and must not mutate `all_gen_args`, which is shared
                # across schemas.
                schema_gen_args = dict(all_gen_args)

                # special check for output key because ExcelGenerator and
                # SSSOMGenerator read in output file name during initialization
                if "output" in schema_gen_args:
                    schema_gen_args["output"] = schema_gen_args["output"].format(name=name, parent=parent_dir)

                # Some generators (e.g. JavaGenerator) accept an arg only in
                # serialize(), not in their constructor; keep this generator's
                # serialize-only keys out of the constructor call.
                constructor_args = {k: v for k, v in schema_gen_args.items() if k not in gen_config.serialize_only}
                gen = gen_config.generator(local_path, **constructor_args)

                serialize_args = {"mergeimports": config.mergeimports}
                for k, v in schema_gen_args.items():
                    # all ARG_DICT values are interpolatable
                    if isinstance(v, str):
                        v = v.format(name=name, parent=parent_dir)
                    serialize_args[k] = v
                logger.info(f" {gen_name} ARGS: {serialize_args}")
                gen_dump = gen.serialize(**serialize_args)

                # Generators like ExcelGenerator and JavaGenerator write their
                # own output file(s) internally and return None from
                # serialize(); there is nothing left for us to write out.
                if gen_dump is None:
                    continue
                if gen_path_full.suffix != "":
                    logger.info(f"  WRITING TO: {gen_path_full}")
                    with open(gen_path_full, "w", encoding="UTF-8") as stream:
                        stream.write(gen_dump)


@click.command(name="project")
@click.option(
    "--dir",
    "-d",
    help="directory in which to place generated files. E.g. linkml_model, biolink_model",
)
@click.option("--generator-arguments", "-A", help="yaml configuration for generators")
@click.option("--config-file", "-C", type=click.File("rb"), help="path to yaml configuration")
@click.option("--exclude", "-X", multiple=True, help="list of artefacts to be excluded")  # TODO: make this an enum
@click.option(
    "--include",
    "-I",
    multiple=True,
    help="list of artefacts to be included. If not set, defaults to all",
)  # TODO: make this an enum
@click.option(
    "--mergeimports/--no-mergeimports",
    default=True,
    show_default=True,
    help="Merge imports into source file",
)
@log_level_option
@click.argument("yamlfile")
@click.version_option(__version__, "-V", "--version")
def cli(
    yamlfile,
    dir,
    exclude: list[str],
    include: list[str],
    config_file,
    mergeimports,
    generator_arguments: str,
    **kwargs,
):
    """
    Generate an entire project LinkML schema

    Generate all downstream artefacts using default configuration:

    .. code-block: bash

        gen-project -d . personinfo.yaml

    Exclusion lists: all except ShEx:

    .. code-block: bash

        gen-project --exclude shex -d . personinfo.yaml

    Inclusion lists: only jsonschema and python:

    .. code-block: bash

       gen-project -I python -I jsonschema -d . personinfo.yaml

    Configuration, on command line:

    .. code-block: bash

        gen-project -A 'jsonschema: {top_class: Container}' -d . personinfo.yaml

    Configuration, via yaml file:

    .. code-block: bash

        gen-project --config config.yaml personinfo.yaml

    config.yaml:

    .. code-block: yaml

        directory: .
        generator_args:
          json_schema:
            top_class: Container

    """
    project_config = ProjectConfiguration()
    if config_file is not None:
        for k, v in yaml.safe_load(config_file).items():
            setattr(project_config, k, v)
    if exclude:
        project_config.excludes = list(exclude)
    if include:
        project_config.includes = list(include)
    if generator_arguments is not None:
        try:
            project_config.generator_args = yaml.safe_load(generator_arguments)
        except Exception:
            raise Exception("Argument must be a valid YAML blob")
        logger.info(f"generator args: {project_config.generator_args}")
    if dir is not None:
        project_config.directory = dir
    project_config.mergeimports = mergeimports
    gen = ProjectGenerator()
    # A bad `generator_args` value surfaces from Generator.validate_generator_args()
    # as a click.UsageError, which click reports on its own; nothing to catch here.
    gen.generate(yamlfile, project_config)


if __name__ == "__main__":
    cli()
