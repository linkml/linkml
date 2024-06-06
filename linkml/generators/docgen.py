import importlib.util
import logging
import os
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import click
from jinja2 import Environment, FileSystemLoader, Template
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    Definition,
    DefinitionName,
    Element,
    EnumDefinition,
    SlotDefinition,
    SlotDefinitionName,
    SubsetDefinition,
    TypeDefinition,
    TypeDefinitionName,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.erdiagramgen import ERDiagramGenerator
from linkml.generators.plantumlgen import PlantumlGenerator
from linkml.utils.generator import Generator, shared_arguments
from linkml.workspaces.example_runner import ExampleRunner


class MarkdownDialect(Enum):
    python = "python"  # https://python-markdown.github.io/ -- used by mkdocs
    myst = "myst"  # https://myst-parser.readthedocs.io/en/latest/ -- used by sphinx


class DiagramType(Enum):
    mermaid_class_diagram = "mermaid_class_diagram"
    plantuml_class_diagram = "plantuml_class_diagram"
    er_diagram = "er_diagram"


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
    if len(input) > MAX_CHARS_IN_TABLE - 3:
        input = input[0 : MAX_CHARS_IN_TABLE - 3] + "..."
    return input


def customize_environment(env: Environment):
    env.filters["enshorten"] = enshorten


def _ensure_ranked(elements: Iterable[Element]):
    for x in elements:
        if x.rank is None:
            x.rank = MAX_RANK


@dataclass
class DocGenerator(Generator):
    """
    Generates documentation from a schema

    Note: this is a replacement for MarkdownGenerator

    Documents can be generated using either provided Jinja2 templates, or by
    providing your own

    Currently the provided templates are for markdown but this framework allows
    direct generation to rst, html, etc

    This works via jinja2 templates (found in docgen/ folder). By default, only
    markdown templates are provided. You can either override these, or you can
    create entirely different templates e.g. for html, latex, etc

    The template folder is expected to have files:

        - class.FMT.jinja2
        - enum.FMT.jinja2
        - type.FMT.jinja2
        - slot.FMT.jinja2
        - schema.FMT.jinja2
        - subset.FMT.jinja2
        - index.FMT.jinja2

    Most of these accept a jinja2 variable `element`, except index, schema,
    which accept `schema`. See docgen for examples This will generate a single
    document for every

    - class, enum, type, slot
    - subset
    - imported schema

    It will also create an index file
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["markdown", "rst", "html", "latex"]
    uses_schemaloader = False
    requires_metamodel = False

    # ObjectVars
    dialect: Optional[Union[DIALECT, str]] = None
    """markdown dialect (e.g MyST, Python)"""
    sort_by: str = "name"
    visit_all_class_slots = False
    template_mappings: Dict[str, str] = None
    directory: str = None
    """directory in which to write documents"""

    index_name: str = "index"
    """name of the index document"""

    template_directory: str = None
    """directory for custom templates"""

    diagram_type: Optional[Union[DiagramType, str]] = None
    """style of diagram (ER, UML)"""

    include_top_level_diagram: bool = False
    """Whether the index page should include a schema diagram"""

    example_directory: Optional[str] = None
    example_runner: ExampleRunner = field(default_factory=lambda: ExampleRunner())

    genmeta: bool = False
    gen_classvars: bool = True
    gen_slots: bool = True
    no_types_dir: bool = False
    use_slot_uris: bool = False
    use_class_uris: bool = False
    hierarchical_class_view: bool = False

    def __post_init__(self):
        dialect = self.dialect
        if dialect is not None:
            # TODO: simplify this
            if isinstance(dialect, str):
                if dialect == MarkdownDialect.myst.value:
                    dialect = MarkdownDialect.myst
                elif dialect == MarkdownDialect.python.value:
                    dialect = MarkdownDialect.python
                else:
                    raise NotImplementedError(f"{dialect} not supported")
            self.dialect = dialect
        if isinstance(self.diagram_type, str):
            self.diagram_type = DiagramType[self.diagram_type]
        if self.example_directory:
            self.example_runner = ExampleRunner(input_directory=Path(self.example_directory))
        super().__post_init__()
        self.logger = logging.getLogger(__name__)
        self.schemaview = SchemaView(self.schema, merge_imports=self.mergeimports)

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
            raise ValueError("Directory must be provided")
        template_vars = {
            "sort_by": self.sort_by,
            "diagram_type": self.diagram_type.value if self.diagram_type else None,
            "include_top_level_diagram": self.include_top_level_diagram,
        }
        self.logger.debug("Processing Index")
        template = self._get_template("index")
        out_str = template.render(gen=self, schema=sv.schema, schemaview=sv, **template_vars)
        self._write(out_str, directory, self.index_name)
        if self._is_single_file_format(self.format):
            self.logger.info(f"{self.format} is a single-page format, skipping non-index elements")
            return
        self.logger.debug("Processing Schemas...")
        template = self._get_template("schema")
        for schema_name in sv.imports_closure():
            self.logger.debug(f"  Generating doc for {schema_name}")
            imported_schema = sv.schema_map.get(schema_name)
            out_str = template.render(gen=self, schema=imported_schema, schemaview=sv, **template_vars)
            self._write(out_str, directory, imported_schema.name)
        self.logger.debug("Processing Classes...")
        template = self._get_template("class")
        for cn, c in sv.all_classes().items():
            if self._is_external(c):
                continue
            n = self.name(c)
            self.logger.debug(f"  Generating doc for {n}")
            out_str = template.render(gen=self, element=c, schemaview=sv, **template_vars)
            self._write(out_str, directory, n)
        self.logger.debug("Processing Slots...")
        template = self._get_template("slot")
        for sn, s in sv.all_slots().items():
            if self._is_external(s):
                continue
            n = self.name(s)
            self.logger.debug(f"  Generating doc for {n}")
            s = sv.induced_slot(sn)
            out_str = template.render(gen=self, element=s, schemaview=sv, **template_vars)
            self._write(out_str, directory, n)
        self.logger.debug("Processing Enums...")
        template = self._get_template("enum")
        for en, e in sv.all_enums().items():
            if self._is_external(e):
                continue
            n = self.name(e)
            self.logger.debug(f"  Generating doc for {n}")
            out_str = template.render(gen=self, element=e, schemaview=sv, **template_vars)
            self._write(out_str, directory, n)
        self.logger.debug("Processing Types...")
        template = self._get_template("type")
        for tn, t in sv.all_types().items():
            if self._exclude_type(t):
                continue
            n = self.name(t)
            self.logger.debug(f"  Generating doc for {n}")
            t = sv.induced_type(tn)
            out_str = template.render(gen=self, element=t, schemaview=sv, **template_vars)
            self._write(out_str, directory, n)
        self.logger.debug("Processing Subsets...")
        template = self._get_template("subset")
        for _, s in sv.all_subsets().items():
            if self._is_external(c):
                continue
            n = self.name(s)
            self.logger.debug(f"  Generating doc for {n}")
            out_str = template.render(gen=self, element=s, schemaview=sv, **template_vars)
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
        file_name = f"{name}.{self._file_suffix()}"
        self.logger.debug(f"  Writing file: {file_name}")
        with open(path / file_name, "w", encoding="UTF-8") as stream:
            stream.write(out_str)

    def _file_suffix(self):
        """
        File suffix to be used for both outputs and template files

        Template files are assumed to be of the form TYPE.FILE_SUFFIX.jinja2
        :return:
        """
        if self.format == "markdown":
            return "md"
        elif self.format == "latex":
            return "tex"
        else:
            return self.format

    def _get_template(self, element_type: str) -> Template:
        """
        Create a jinja2 template object for a given schema element type

        The default location for templates is in the linkml/docgen folder,
        but this can be overridden
        :param element_type: e.g. class, enum, index, subset, ...
        :return:
        """
        if self.template_mappings and element_type in self.template_mappings:
            path = self.template_mappings[element_type]
            # TODO: relative paths
            # loader = FileSystemLoader()
            env = Environment()
            customize_environment(env)
            return env.get_template(path)
        else:
            base_file_name = f"{element_type}.{self._file_suffix()}.jinja2"
            folder = None
            if self.template_directory:
                p = Path(self.template_directory) / base_file_name
                if p.is_file():
                    folder = self.template_directory
                else:
                    self.logger.info(
                        f"Could not find {base_file_name} in {self.template_directory} - falling back to default"
                    )
            if not folder:
                package_dir = os.path.dirname(importlib.util.find_spec(__name__).origin)
                folder = os.path.join(package_dir, "docgen", "")
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
        if type(element).class_name == "slot_definition":
            if self.use_slot_uris:
                curie = self.schemaview.get_uri(element)
                if curie:
                    return curie.split(":")[1]

            return underscore(element.name)
        elif type(element).class_name == "class_definition":
            if self.use_class_uris:
                curie = self.schemaview.get_uri(element)
                if curie:
                    return curie.split(":")[1]

            return camelcase(element.name)
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

    def uri_link(self, element: Union[Element, str]) -> str:
        """Returns a link string (default: markdown links) for a schema element

        :param element: uri string or linkml model element
        :return: hyperlinked markdown or web links
        """
        if isinstance(element, str):
            uri = self.schemaview.expand_curie(element)
            return f"[{element}]({uri})"

        uri = self.uri(element)
        curie = self.uri(element, expand=False)
        return f"[{curie}]({uri})"

    def link(self, e: Union[Definition, DefinitionName]) -> str:
        """
        Render an element as a hyperlink

        :param e:
        :return:
        """
        if e is None:
            return "NONE"
        if not isinstance(e, Definition):
            e = self.schemaview.get_element(e)
        if self._is_external(e):
            return self.uri_link(e)
        elif isinstance(e, ClassDefinition):
            if self.use_class_uris:
                curie = self.schemaview.get_uri(e)
                if curie is not None:
                    return self._markdown_link(n=curie.split(":")[1], name=e.name)
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, EnumDefinition):
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, SlotDefinition):
            if self.use_slot_uris:
                curie = self.schemaview.get_uri(e)
                if curie is not None:
                    return self._markdown_link(n=curie.split(":")[1], name=e.name)
            return self._markdown_link(underscore(e.name))
        elif isinstance(e, TypeDefinition):
            return self._markdown_link(camelcase(e.name))
        elif isinstance(e, SubsetDefinition):
            return self._markdown_link(camelcase(e.name))
        else:
            return e.name

    def links(self, e_list: List[DefinitionName]) -> List[str]:
        """Render list of element documentation pages as hyperlinks.

        :param e_list: list of elements
        :return: list of hyperlinked elements
        """
        return list(map(self.link, e_list))

    def _exclude_type(self, t: TypeDefinition) -> bool:
        return self._is_external(t) and not self.schemaview.schema.id.startswith("https://w3id.org/linkml/")

    def _is_external(self, element: Element) -> bool:
        # note: this is currently incomplete. See: https://github.com/linkml/linkml/issues/782
        if element.from_schema == "https://w3id.org/linkml/types" and not self.genmeta:
            return True
        else:
            return False

    @staticmethod
    def _markdown_link(n: str, name: str = None, subfolder: str = None) -> str:
        if subfolder:
            rel_path = f"{subfolder}/{n}"
        else:
            rel_path = n

        # if explicit name is provided use that for display name
        if name:
            n = name

        return f"[{n}]({rel_path}.md)"

    def inheritance_tree(self, element: Definition, children: bool = True, **kwargs) -> str:
        """
        Show an element in the context of its is-a hierarchy

        Limitations: currently only implemented for markdown (uses nested bullets)

        :param element: slot or class to be shown
        :param children: if true, show direct children
        :param mixins: if true, show mixins alongside each element
        :param kwargs:
        :return:
        """
        s, depth = self._tree(element, focus=element.name, **kwargs)
        if children:
            if isinstance(element, ClassDefinition):
                all_children = self.schemaview.class_children(element.name, mixins=False)
            else:
                all_children = self.schemaview.slot_children(element.name, mixins=False)
            for c in all_children:
                s += self._tree_info(self.schemaview.get_element(c), depth + 1, **kwargs)
        return s

    def _tree(
        self,
        element: Definition,
        mixins=True,
        descriptions=False,
        focus: DefinitionName = None,
    ) -> Tuple[str, int]:
        sv = self.schemaview
        if element.is_a:
            pre, depth = self._tree(
                sv.get_element(element.is_a),
                mixins=mixins,
                descriptions=descriptions,
                focus=focus,
            )
            depth += 1
        else:
            pre, depth = "", 0
        s = pre
        s += self._tree_info(element, depth, mixins=mixins, descriptions=descriptions, focus=focus)
        return s, depth

    def _tree_info(
        self,
        element: Definition,
        depth: int,
        mixins=True,
        descriptions=False,
        focus: DefinitionName = None,
    ) -> str:
        indent = " " * depth * 4

        if self.use_slot_uris or self.use_class_uris:
            name = self.schemaview.get_element(element).name
        else:
            name = self.name(element)

        if element.name == focus:
            lname = f"**{name}**"
        else:
            lname = self.link(element)
        s = f"{indent}* {lname}"
        if mixins and element.mixins:
            s += " ["
            if element.mixins:
                for m in element.mixins:
                    s += f" {self.link(m)}"
            s += "]"
        s += "\n"
        return s

    @staticmethod
    def bullet(e: Element, meta_slot: SlotDefinitionName, backquote=False) -> str:
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
                v = v.replace("`", "\\`")
                v = f"`{v}`"
            return f"* [{meta_slot}](https://w3id.org/linkml/{meta_slot}): {v}\n"
        else:
            return ""

    @staticmethod
    def number_value_range(e: Union[SlotDefinition, TypeDefinition]) -> str:
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
                r = f"{e.minimum_value} to {e.maximum_value}"
            else:
                r = f">= {e.minimum_value}"
        else:
            if e.maximum_value is not None:
                r = f"<= {e.maximum_value}"
        return r

    @staticmethod
    def cardinality(slot: SlotDefinition) -> str:
        """
        Render combination of required, multivalued, recommended, and exact_cardinality as a range,
        according to Mermaid conventions. Considers 'required' and 'multivalued' to set defaults
        for 'minimum_cardinality' and 'maximum_cardinality'.

        Reference: https://mermaid.js.org/syntax/classDiagram.html#cardinality-multiplicity-on-relations

        The different cardinality options are:
        - 1 Only 1
        - 0..1 Zero or One
        - 1..* One or more
        - * Many
        - n n (where n>1)
        - 0..n zero to n (where n>1)
        - 1..n one to n (where n>1)
        :param slot: SlotDefinition
        :return: cardinality string as used in Mermaid diagrams
        """
        if slot.exact_cardinality is not None:
            cardinality = str(slot.exact_cardinality)  # handles 'n' case
        else:
            if slot.required or slot.identifier:
                min_card = "1"
            else:
                min_card = str(slot.minimum_cardinality) if slot.minimum_cardinality is not None else "0"

            if slot.multivalued:
                max_card = "*"
            else:
                max_card = str(slot.maximum_cardinality) if slot.maximum_cardinality is not None else "1"

            if min_card == "0":
                if max_card == "1":
                    cardinality = "0..1"  # handles '0..1' case
                elif max_card == "*":
                    cardinality = "*"  # handles '*' case
                else:
                    cardinality = f"0..{max_card}"  # handles '0..n' case
            elif min_card == "1":
                if max_card == "1":
                    cardinality = "1"  # handles '1' case
                elif max_card == "*":
                    cardinality = "1..*"  # handles '1..*' case
                else:
                    cardinality = f"1..{max_card}"  # handles '1..n' case
            else:
                if max_card == "*":
                    cardinality = f"{min_card}..*"  # handles 'n..*' case
                else:
                    cardinality = f"{min_card}..{max_card}"  # handles 'n..m' case

        if slot.recommended:
            cardinality += " _recommended_"

        return cardinality

    def mermaid_directive(self) -> str:
        """
        Writes a mermaid directive. See <https://mermaid-js.github.io/mermaid/#/>_

        This comes after the triple-backtick.

        Note that the directive varies depending on whether the dialect is
        the default python markdown (used by mkdocs) or MyST (used if you
        have a sphinx site)
        """
        if self.dialect is not None and self.dialect == MarkdownDialect.myst:
            return "{mermaid}"
        else:
            return "mermaid"

    def mermaid_diagram(self, class_names: List[Union[str, ClassDefinitionName]] = None) -> str:
        """
        Render a mermaid diagram for a set of classes

        :param class_names:
        :return:
        """
        if self.diagram_type.value == DiagramType.er_diagram.value:
            erdgen = ERDiagramGenerator(self.schemaview.schema, format="mermaid")
            if class_names:
                return erdgen.serialize_classes(class_names, follow_references=True, max_hops=2)
            else:
                return erdgen.serialize()
        elif self.diagram_type.value == DiagramType.mermaid_class_diagram.value:
            self.logger.info("This is currently handled in the jinja templates")
        elif self.diagram_type.value == DiagramType.plantuml_class_diagram.value:
            plantumlgen = PlantumlGenerator(self.schema)
            plantuml_diagram = plantumlgen.serialize(classes=class_names)
            self.logger.debug(f"Created PlantUML diagram for class: {class_names}")
            return plantuml_diagram
        else:
            raise NotImplementedError(f"Diagram type {self.diagram_type} not implemented")

    @staticmethod
    def latex(text: Optional[str]) -> str:
        """
        Makes text safe for latex

        NOTE: may be incomplete!

        :param text:
        :return:
        """
        if text is None:
            text = ""
        return text.replace("_", "\\_")

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
                raise ValueError(f"Inferred only applicable for classes, not {element.name} {type(element)}")
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
        elts = self.schemaview.all_classes(imports=self.mergeimports).values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_slot_objects(self) -> Iterator[SlotDefinition]:
        """
        all slot objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_slots(imports=self.mergeimports).values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_type_objects(self) -> Iterator[TypeDefinition]:
        """
        all type objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_types(imports=self.mergeimports).values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_type_object_names(self) -> List[TypeDefinitionName]:
        return [t.name for t in list(self.all_type_objects())]

    def all_enum_objects(self) -> Iterator[EnumDefinition]:
        """
        all enum objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_enums(imports=self.mergeimports).values()
        _ensure_ranked(elts)
        for e in elts:
            yield e

    def all_subset_objects(self) -> Iterator[SubsetDefinition]:
        """
        all enum objects in schema

        Ensures rank is non-null
        :return: iterator
        """
        elts = self.schemaview.all_subsets(imports=self.mergeimports).values()
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
        roots = sv.class_roots(mixins=False, imports=self.mergeimports)

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
            children = sorted(
                sv.class_children(class_name=class_name, mixins=False, imports=self.mergeimports),
                key=str.casefold,
                reverse=True,
            )
            for child in children:
                # depth first - place at end of stack (to be processed next)
                stack.append((depth + 1, child))

    @staticmethod
    def _is_single_file_format(format: str):
        if format == "latex":
            return True
        else:
            return False

    def inject_slot_info(self, slot: SlotDefinition) -> SlotDefinition:
        """
        Injects additional information into a slot

        TODO: move this functionality into schemaview
        :param slot:
        :return:
        """
        sv = self.schemaview
        if not slot.range:
            slot.range = sv.schema.default_range
        if not slot.range:
            slot.range = "string"
        return slot

    @staticmethod
    def get_direct_slot_names(cls: ClassDefinition) -> List[SlotDefinitionName]:
        """Fetch list of all own attributes of a class, i.e.,
        all slot names of slots that belong to the domain of a class.

        :param cls: class for which we want to determine the attributes
        :return: list of names of all own attributes of a class
        """
        return cls.slots + list(cls.attributes.keys())

    def get_direct_slots(self, cls: ClassDefinition) -> List[SlotDefinition]:
        """Fetch list of all own attributes of a class, i.e.,
        all slots that belong to the domain of a class.

        :param cls: class for which we want to determine the attributes
        :return: list of all own attributes of a class
        """
        return [
            self.inject_slot_info(self.schemaview.induced_slot(sn, cls.name)) for sn in self.get_direct_slot_names(cls)
        ]

    def get_indirect_slots(self, cls: ClassDefinition) -> List[SlotDefinition]:
        """Fetch list of all inherited attributes of a class, i.e.,
        all slots that belong to the domain of a class.

        :param cls: class for which we want to determine the attributes
        :return: list of all own attributes of a class
        """
        sv = self.schemaview
        direct_slot_names = self.get_direct_slot_names(cls)
        return [
            self.inject_slot_info(slot)
            for slot in sv.class_induced_slots(cls.name)
            if slot.name not in direct_slot_names
        ]

    def get_slot_inherited_from(
        self, class_name: ClassDefinitionName, slot_name: SlotDefinitionName
    ) -> List[ClassDefinitionName]:
        """Get the name of the class that a given slot is inherited from.

        :param class_name: name of the class whose slot we are checking
        :param slot_name: name of slot in consideration
        :return: list of classes
        """
        sv = self.schemaview
        induced_slot = sv.induced_slot(slot_name, class_name)
        ancestors = sv.class_ancestors(class_name)
        return list(set(induced_slot.domain_of).intersection(ancestors))

    def get_mixin_inherited_slots(self, cls: ClassDefinition) -> Dict[str, List[str]]:
        """Fetch list of all slots acquired through mixing.

        :param cls: class for which we want to determine the mixed in slots
        :return: list of all mixed in slots from each mixin class
        """
        mixed_in_slots = {}
        sv = self.schemaview

        mixins = sv.class_parents(class_name=cls.name, mixins=True, is_a=False)
        for c in mixins:
            mixed_in_slots[c] = sv.class_slots(c)

        return mixed_in_slots

    def example_object_blobs(self, class_name: str) -> List[Tuple[str, str]]:
        """Fetch list of all examples of a class.

        :param class_name: class for which we want to determine the examples
        :return: list of all examples of a class
        """
        if not self.example_runner:
            return []
        inputs = self.example_runner.example_source_inputs(class_name)
        objs = []
        for input in inputs:
            stem = Path(input).stem
            with open(input, encoding="utf-8") as f:
                objs.append((stem, f.read()))
        return objs


@shared_arguments(DocGenerator)
@click.option(
    "--directory",
    "-d",
    required=True,
    help="Folder to which document files are written",
)
@click.option("--index-name", default="index", show_default=True, help="Name of the index document.")
@click.option("--dialect", help="Dialect or 'flavor' of Markdown used.")
@click.option(
    "--diagram-type",
    type=click.Choice([e.value for e in DiagramType]),
    help="Type of UML diagram to be rendered on class documentation pages.",
)
@click.option(
    "--include-top-level-diagram/--no-include-top-level-diagram",
    default=False,
    show_default=True,
    help="Include ER diagram of the entire schema on index page.",
)
@click.option(
    "--sort-by",
    default="name",
    show_default=True,
    help="Metaslot to use to sort elements by e.g. rank, name, title",
)
@click.option(
    "--genmeta/--no-genmeta",
    default=False,
    show_default=True,
    help="Generating metamodel. Only use this for generating meta.py",
)
@click.option("--template-directory", help="Folder in which custom templates are kept")
@click.option(
    "--use-slot-uris/--no-use-slot-uris",
    default=False,
    help="Use IDs from slot_uri instead of names",
)
@click.option(
    "--use-class-uris/--no-use-class-uris",
    default=False,
    help="Use IDs from class_uri instead of names",
)
@click.option(
    "--hierarchical-class-view/--no-hierarchical-class-view",
    default=True,
    help="Render class table on index page in a hierarchically indented view",
)
@click.option(
    "--example-directory",
    help="Folder in which example files are found. These are used to make inline examples",
)
@click.option(
    "-d",
    "--include",
    help="""
Include LinkML Schema outside of imports mechanism.  Helpful in including deprecated classes and slots in a separate
YAML, and including it when necessary but not by default (e.g. in documentation or for backwards compatibility)
""",
)
@click.version_option(__version__, "-V", "--version")
@click.command()
def cli(
    yamlfile,
    directory,
    index_name,
    dialect,
    template_directory,
    use_slot_uris,
    use_class_uris,
    hierarchical_class_view,
    **args,
):
    """Generate documentation folder from a LinkML YAML schema

    Currently a default set of templates for markdown is provided (see the
    folder linkml/generators/docgen/)

    If you specify another format (e.g. html) then you need to provide a
    template_directory argument, with a template for each type of entity inside.

    Examples can optionally be integrated into the documentation; to enable
    this, pass in the --example-directory argument.  The example directory
    should contain one file per example, following the naming convention
    <ClassName>-<ExampleName>.<extension>.

    For example, to include examples on the page for Person, include examples

    Person-001.yaml, Person-002.yaml, etc.

    Currently examples must be in yaml
    """
    gen = DocGenerator(
        yamlfile,
        directory=directory,
        dialect=dialect,
        template_directory=template_directory,
        use_slot_uris=use_slot_uris,
        use_class_uris=use_class_uris,
        hierarchical_class_view=hierarchical_class_view,
        index_name=index_name,
        **args,
    )
    print(gen.serialize())


if __name__ == "__main__":
    cli()
