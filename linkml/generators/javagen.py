import keyword
import os
import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set
import logging

import click
from jinja2 import Template

from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators import JAVA_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinition, ClassDefinition, ClassDefinitionName, \
    SlotDefinitionName, DefinitionName, Element, TypeDefinition, Definition, EnumDefinition, PermissibleValue

from linkml.generators.oocodegen import OOCodeGenerator, PACKAGE
from linkml.utils.generator import Generator, shared_arguments

template = """
{#-

  Jinja2 Template for a Java class

-#}
package {{ doc.package }};

import java.util.List;

{% for imp in doc.imports %}
import {{ imp }};
{% endfor %}

{% for ann in cls.annotations %}
@{{ ann }};
{%- endfor %}

public class {{ cls.name }} {% if cls.is_a -%} extends {{ cls.is_a }} {%- endif %} {

{% for f in cls.fields %}
  private {{f.range}} {{ f.name }};
{%- endfor %}

} 
"""

TYPEMAP = {
    "str": "String",
    "int": "Integer",
    "float": "Float",
    "Bool": "Boolean",
    "XSDDate": "String", # TODO: import java.time.LocalDate ?
    "URIorCURIE": "String" # TODO: generate this class here? import?
}

@dataclass
class JsonView:
    import_package: PACKAGE = None
    default_view: str = None

@dataclass
class Lombok:
    import_package: PACKAGE = None

@dataclass
class Hibernate:
    audited: bool
    indexed: bool


@dataclass
class JavaConfig:
    jsonView: JsonView = None
    lombok: Lombok = None
    hibernate: Hibernate = None


class JavaGenerator(OOCodeGenerator):
    generatorname = os.path.basename(__file__)
    generatorversion = JAVA_GEN_VERSION
    valid_formats = ['java']
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 config: JavaConfig = None,
                 package: str = None,
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.config = config
        self.package = package

    def map_type(self, t: TypeDefinition) -> str:
        return TYPEMAP.get(t.base, t.base)

    def serialize(self, directory: str) -> None:
        sv = self.schemaview
        template_obj = Template(template)
        oodocs = self.create_documents()
        self.directory = directory
        config = self.config
        for oodoc in oodocs:
            # Apply configurations. TODO: this is currently incomplete and intended as an exemplar
            # if config.lombok:
            #     oodoc.imports.append('lombok.*')
            # if config.jsonView:
            #     oodoc.imports.append('com.fasterxml.jackson.annotation.JsonView')
            #     oodoc.imports.append(config.jsonView.import_package)
            cls = oodoc.classes[0]
            code = template_obj.render(doc=oodoc, cls=cls)
            oodoc.package = self.package
            os.makedirs(directory, exist_ok=True)
            filename = f'{oodoc.name}.java'
            path = os.path.join(directory, filename)
            with open(path, 'w') as stream:
                stream.write(code)


@shared_arguments(JavaGenerator)
@click.command()
def cli(yamlfile, output_directory=None, package=None, head=True, emit_metadata=False, genmeta=False, classvars=True, slots=True, **args):
    """Generate java classes to represent a LinkML model"""
    JavaGenerator(yamlfile, package=package, emit_metadata=head, genmeta=genmeta, gen_classvars=classvars, gen_slots=slots,  **args).serialize(output_directory)


if __name__ == '__main__':
    cli()
