# Auto generated from meta.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-01-18 15:12
# Schema: metamodel
#
# id: https://w3id.org/linkml/meta
# description: A metamodel for defining biolink related schemas
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
if sys.version_info < (3, 7, 6):
    from linkml.utils.dataclass_extensions_375 import dataclasses_init_fn_with_kwargs
else:
    from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace
from linkml.utils.metamodelcore import Bool, NCName, URI, URIorCURIE, XSDDateTime
from includes.annotations import Annotation
from includes.extensions import Extension
from includes.types import Boolean, Datetime, Integer, Ncname, String, Uri, Uriorcurie

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
OIO = CurieNamespace('OIO', 'http://www.geneontology.org/formats/oboInOwl#')
BIBO = CurieNamespace('bibo', 'http://purl.org/ontology/bibo/')
BIOLINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
META = CurieNamespace('meta', 'https://w3id.org/linkml/meta/')
OSLC = CurieNamespace('oslc', 'http://open-services.net/ns/core#')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = META


# Types

# Class references
class ElementName(extended_str):
    pass


class SchemaDefinitionName(NCName):
    pass


class TypeDefinitionName(ElementName):
    pass


class SubsetDefinitionName(ElementName):
    pass


class DefinitionName(ElementName):
    pass


class EnumDefinitionName(ElementName):
    pass


class SlotDefinitionName(DefinitionName):
    pass


class ClassDefinitionName(DefinitionName):
    pass


class PrefixPrefixPrefix(NCName):
    pass


class LocalNameLocalNameSource(NCName):
    pass


class AltDescriptionSource(extended_str):
    pass


class PermissibleValueText(extended_str):
    pass


@dataclass
class Element(YAMLRoot):
    """
    a named element in the model
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.Element
    class_class_curie: ClassVar[str] = "meta:Element"
    class_name: ClassVar[str] = "element"
    class_model_uri: ClassVar[URIRef] = META.Element

    name: Union[str, ElementName] = None
    id_prefixes: Optional[Union[Union[str, NCName], List[Union[str, NCName]]]] = empty_list()
    definition_uri: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    local_names: Optional[Union[Dict[Union[str, LocalNameLocalNameSource], Union[dict, "LocalName"]], List[Union[dict, "LocalName"]]]] = empty_dict()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    extensions: Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]] = empty_list()
    annotations: Optional[Union[Union[dict, Annotation], List[Union[dict, Annotation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, ElementName):
            self.name = ElementName(self.name)

        if self.id_prefixes is None:
            self.id_prefixes = []
        if not isinstance(self.id_prefixes, list):
            self.id_prefixes = [self.id_prefixes]
        self.id_prefixes = [v if isinstance(v, NCName) else NCName(v) for v in self.id_prefixes]

        if self.definition_uri is not None and not isinstance(self.definition_uri, URIorCURIE):
            self.definition_uri = URIorCURIE(self.definition_uri)

        if self.aliases is None:
            self.aliases = []
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases]
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        if self.local_names is None:
            self.local_names = []
        if not isinstance(self.local_names, (list, dict)):
            self.local_names = [self.local_names]
        self._normalize_inlined_slot(slot_name="local_names", slot_type=LocalName, key_name="local_name_source", inlined_as_list=None, keyed=True)

        if self.mappings is None:
            self.mappings = []
        if not isinstance(self.mappings, list):
            self.mappings = [self.mappings]
        self.mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.mappings]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.alt_descriptions is None:
            self.alt_descriptions = []
        if not isinstance(self.alt_descriptions, (list, dict)):
            self.alt_descriptions = [self.alt_descriptions]
        self._normalize_inlined_slot(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", inlined_as_list=None, keyed=True)

        if self.deprecated is not None and not isinstance(self.deprecated, str):
            self.deprecated = str(self.deprecated)

        if self.todos is None:
            self.todos = []
        if not isinstance(self.todos, list):
            self.todos = [self.todos]
        self.todos = [v if isinstance(v, str) else str(v) for v in self.todos]

        if self.notes is None:
            self.notes = []
        if not isinstance(self.notes, list):
            self.notes = [self.notes]
        self.notes = [v if isinstance(v, str) else str(v) for v in self.notes]

        if self.comments is None:
            self.comments = []
        if not isinstance(self.comments, list):
            self.comments = [self.comments]
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if self.examples is None:
            self.examples = []
        if not isinstance(self.examples, list):
            self.examples = [self.examples]
        self.examples = [v if isinstance(v, Example) else Example(**v) for v in self.examples]

        if self.in_subset is None:
            self.in_subset = []
        if not isinstance(self.in_subset, list):
            self.in_subset = [self.in_subset]
        self.in_subset = [v if isinstance(v, SubsetDefinitionName) else SubsetDefinitionName(v) for v in self.in_subset]

        if self.from_schema is not None and not isinstance(self.from_schema, URI):
            self.from_schema = URI(self.from_schema)

        if self.imported_from is not None and not isinstance(self.imported_from, str):
            self.imported_from = str(self.imported_from)

        if self.see_also is None:
            self.see_also = []
        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also]
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.exact_mappings is None:
            self.exact_mappings = []
        if not isinstance(self.exact_mappings, list):
            self.exact_mappings = [self.exact_mappings]
        self.exact_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.exact_mappings]

        if self.close_mappings is None:
            self.close_mappings = []
        if not isinstance(self.close_mappings, list):
            self.close_mappings = [self.close_mappings]
        self.close_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.close_mappings]

        if self.related_mappings is None:
            self.related_mappings = []
        if not isinstance(self.related_mappings, list):
            self.related_mappings = [self.related_mappings]
        self.related_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.related_mappings]

        if self.narrow_mappings is None:
            self.narrow_mappings = []
        if not isinstance(self.narrow_mappings, list):
            self.narrow_mappings = [self.narrow_mappings]
        self.narrow_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.narrow_mappings]

        if self.broad_mappings is None:
            self.broad_mappings = []
        if not isinstance(self.broad_mappings, list):
            self.broad_mappings = [self.broad_mappings]
        self.broad_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.broad_mappings]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if self.extensions is None:
            self.extensions = []
        if not isinstance(self.extensions, list):
            self.extensions = [self.extensions]
        self._normalize_inlined_slot(slot_name="extensions", slot_type=Extension, key_name="tag", inlined_as_list=True, keyed=False)

        if self.annotations is None:
            self.annotations = []
        if not isinstance(self.annotations, list):
            self.annotations = [self.annotations]
        self._normalize_inlined_slot(slot_name="annotations", slot_type=Annotation, key_name="tag", inlined_as_list=True, keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class SchemaDefinition(Element):
    """
    a collection of subset, type, slot and class definitions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.SchemaDefinition
    class_class_curie: ClassVar[str] = "meta:SchemaDefinition"
    class_name: ClassVar[str] = "schema_definition"
    class_model_uri: ClassVar[URIRef] = META.SchemaDefinition

    name: Union[str, SchemaDefinitionName] = None
    id: Union[str, URI] = None
    title: Optional[str] = None
    version: Optional[str] = None
    imports: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    license: Optional[str] = None
    prefixes: Optional[Union[Dict[Union[str, PrefixPrefixPrefix], Union[dict, "Prefix"]], List[Union[dict, "Prefix"]]]] = empty_dict()
    emit_prefixes: Optional[Union[Union[str, NCName], List[Union[str, NCName]]]] = empty_list()
    default_curi_maps: Optional[Union[str, List[str]]] = empty_list()
    default_prefix: Optional[str] = None
    default_range: Optional[Union[str, TypeDefinitionName]] = None
    subsets: Optional[Union[Dict[Union[str, SubsetDefinitionName], Union[dict, "SubsetDefinition"]], List[Union[dict, "SubsetDefinition"]]]] = empty_dict()
    types: Optional[Union[Dict[Union[str, TypeDefinitionName], Union[dict, "TypeDefinition"]], List[Union[dict, "TypeDefinition"]]]] = empty_dict()
    enums: Optional[Union[Dict[Union[str, EnumDefinitionName], Union[dict, "EnumDefinition"]], List[Union[dict, "EnumDefinition"]]]] = empty_dict()
    slots: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, "SlotDefinition"]], List[Union[dict, "SlotDefinition"]]]] = empty_dict()
    classes: Optional[Union[Dict[Union[str, ClassDefinitionName], Union[dict, "ClassDefinition"]], List[Union[dict, "ClassDefinition"]]]] = empty_dict()
    metamodel_version: Optional[str] = None
    source_file: Optional[str] = None
    source_file_date: Optional[Union[str, XSDDateTime]] = None
    source_file_size: Optional[int] = None
    generation_date: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.default_prefix is None:
            self.default_prefix = sfx(str(self.id))
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, SchemaDefinitionName):
            self.name = SchemaDefinitionName(self.name)

        if self.id is None:
            raise ValueError("id must be supplied")
        if not isinstance(self.id, URI):
            self.id = URI(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.imports is None:
            self.imports = []
        if not isinstance(self.imports, list):
            self.imports = [self.imports]
        self.imports = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.imports]

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.prefixes is None:
            self.prefixes = []
        if not isinstance(self.prefixes, (list, dict)):
            self.prefixes = [self.prefixes]
        self._normalize_inlined_slot(slot_name="prefixes", slot_type=Prefix, key_name="prefix_prefix", inlined_as_list=None, keyed=True)

        if self.emit_prefixes is None:
            self.emit_prefixes = []
        if not isinstance(self.emit_prefixes, list):
            self.emit_prefixes = [self.emit_prefixes]
        self.emit_prefixes = [v if isinstance(v, NCName) else NCName(v) for v in self.emit_prefixes]

        if self.default_curi_maps is None:
            self.default_curi_maps = []
        if not isinstance(self.default_curi_maps, list):
            self.default_curi_maps = [self.default_curi_maps]
        self.default_curi_maps = [v if isinstance(v, str) else str(v) for v in self.default_curi_maps]

        if self.default_prefix is not None and not isinstance(self.default_prefix, str):
            self.default_prefix = str(self.default_prefix)

        if self.default_range is not None and not isinstance(self.default_range, TypeDefinitionName):
            self.default_range = TypeDefinitionName(self.default_range)

        if self.subsets is None:
            self.subsets = []
        if not isinstance(self.subsets, (list, dict)):
            self.subsets = [self.subsets]
        self._normalize_inlined_slot(slot_name="subsets", slot_type=SubsetDefinition, key_name="name", inlined_as_list=None, keyed=True)

        if self.types is None:
            self.types = []
        if not isinstance(self.types, (list, dict)):
            self.types = [self.types]
        self._normalize_inlined_slot(slot_name="types", slot_type=TypeDefinition, key_name="name", inlined_as_list=None, keyed=True)

        if self.enums is None:
            self.enums = []
        if not isinstance(self.enums, (list, dict)):
            self.enums = [self.enums]
        self._normalize_inlined_slot(slot_name="enums", slot_type=EnumDefinition, key_name="name", inlined_as_list=None, keyed=True)

        if self.slots is None:
            self.slots = []
        if not isinstance(self.slots, (list, dict)):
            self.slots = [self.slots]
        self._normalize_inlined_slot(slot_name="slots", slot_type=SlotDefinition, key_name="name", inlined_as_list=None, keyed=True)

        if self.classes is None:
            self.classes = []
        if not isinstance(self.classes, (list, dict)):
            self.classes = [self.classes]
        self._normalize_inlined_slot(slot_name="classes", slot_type=ClassDefinition, key_name="name", inlined_as_list=None, keyed=True)

        if self.metamodel_version is not None and not isinstance(self.metamodel_version, str):
            self.metamodel_version = str(self.metamodel_version)

        if self.source_file is not None and not isinstance(self.source_file, str):
            self.source_file = str(self.source_file)

        if self.source_file_date is not None and not isinstance(self.source_file_date, XSDDateTime):
            self.source_file_date = XSDDateTime(self.source_file_date)

        if self.source_file_size is not None and not isinstance(self.source_file_size, int):
            self.source_file_size = int(self.source_file_size)

        if self.generation_date is not None and not isinstance(self.generation_date, XSDDateTime):
            self.generation_date = XSDDateTime(self.generation_date)

        super().__post_init__(**kwargs)


@dataclass
class TypeDefinition(Element):
    """
    A data type definition.
    """
    _inherited_slots: ClassVar[List[str]] = ["base", "uri", "repr"]

    class_class_uri: ClassVar[URIRef] = META.TypeDefinition
    class_class_curie: ClassVar[str] = "meta:TypeDefinition"
    class_name: ClassVar[str] = "type_definition"
    class_model_uri: ClassVar[URIRef] = META.TypeDefinition

    name: Union[str, TypeDefinitionName] = None
    typeof: Optional[Union[str, TypeDefinitionName]] = None
    base: Optional[str] = None
    uri: Optional[Union[str, URIorCURIE]] = None
    repr: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, TypeDefinitionName):
            self.name = TypeDefinitionName(self.name)

        if self.typeof is not None and not isinstance(self.typeof, TypeDefinitionName):
            self.typeof = TypeDefinitionName(self.typeof)

        if self.base is not None and not isinstance(self.base, str):
            self.base = str(self.base)

        if self.uri is not None and not isinstance(self.uri, URIorCURIE):
            self.uri = URIorCURIE(self.uri)

        if self.repr is not None and not isinstance(self.repr, str):
            self.repr = str(self.repr)

        super().__post_init__(**kwargs)


@dataclass
class SubsetDefinition(Element):
    """
    the name and description of a subset
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.SubsetDefinition
    class_class_curie: ClassVar[str] = "meta:SubsetDefinition"
    class_name: ClassVar[str] = "subset_definition"
    class_model_uri: ClassVar[URIRef] = META.SubsetDefinition

    name: Union[str, SubsetDefinitionName] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, SubsetDefinitionName):
            self.name = SubsetDefinitionName(self.name)

        super().__post_init__(**kwargs)


@dataclass
class Definition(Element):
    """
    base class for definitions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.Definition
    class_class_curie: ClassVar[str] = "meta:Definition"
    class_name: ClassVar[str] = "definition"
    class_model_uri: ClassVar[URIRef] = META.Definition

    name: Union[str, DefinitionName] = None
    is_a: Optional[Union[str, DefinitionName]] = None
    abstract: Optional[Union[bool, Bool]] = None
    mixin: Optional[Union[bool, Bool]] = None
    mixins: Optional[Union[Union[str, DefinitionName], List[Union[str, DefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, DefinitionName], List[Union[str, DefinitionName]]]] = empty_list()
    values_from: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.is_a is not None and not isinstance(self.is_a, DefinitionName):
            self.is_a = DefinitionName(self.is_a)

        if self.abstract is not None and not isinstance(self.abstract, Bool):
            self.abstract = Bool(self.abstract)

        if self.mixin is not None and not isinstance(self.mixin, Bool):
            self.mixin = Bool(self.mixin)

        if self.mixins is None:
            self.mixins = []
        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins]
        self.mixins = [v if isinstance(v, DefinitionName) else DefinitionName(v) for v in self.mixins]

        if self.apply_to is None:
            self.apply_to = []
        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to]
        self.apply_to = [v if isinstance(v, DefinitionName) else DefinitionName(v) for v in self.apply_to]

        if self.values_from is None:
            self.values_from = []
        if not isinstance(self.values_from, list):
            self.values_from = [self.values_from]
        self.values_from = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.values_from]

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        super().__post_init__(**kwargs)


@dataclass
class EnumDefinition(Element):
    """
    List of values that constrain the range of a slot
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.EnumDefinition
    class_class_curie: ClassVar[str] = "meta:EnumDefinition"
    class_name: ClassVar[str] = "enum_definition"
    class_model_uri: ClassVar[URIRef] = META.EnumDefinition

    name: Union[str, EnumDefinitionName] = None
    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[Dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], List[Union[dict, "PermissibleValue"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, EnumDefinitionName):
            self.name = EnumDefinitionName(self.name)

        if self.code_set is not None and not isinstance(self.code_set, URIorCURIE):
            self.code_set = URIorCURIE(self.code_set)

        if self.code_set_tag is not None and not isinstance(self.code_set_tag, str):
            self.code_set_tag = str(self.code_set_tag)

        if self.code_set_version is not None and not isinstance(self.code_set_version, str):
            self.code_set_version = str(self.code_set_version)

        if self.pv_formula is not None and not isinstance(self.pv_formula, PvFormulaOptions):
            self.pv_formula = PvFormulaOptions(self.pv_formula)

        if self.permissible_values is None:
            self.permissible_values = []
        if not isinstance(self.permissible_values, (list, dict)):
            self.permissible_values = [self.permissible_values]
        self._normalize_inlined_slot(slot_name="permissible_values", slot_type=PermissibleValue, key_name="text", inlined_as_list=None, keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class SlotDefinition(Definition):
    """
    the definition of a property or a slot
    """
    _inherited_slots: ClassVar[List[str]] = ["domain", "range", "multivalued", "inherited", "readonly", "ifabsent", "required", "inlined", "inlined_as_list", "key", "identifier", "role", "minimum_value", "maximum_value", "pattern"]

    class_class_uri: ClassVar[URIRef] = META.SlotDefinition
    class_class_curie: ClassVar[str] = "meta:SlotDefinition"
    class_name: ClassVar[str] = "slot_definition"
    class_model_uri: ClassVar[URIRef] = META.SlotDefinition

    name: Union[str, SlotDefinitionName] = None
    singular_name: Optional[str] = None
    domain: Optional[Union[str, ClassDefinitionName]] = None
    range: Optional[Union[str, ElementName]] = None
    slot_uri: Optional[Union[str, URIorCURIE]] = None
    multivalued: Optional[Union[bool, Bool]] = None
    inherited: Optional[Union[bool, Bool]] = None
    readonly: Optional[str] = None
    ifabsent: Optional[str] = None
    required: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    key: Optional[Union[bool, Bool]] = None
    identifier: Optional[Union[bool, Bool]] = None
    alias: Optional[str] = None
    owner: Optional[Union[str, DefinitionName]] = None
    domain_of: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()
    subproperty_of: Optional[Union[str, SlotDefinitionName]] = None
    symmetric: Optional[Union[bool, Bool]] = None
    inverse: Optional[Union[str, SlotDefinitionName]] = None
    is_class_field: Optional[Union[bool, Bool]] = None
    role: Optional[str] = None
    is_usage_slot: Optional[Union[bool, Bool]] = None
    usage_slot_name: Optional[str] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    pattern: Optional[str] = None
    string_serialization: Optional[str] = None
    is_a: Optional[Union[str, SlotDefinitionName]] = None
    mixins: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, SlotDefinitionName):
            self.name = SlotDefinitionName(self.name)

        if self.singular_name is not None and not isinstance(self.singular_name, str):
            self.singular_name = str(self.singular_name)

        if self.domain is not None and not isinstance(self.domain, ClassDefinitionName):
            self.domain = ClassDefinitionName(self.domain)

        if self.range is not None and not isinstance(self.range, ElementName):
            self.range = ElementName(self.range)

        if self.slot_uri is not None and not isinstance(self.slot_uri, URIorCURIE):
            self.slot_uri = URIorCURIE(self.slot_uri)

        if self.multivalued is not None and not isinstance(self.multivalued, Bool):
            self.multivalued = Bool(self.multivalued)

        if self.inherited is not None and not isinstance(self.inherited, Bool):
            self.inherited = Bool(self.inherited)

        if self.readonly is not None and not isinstance(self.readonly, str):
            self.readonly = str(self.readonly)

        if self.ifabsent is not None and not isinstance(self.ifabsent, str):
            self.ifabsent = str(self.ifabsent)

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.key is not None and not isinstance(self.key, Bool):
            self.key = Bool(self.key)

        if self.identifier is not None and not isinstance(self.identifier, Bool):
            self.identifier = Bool(self.identifier)

        if self.alias is not None and not isinstance(self.alias, str):
            self.alias = str(self.alias)

        if self.owner is not None and not isinstance(self.owner, DefinitionName):
            self.owner = DefinitionName(self.owner)

        if self.domain_of is None:
            self.domain_of = []
        if not isinstance(self.domain_of, list):
            self.domain_of = [self.domain_of]
        self.domain_of = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.domain_of]

        if self.subproperty_of is not None and not isinstance(self.subproperty_of, SlotDefinitionName):
            self.subproperty_of = SlotDefinitionName(self.subproperty_of)

        if self.symmetric is not None and not isinstance(self.symmetric, Bool):
            self.symmetric = Bool(self.symmetric)

        if self.inverse is not None and not isinstance(self.inverse, SlotDefinitionName):
            self.inverse = SlotDefinitionName(self.inverse)

        if self.is_class_field is not None and not isinstance(self.is_class_field, Bool):
            self.is_class_field = Bool(self.is_class_field)

        if self.role is not None and not isinstance(self.role, str):
            self.role = str(self.role)

        if self.is_usage_slot is not None and not isinstance(self.is_usage_slot, Bool):
            self.is_usage_slot = Bool(self.is_usage_slot)

        if self.usage_slot_name is not None and not isinstance(self.usage_slot_name, str):
            self.usage_slot_name = str(self.usage_slot_name)

        if self.minimum_value is not None and not isinstance(self.minimum_value, int):
            self.minimum_value = int(self.minimum_value)

        if self.maximum_value is not None and not isinstance(self.maximum_value, int):
            self.maximum_value = int(self.maximum_value)

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.string_serialization is not None and not isinstance(self.string_serialization, str):
            self.string_serialization = str(self.string_serialization)

        if self.is_a is not None and not isinstance(self.is_a, SlotDefinitionName):
            self.is_a = SlotDefinitionName(self.is_a)

        if self.mixins is None:
            self.mixins = []
        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins]
        self.mixins = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.mixins]

        if self.apply_to is None:
            self.apply_to = []
        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to]
        self.apply_to = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.apply_to]

        super().__post_init__(**kwargs)


@dataclass
class ClassDefinition(Definition):
    """
    the definition of a class or interface
    """
    _inherited_slots: ClassVar[List[str]] = ["defining_slots"]

    class_class_uri: ClassVar[URIRef] = META.ClassDefinition
    class_class_curie: ClassVar[str] = "meta:ClassDefinition"
    class_name: ClassVar[str] = "class_definition"
    class_model_uri: ClassVar[URIRef] = META.ClassDefinition

    name: Union[str, ClassDefinitionName] = None
    slots: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()
    slot_usage: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], List[Union[dict, SlotDefinition]]]] = empty_dict()
    attributes: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], List[Union[dict, SlotDefinition]]]] = empty_dict()
    class_uri: Optional[Union[str, URIorCURIE]] = None
    subclass_of: Optional[Union[str, URIorCURIE]] = None
    union_of: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()
    defining_slots: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()
    tree_root: Optional[Union[bool, Bool]] = None
    is_a: Optional[Union[str, ClassDefinitionName]] = None
    mixins: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, ClassDefinitionName):
            self.name = ClassDefinitionName(self.name)

        if self.slots is None:
            self.slots = []
        if not isinstance(self.slots, list):
            self.slots = [self.slots]
        self.slots = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.slots]

        if self.slot_usage is None:
            self.slot_usage = []
        if not isinstance(self.slot_usage, (list, dict)):
            self.slot_usage = [self.slot_usage]
        self._normalize_inlined_slot(slot_name="slot_usage", slot_type=SlotDefinition, key_name="name", inlined_as_list=None, keyed=True)

        if self.attributes is None:
            self.attributes = []
        if not isinstance(self.attributes, (list, dict)):
            self.attributes = [self.attributes]
        self._normalize_inlined_slot(slot_name="attributes", slot_type=SlotDefinition, key_name="name", inlined_as_list=None, keyed=True)

        if self.class_uri is not None and not isinstance(self.class_uri, URIorCURIE):
            self.class_uri = URIorCURIE(self.class_uri)

        if self.subclass_of is not None and not isinstance(self.subclass_of, URIorCURIE):
            self.subclass_of = URIorCURIE(self.subclass_of)

        if self.union_of is None:
            self.union_of = []
        if not isinstance(self.union_of, list):
            self.union_of = [self.union_of]
        self.union_of = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.union_of]

        if self.defining_slots is None:
            self.defining_slots = []
        if not isinstance(self.defining_slots, list):
            self.defining_slots = [self.defining_slots]
        self.defining_slots = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.defining_slots]

        if self.tree_root is not None and not isinstance(self.tree_root, Bool):
            self.tree_root = Bool(self.tree_root)

        if self.is_a is not None and not isinstance(self.is_a, ClassDefinitionName):
            self.is_a = ClassDefinitionName(self.is_a)

        if self.mixins is None:
            self.mixins = []
        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins]
        self.mixins = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.mixins]

        if self.apply_to is None:
            self.apply_to = []
        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to]
        self.apply_to = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.apply_to]

        super().__post_init__(**kwargs)


@dataclass
class Prefix(YAMLRoot):
    """
    prefix URI tuple
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.Prefix
    class_class_curie: ClassVar[str] = "meta:Prefix"
    class_name: ClassVar[str] = "prefix"
    class_model_uri: ClassVar[URIRef] = META.Prefix

    prefix_prefix: Union[str, PrefixPrefixPrefix] = None
    prefix_reference: Union[str, URI] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.prefix_prefix is None:
            raise ValueError("prefix_prefix must be supplied")
        if not isinstance(self.prefix_prefix, PrefixPrefixPrefix):
            self.prefix_prefix = PrefixPrefixPrefix(self.prefix_prefix)

        if self.prefix_reference is None:
            raise ValueError("prefix_reference must be supplied")
        if not isinstance(self.prefix_reference, URI):
            self.prefix_reference = URI(self.prefix_reference)

        super().__post_init__(**kwargs)


@dataclass
class LocalName(YAMLRoot):
    """
    an attributed label
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.LocalName
    class_class_curie: ClassVar[str] = "meta:LocalName"
    class_name: ClassVar[str] = "local_name"
    class_model_uri: ClassVar[URIRef] = META.LocalName

    local_name_source: Union[str, LocalNameLocalNameSource] = None
    local_name_value: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.local_name_source is None:
            raise ValueError("local_name_source must be supplied")
        if not isinstance(self.local_name_source, LocalNameLocalNameSource):
            self.local_name_source = LocalNameLocalNameSource(self.local_name_source)

        if self.local_name_value is None:
            raise ValueError("local_name_value must be supplied")
        if not isinstance(self.local_name_value, str):
            self.local_name_value = str(self.local_name_value)

        super().__post_init__(**kwargs)


@dataclass
class Example(YAMLRoot):
    """
    usage example and description
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.Example
    class_class_curie: ClassVar[str] = "meta:Example"
    class_name: ClassVar[str] = "example"
    class_model_uri: ClassVar[URIRef] = META.Example

    value: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class AltDescription(YAMLRoot):
    """
    an attributed description
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.AltDescription
    class_class_curie: ClassVar[str] = "meta:AltDescription"
    class_name: ClassVar[str] = "alt_description"
    class_model_uri: ClassVar[URIRef] = META.AltDescription

    source: Union[str, AltDescriptionSource] = None
    description: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.source is None:
            raise ValueError("source must be supplied")
        if not isinstance(self.source, AltDescriptionSource):
            self.source = AltDescriptionSource(self.source)

        if self.description is None:
            raise ValueError("description must be supplied")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class PermissibleValue(YAMLRoot):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = META.PermissibleValue
    class_class_curie: ClassVar[str] = "meta:PermissibleValue"
    class_name: ClassVar[str] = "permissible_value"
    class_model_uri: ClassVar[URIRef] = META.PermissibleValue

    text: Union[str, PermissibleValueText] = None
    description: Optional[str] = None
    meaning: Optional[Union[str, URIorCURIE]] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, AltDescription]], List[Union[dict, AltDescription]]]] = empty_dict()
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, Example], List[Union[dict, Example]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    is_a: Optional[Union[str, PermissibleValueText]] = None
    mixins: Optional[Union[Union[str, PermissibleValueText], List[Union[str, PermissibleValueText]]]] = empty_list()
    extensions: Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]] = empty_list()
    annotations: Optional[Union[Union[dict, Annotation], List[Union[dict, Annotation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.text is None:
            raise ValueError("text must be supplied")
        if not isinstance(self.text, PermissibleValueText):
            self.text = PermissibleValueText(self.text)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.meaning is not None and not isinstance(self.meaning, URIorCURIE):
            self.meaning = URIorCURIE(self.meaning)

        if self.alt_descriptions is None:
            self.alt_descriptions = []
        if not isinstance(self.alt_descriptions, (list, dict)):
            self.alt_descriptions = [self.alt_descriptions]
        self._normalize_inlined_slot(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", inlined_as_list=None, keyed=True)

        if self.deprecated is not None and not isinstance(self.deprecated, str):
            self.deprecated = str(self.deprecated)

        if self.todos is None:
            self.todos = []
        if not isinstance(self.todos, list):
            self.todos = [self.todos]
        self.todos = [v if isinstance(v, str) else str(v) for v in self.todos]

        if self.notes is None:
            self.notes = []
        if not isinstance(self.notes, list):
            self.notes = [self.notes]
        self.notes = [v if isinstance(v, str) else str(v) for v in self.notes]

        if self.comments is None:
            self.comments = []
        if not isinstance(self.comments, list):
            self.comments = [self.comments]
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if self.examples is None:
            self.examples = []
        if not isinstance(self.examples, list):
            self.examples = [self.examples]
        self.examples = [v if isinstance(v, Example) else Example(**v) for v in self.examples]

        if self.in_subset is None:
            self.in_subset = []
        if not isinstance(self.in_subset, list):
            self.in_subset = [self.in_subset]
        self.in_subset = [v if isinstance(v, SubsetDefinitionName) else SubsetDefinitionName(v) for v in self.in_subset]

        if self.from_schema is not None and not isinstance(self.from_schema, URI):
            self.from_schema = URI(self.from_schema)

        if self.imported_from is not None and not isinstance(self.imported_from, str):
            self.imported_from = str(self.imported_from)

        if self.see_also is None:
            self.see_also = []
        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also]
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if self.is_a is not None and not isinstance(self.is_a, PermissibleValueText):
            self.is_a = PermissibleValueText(self.is_a)

        if self.mixins is None:
            self.mixins = []
        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins]
        self.mixins = [v if isinstance(v, PermissibleValueText) else PermissibleValueText(v) for v in self.mixins]

        if self.extensions is None:
            self.extensions = []
        if not isinstance(self.extensions, list):
            self.extensions = [self.extensions]
        self._normalize_inlined_slot(slot_name="extensions", slot_type=Extension, key_name="tag", inlined_as_list=True, keyed=False)

        if self.annotations is None:
            self.annotations = []
        if not isinstance(self.annotations, list):
            self.annotations = [self.annotations]
        self._normalize_inlined_slot(slot_name="annotations", slot_type=Annotation, key_name="tag", inlined_as_list=True, keyed=False)

        super().__post_init__(**kwargs)


# Enumerations
class PvFormulaOptions(EnumDefinitionImpl):
    """
    The formula used to generate the set of permissible values from the code_set values
    """
    CODE = PermissibleValue(text="CODE",
                               description="The permissible values are the set of possible codes in the code set")
    CURIE = PermissibleValue(text="CURIE",
                                 description="The permissible values are the set of CURIES in the code set")
    URI = PermissibleValue(text="URI",
                             description="The permissible values are the set of code URIs in the code set")
    FHIR_CODING = PermissibleValue(text="FHIR_CODING",
                                             description="The permissible values are the set of FHIR coding elements derived from the code set")

    _defn = EnumDefinition(
        name="PvFormulaOptions",
        description="The formula used to generate the set of permissible values from the code_set values",
    )

# Slots
class slots:
    pass

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=META.name, domain=Element, range=Union[str, ElementName], mappings = [SCHEMA.name])

slots.definition_uri = Slot(uri=META.definition_uri, name="definition_uri", curie=META.curie('definition_uri'),
                   model_uri=META.definition_uri, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.id_prefixes = Slot(uri=META.id_prefixes, name="id_prefixes", curie=META.curie('id_prefixes'),
                   model_uri=META.id_prefixes, domain=Element, range=Optional[Union[Union[str, NCName], List[Union[str, NCName]]]])

slots.description = Slot(uri=SKOS.definition, name="description", curie=SKOS.curie('definition'),
                   model_uri=META.description, domain=Element, range=Optional[str])

slots.aliases = Slot(uri=SKOS.altLabel, name="aliases", curie=SKOS.curie('altLabel'),
                   model_uri=META.aliases, domain=Element, range=Optional[Union[str, List[str]]])

slots.deprecated = Slot(uri=META.deprecated, name="deprecated", curie=META.curie('deprecated'),
                   model_uri=META.deprecated, domain=Element, range=Optional[str])

slots.todos = Slot(uri=META.todos, name="todos", curie=META.curie('todos'),
                   model_uri=META.todos, domain=Element, range=Optional[Union[str, List[str]]])

slots.notes = Slot(uri=SKOS.editorialNote, name="notes", curie=SKOS.curie('editorialNote'),
                   model_uri=META.notes, domain=Element, range=Optional[Union[str, List[str]]])

slots.comments = Slot(uri=SKOS.note, name="comments", curie=SKOS.curie('note'),
                   model_uri=META.comments, domain=Element, range=Optional[Union[str, List[str]]])

slots.in_subset = Slot(uri=OIO.inSubset, name="in_subset", curie=OIO.curie('inSubset'),
                   model_uri=META.in_subset, domain=Element, range=Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]])

slots.from_schema = Slot(uri=SKOS.inScheme, name="from_schema", curie=SKOS.curie('inScheme'),
                   model_uri=META.from_schema, domain=Element, range=Optional[Union[str, URI]])

slots.imported_from = Slot(uri=META.imported_from, name="imported_from", curie=META.curie('imported_from'),
                   model_uri=META.imported_from, domain=Element, range=Optional[str])

slots.see_also = Slot(uri=RDFS.seeAlso, name="see_also", curie=RDFS.curie('seeAlso'),
                   model_uri=META.see_also, domain=Element, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.created_by = Slot(uri=PAV.createdBy, name="created_by", curie=PAV.curie('createdBy'),
                   model_uri=META.created_by, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.created_on = Slot(uri=PAV.createdOn, name="created_on", curie=PAV.curie('createdOn'),
                   model_uri=META.created_on, domain=Element, range=Optional[Union[str, XSDDateTime]])

slots.last_updated_on = Slot(uri=PAV.lastUpdatedOn, name="last_updated_on", curie=PAV.curie('lastUpdatedOn'),
                   model_uri=META.last_updated_on, domain=Element, range=Optional[Union[str, XSDDateTime]])

slots.modified_by = Slot(uri=OSLC.modifiedBy, name="modified_by", curie=OSLC.curie('modifiedBy'),
                   model_uri=META.modified_by, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.status = Slot(uri=BIBO.status, name="status", curie=BIBO.curie('status'),
                   model_uri=META.status, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.is_a = Slot(uri=META.is_a, name="is_a", curie=META.curie('is_a'),
                   model_uri=META.is_a, domain=Definition, range=Optional[Union[str, DefinitionName]])

slots.abstract = Slot(uri=META.abstract, name="abstract", curie=META.curie('abstract'),
                   model_uri=META.abstract, domain=Definition, range=Optional[Union[bool, Bool]])

slots.mixin = Slot(uri=META.mixin, name="mixin", curie=META.curie('mixin'),
                   model_uri=META.mixin, domain=Definition, range=Optional[Union[bool, Bool]])

slots.mixins = Slot(uri=META.mixins, name="mixins", curie=META.curie('mixins'),
                   model_uri=META.mixins, domain=Definition, range=Optional[Union[Union[str, DefinitionName], List[Union[str, DefinitionName]]]])

slots.apply_to = Slot(uri=META.apply_to, name="apply_to", curie=META.curie('apply_to'),
                   model_uri=META.apply_to, domain=Definition, range=Optional[Union[Union[str, DefinitionName], List[Union[str, DefinitionName]]]])

slots.values_from = Slot(uri=META.values_from, name="values_from", curie=META.curie('values_from'),
                   model_uri=META.values_from, domain=Definition, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.code_set = Slot(uri=META.code_set, name="code_set", curie=META.curie('code_set'),
                   model_uri=META.code_set, domain=EnumDefinition, range=Optional[Union[str, URIorCURIE]])

slots.code_set_version = Slot(uri=META.code_set_version, name="code_set_version", curie=META.curie('code_set_version'),
                   model_uri=META.code_set_version, domain=EnumDefinition, range=Optional[str])

slots.code_set_tag = Slot(uri=META.code_set_tag, name="code_set_tag", curie=META.curie('code_set_tag'),
                   model_uri=META.code_set_tag, domain=EnumDefinition, range=Optional[str])

slots.pv_formula = Slot(uri=META.pv_formula, name="pv_formula", curie=META.curie('pv_formula'),
                   model_uri=META.pv_formula, domain=EnumDefinition, range=Optional[Union[str, "PvFormulaOptions"]])

slots.permissible_values = Slot(uri=META.permissible_values, name="permissible_values", curie=META.curie('permissible_values'),
                   model_uri=META.permissible_values, domain=EnumDefinition, range=Optional[Union[Dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], List[Union[dict, "PermissibleValue"]]]])

slots.text = Slot(uri=META.text, name="text", curie=META.curie('text'),
                   model_uri=META.text, domain=PermissibleValue, range=Union[str, PermissibleValueText])

slots.meaning = Slot(uri=META.meaning, name="meaning", curie=META.curie('meaning'),
                   model_uri=META.meaning, domain=PermissibleValue, range=Optional[Union[str, URIorCURIE]])

slots.id = Slot(uri=META.id, name="id", curie=META.curie('id'),
                   model_uri=META.id, domain=SchemaDefinition, range=Union[str, URI])

slots.emit_prefixes = Slot(uri=META.emit_prefixes, name="emit_prefixes", curie=META.curie('emit_prefixes'),
                   model_uri=META.emit_prefixes, domain=SchemaDefinition, range=Optional[Union[Union[str, NCName], List[Union[str, NCName]]]])

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=META.title, domain=SchemaDefinition, range=Optional[str])

slots.version = Slot(uri=PAV.version, name="version", curie=PAV.curie('version'),
                   model_uri=META.version, domain=SchemaDefinition, range=Optional[str], mappings = [SCHEMA.schemaVersion])

slots.imports = Slot(uri=META.imports, name="imports", curie=META.curie('imports'),
                   model_uri=META.imports, domain=SchemaDefinition, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.license = Slot(uri=DCTERMS.license, name="license", curie=DCTERMS.curie('license'),
                   model_uri=META.license, domain=SchemaDefinition, range=Optional[str])

slots.default_curi_maps = Slot(uri=META.default_curi_maps, name="default_curi_maps", curie=META.curie('default_curi_maps'),
                   model_uri=META.default_curi_maps, domain=SchemaDefinition, range=Optional[Union[str, List[str]]])

slots.default_prefix = Slot(uri=META.default_prefix, name="default_prefix", curie=META.curie('default_prefix'),
                   model_uri=META.default_prefix, domain=SchemaDefinition, range=Optional[str])

slots.default_range = Slot(uri=META.default_range, name="default_range", curie=META.curie('default_range'),
                   model_uri=META.default_range, domain=SchemaDefinition, range=Optional[Union[str, TypeDefinitionName]])

slots.subsets = Slot(uri=META.subsets, name="subsets", curie=META.curie('subsets'),
                   model_uri=META.subsets, domain=SchemaDefinition, range=Optional[Union[Dict[Union[str, SubsetDefinitionName], Union[dict, "SubsetDefinition"]], List[Union[dict, "SubsetDefinition"]]]])

slots.types = Slot(uri=META.types, name="types", curie=META.curie('types'),
                   model_uri=META.types, domain=SchemaDefinition, range=Optional[Union[Dict[Union[str, TypeDefinitionName], Union[dict, "TypeDefinition"]], List[Union[dict, "TypeDefinition"]]]])

slots.enums = Slot(uri=META.enums, name="enums", curie=META.curie('enums'),
                   model_uri=META.enums, domain=SchemaDefinition, range=Optional[Union[Dict[Union[str, EnumDefinitionName], Union[dict, "EnumDefinition"]], List[Union[dict, "EnumDefinition"]]]])

slots.slot_definitions = Slot(uri=META.slots, name="slot_definitions", curie=META.curie('slots'),
                   model_uri=META.slot_definitions, domain=SchemaDefinition, range=Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, "SlotDefinition"]], List[Union[dict, "SlotDefinition"]]]])

slots.classes = Slot(uri=META.classes, name="classes", curie=META.curie('classes'),
                   model_uri=META.classes, domain=SchemaDefinition, range=Optional[Union[Dict[Union[str, ClassDefinitionName], Union[dict, "ClassDefinition"]], List[Union[dict, "ClassDefinition"]]]])

slots.metamodel_version = Slot(uri=META.metamodel_version, name="metamodel_version", curie=META.curie('metamodel_version'),
                   model_uri=META.metamodel_version, domain=SchemaDefinition, range=Optional[str])

slots.source_file = Slot(uri=META.source_file, name="source_file", curie=META.curie('source_file'),
                   model_uri=META.source_file, domain=SchemaDefinition, range=Optional[str])

slots.source_file_date = Slot(uri=META.source_file_date, name="source_file_date", curie=META.curie('source_file_date'),
                   model_uri=META.source_file_date, domain=SchemaDefinition, range=Optional[Union[str, XSDDateTime]])

slots.source_file_size = Slot(uri=META.source_file_size, name="source_file_size", curie=META.curie('source_file_size'),
                   model_uri=META.source_file_size, domain=SchemaDefinition, range=Optional[int])

slots.generation_date = Slot(uri=META.generation_date, name="generation_date", curie=META.curie('generation_date'),
                   model_uri=META.generation_date, domain=SchemaDefinition, range=Optional[Union[str, XSDDateTime]])

slots.slots = Slot(uri=META.slots, name="slots", curie=META.curie('slots'),
                   model_uri=META.slots, domain=ClassDefinition, range=Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]])

slots.slot_usage = Slot(uri=META.slot_usage, name="slot_usage", curie=META.curie('slot_usage'),
                   model_uri=META.slot_usage, domain=ClassDefinition, range=Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], List[Union[dict, SlotDefinition]]]])

slots.attributes = Slot(uri=META.attributes, name="attributes", curie=META.curie('attributes'),
                   model_uri=META.attributes, domain=ClassDefinition, range=Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], List[Union[dict, SlotDefinition]]]])

slots.class_uri = Slot(uri=META.class_uri, name="class_uri", curie=META.curie('class_uri'),
                   model_uri=META.class_uri, domain=ClassDefinition, range=Optional[Union[str, URIorCURIE]])

slots.subclass_of = Slot(uri=RDFS.subClassOf, name="subclass_of", curie=RDFS.curie('subClassOf'),
                   model_uri=META.subclass_of, domain=ClassDefinition, range=Optional[Union[str, URIorCURIE]])

slots.defining_slots = Slot(uri=META.defining_slots, name="defining_slots", curie=META.curie('defining_slots'),
                   model_uri=META.defining_slots, domain=ClassDefinition, range=Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]])

slots.union_of = Slot(uri=META.union_of, name="union_of", curie=META.curie('union_of'),
                   model_uri=META.union_of, domain=ClassDefinition, range=Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]])

slots.tree_root = Slot(uri=META.tree_root, name="tree_root", curie=META.curie('tree_root'),
                   model_uri=META.tree_root, domain=ClassDefinition, range=Optional[Union[bool, Bool]])

slots.domain = Slot(uri=META.domain, name="domain", curie=META.curie('domain'),
                   model_uri=META.domain, domain=SlotDefinition, range=Optional[Union[str, ClassDefinitionName]])

slots.range = Slot(uri=META.range, name="range", curie=META.curie('range'),
                   model_uri=META.range, domain=SlotDefinition, range=Optional[Union[str, ElementName]])

slots.slot_uri = Slot(uri=META.slot_uri, name="slot_uri", curie=META.curie('slot_uri'),
                   model_uri=META.slot_uri, domain=SlotDefinition, range=Optional[Union[str, URIorCURIE]])

slots.multivalued = Slot(uri=META.multivalued, name="multivalued", curie=META.curie('multivalued'),
                   model_uri=META.multivalued, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inherited = Slot(uri=META.inherited, name="inherited", curie=META.curie('inherited'),
                   model_uri=META.inherited, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.readonly = Slot(uri=META.readonly, name="readonly", curie=META.curie('readonly'),
                   model_uri=META.readonly, domain=SlotDefinition, range=Optional[str])

slots.ifabsent = Slot(uri=META.ifabsent, name="ifabsent", curie=META.curie('ifabsent'),
                   model_uri=META.ifabsent, domain=SlotDefinition, range=Optional[str])

slots.singular_name = Slot(uri=SKOS.altLabel, name="singular_name", curie=SKOS.curie('altLabel'),
                   model_uri=META.singular_name, domain=SlotDefinition, range=Optional[str])

slots.required = Slot(uri=META.required, name="required", curie=META.curie('required'),
                   model_uri=META.required, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inlined = Slot(uri=META.inlined, name="inlined", curie=META.curie('inlined'),
                   model_uri=META.inlined, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inlined_as_list = Slot(uri=META.inlined_as_list, name="inlined_as_list", curie=META.curie('inlined_as_list'),
                   model_uri=META.inlined_as_list, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.key = Slot(uri=META.key, name="key", curie=META.curie('key'),
                   model_uri=META.key, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.identifier = Slot(uri=META.identifier, name="identifier", curie=META.curie('identifier'),
                   model_uri=META.identifier, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.alias = Slot(uri=META.alias, name="alias", curie=META.curie('alias'),
                   model_uri=META.alias, domain=SlotDefinition, range=Optional[str])

slots.owner = Slot(uri=META.owner, name="owner", curie=META.curie('owner'),
                   model_uri=META.owner, domain=SlotDefinition, range=Optional[Union[str, DefinitionName]])

slots.domain_of = Slot(uri=META.domain_of, name="domain_of", curie=META.curie('domain_of'),
                   model_uri=META.domain_of, domain=SlotDefinition, range=Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]])

slots.is_usage_slot = Slot(uri=META.is_usage_slot, name="is_usage_slot", curie=META.curie('is_usage_slot'),
                   model_uri=META.is_usage_slot, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.usage_slot_name = Slot(uri=META.usage_slot_name, name="usage_slot_name", curie=META.curie('usage_slot_name'),
                   model_uri=META.usage_slot_name, domain=SlotDefinition, range=Optional[str])

slots.subproperty_of = Slot(uri=RDFS.subPropertyOf, name="subproperty_of", curie=RDFS.curie('subPropertyOf'),
                   model_uri=META.subproperty_of, domain=SlotDefinition, range=Optional[Union[str, SlotDefinitionName]])

slots.symmetric = Slot(uri=META.symmetric, name="symmetric", curie=META.curie('symmetric'),
                   model_uri=META.symmetric, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inverse = Slot(uri=OWL.inverseOf, name="inverse", curie=OWL.curie('inverseOf'),
                   model_uri=META.inverse, domain=SlotDefinition, range=Optional[Union[str, SlotDefinitionName]])

slots.is_class_field = Slot(uri=META.is_class_field, name="is_class_field", curie=META.curie('is_class_field'),
                   model_uri=META.is_class_field, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.role = Slot(uri=META.role, name="role", curie=META.curie('role'),
                   model_uri=META.role, domain=SlotDefinition, range=Optional[str])

slots.minimum_value = Slot(uri=META.minimum_value, name="minimum_value", curie=META.curie('minimum_value'),
                   model_uri=META.minimum_value, domain=SlotDefinition, range=Optional[int])

slots.maximum_value = Slot(uri=META.maximum_value, name="maximum_value", curie=META.curie('maximum_value'),
                   model_uri=META.maximum_value, domain=SlotDefinition, range=Optional[int])

slots.pattern = Slot(uri=META.pattern, name="pattern", curie=META.curie('pattern'),
                   model_uri=META.pattern, domain=SlotDefinition, range=Optional[str])

slots.string_serialization = Slot(uri=META.string_serialization, name="string_serialization", curie=META.curie('string_serialization'),
                   model_uri=META.string_serialization, domain=SlotDefinition, range=Optional[str])

slots.typeof = Slot(uri=META.typeof, name="typeof", curie=META.curie('typeof'),
                   model_uri=META.typeof, domain=TypeDefinition, range=Optional[Union[str, TypeDefinitionName]])

slots.base = Slot(uri=META.base, name="base", curie=META.curie('base'),
                   model_uri=META.base, domain=TypeDefinition, range=Optional[str])

slots.type_uri = Slot(uri=META.uri, name="type_uri", curie=META.curie('uri'),
                   model_uri=META.type_uri, domain=TypeDefinition, range=Optional[Union[str, URIorCURIE]])

slots.repr = Slot(uri=META.repr, name="repr", curie=META.curie('repr'),
                   model_uri=META.repr, domain=TypeDefinition, range=Optional[str])

slots.alt_description_text = Slot(uri=META.description, name="alt_description_text", curie=META.curie('description'),
                   model_uri=META.alt_description_text, domain=AltDescription, range=str)

slots.alt_description_source = Slot(uri=META.source, name="alt_description_source", curie=META.curie('source'),
                   model_uri=META.alt_description_source, domain=AltDescription, range=Union[str, AltDescriptionSource])

slots.alt_descriptions = Slot(uri=META.alt_descriptions, name="alt_descriptions", curie=META.curie('alt_descriptions'),
                   model_uri=META.alt_descriptions, domain=Element, range=Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]])

slots.value = Slot(uri=SKOS.example, name="value", curie=SKOS.curie('example'),
                   model_uri=META.value, domain=Example, range=Optional[str])

slots.value_description = Slot(uri=META.description, name="value_description", curie=META.curie('description'),
                   model_uri=META.value_description, domain=Example, range=Optional[str])

slots.examples = Slot(uri=META.examples, name="examples", curie=META.curie('examples'),
                   model_uri=META.examples, domain=Element, range=Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]])

slots.prefix_prefix = Slot(uri=META.prefix_prefix, name="prefix_prefix", curie=META.curie('prefix_prefix'),
                   model_uri=META.prefix_prefix, domain=Prefix, range=Union[str, PrefixPrefixPrefix])

slots.prefix_reference = Slot(uri=META.prefix_reference, name="prefix_reference", curie=META.curie('prefix_reference'),
                   model_uri=META.prefix_reference, domain=Prefix, range=Union[str, URI])

slots.prefixes = Slot(uri=META.prefixes, name="prefixes", curie=META.curie('prefixes'),
                   model_uri=META.prefixes, domain=SchemaDefinition, range=Optional[Union[Dict[Union[str, PrefixPrefixPrefix], Union[dict, "Prefix"]], List[Union[dict, "Prefix"]]]])

slots.local_name_source = Slot(uri=META.local_name_source, name="local_name_source", curie=META.curie('local_name_source'),
                   model_uri=META.local_name_source, domain=LocalName, range=Union[str, LocalNameLocalNameSource])

slots.local_name_value = Slot(uri=SKOS.altLabel, name="local_name_value", curie=SKOS.curie('altLabel'),
                   model_uri=META.local_name_value, domain=LocalName, range=str)

slots.local_names = Slot(uri=META.local_names, name="local_names", curie=META.curie('local_names'),
                   model_uri=META.local_names, domain=Element, range=Optional[Union[Dict[Union[str, LocalNameLocalNameSource], Union[dict, "LocalName"]], List[Union[dict, "LocalName"]]]])

slots.schema_definition_name = Slot(uri=META.name, name="schema_definition_name", curie=META.curie('name'),
                   model_uri=META.schema_definition_name, domain=SchemaDefinition, range=Union[str, SchemaDefinitionName])

slots.slot_definition_is_a = Slot(uri=META.is_a, name="slot_definition_is_a", curie=META.curie('is_a'),
                   model_uri=META.slot_definition_is_a, domain=SlotDefinition, range=Optional[Union[str, SlotDefinitionName]])

slots.slot_definition_mixins = Slot(uri=META.mixins, name="slot_definition_mixins", curie=META.curie('mixins'),
                   model_uri=META.slot_definition_mixins, domain=SlotDefinition, range=Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]])

slots.slot_definition_apply_to = Slot(uri=META.apply_to, name="slot_definition_apply_to", curie=META.curie('apply_to'),
                   model_uri=META.slot_definition_apply_to, domain=SlotDefinition, range=Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]])

slots.class_definition_is_a = Slot(uri=META.is_a, name="class_definition_is_a", curie=META.curie('is_a'),
                   model_uri=META.class_definition_is_a, domain=ClassDefinition, range=Optional[Union[str, ClassDefinitionName]])

slots.class_definition_mixins = Slot(uri=META.mixins, name="class_definition_mixins", curie=META.curie('mixins'),
                   model_uri=META.class_definition_mixins, domain=ClassDefinition, range=Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]])

slots.class_definition_apply_to = Slot(uri=META.apply_to, name="class_definition_apply_to", curie=META.curie('apply_to'),
                   model_uri=META.class_definition_apply_to, domain=ClassDefinition, range=Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]])

slots.permissible_value_is_a = Slot(uri=META.is_a, name="permissible_value_is_a", curie=META.curie('is_a'),
                   model_uri=META.permissible_value_is_a, domain=PermissibleValue, range=Optional[Union[str, PermissibleValueText]])

slots.permissible_value_mixins = Slot(uri=META.mixins, name="permissible_value_mixins", curie=META.curie('mixins'),
                   model_uri=META.permissible_value_mixins, domain=PermissibleValue, range=Optional[Union[Union[str, PermissibleValueText], List[Union[str, PermissibleValueText]]]])
