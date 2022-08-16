"""fhirgen: FHIR-related generators

Currently, only supports Enum -> ValueSet

Temp development notes
  - Mapping path: /Users/joeflack4/projects/linkml/linkml/generators/fhirgen/mapping__enum_valueset.csv

Resources
 1. Enum def: https://linkml.io/linkml-model/docs/EnumDefinition/
 2. ValueSet def: https://www.hl7.org/fhir/valueset.html
 3. Issue:https://github.com/linkml/linkml/issues/905
 4. PR: https://github.com/linkml/linkml/pull/913
 5. Mapping sheet source:
   https://docs.google.com/spreadsheets/d/1Y35SpVv09phns3v6QZ5mlzf8NfXGzSU1vcodo4TR8yQ/edit#gid=1898715155
 6. Link to old CCDH Enum/CodeSet model (if useful):
   https://raw.githubusercontent.com/cancerDHC/ccdhmodel/main/model/schema/crdch_model.yaml

TODO's
 1. R5: Need to see if it is different than R4 for ValueSet.
 2. Delete all stuff from file that I don't need
 3. Finish mapping__enum_valueset.csv
   - Add FHIR's Nested objects: e.g. `identifier`
   - 1st: Do all IMPT fhir fields
   - 2nd: Do all the IMPT linkml fields (need to go to dynamic-enums-example.yaml, from line 78, and add all the fields
     that appear in the file as 'IMPT'.
 4. Evaluate 'abritrary data model mapping' standards/formats/tools to potentially use over my ad-hoc CSV approach:
   (i) https://github.com/cmungall/linkml-transformer (ii) https://docs.google.com/presentation/d/
   1ctgT1IfwPjnFQO2Q0sYlM8qk0wiB2_32JyeKyN4Uf8k/edit?usp=drive_web&ouid=109884413503012482953 (iii) YARRRML (rdf only?)
todo later's
 1. XML output
"""
import csv
import json
import os
# from copy import deepcopy
# from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, TextIO, Union
# from typing import Callable, Dict, Iterator, TextIO, Tuple, Union

import click

# from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model.meta import EnumDefinition, SchemaDefinition
# from linkml_runtime.linkml_model.meta import ClassDefinition, ClassDefinitionName, Definition, DefinitionName, \
#     Element, EnumDefinition, SchemaDefinition, SlotDefinition, SubsetDefinition, TypeDefinition
# from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView
# from linkml.utils.generator import Generator, shared_arguments
# todo: Do I need _ensure_ranked? If so, move out of docgen?
# from linkml.generators.docgen import _ensure_ranked
from linkml.utils.generator import Generator, shared_arguments

# todo: make some of these class properties?
FHIRGEN_DIR = os.path.join(os.path.dirname(__file__), 'fhirgen')
MODEL_MAPPING_PATH = os.path.join(FHIRGEN_DIR, 'mapping__enum_valueset.csv')
SUPPORTED_FORMATS = ['json']  # todo: later: xml
FHIR_VALUESET_FIELD_MUTATIONS: Dict[str, Callable] = {
    'status': lambda x: 'unknown'  # todo: temp
}


# TODO: when rebasing, this will be a dataclass. outdir will become a standard dataclass obj for example. don't make
#  ...any of these changes before the dataclass PR is merged. (https://github.com/linkml/linkml/pull/924)
class FhirValueSetGenerator(Generator):
    """Generate FHIR ValueSet JSON from a LinkML YAML Enum schema"""
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = SUPPORTED_FORMATS

    def __init__(
        self,
        schema: Union[str, TextIO, SchemaDefinition],
        outdir: str = None,
        format: str = None,
    ) -> None:
        """
        Creates a generator object that can write output

        :param schema: path to schema file or schema object
        :param outdir: path to directory save file or file(s)
        :param genmeta:
        """
        self.sourcefile = schema
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        self.outdir = outdir
        self.format = format

    def serialize(self, save: bool = True, outdir: str = None, save_format='json') -> List[Dict]:
        """
        Serialize Enums in schema to JSON

        :param save: if True, saves to disk.
        :param outdir: path to directory save file or file(s)
        :param save_format: Format to save.
        :return: List of enums as dictionaries.
        """
        if save_format not in SUPPORTED_FORMATS:
            raise ValueError(f'Format {save_format} not supported. Use one of: {",".join(SUPPORTED_FORMATS)}')
        _outdir = outdir if outdir else self.outdir
        if save and not _outdir:
            raise RuntimeError('Tried to save, but did not supply `outdir`.')
        sv = self.schemaview
        linkml_dict_enums: Dict[str, EnumDefinition] = sv.all_enums()
        fhir_dict_enums = []
        for en, e in linkml_dict_enums.items():
            d: Dict = self.serialize_enum(en, e)
            fhir_dict_enums.append(fhir_dict_enums)
            if save and save_format == 'json':
                out_str: str = json.dumps(d)
                self._write(out_str=out_str, outdir=_outdir, name=en, format=save_format)
        return fhir_dict_enums


    @staticmethod
    def model_mappings(path: str = MODEL_MAPPING_PATH) -> Dict[str, str]:
        """Get model mappings from CSV"""
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = [x for x in reader][1:]  # don't need header
        d = {
            row[0]: row[1]  # easiest way; assumes linkml is always col 1, and fhir is col 2
            for row in rows
        }
        d = {k: v for k, v in d.items() if k}  # removes anything left over from empty CSV rows

        return d

    # TODO: Most of the work should go here
    # todo: Since I want to return a dict, should I call this dictify instead of serialize?
    def serialize_enum(self, enum_name: str, enum: EnumDefinition) -> Dict:
        """
        Serialize Enums in schema to JSON

        todo: use enum_name if needed
        :param enum_name: The enum name
        :param enum: The enum
        :return:
        """
        d = {}
        mappings: Dict[str, str] = self.model_mappings()

        for linkml_field, target_field in mappings.items():
            linkml_val: Any = getattr(enum, linkml_field)
            if not linkml_val:
                continue
            # TODO: Add handling of nested vals
            d[target_field] = linkml_val
            if linkml_field in FHIR_VALUESET_FIELD_MUTATIONS:
                d[target_field] = FHIR_VALUESET_FIELD_MUTATIONS[linkml_field](linkml_val)

        return d

    def _write(self, out_str: str, outdir: str, name: str, format: str = None) -> None:
        """
        Writes to disk

        :param out_str: string to be written
        :param outdir: path to directory save file or file(s)
        :param name: base name - should correspond to element name
        :param format: The data format
        # todo: Move `save` params in here, expose to user, and add json.dump() here?
        """
        if not format:
            format = self.format
        Path(outdir).mkdir(parents=True, exist_ok=True)
        file_name = f"{name}.{format}"
        outpath = os.path.join(outdir, file_name)
        with open(outpath, "w", encoding="UTF-8") as stream:
            stream.write(out_str)

    # def schema_title(self) -> str:
    #     """
    #     Returns the title of the schema.
    #
    #     Uses title field if present, otherwise name
    #
    #     :return:
    #     """
    #     s = self.schemaview.schema
    #     if s.title:
    #         return s.title
    #     else:
    #         return s.name

    # def name(self, element: Element) -> str:
    #     """
    #     Returns the name of the element in its canonical form
    #
    #     :param element: SchemaView element definition
    #     :return: slot name or numeric portion of CURIE prefixed
    #     slot_uri
    #     """
    #     if type(element).class_name == "slot_definition":
    #
    #         if self.use_slot_uris:
    #             if element.slot_uri is not None:
    #                 return element.slot_uri.split(":")[1]
    #             else:
    #                 return underscore(element.name)
    #
    #         return underscore(element.name)
    #     else:
    #         return camelcase(element.name)
    #
    # def uri(self, element: Element, expand=True) -> str:
    #     """
    #     Fetches the URI string for the relevant element
    #
    #     :param element:
    #     :return:
    #     """
    #     if isinstance(element, (EnumDefinition, SubsetDefinition)):
    #         # TODO: fix schema view to handle URIs for enums and subsets
    #         return self.name(element)
    #     return self.schemaview.get_uri(element, expand=expand)
    #
    # def uri_link(self, element: Element) -> str:
    #     """
    #     Returns a link string (default: markdown links) for a schema element
    #
    #     :param element:
    #     :return:
    #     """
    #     uri = self.uri(element)
    #     curie = self.uri(element, expand=False)
    #     sc = element.from_schema
    #     return f"[{curie}]({uri})"
    #
    # def inheritance_tree(
    #     self, element: Definition, children: bool = True, **kwargs
    # ) -> str:
    #     """
    #     Show an element in the context of its is-a hierachy
    #
    #     Limitations: currently only implemented for markdown (uses nested bullets)
    #
    #     :param element: slot or class to be shown
    #     :param children: if true, show direct children
    #     :param mixins: if true, show mixins alongside each element
    #     :param kwargs:
    #     :return:
    #     """
    #     s, depth = self._tree(element, focus=element.name, **kwargs)
    #     if children:
    #         for c in self.schemaview.class_children(element.name, mixins=False):
    #             s += self._tree_info(self.schemaview.get_class(c), depth + 1, **kwargs)
    #     return s
    #
    # def _tree(
    #     self,
    #     element: Definition,
    #     mixins=True,
    #     descriptions=False,
    #     focus: DefinitionName = None,
    # ) -> Tuple[str, int]:
    #     sv = self.schemaview
    #     if element.is_a:
    #         pre, depth = self._tree(
    #             sv.get_element(element.is_a),
    #             mixins=mixins,
    #             descriptions=descriptions,
    #             focus=focus,
    #         )
    #         depth += 1
    #     else:
    #         pre, depth = "", 0
    #     s = pre
    #     s += self._tree_info(
    #         element, depth, mixins=mixins, descriptions=descriptions, focus=focus
    #     )
    #     return s, depth
    #
    # def _tree_info(
    #     self,
    #     element: Definition,
    #     depth: int,
    #     mixins=True,
    #     descriptions=False,
    #     focus: DefinitionName = None,
    # ) -> str:
    #     indent = " " * depth * 4
    #     name = self.name(element)
    #     if element.name == focus:
    #         lname = f"**{name}**"
    #     else:
    #         lname = self.link(element)
    #     s = f"{indent}* {lname}"
    #     if mixins and element.mixins:
    #         s += " ["
    #         if element.mixins:
    #             for m in element.mixins:
    #                 s += f" {m}"
    #         s += "]"
    #     s += "\n"
    #     return s
    #
    # def yaml(self, element: Element, inferred=False) -> str:
    #     """
    #     Render element as YAML
    #
    #     :param element:
    #     :param inferred: (classes only) show all induced slots as attributes
    #     :return: yaml string
    #     """
    #     if not inferred:
    #         return yaml_dumper.dumps(element)
    #     else:
    #         if not isinstance(element, ClassDefinition):
    #             raise ValueError(
    #                 f"Inferred only applicable for classes, not {element.name} {type(element)}"
    #             )
    #         # TODO: move this code to schemaview
    #         c = deepcopy(element)
    #         attrs = self.schemaview.class_induced_slots(c.name)
    #         for a in attrs:
    #             c.attributes[a.name] = a
    #         c.slots = []
    #         return yaml_dumper.dumps(c)
    #
    # def all_enum_objects(self) -> Iterator[EnumDefinition]:
    #     """
    #     all enum objects in schema
    #
    #     Ensures rank is non-null
    #     :return: iterator
    #     """
    #     elts = self.schemaview.all_enums().values()
    #     _ensure_ranked(elts)
    #     for e in elts:
    #         yield e
    #
    # def class_hierarchy_as_tuples(self) -> Iterator[Tuple[int, ClassDefinitionName]]:
    #     """
    #     Generate a hierarchical representation of all classes in the schema
    #
    #     This is represented as a list of tuples (depth: int, cls: ClassDefinitionName),
    #     where the order is pre-order depth first traversal
    #
    #     This can then be used to draw a hierarchy within jinja in a number of ways; e.g
    #
    #     - markdown (by using indentation of " " * depth on a list)
    #     - tables (by placing fake indentation e.g using underscores)
    #
    #     Simply iterate through all tuples, drawing each in the appropriate way
    #
    #     Note: By default all classes are ordered alphabetically
    #
    #     :return: tuples (depth: int, cls: ClassDefinitionName)
    #     """
    #     sv = self.schemaview
    #     roots = sv.class_roots(mixins=False)
    #
    #     # by default the classes are sorted alphabetically
    #     roots = sorted(roots, key=str.casefold, reverse=True)
    #
    #     # the stack holds tuples of depth-class that have still to be processed.
    #     # we seed this with all root classes (which have depth 0)
    #     # note the stack is processed from the last element first, ie. LIFO
    #     stack = [(0, root) for root in roots]
    #     # use iterative depth first traversal
    #     while len(stack) > 0:
    #         depth, class_name = stack.pop()
    #         yield depth, class_name
    #         children = sorted(
    #             sv.class_children(class_name=class_name, mixins=False),
    #             key=str.casefold,
    #             reverse=True,
    #         )
    #         for child in children:
    #             # depth first - place at end of stack (to be processed next)
    #             stack.append((depth + 1, child))


# todo: Consider: Which `utils/generator.py.shared_arguments.decorator` to support: --log_level? --verbose?
# @shared_arguments(FhirValueSetGenerator)
@click.option(
    "--outdir",
    "-o",
    required=True,
    help="Path for output directory where files will be stored in",
)
@click.command()
def cli(yamlfile, outdir, format, **args):
    """Generate FHIR ValueSet JSON from a LinkML YAML Enum schema"""
    FhirValueSetGenerator(
        yamlfile,
        outdir=outdir,
        format=format,
        **args,
    )


if __name__ == "__main__":
    cli()
