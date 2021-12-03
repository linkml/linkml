import os
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set
from copy import deepcopy

import click
import pkg_resources
from jinja2 import Template, FileSystemLoader, Environment
from linkml_runtime.dumpers import yaml_dumper

from linkml_runtime.utils.schemaview import SchemaView

#from linkml.generators import pydantic_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, TypeDefinition, ClassDefinition, Annotation, Element, \
    SlotDefinition, SlotDefinitionName, Definition, DefinitionName, EnumDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore

from linkml.generators.oocodegen import OOCodeGenerator
from linkml.utils.generator import shared_arguments, Generator


class DocGenerator(Generator):
    """
    Generates documentation from a schema (ALPHA CODE)

    Documents can be generated using either provided Jinja2 templates, or by providing your own

    Currently the provided templates are for markdown but this framework allows direct generation
    to rst, html, etc
    """
    generatorname = os.path.basename(__file__)
    generatorversion = '0.0.1'
    valid_formats = ['markdown']
    visit_all_class_slots = False
    template_mappings: Dict[str, str] = None
    directory = None

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 template_file: str = None,
                 directory: str = None,
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.template_file = template_file
        self.directory = directory

    def serialize(self, directory: str = None) -> None:
        sv = self.schemaview
        if directory is None:
            directory = self.directory
        if directory is None:
            raise ValueError(f'Directory must be provided')
        template = self._get_template('index')
        out_str = template.render(gen=self,
                                  schema=sv.schema,
                                  schemaview=sv)
        self._write(out_str, directory, 'index')  ## TODO: make configurable
        template = self._get_template('schema')
        for schema_name in sv.imports_closure():
            imported_schema = sv.schema_map.get(schema_name)
            out_str = template.render(gen=self,
                                      schema=imported_schema,
                                      schemaview=sv)
            self._write(out_str, directory, imported_schema.name)
        template = self._get_template('class')
        for cn, c in sv.all_classes().items():
            n = self.name(c)
            out_str = template.render(gen=self,
                                      element=c,
                                      schemaview=sv)
            self._write(out_str, directory, n)
        template = self._get_template('slot')
        for sn, s in sv.all_slots().items():
            n = self.name(s)
            out_str = template.render(gen=self,
                                      element=s,
                                      schemaview=sv)
            self._write(out_str, directory, n)
        template = self._get_template('enum')
        for en, e in sv.all_enums().items():
            n = self.name(e)
            out_str = template.render(gen=self,
                                      element=e,
                                      schemaview=sv)
            self._write(out_str, directory, n)
        template = self._get_template('type')
        for tn, t in sv.all_types().items():
            n = self.name(t)
            out_str = template.render(gen=self,
                                      element=t,
                                      schemaview=sv)
            self._write(out_str, directory, n)

    def _write(self, out_str: str, directory: str, name: str) -> None:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        with open(path / f'{name}.md', 'w') as stream:
            stream.write(out_str)


    def _get_template(self, element_type: str) -> Template:
        if self.template_mappings and element_type in self.template_mappings:
            path = self.template_mappings[element_type]
            # TODO: relative paths
            #loader = FileSystemLoader()
            env = Environment()
            return env.get_template(path)
        else:
            folder = pkg_resources.resource_filename(__name__, 'docgen')
            loader = FileSystemLoader(folder)
            env = Environment(loader=loader)
            return env.get_template(f'{element_type}.md.jinja2')



    def name(self, element: Element) -> str:
        if type(element).class_name == 'slot_definition':
            return underscore(element.name)
        else:
            return camelcase(element.name)

    def uri(self, element: Element) -> str:
        if isinstance(element, EnumDefinition):
            # TODO: fix schema view to handle URIs for enums
            return self.name(element)
        return self.schemaview.get_uri(element, expand=True)

    def link(self, e: Union[Definition, DefinitionName]) -> str:
        if e is None:
            return 'NONE'
        if not isinstance(e, Definition):
            e = self.schemaview.get_element(e)
        if isinstance(e, ClassDefinition):
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, EnumDefinition):
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, SlotDefinition):
            return self._markdown_link(underscore(e.name))
        elif isinstance(e, TypeDefinition):
            return self._markdown_link(underscore(e.name))
        else:
            return e.name

    def _markdown_link(self, n: str, subfolder: str = None) -> str:
        if subfolder:
            rel_path = f'{subfolder}/{n}'
        else:
            rel_path = n
        return f'[{n}]({rel_path})'

    def inheritance_tree(self, element: Definition, children:bool = True, **kwargs) -> str:
        s, depth = self._tree(element, **kwargs)
        if children:
            for c in self.schemaview.class_children(element.name, mixins=False):
                s += self._tree_info(self.schemaview.get_class(c), depth+1, focus=element.name, **kwargs)
        return s

    def _tree(self, element: Definition, mixins=True, descriptions=False, focus: DefinitionName = None) -> Tuple[str, int]:
        sv = self.schemaview
        if element.is_a:
            pre, depth = self._tree(sv.get_element(element.is_a), mixins=mixins, descriptions=descriptions, focus=focus)
            depth += 1
        else:
            pre, depth = '', 0
        s = pre
        s += self._tree_info(element, depth, mixins=mixins, descriptions=descriptions, focus=focus)
        return s, depth

    def _tree_info(self, element: Definition, depth: int, mixins=True, descriptions=False, focus: DefinitionName = None) -> str:
        indent = ' ' * depth * 4
        name = self.name(element)
        if element.name == focus:
            lname = name
        else:
            lname = self.link(element)
        s = f'{indent}* {lname}'
        if mixins and element.mixins:
            s += ' ['
            if element.mixins:
                for m in element.mixins:
                    s += f' {m}'
            s += ']'
        s += '\n'
        return s

    def bullet(self, e: Element, meta_slot: SlotDefinitionName, backquote = False) -> str:
        v = getattr(e, meta_slot, None)
        if v:
            if backquote:
                v = v.replace('`', '\\`')
                v = f'`{v}`'
            return f'* [{meta_slot}](https://w3id.org/linkml/{meta_slot}): {v}\n'
        else:
            return ''

    def number_value_range(self, e: Union[SlotDefinition, TypeDefinition]) -> str:
        r = None
        if isinstance(e, TypeDefinition):
            # TODO: new version
            return None
        if e.minimum_value is not None:
            if e.maximum_value is not None:
                r = f'{e.minimum_value} to {e.maximum_value}'
            else:
                r = f'>= {e.minimum_value}'
        else:
            if e.maximum_value is not None:
                r = f'<= {e.maximum_value}'
        return r

    def cardinality(self, slot: SlotDefinition) -> str:
        if slot.required:
            min = '1'
        else:
            min = '0'
        if slot.multivalued:
            max = '*'
        else:
            max = '1'
        return f'{min}..{max}'

    def yaml(self, element: Element, inferred=False) -> str:
        if not inferred:
            return yaml_dumper.dumps(element)
        else:
            if not isinstance(element, ClassDefinition):
                raise ValueError(f'Inferred only applicable for classes, not {element.name} {type(element)}')
            c = deepcopy(element)
            attrs = self.schemaview.class_induced_slots(c.name)
            for a in attrs:
                c.attributes[a.name] = a
            c.slots = []
            return yaml_dumper.dumps(c)



@shared_arguments(DocGenerator)
@click.option("--template_file", help="Optional jinja2 template to use for class generation")
@click.command()
def cli(yamlfile, template_file=None, head=True, emit_metadata=False, genmeta=False, classvars=True, slots=True, **args):
    """Generate pydantic classes to represent a LinkML model"""
    gen = DocGenerator(yamlfile, template_file=template_file, emit_metadata=head, genmeta=genmeta, gen_classvars=classvars, gen_slots=slots,  **args)
    print(gen.serialize())


if __name__ == '__main__':
    cli()
