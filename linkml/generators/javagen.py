import importlib.util
import os
from dataclasses import dataclass
from typing import Optional

import click
from jinja2 import Environment, FileSystemLoader, Template
from linkml_runtime.linkml_model.meta import TypeDefinition

from linkml._version import __version__
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments

default_template = """
{#-

  Jinja2 Template for a Java class with Lombok @Data annotation
  Annotation details at https://projectlombok.org
-#}
package {{ doc.package }};

import java.util.List;
import lombok.*;


{% if metamodel_version %}/* metamodel_version: {{metamodel_version}} */{% endif %}
{% if model_version %}/* version: {{model_version}} */{% endif %}


{% if cls.source_class.description %}/**
  {{ cls.source_class.description }}
**/{% endif %}
@Data
@EqualsAndHashCode(callSuper=false)
public{% if cls.abstract %} abstract{% endif %} class {{ cls.name }} {% if cls.is_a -%} extends {{ cls.is_a }} {%- endif %} {
{% for f in cls.fields %}
  private {{f.range}} {{ f.name }};
{%- endfor %}

}"""  # noqa: E501

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


@dataclass
class JavaGenerator(OOCodeGenerator):
    """
    Generates java code from a LinkML schema.

    Two styles are supported:

    - java classes, using lombok annotations
    - java records
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["java"]
    file_extension = "java"

    # ObjectVars
    generate_records: bool = False
    """If True then use java records (introduced in java 14) rather than classes"""

    template_file: Optional[str] = None

    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False
    emit_metadata: bool = True

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

    def serialize(self, directory: str, **kwargs) -> None:
        if self.generate_records:
            package_dir = os.path.dirname(importlib.util.find_spec(__name__).origin)
            javagen_folder = os.path.join(package_dir, "javagen", "")
            loader = FileSystemLoader(javagen_folder)
            env = Environment(loader=loader)
            template_obj = env.get_template("java_record_template.jinja2")
        elif self.template_file is not None:
            with open(self.template_file) as template_file:
                template_obj = Template(template_file.read())
        else:
            template_obj = Template(default_template)

        oodocs = self.create_documents()
        self.directory = directory
        for oodoc in oodocs:
            cls = oodoc.classes[0]
            code = template_obj.render(
                doc=oodoc,
                cls=cls,
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
@click.option("--template-file", help="Optional jinja2 template to use for class generation")
@click.option(
    "--generate-records/--no-generate-records",
    default=False,
    help="Optional Java 17 record implementation",
)
@click.version_option(__version__, "-V", "--version")
@click.command()
def cli(
    yamlfile,
    output_directory=None,
    package=None,
    template_file=None,
    generate_records=False,
    head=True,
    emit_metadata=False,
    genmeta=False,
    classvars=True,
    slots=True,
    **args,
):
    """Generate java classes to represent a LinkML model"""
    JavaGenerator(
        yamlfile,
        package=package,
        template_file=template_file,
        generate_records=generate_records,
        emit_metadata=head,
        genmeta=genmeta,
        gen_classvars=classvars,
        gen_slots=slots,
        **args,
    ).serialize(output_directory, **args)


if __name__ == "__main__":
    cli()
