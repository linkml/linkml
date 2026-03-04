import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

import click
from jinja2 import Template

from linkml._version import __version__
from linkml.generators.oocodegen import OOCodeGenerator, OODocument
from linkml.utils.deprecation import deprecated_fields, deprecation_warning
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition, TypeDefinition
from linkml_runtime.utils.formatutils import camelcase

DEFAULT_TEMPLATE_DIR = Path(__file__).parent.resolve() / "javagen"

TYPEMAP = {
    "xsd:string": "String",
    "xsd:integer": "Integer",
    "xsd:float": "Float",
    "xsd:double": "Double",
    "xsd:boolean": "Boolean",
    "xsd:dateTime": "ZonedDateTime",
    "xsd:date": "LocalDate",
    "xsd:time": "LocalTime",
    "xsd:anyURI": "String",
    "xsd:decimal": "BigDecimal",
}

TYPE_DEFAULTS = {"boolean": "false", "int": "0", "float": "0f", "double": "0d", "String": '""'}


@dataclass
class OOCustomDocument(OODocument):
    """A document that represents something else than a class or an enum."""

    type: str = None


@dataclass
class OOVisitorDocument(OOCustomDocument):
    """A document representing a visitor interface."""

    visited_object: str = None

    def __post_init__(self):
        self.type = "_visitor"


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

    def get_template(self, name: str, fallback: str = "class", variant: str | None = None) -> Template | None:
        """Finds the template for a given object.

        :param name: The name of the object for which a template is required.
        :param fallback: The name of the fallback template to use if there is
            no specific template for the given object name.
        :param variant: The name of an optional template variant.
        :return: The requested template, or None if no suitable template is
            available.
        """

        candidate: Path | None = None

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
    template_file: str | None = None
    template_dir: Path | None = None
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

    def map_class(self, c: ClassDefinition) -> str:
        # A slot intended to accept anything is represented in Java as
        # an Object-typed slot
        if c.class_uri == "linkml:Any":
            return "Object"
        else:
            return super().map_class(c)

    def map_type(self, t: TypeDefinition, required: bool = False) -> str:
        if t.uri:
            # We use "boxed" types (Boolean, Integer, Double, Float) by
            # default because we need to represent the case where a
            # value has not explicitly been set. But that requirement no
            # longer holds when required == true, so in that case we can
            # use primitive types (boolean, int, double, float) instead.
            typ = TYPEMAP.get(t.uri)
            if required and (typ == "Boolean" or typ == "Double" or typ == "Float"):
                typ = typ.lower()
            elif required and typ == "Integer":
                typ = "int"
            return typ
        elif t.typeof:
            return self.map_type(self.schemaview.get_type(t.typeof))
        else:
            raise ValueError(f"{t} cannot be mapped to a type")

    def serialize(
        self,
        directory: str,
        template_variant: str | None = None,
        extra_templates: list[str] | None = None,
        visitors: list[str] | None = None,
        **kwargs,
    ) -> None:
        """Generate and write the Java code to files.

        :param directory: The directory where to write the code files.
        :param template_variant: The name of the template variant to use, if any.
        :param extra_templates: A list of additional templates from which to generate
            additional code files. For example, if set to `[Foo,Bar]`, this will
            generate two additional files `Foo.java` and `Bar.java` (assuming the
            template directory contains the required templates `Foo.jinja2` and
            `Bar.jinja2`). Users can exploit such additional files to generate any
            code they might need in addition to the code generated for each class
            and each enum in the model.
        :param visitors: A list of class names for which to generate a visitor
            interface. For example, if set to `[Foo]`, this will generate a
            `IFooVisitor` interface, and the generated code for both the `Foo`
            class and all its descendants will include a `accept(IFooVisitor)`
            method.
        """
        oodocs = self.create_documents()
        # Create additional documents for additional templates and visitors
        if extra_templates:
            for extra_template in extra_templates:
                oodocs.append(OOCustomDocument(name=extra_template, package=self.package, type=extra_template))
        if visitors is not None:
            for visitor in visitors:
                visited_name = visitor
                visitor_name = "I" + camelcase(visited_name) + "Visitor"
                oodocs.append(OOVisitorDocument(name=visitor_name, package=self.package, visited_object=visited_name))
        else:
            visitors = []
        self.directory = directory
        for oodoc in oodocs:
            cls = None
            enum = None
            if oodoc.classes:
                cls = oodoc.classes[0]
                type = "class"
            elif oodoc.enums:
                enum = oodoc.enums[0]
                type = "enum"
            else:
                # Should be a OOCustomDocument
                type = oodoc.type
            template = self.template_cache.get_template(oodoc.name, type, template_variant)
            if template is None:
                raise Exception(f"Missing template for {oodoc.name}")

            code = template.render(
                doc=oodoc,
                cls=cls,
                enum=enum,
                gen=self,
                visitors=visitors,
                metamodel_version=self.schema.metamodel_version,
                model_version=self.schema.version,
            )

            os.makedirs(directory, exist_ok=True)
            filename = f"{oodoc.name}.java"
            path = os.path.join(directory, filename)
            with open(path, "w", encoding="UTF-8") as stream:
                stream.write(code)

    # The following methods are intended to be used from within a code
    # template.

    def has_ancestor(self, cls: ClassDefinition, name: str) -> bool:
        """Checks for an ancestor in a class inheritance tree.

        :param cls: A ClassDefinition object.
        :param name: A class name.
        :returns: True if cls has any ancestor with the specified name.
        """
        if cls.is_a is None:
            return False
        elif cls.is_a == name:
            return True
        else:
            return self.has_ancestor(self.schemaview.get_class(cls.is_a), name)

    def get_descendants(self, name: str, _descendants=None) -> list[str]:
        """Gets all the descendants of a class.

        :param name: A class name.
        :param _descendants: The list to which to append the names of the
            descendant classes.
        :returns: A flat list of the names of all classes that inherit from
            the named class.
        """
        if _descendants is None:
            _descendants = []
        for child in self.schemaview.class_children(name):
            _descendants.append(child)
            self.get_descendants(child, _descendants)
        return _descendants

    def get_class_name(self, name: str) -> str:
        """Converts a LinkML class name to a Java class name."""
        return camelcase(name)

    def get_write_accessor_name(self, slot: SlotDefinition) -> str:
        """Gets the name of the write accessor for the given slot.

        This is to allow templates to generate their own write accessors,
        should they prefer not to use Lombok.
        """
        if slot.range == "boolean" and slot.required:
            # This replicates the logic used by Lombok for boolean-typed fields:
            # - foo -> setFoo() (general case)
            # - isFoo -> setFoo() (special case to avoid setIsFoo())
            if len(slot.name) > 2 and slot.name[:2] == "is" and not slot.name[2].islower():
                return "set" + camelcase(slot.name[2:])
        return "set" + camelcase(slot.name)

    def get_read_accessor_name(self, slot: SlotDefinition) -> str:
        """Gets the name of the read accessor for the given slot."""
        if slot.range == "boolean" and slot.required:
            # This replicates the logic used by Lombok for boolean-typed fields
            # - foo -> isFoo() (general case)
            # - isFoo -> isFoo() (special case to avoid isIsFoo())
            if len(slot.name) > 2 and slot.name[:2] == "is" and not slot.name[2].islower():
                return self.get_slot_name(slot.name)
            else:
                return "is" + camelcase(slot.name)
        else:
            return "get" + camelcase(slot.name)


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
@click.option("--extra-template", multiple=True, help="Name of an additional, arbitrary template to use")
@click.option("--visitor", multiple=True, help="Generate a visitor interface for the specified class")
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
    extra_template=[],
    visitor=[],
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
    ).serialize(
        output_directory, template_variant=template_variant, extra_templates=extra_template, visitors=visitor, **args
    )


if __name__ == "__main__":
    cli()
