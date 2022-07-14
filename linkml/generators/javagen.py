import os
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set

import click
import pkg_resources
from jinja2 import Template, FileSystemLoader, Environment

from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators import JAVA_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, TypeDefinition

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
public {% if cls.abstract -%}abstract {%- endif %}class {{ cls.name }} {% if cls.is_a -%} extends {{ cls.is_a }} {%- endif %} {
{% for f in cls.fields %}
  private {{f.range}} {{ f.name }};
{%- endfor %}

}"""

TYPEMAP = {
    "xsd:string": "String",
    "xsd:integer": "Integer",
    "xsd:float": "Float",
    "xsd:double": "Double",
    "xsd:boolean": "Boolean",
    "xds:dateTime": "ZonedDateTime",
    "xds:date": "LocalDateTime",
    "xds:time": "Instant",
    "xsd:anyURI": "String",
    "xsd:decimal": "BigDecimal",
}


class JavaGenerator(OOCodeGenerator):
    generatorname = os.path.basename(__file__)
    generatorversion = JAVA_GEN_VERSION
    valid_formats = ['java']
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 package: str = None,
                 template_file: str = None,
                 generate_records: bool = False,
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs
        ) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.package = package
        self.template_file = template_file
        self.generate_records = generate_records

    def map_type(self, t: TypeDefinition) -> str:
        if t.uri:
            return TYPEMAP.get(t.uri)
        elif t.typeof:
            return self.map_type(self.schemaview.get_type(t.typeof))
        else:
            raise ValueError(f"{t} cannot be mapped to a type")

    def serialize(self, directory: str, **kwargs) -> None:
        sv = self.schemaview

        if self.generate_records:
            javagen_folder = pkg_resources.resource_filename(__name__, 'javagen')
            loader = FileSystemLoader(javagen_folder)
            env = Environment(loader=loader)
            template_obj = env.get_template('java_record_template.jinja2')
        elif self.template_file is not None:
            with open(self.template_file) as template_file:
                template_obj = Template(template_file.read())
        else:
            template_obj = Template(default_template)

        oodocs = self.create_documents()
        self.directory = directory
        for oodoc in oodocs:
            cls = oodoc.classes[0]
            code = template_obj.render(doc=oodoc, cls=cls, metamodel_version=self.schema.metamodel_version, model_version=self.schema.version)

            os.makedirs(directory, exist_ok=True)
            filename = f'{oodoc.name}.java'
            path = os.path.join(directory, filename)
            with open(path, 'w', encoding='UTF-8') as stream:
                stream.write(code)


@shared_arguments(JavaGenerator)
@click.option("--output-directory", default="output", show_default=True, help="Output directory for individually generated class files")
@click.option("--package", help="Package name where relevant for generated class files")
@click.option("--template-file", help="Optional jinja2 template to use for class generation")
@click.option("--generate-records/--no-generate-records", default=False, help="Optional Java 17 record implementation")
@click.command()
def cli(yamlfile, output_directory=None, package=None, template_file=None, generate_records=False, head=True, emit_metadata=False,
        genmeta=False, classvars=True, slots=True, **args):
    """Generate java classes to represent a LinkML model"""
    JavaGenerator(yamlfile, package=package, template_file=template_file, generate_records=generate_records, emit_metadata=head, genmeta=genmeta,
                  gen_classvars=classvars, gen_slots=slots,  **args).serialize(output_directory, **args)


if __name__ == '__main__':
    cli()
