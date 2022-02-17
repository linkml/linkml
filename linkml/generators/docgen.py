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

from linkml_runtime.linkml_model.meta import SchemaDefinition, TypeDefinition, ClassDefinition, Annotation, Element, \
    SlotDefinition, SlotDefinitionName, Definition, DefinitionName, EnumDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore

from linkml.utils.generator import shared_arguments, Generator


class DocGenerator(Generator):
    """
    Generates documentation from a schema (ALPHA CODE)

    Documents can be generated using either provided Jinja2 templates, or by providing your own

    Currently the provided templates are for markdown but this framework allows direct generation
    to rst, html, etc

    This works via jinja2 templates (found in docgen/ folder). By default, only markdown templates
    are provided. You can either override these, or you can create entirely different templates
    e.g. for html, latex, etc

    The template folder is expected to have files:

        - class.FMT.jinja2
        - enum.FMT.jinja2
        - type.FMT.jinja2
        - slot.FMT.jinja2
        - schema.FMT.jinja2
        - subset.FMT.jinja2
        - index.FMT.jinja2

    Most of these accept a jinja2 variable `element`, except index, schema, which accept `schema`. See docgen for examples
    This will generate a single document for every

    - class, enum, type, slot
    - subset
    - imported schema

    It will also create an index file
    """
    generatorname = os.path.basename(__file__)
    generatorversion = '0.0.1'
    valid_formats = ['markdown', 'rst', 'html', 'latex']
    visit_all_class_slots = False
    template_mappings: Dict[str, str] = None
    directory = None
    template_directory = None

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 directory: str = None,
                 template_directory: str = None,
                 format: str = valid_formats[0],
                 genmeta: bool=False, gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        """
        Creates a generator object that can write documents to a directory from a schema

        :param schema: path to schema file or schema object
        :param directory: directory in which to write documents
        :param template_directory: directory for custom templates
        :param format: only markdown is supported by default
        :param genmeta:
        :param gen_classvars:
        :param gen_slots:
        :param kwargs:
        """
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.format = format
        self.directory = directory
        self.template_directory = template_directory

    def serialize(self, directory: str = None) -> None:
        """
        Serialize a schema as a collection of documents

        :param directory: relative or absolute path to directory in which documents are to be written
        :return:
        """
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
        """
        Writes a string in desired format (e.g. markdown) to the appropriate file in a directory

        :param out_str: string to be written
        :param directory: location
        :param name: base name - should correspond to element name
        :return:
        """
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        file_name = f'{name}.{self._file_suffix()}'
        with open(path / file_name, 'w', encoding='UTF-8') as stream:
            stream.write(out_str)

    def _file_suffix(self):
        """
        File suffix to be used for both outputs and template files

        Template files are assumed to be of the form TYPE.FILE_SUFFIX.jinja2
        :return:
        """
        if self.format == 'markdown':
            return 'md'
        else:
            return self.format

    def _get_template(self, element_type: str) -> Template:
        """
        Create a jinja2 template object for a given schema element type

        The default location for templates is in the linkml/docgen folder,
        but this can be overriden
        :param element_type: e.g. class, enum, index, subset, ...
        :return:
        """
        if self.template_mappings and element_type in self.template_mappings:
            path = self.template_mappings[element_type]
            # TODO: relative paths
            #loader = FileSystemLoader()
            env = Environment()
            return env.get_template(path)
        else:
            base_file_name = f'{element_type}.{self._file_suffix()}.jinja2'
            folder = None
            if self.template_directory:
                p = Path(self.template_directory) / base_file_name
                if (Path(self.template_directory) / base_file_name).is_file():
                    folder = self.template_directory
                else:
                    logging.warning(f'Could not find {base_file_name} in {self.template_directory} - falling back to default')
            if not folder:
                folder = pkg_resources.resource_filename(__name__, 'docgen')
            loader = FileSystemLoader(folder)
            env = Environment(loader=loader)
            return env.get_template(base_file_name)



    def name(self, element: Element) -> str:
        """
        Returns the name of the element in its canonical form

        :param element:
        :return:
        """
        if type(element).class_name == 'slot_definition':
            return underscore(element.name)
        else:
            return camelcase(element.name)

    def uri(self, element: Element, expand=True) -> str:
        """
        Fetches the URI string for the relevant element

        :param element:
        :return:
        """
        if isinstance(element, EnumDefinition):
            # TODO: fix schema view to handle URIs for enums
            return self.name(element)
        return self.schemaview.get_uri(element, expand=expand)

    def uri_link(self, element: Element) -> str:
        """
        Returns a link string (default: markdown links) for a schema element

        :param element:
        :return:
        """
        uri = self.uri(element)
        curie = self.uri(element, expand=False)
        sc = element.from_schema
        return f'[{curie}]({uri})'


    def link(self, e: Union[Definition, DefinitionName]) -> str:
        """
        Render an element as a hyperlink

        :param e:
        :return:
        """
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
        return f'[{n}]({rel_path}.md)'

    def inheritance_tree(self, element: Definition, children: bool = True, **kwargs) -> str:
        """
        Show an element in the context of its is-a hierachy

        Limitations: currently only implemented for markdown (uses nested bullets)

        :param element: slot or class to be shown
        :param children: if true, show direct children
        :param mixins: if true, show mixins alongside each element
        :param kwargs:
        :return:
        """
        s, depth = self._tree(element, focus=element.name, **kwargs)
        if children:
            for c in self.schemaview.class_children(element.name, mixins=False):
                s += self._tree_info(self.schemaview.get_class(c), depth+1, **kwargs)
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
            lname = f'**{name}**'
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
        """
        Render tag-value for an element as a bullet

        Limitations: currently hardcoded to be markdown
        :param e: element that holds the property, e.g. Person
        :param meta_slot: metamodel property to be shown, e.g. comments
        :param backquote: if true, render as backquote
        :return: formatted string
        """
        v = getattr(e, meta_slot, None)
        if v:
            if backquote:
                v = v.replace('`', '\\`')
                v = f'`{v}`'
            return f'* [{meta_slot}](https://w3id.org/linkml/{meta_slot}): {v}\n'
        else:
            return ''

    def number_value_range(self, e: Union[SlotDefinition, TypeDefinition]) -> str:
        """
        Render the minimum and maximum values for a slot or type as a range, e.g 5-100

        :param e:
        :return:
        """
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
        """
        Render combination of required, multivalued, and recommended as a range, e.g. 0..*
        :param slot:
        :return:
        """
        if slot.required:
            min = '1'
        else:
            min = '0'
        if slot.multivalued:
            max = '*'
        else:
            max = '1'
        if slot.recommended:
            info = ' _recommended_'
        else:
            info = ''
        return f'{min}..{max}{info}'

    def yaml(self, element: Element, inferred=False) -> str:
        """
        Render element as YAML

        :param element:
        :param inferred: (classes only) show all induced slots as attributes
        :return: yaml string
        """
        if not inferred:
            return yaml_dumper.dumps(element)
        else:
            if not isinstance(element, ClassDefinition):
                raise ValueError(f'Inferred only applicable for classes, not {element.name} {type(element)}')
            # TODO: move this code to schemaview
            c = deepcopy(element)
            attrs = self.schemaview.class_induced_slots(c.name)
            for a in attrs:
                c.attributes[a.name] = a
            c.slots = []
            return yaml_dumper.dumps(c)



@shared_arguments(DocGenerator)
@click.option("--directory", "-d", required=True, help="Folder to which document files are written")
@click.option("--template-directory", help="Folder in which custom templates are kept")
@click.command()
def cli(yamlfile, directory, template_directory, **args):
    """Generate documentation folder from a LinkML YAML schema

    Currently a default set of templates for markdown is provided (see the folder linkml/generators/docgen/)

    If you specify another format (e.g. html) then you need to provide a template_directory argument, with a template for
    each type of entity inside
    """
    gen = DocGenerator(yamlfile, directory=directory, template_directory=template_directory, **args)
    print(gen.serialize())


if __name__ == '__main__':
    cli()
