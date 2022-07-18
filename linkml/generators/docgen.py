import os
import logging
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set, TypeVar, Iterable
from copy import deepcopy

import click
import pkg_resources
from jinja2 import Template, FileSystemLoader, Environment
from linkml_runtime.dumpers import yaml_dumper

from linkml_runtime.utils.schemaview import SchemaView

from linkml_runtime.linkml_model.meta import SchemaDefinition, TypeDefinition, ClassDefinition, Annotation, Element, \
    SlotDefinition, SlotDefinitionName, Definition, DefinitionName, EnumDefinition, ClassDefinitionName, SubsetDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore

from linkml.utils.generator import shared_arguments, Generator

class MarkdownDialect(Enum):
    python = "python"  ## https://python-markdown.github.io/ -- used by mkdocs
    myst = "myst"      ## https://myst-parser.readthedocs.io/en/latest/ -- used by sphinx


# In future this may become a Union statement, but for now we only have dialects for markdown
DIALECT = MarkdownDialect

MAX_CHARS_IN_TABLE = 80
MAX_RANK = 1000


def enshorten(input):
    """
    Custom filter to truncate any long text intended to go in a table,
    and to remove anything after a newline"""
    if input is None:
        return ""
    if "\n" in input:
        toks = input.split("\n")
        input = toks[0]
    if "." in input:
        toks = input.split(".")
        input = toks[0]
    if len(input) > MAX_CHARS_IN_TABLE-3:
        input = input[0:MAX_CHARS_IN_TABLE-3] + "..."
    return input


def customize_environment(env: Environment):
    env.filters['enshorten'] = enshorten


def _ensure_ranked(elements: Iterable[Element]):
    for x in elements:
        if x.rank is None:
            x.rank = MAX_RANK

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
    dialect: DIALECT = None
    sort_by: sort_by = None
    visit_all_class_slots = False
    template_mappings: Dict[str, str] = None
    directory = None
    template_directory = None
    genmeta = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition],
                 directory: str = None,
                 template_directory: str = None,
                 use_slot_uris: bool = False,
                 format: str = valid_formats[0],
                 dialect: Optional[Union[DIALECT, str]] = None,
                 sort_by: str = None,
                 genmeta: bool=False,
                 gen_classvars: bool=True, gen_slots: bool=True, **kwargs) -> None:
        """
        Creates a generator object that can write documents to a directory from a schema

        :param schema: path to schema file or schema object
        :param directory: directory in which to write documents
        :param template_directory: directory for custom templates
        :param format: only markdown is supported by default
        :param dialect: markdown dialect (e.g MyST, Python)
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
        self.use_slot_uris = use_slot_uris
        self.genmeta = genmeta
        if sort_by is None:
            sort_by = 'name'
        self.sort_by = sort_by
        if dialect is not None:
            if isinstance(dialect, str):
                if dialect == MarkdownDialect.myst.value:
                    dialect = MarkdownDialect.myst
                elif dialect == MarkdownDialect.python.value:
                    dialect = MarkdownDialect.python
                else:
                    raise NotImplemented(f'{dialect} not supported')
            self.dialect = dialect



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
        template_vars = {
            'sort_by': self.sort_by
        }
        template = self._get_template('index')
        out_str = template.render(gen=self,
                                  schema=sv.schema,
                                  schemaview=sv,
                                  **template_vars)
        self._write(out_str, directory, 'index')  ## TODO: make configurable
        if self._is_single_file_format(self.format):
            logging.info(f'{self.format} is a single-page format, skipping non-index elements')
            return
        template = self._get_template('schema')
        for schema_name in sv.imports_closure():
            imported_schema = sv.schema_map.get(schema_name)
            out_str = template.render(gen=self,
                                      schema=imported_schema,
                                      schemaview=sv,
                                      **template_vars)
            self._write(out_str, directory, imported_schema.name)
        template = self._get_template('class')
        for cn, c in sv.all_classes().items():
            if self._is_external(c):
                continue
            n = self.name(c)
            out_str = template.render(gen=self,
                                      element=c,
                                      schemaview=sv,
                                      **template_vars)
            self._write(out_str, directory, n)
        template = self._get_template('slot')
        for sn, s in sv.all_slots().items():
            if self._is_external(s):
                continue
            n = self.name(s)
            s = sv.induced_slot(sn)
            out_str = template.render(gen=self,
                                      element=s,
                                      schemaview=sv,
                                      **template_vars)
            self._write(out_str, directory, n)
        template = self._get_template('enum')
        for en, e in sv.all_enums().items():
            if self._is_external(e):
                continue
            n = self.name(e)
            out_str = template.render(gen=self,
                                      element=e,
                                      schemaview=sv,
                                      **template_vars)
            self._write(out_str, directory, n)
        template = self._get_template('type')
        for tn, t in sv.all_types().items():
            if self._exclude_type(t):
                continue
            n = self.name(t)
            t = sv.induced_type(tn)
            out_str = template.render(gen=self,
                                      element=t,
                                      schemaview=sv,
                                      **template_vars)
            self._write(out_str, directory, n)
        template = self._get_template('subset')
        for _, s in sv.all_subsets().items():
            if self._is_external(c):
                continue
            n = self.name(s)
            out_str = template.render(gen=self,
                                      element=s,
                                      schemaview=sv,
                                      **template_vars)
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
        elif self.format == 'latex':
            return 'tex'
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
            customize_environment(env)
            return env.get_template(path)
        else:
            base_file_name = f'{element_type}.{self._file_suffix()}.jinja2'
            folder = None
            if self.template_directory:
                p = Path(self.template_directory) / base_file_name
                if p.is_file():
                    folder = self.template_directory
                else:
                    logging.info(f'Could not find {base_file_name} in {self.template_directory} - falling back to default')
            if not folder:
                folder = pkg_resources.resource_filename(__name__, 'docgen')
            loader = FileSystemLoader(folder)
            env = Environment(loader=loader)
            customize_environment(env)
            return env.get_template(base_file_name)

    def schema_title(self) -> str:
        """
        Returns the title of the schema.

        Uses title field if present, otherwise name

        :return:
        """
        s = self.schemaview.schema
        if s.title:
            return s.title
        else:
            return s.name


    def name(self, element: Element) -> str:
        """
        Returns the name of the element in its canonical form

        :param element: SchemaView element definition
        :return: slot name or numeric portion of CURIE prefixed 
        slot_uri
        """
        if type(element).class_name == 'slot_definition':

            if self.use_slot_uris:
                if element.slot_uri is not None:
                    return element.slot_uri.split(":")[1]
                else:
                    return underscore(element.name)

            return underscore(element.name)
        else:
            return camelcase(element.name)

    def uri(self, element: Element, expand=True) -> str:
        """
        Fetches the URI string for the relevant element

        :param element:
        :return:
        """
        if isinstance(element, (EnumDefinition, SubsetDefinition)):
            # TODO: fix schema view to handle URIs for enums and subsets
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
        if self._is_external(e):
            return self.uri_link(e)
        elif isinstance(e, ClassDefinition):
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, EnumDefinition):
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, SlotDefinition):
            if self.use_slot_uris:
                if e.slot_uri is not None:
                    return self._markdown_link(e.slot_uri.split(":")[1])
            return self._markdown_link(underscore(e.name))
        elif isinstance(e, TypeDefinition):
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, SubsetDefinition):
            return self._markdown_link(camelcase(e.name))
        else:
            return e.name

    def _exclude_type(self, t: TypeDefinition) -> bool:
        return self._is_external(t) and not self.schemaview.schema.id.startswith("https://w3id.org/linkml/")

    def _is_external(self, element: Element) -> bool:
        # note: this is currently incomplete. See: https://github.com/linkml/linkml/issues/782
        if element.from_schema == 'https://w3id.org/linkml/types' and not self.genmeta:
            return True
        else:
            return False

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
        if slot.required or slot.identifier:
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

    def mermaid_directive(self) -> str:
        """
        Writes a mermaid directive. See <https://mermaid-js.github.io/mermaid/#/>_

        This comes after the triple-backtick.

        Note that the directive varies depending on whether the dialect is
        the default python markdown (used by mkdocs) or MyST (used if you
        have a sphinx site)
        """
        if self.dialect is not None and self.dialect == MarkdownDialect.myst:
            return '{mermaid}'
        else:
            return 'mermaid'

    def latex(self, text: Optional[str]) -> str:
        """
        Makes text safe for latex

        NOTE: may be incomplete!

        :param text:
        :return:
        """
        if text is None:
            text = ''
        return text.replace('_', '\\_')

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

    def class_induced_slots(self, class_name: ClassDefinitionName) -> Iterator[SlotDefinition]:
        """
        Yields all induced slots for a class

        Ensures rank is non-null

        :param class_name:
        :return: iterator
        """
        elts = self.schemaview.class_induced_slots(class_name)
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_class_objects(self) -> Iterator[ClassDefinition]:
        """
        all class objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_classes().values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_slot_objects(self) -> Iterator[SlotDefinition]:
        """
        all slot objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_slots().values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_type_objects(self) -> Iterator[TypeDefinition]:
        """
        all type objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_types().values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_enum_objects(self) -> Iterator[EnumDefinition]:
        """
        all enum objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_enums().values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_subset_objects(self) -> Iterator[SubsetDefinition]:
        """
        all enum objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_subsets().values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def class_hierarchy_as_tuples(self) -> Iterator[Tuple[int, ClassDefinitionName]]:
        """
        Generate a hierarchical representation of all classes in the schema

        This is represented as a list of tuples (depth: int, cls: ClassDefinitionName),
        where the order is pre-order depth first traversal

        This can then be used to draw a hierarchy within jinja in a number of ways; e.g

        - markdown (by using indentation of " " * depth on a list)
        - tables (by placing fake indentation e.g using underscores)

        Simply iterate through all tuples, drawing each in the appropriate way

        Note: By default all classes are ordered alphabetically

        :return: tuples (depth: int, cls: ClassDefinitionName)
        """
        sv = self.schemaview
        roots = sv.class_roots(mixins=False)

        # by default the classes are sorted alphabetically
        roots = sorted(roots, key=str.casefold, reverse=True)

        # the stack holds tuples of depth-class that have still to be processed.
        # we seed this with all root classes (which have depth 0)
        # note the stack is processed from the last element first, ie. LIFO
        stack = [(0, root) for root in roots]
        # use iterative depth first traversal
        while len(stack) > 0:
            depth, class_name = stack.pop()
            yield depth, class_name
            children = sorted(sv.class_children(class_name=class_name, mixins=False), key=str.casefold, reverse=True)
            for child in children:
                # depth first - place at end of stack (to be processed next)
                stack.append((depth+1, child))

    def _is_single_file_format(self, format: str):
        if format == 'latex':
            return True
        else:
            return False


@shared_arguments(DocGenerator)
@click.option("--directory", "-d", required=True, help="Folder to which document files are written")
@click.option("--dialect",  help="Dialect or 'flavor' of Markdown used.")
@click.option("--sort-by",
              default='name',
              show_default=True,
              help="Metaslot to use to sort elements by e.g. rank, name, title")
@click.option("--genmeta/--no-genmeta",
              default=False,
              show_default=True,
              help="Generating metamodel. Only use this for generating meta.py")
@click.option("--template-directory", help="Folder in which custom templates are kept")
@click.option("--use-slot-uris/--no-use-slot-uris", default=False, help="Use IDs from slot_uri instead of names")
@click.command()
def cli(yamlfile, directory, dialect, template_directory, use_slot_uris, **args):
    """Generate documentation folder from a LinkML YAML schema

    Currently a default set of templates for markdown is provided (see the folder linkml/generators/docgen/)

    If you specify another format (e.g. html) then you need to provide a template_directory argument, with a template for
    each type of entity inside
    """
    gen = DocGenerator(
        yamlfile,
        directory=directory,
        dialect=dialect,
        template_directory=template_directory,
        use_slot_uris=use_slot_uris,
        **args)
    print(gen.serialize())


if __name__ == '__main__':
    cli()
