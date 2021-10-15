import os
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set

import click
from jinja2 import Template

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
    "str": "String",
    "int": "Integer",
    "float": "Float",
    "Bool": "Boolean",
    "XSDDate": "String",
    "URIorCURIE": "String"
}


class JavaGenerator(OOCodeGenerator):
    generatorname = os.path.basename(__file__)
    generatorversion = JAVA_GEN_VERSION
    valid_formats = ['java']
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 package: str = None,
                 template_file: str = None,
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.package = package
        self.template_file = template_file

    def map_type(self, t: TypeDefinition) -> str:
        return TYPEMAP.get(t.base, t.base)

    def serialize(self, directory: str) -> None:
        sv = self.schemaview

        if self.template_file is not None:
            with open(self.template_file) as template_file:
                template_obj = Template(template_file.read())
        else:
            template_obj = Template(default_template)

        oodocs = self.create_documents()
        self.directory = directory
        for oodoc in oodocs:
            cls = oodoc.classes[0]
            code = template_obj.render(doc=oodoc, cls=cls)

            os.makedirs(directory, exist_ok=True)
            filename = f'{oodoc.name}.java'
            path = os.path.join(directory, filename)
            with open(path, 'w') as stream:
                stream.write(code)


@shared_arguments(JavaGenerator)
@click.option("--output_directory", default="output", help="Output directory for individually generated class files")
@click.option("--package", help="Package name where relevant for generated class files")
@click.option("--template_file", help="Optional jinja2 template to use for class generation")
@click.command()
def cli(yamlfile, output_directory=None, package=None, template_file=None, head=True, emit_metadata=False,
        genmeta=False, classvars=True, slots=True, **args):
    """Generate java classes to represent a LinkML model"""
    JavaGenerator(yamlfile, package=package, template_file=template_file, emit_metadata=head, genmeta=genmeta,
                  gen_classvars=classvars, gen_slots=slots,  **args).serialize(output_directory)


if __name__ == '__main__':
    cli()
