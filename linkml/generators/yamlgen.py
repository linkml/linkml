"""Validate linkml input and optionally emit completely resolved biolink yaml output

"""
import os
from dataclasses import dataclass, field
from typing import TextIO, Union

import click
from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.utils.yamlutils import as_yaml

from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.schemaloader import load_raw_schema


@dataclass
class YAMLGenerator(Generator):
    """
    A generator that produces a schema as a YAML Document
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["yaml"]
    uses_schemaloader = True

    # ObjectVars
    validateonly: bool = field(default_factory=lambda: False)

    def serialize(self, validateonly: bool = False, **kwargs) -> str:
        if validateonly:
            return self.synopsis.summary()
        else:
            return as_yaml(self.schema)


@shared_arguments(YAMLGenerator)
@click.command()
@click.option(
    "--raw/--no-raw",
    default=False,
    show_default=True,
    help="Use the raw loader and do not inject additional information",
)
@click.option(
    "--validateonly/--generate",
    "-V/-g",
    default=False,
    show_default=True,
    help="Just validate / generate output (default: generate)",
)
def cli(yamlfile, raw: bool, **args):
    """Validate input and produce fully resolved yaml equivalent"""
    if raw:
        s = load_raw_schema(yamlfile)
        print(as_yaml(s))
    else:
        gen = YAMLGenerator(yamlfile, **args)
        print(gen.serialize(**args))


if __name__ == "__main__":
    cli()
