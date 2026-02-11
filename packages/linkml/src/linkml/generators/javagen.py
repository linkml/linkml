import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import click
from jinja2 import Template

from linkml._version import __version__
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.deprecation import deprecated_fields, deprecation_warning
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model.meta import TypeDefinition

DEFAULT_TEMPLATE_DIR = Path(__file__).parent.resolve() / "javagen"

TYPEMAP = {
    "xsd:string": "String",
    "xsd:integer": "Integer",
    "xsd:float": "Float",
    "xsd:double": "Double",
    "xsd:boolean": "boolean",
    "xsd:dateTime": "ZonedDateTime",
    "xsd:date": "LocalDate",
    "xsd:time": "Instant",
    "xsd:anyURI": "String",
    "xsd:decimal": "BigDecimal",
}

TYPE_DEFAULTS = {"boolean": "false", "int": "0", "float": "0f", "double": "0d", "String": '""'}


class TemplateCache:
    """Cache for template objects.

    The purpose of this class is twofold:

    * It implements the logic needed to find the correct template based on (1)
      which templates are available, (2) which type of object is a template
      required for, (3) whether a specific “variant“ of templates has been
      requested.
    * It keeps templates that have already been read from disk in memory, so
      that we don’t have to read them over again when the same template is used
      many times (which should be the typical case).
    """

    def __init__(self):
        self.template_files: dict[str, Path] = {}
        self.templates: dict[Path, Template] = {}

    def add_directory(self, template_dir: Path) -> None:
        """Adds all templates in the specified directory to the cache."""

        for template in template_dir.glob("*.jinja2"):
            self.template_files[template.stem] = template

    def force_template(self, template_file: Path) -> None:
        """Sets the template to systematically use for all objects.

        This method is used to implement the `--template-file` option, allowing
        users to forcibly use one specific template file, regardless of the
        contents of the templates directory.
        """

        self.template_files["__FORCE__"] = template_file

    def get_template(self, name: str, fallback: str = "class", variant: Optional[str] = None) -> Optional[Template]:
        """Finds the template for a given object.

        :param name: The name of the object for which a template is required.
        :param fallback: The name of the fallback template to use if there is
            no specific template for the given object name.
        :param variant: The name of an optional template variant.
        :return: The requested template, or None if no suitable template is
            available.
        """

        candidate: Optional[Path] = None

        candidate = self.template_files.get("__FORCE__")

        if candidate is None and variant is not None:
            candidate = self.template_files.get(name + "-" + variant)
            if candidate is None:
                candidate = self.template_files.get(fallback + "-" + variant)

        if candidate is None:
            candidate = self.template_files.get(name)
        if candidate is None:
            candidate = self.template_files.get(fallback)

        if candidate is None:
            return None

        if candidate not in self.templates:
            with candidate.open("r") as f:
                self.templates[candidate] = Template(f.read())
        return self.templates[candidate]


@deprecated_fields({"head": "metadata", "emit_metadata": "metadata"})
@dataclass
class JavaGenerator(OOCodeGenerator):
    """
    Generates java code from a LinkML schema.

    This generators supports an arbitrary number of different styles through
    the use of “template variants“.

    Currently, two variants are available:

    - the default variant represents LinkML classes as Java classes carrying
      Lombok annotations (https://projectlombok.org);
    - the `records` variant represents LinkML classes as Java 16 records.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["java"]
    file_extension = "java"

    # ObjectVars
    template_file: Optional[str] = None
    template_dir: Optional[Path] = None
    template_cache: TemplateCache = field(default_factory=lambda: TemplateCache())

    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False

    def __post_init__(self) -> None:
        self.template_cache.add_directory(DEFAULT_TEMPLATE_DIR)
        if self.template_dir is not None:
            self.template_cache.add_directory(self.template_dir)
        if self.template_file is not None:
            self.template_cache.force_template(Path(self.template_file))
        super().__post_init__()

    def default_value_for_type(self, typ: str) -> str:
        return TYPE_DEFAULTS.get(typ, "null")

    def map_type(self, t: TypeDefinition, required: bool = False) -> str:
        if t.uri:
            # only return a Integer, Double Float when required == false
            typ = TYPEMAP.get(t.uri)
            if required and (typ == "Double" or typ == "Float"):
                typ = typ.lower()
            elif required and typ == "Integer":
                typ = "int"
            return typ
        elif t.typeof:
            return self.map_type(self.schemaview.get_type(t.typeof))
        else:
            raise ValueError(f"{t} cannot be mapped to a type")

    def serialize(self, directory: str, template_variant: Optional[str] = None, **kwargs) -> None:
        oodocs = self.create_documents()
        self.directory = directory
        for oodoc in oodocs:
            if oodoc.classes:
                cls = oodoc.classes[0]
                enum = None
                type = "class"
            else:
                cls = None
                enum = oodoc.enums[0]
                type = "enum"
            template = self.template_cache.get_template(oodoc.name, type, template_variant)
            if template is None:
                # This should never happen as the default template directory
                # (which is always queried as a last resort) should always
                # contain at least a default `class` template and a default
                # `enum` template.
                raise Exception("Missing template")

            code = template.render(
                doc=oodoc,
                cls=cls,
                enum=enum,
                metamodel_version=self.schema.metamodel_version,
                model_version=self.schema.version,
            )

            os.makedirs(directory, exist_ok=True)
            filename = f"{oodoc.name}.java"
            path = os.path.join(directory, filename)
            with open(path, "w", encoding="UTF-8") as stream:
                stream.write(code)


@shared_arguments(JavaGenerator)
@click.option(
    "--output-directory",
    default="output",
    show_default=True,
    help="Output directory for individually generated class files",
)
@click.option("--package", help="Package name where relevant for generated class files")
@click.option(
    "--template-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Directory containing the Jinja2 templates to use",
)
@click.option("--template-variant", help="Use the specified template variant")
@click.option(
    "--template-file",
    help="""Optional jinja2 template to use for class generation
            (takes precedence over --template-dir)""",
)
@click.option(
    "--generate-records/--no-generate-records",
    default=False,
    help="""Optional Java 17 record implementation
            (deprecated, use --template-variant=records instead)""",
)
@click.option("--true-enums/--no-true-enums", default=False, help="Treat enums as distinct types rather than strings")
@click.version_option(__version__, "-V", "--version")
@click.command(name="java")
def cli(
    yamlfile,
    output_directory=None,
    package=None,
    template_dir=None,
    template_variant=None,
    template_file=None,
    generate_records=False,
    head=None,
    emit_metadata=None,
    genmeta=False,
    classvars=True,
    slots=True,
    true_enums=False,
    **args,
):
    """Generate java classes to represent a LinkML model"""
    if generate_records:
        template_variant = "records"
    if template_file is not None:
        if template_dir is not None or template_variant is not None:
            logging.warning("--template-file will take precedence over --template-dir and --template-variant")

    # default is adding metadata to the generated code
    if "metadata" not in args:
        args["metadata"] = True
    # deprecated arguments are replaced, head overwrites emit_metadata
    if emit_metadata is not None:
        deprecation_warning("metadata-flag")
        args["metadata"] = emit_metadata
    if head is not None:
        deprecation_warning("metadata-flag")
        args["metadata"] = head
    JavaGenerator(
        yamlfile,
        package=package,
        template_dir=template_dir,
        template_file=template_file,
        genmeta=genmeta,
        gen_classvars=classvars,
        gen_slots=slots,
        true_enums=true_enums,
        **args,
    ).serialize(output_directory, template_variant=template_variant, **args)


if __name__ == "__main__":
    cli()
