import importlib
import logging
from dataclasses import dataclass
from typing import Optional

import click

from linkml._version import __version__
from linkml.generators.oocodegen import OODocument

from .dataframe_generator import DataframeGenerator
from .pandera.pandera_dataframe_generator import PanderaDataframeGenerator
from .polars_schema.polars_schema_dataframe_generator import PolarsSchemaDataframeGenerator

# Allowed template directories
ALLOWED_TEMPLATE_DIRECTORIES = ["panderagen_class_based", "panderagen_polars_schema"]


# Available generator classes
GENERATOR_CLASSES = {
    "PanderaDataframeGenerator": {
        "class": PanderaDataframeGenerator,
        "module": "linkml.generators.panderagen.pandera_dataframe_generator",
    },
    "PolarsSchemaDataframeGenerator": {
        "class": PolarsSchemaDataframeGenerator,
        "module": "linkml.generators.panderagen.polars_schema_dataframe_generator",
    },
}

logger = logging.getLogger(__name__)


@dataclass
class DataframeGeneratorCli:
    """CLI wrapper for dataframe generators with serialization capabilities."""

    DEFAULT_TEMPLATE_PATH = "panderagen_class_based"
    DEFAULT_TEMPLATE_FILE = "pandera.jinja2"
    DEFAULT_GENERATOR_CLASS = PanderaDataframeGenerator

    generator: DataframeGenerator
    template_path: str = DEFAULT_TEMPLATE_PATH
    template_file: Optional[str] = None

    def read_validator_helper(self) -> str:
        """
        Return the linkml_pandera_validator python module code as a string.

        The generated pandera classes use a mixin helper.
        This is currently inlined in the generated code.

        TODO: generalize this for other dataframe targets (possible all Pandera targets)
        """
        linkml_pandera_validator = importlib.import_module("linkml.generators.panderagen.linkml_pandera_validator")
        module_path = linkml_pandera_validator.__file__

        try:
            with open(module_path) as file:
                return file.read().replace("LinkmlPanderaValidator", "_LinkmlPanderaValidator")
        except Exception as e:
            logger.warning(f"Unable to read linkml_pandera_validator module: {e}")
            return None

    def serialize(self, directory: Optional[str] = None, rendered_module: Optional[OODocument] = None) -> str:
        """
        Serialize the dataframe schema to a Python module as a string
        """
        # Set template path and file on generator if provided
        if self.template_path != self.DEFAULT_TEMPLATE_PATH:
            self.generator.template_path = self.template_path
        if self.template_file is not None:
            self.generator.template_file = self.template_file

        code = self.generator.serialize(rendered_module=rendered_module)

        return code


@click.option("--template-path", help="Optional jinja2 template directory within module")
@click.option("--template-file", help="Optional jinja2 template to use for class generation")
@click.option(
    "--generator-class",
    help=f"Generator class to use. Options: {list(GENERATOR_CLASSES.keys())}",
    default="PanderaDataframeGenerator",
)
@click.version_option(__version__, "-V", "--version")
@click.argument("yamlfile")
@click.command(name="gen-pandera")
def cli(
    yamlfile,
    template_path=None,
    template_file=None,
    generator_class=None,
    **args,
):
    if template_path is not None and template_path not in ALLOWED_TEMPLATE_DIRECTORIES:
        raise Exception(f"Template {template_path} not supported. Available: {ALLOWED_TEMPLATE_DIRECTORIES}")

    """Generate Pandera classes to represent a LinkML model"""

    # Get generator class
    if generator_class is None or generator_class == "PanderaDataframeGenerator":
        gen_class = DataframeGeneratorCli.DEFAULT_GENERATOR_CLASS
    elif generator_class in GENERATOR_CLASSES:
        gen_class = GENERATOR_CLASSES[generator_class]["class"]
    else:
        raise Exception(f"Generator class {generator_class} not supported. Available: {list(GENERATOR_CLASSES.keys())}")

    generator: DataframeGenerator = gen_class(
        yamlfile,
        template_path=template_path,
        template_file=template_file,
        **args,
    )

    cli_wrapper = DataframeGeneratorCli(
        generator=generator,
        template_path=template_path or DataframeGeneratorCli.DEFAULT_TEMPLATE_PATH,
        template_file=template_file,
    )
    print(cli_wrapper.serialize())


if __name__ == "__main__":
    cli()
