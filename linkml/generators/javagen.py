import keyword
import os
import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set
import logging

import click
from linkml_runtime.linkml_model import linkml_files
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import URIRef

import linkml
from linkml.generators import JAVA_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinition, ClassDefinition, ClassDefinitionName, \
    SlotDefinitionName, DefinitionName, Element, TypeDefinition, Definition, EnumDefinition, PermissibleValue
from linkml_runtime.utils.formatutils import camelcase, underscore, be, wrapped_annotation, split_line, sfx

from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.ifabsent_functions import ifabsent_value_declaration, ifabsent_postinit_declaration, \
    default_curie_or_uri
from linkml_runtime.utils.metamodelcore import builtinnames

template = """
{#-

  Jinja2 Template for a Java class

-#}
package {{ package }};

{% for imp in imports %}
import {{ imp }};
{% endfor %}

import lombok.*;

{% for ann in class.annotations %}
@{{ ann }};
{% endfor %}

public class {{ cls.name }} {% if cls.is_a %} extends {{ cls.is_a }} {% endif %} {

{% for s in slots %}
  private {{s.range}} {{ s.name }};
{% endfor %}

} 
"""



class JavaGenerator(OOCodeGenerator):
    generatorname = os.path.basename(__file__)
    generatorversion = JAVA_GEN_VERSION
    valid_formats = ['java']
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)

    def visit_schema(self, directory: str = None, classes: Set[ClassDefinitionName] = None, image_dir: bool = False,
                     index_file: str = 'index.md',
                     noimages: bool = False, **_) -> None:
        sv = SchemaView(self.schema)
        oodocs = self.create_documents()
        self.directory = directory
        for oodoc in oodocs:
            if directory:
                os.makedirs(directory, exist_ok=True)




@shared_arguments(JavaGenerator)
@click.command()
def cli(yamlfile, head=True, genmeta=False, classvars=True, slots=True, **args):
    """Generate java classes to represent a LinkML model"""
    print(JavaGenerator(yamlfile, emit_metadata=head, genmeta=genmeta, gen_classvars=classvars, gen_slots=slots,  **args).serialize(emit_metadata=head, **args))


if __name__ == '__main__':
    cli()
