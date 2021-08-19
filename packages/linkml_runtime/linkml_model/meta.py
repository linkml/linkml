# Auto generated from meta.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-08-19 17:51
# Schema: meta
#
# id: https://w3id.org/linkml/meta
# description: A metamodel for defining linked open data schemas
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from .annotations import Annotation
from .extensions import Extension
from .types import Boolean, Datetime, Integer, Ncname, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, NCName, URI, URIorCURIE, XSDDateTime

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
OIO = CurieNamespace('OIO', 'http://www.geneontology.org/formats/oboInOwl#')
BIBO = CurieNamespace('bibo', 'http://purl.org/ontology/bibo/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OSLC = CurieNamespace('oslc', 'http://open-services.net/ns/core#')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = LINKML


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
class CommonMetadata(YAMLRoot):
    """
    Generic metadata shared across definitions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.CommonMetadata
    class_class_curie: ClassVar[str] = "linkml:CommonMetadata"
    class_name: ClassVar[str] = "common_metadata"
    class_model_uri: ClassVar[URIRef] = LINKML.CommonMetadata

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
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.deprecated is not None and not isinstance(self.deprecated, str):
            self.deprecated = str(self.deprecated)

        if not isinstance(self.todos, list):
            self.todos = [self.todos] if self.todos is not None else []
        self.todos = [v if isinstance(v, str) else str(v) for v in self.todos]

        if not isinstance(self.notes, list):
            self.notes = [self.notes] if self.notes is not None else []
        self.notes = [v if isinstance(v, str) else str(v) for v in self.notes]

        if not isinstance(self.comments, list):
            self.comments = [self.comments] if self.comments is not None else []
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if not isinstance(self.examples, list):
            self.examples = [self.examples] if self.examples is not None else []
        self.examples = [v if isinstance(v, Example) else Example(**as_dict(v)) for v in self.examples]

        if not isinstance(self.in_subset, list):
            self.in_subset = [self.in_subset] if self.in_subset is not None else []
        self.in_subset = [v if isinstance(v, SubsetDefinitionName) else SubsetDefinitionName(v) for v in self.in_subset]

        if self.from_schema is not None and not isinstance(self.from_schema, URI):
            self.from_schema = URI(self.from_schema)

        if self.imported_from is not None and not isinstance(self.imported_from, str):
            self.imported_from = str(self.imported_from)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        super().__post_init__(**kwargs)


@dataclass
class Element(YAMLRoot):
    """
    a named element in the model
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Element
    class_class_curie: ClassVar[str] = "linkml:Element"
    class_name: ClassVar[str] = "element"
    class_model_uri: ClassVar[URIRef] = LINKML.Element

    name: Union[str, ElementName] = None
    id_prefixes: Optional[Union[Union[str, NCName], List[Union[str, NCName]]]] = empty_list()
    definition_uri: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    local_names: Optional[Union[Dict[Union[str, LocalNameLocalNameSource], Union[dict, "LocalName"]], List[Union[dict, "LocalName"]]]] = empty_dict()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    extensions: Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]] = empty_list()
    annotations: Optional[Union[Union[dict, Annotation], List[Union[dict, Annotation]]]] = empty_list()
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
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ElementName):
            self.name = ElementName(self.name)

        if not isinstance(self.id_prefixes, list):
            self.id_prefixes = [self.id_prefixes] if self.id_prefixes is not None else []
        self.id_prefixes = [v if isinstance(v, NCName) else NCName(v) for v in self.id_prefixes]

        if self.definition_uri is not None and not isinstance(self.definition_uri, URIorCURIE):
            self.definition_uri = URIorCURIE(self.definition_uri)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="local_names", slot_type=LocalName, key_name="local_name_source", keyed=True)

        if not isinstance(self.mappings, list):
            self.mappings = [self.mappings] if self.mappings is not None else []
        self.mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.mappings]

        if not isinstance(self.exact_mappings, list):
            self.exact_mappings = [self.exact_mappings] if self.exact_mappings is not None else []
        self.exact_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.exact_mappings]

        if not isinstance(self.close_mappings, list):
            self.close_mappings = [self.close_mappings] if self.close_mappings is not None else []
        self.close_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.close_mappings]

        if not isinstance(self.related_mappings, list):
            self.related_mappings = [self.related_mappings] if self.related_mappings is not None else []
        self.related_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.related_mappings]

        if not isinstance(self.narrow_mappings, list):
            self.narrow_mappings = [self.narrow_mappings] if self.narrow_mappings is not None else []
        self.narrow_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.narrow_mappings]

        if not isinstance(self.broad_mappings, list):
            self.broad_mappings = [self.broad_mappings] if self.broad_mappings is not None else []
        self.broad_mappings = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.broad_mappings]

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=False)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=False)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.deprecated is not None and not isinstance(self.deprecated, str):
            self.deprecated = str(self.deprecated)

        if not isinstance(self.todos, list):
            self.todos = [self.todos] if self.todos is not None else []
        self.todos = [v if isinstance(v, str) else str(v) for v in self.todos]

        if not isinstance(self.notes, list):
            self.notes = [self.notes] if self.notes is not None else []
        self.notes = [v if isinstance(v, str) else str(v) for v in self.notes]

        if not isinstance(self.comments, list):
            self.comments = [self.comments] if self.comments is not None else []
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if not isinstance(self.examples, list):
            self.examples = [self.examples] if self.examples is not None else []
        self.examples = [v if isinstance(v, Example) else Example(**as_dict(v)) for v in self.examples]

        if not isinstance(self.in_subset, list):
            self.in_subset = [self.in_subset] if self.in_subset is not None else []
        self.in_subset = [v if isinstance(v, SubsetDefinitionName) else SubsetDefinitionName(v) for v in self.in_subset]

        if self.from_schema is not None and not isinstance(self.from_schema, URI):
            self.from_schema = URI(self.from_schema)

        if self.imported_from is not None and not isinstance(self.imported_from, str):
            self.imported_from = str(self.imported_from)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        super().__post_init__(**kwargs)


@dataclass
class SchemaDefinition(Element):
    """
    a collection of subset, type, slot and class definitions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.SchemaDefinition
    class_class_curie: ClassVar[str] = "linkml:SchemaDefinition"
    class_name: ClassVar[str] = "schema_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.SchemaDefinition

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
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SchemaDefinitionName):
            self.name = SchemaDefinitionName(self.name)

        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, URI):
            self.id = URI(self.id)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.imports, list):
            self.imports = [self.imports] if self.imports is not None else []
        self.imports = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.imports]

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        self._normalize_inlined_as_dict(slot_name="prefixes", slot_type=Prefix, key_name="prefix_prefix", keyed=True)

        if not isinstance(self.emit_prefixes, list):
            self.emit_prefixes = [self.emit_prefixes] if self.emit_prefixes is not None else []
        self.emit_prefixes = [v if isinstance(v, NCName) else NCName(v) for v in self.emit_prefixes]

        if not isinstance(self.default_curi_maps, list):
            self.default_curi_maps = [self.default_curi_maps] if self.default_curi_maps is not None else []
        self.default_curi_maps = [v if isinstance(v, str) else str(v) for v in self.default_curi_maps]

        if self.default_prefix is not None and not isinstance(self.default_prefix, str):
            self.default_prefix = str(self.default_prefix)

        if self.default_range is not None and not isinstance(self.default_range, TypeDefinitionName):
            self.default_range = TypeDefinitionName(self.default_range)

        self._normalize_inlined_as_dict(slot_name="subsets", slot_type=SubsetDefinition, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="types", slot_type=TypeDefinition, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="enums", slot_type=EnumDefinition, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="slots", slot_type=SlotDefinition, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="classes", slot_type=ClassDefinition, key_name="name", keyed=True)

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

    class_class_uri: ClassVar[URIRef] = LINKML.TypeDefinition
    class_class_curie: ClassVar[str] = "linkml:TypeDefinition"
    class_name: ClassVar[str] = "type_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.TypeDefinition

    name: Union[str, TypeDefinitionName] = None
    typeof: Optional[Union[str, TypeDefinitionName]] = None
    base: Optional[str] = None
    uri: Optional[Union[str, URIorCURIE]] = None
    repr: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
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

    class_class_uri: ClassVar[URIRef] = LINKML.SubsetDefinition
    class_class_curie: ClassVar[str] = "linkml:SubsetDefinition"
    class_name: ClassVar[str] = "subset_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.SubsetDefinition

    name: Union[str, SubsetDefinitionName] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SubsetDefinitionName):
            self.name = SubsetDefinitionName(self.name)

        super().__post_init__(**kwargs)


@dataclass
class Definition(Element):
    """
    base class for definitions
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Definition
    class_class_curie: ClassVar[str] = "linkml:Definition"
    class_name: ClassVar[str] = "definition"
    class_model_uri: ClassVar[URIRef] = LINKML.Definition

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
    string_serialization: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.is_a is not None and not isinstance(self.is_a, DefinitionName):
            self.is_a = DefinitionName(self.is_a)

        if self.abstract is not None and not isinstance(self.abstract, Bool):
            self.abstract = Bool(self.abstract)

        if self.mixin is not None and not isinstance(self.mixin, Bool):
            self.mixin = Bool(self.mixin)

        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins] if self.mixins is not None else []
        self.mixins = [v if isinstance(v, DefinitionName) else DefinitionName(v) for v in self.mixins]

        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to] if self.apply_to is not None else []
        self.apply_to = [v if isinstance(v, DefinitionName) else DefinitionName(v) for v in self.apply_to]

        if not isinstance(self.values_from, list):
            self.values_from = [self.values_from] if self.values_from is not None else []
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

        if self.string_serialization is not None and not isinstance(self.string_serialization, str):
            self.string_serialization = str(self.string_serialization)

        super().__post_init__(**kwargs)


@dataclass
class EnumDefinition(Element):
    """
    List of values that constrain the range of a slot
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.EnumDefinition
    class_class_curie: ClassVar[str] = "linkml:EnumDefinition"
    class_name: ClassVar[str] = "enum_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.EnumDefinition

    name: Union[str, EnumDefinitionName] = None
    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[Dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], List[Union[dict, "PermissibleValue"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
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

        self._normalize_inlined_as_dict(slot_name="permissible_values", slot_type=PermissibleValue, key_name="text", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class SlotDefinition(Definition):
    """
    the definition of a property or a slot
    """
    _inherited_slots: ClassVar[List[str]] = ["domain", "range", "multivalued", "inherited", "readonly", "ifabsent", "required", "recommended", "inlined", "inlined_as_list", "key", "identifier", "designates_type", "role", "minimum_value", "maximum_value", "pattern"]

    class_class_uri: ClassVar[URIRef] = LINKML.SlotDefinition
    class_class_curie: ClassVar[str] = "linkml:SlotDefinition"
    class_name: ClassVar[str] = "slot_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.SlotDefinition

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
    recommended: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    key: Optional[Union[bool, Bool]] = None
    identifier: Optional[Union[bool, Bool]] = None
    designates_type: Optional[Union[bool, Bool]] = None
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
    is_a: Optional[Union[str, SlotDefinitionName]] = None
    mixins: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
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

        if self.recommended is not None and not isinstance(self.recommended, Bool):
            self.recommended = Bool(self.recommended)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.key is not None and not isinstance(self.key, Bool):
            self.key = Bool(self.key)

        if self.identifier is not None and not isinstance(self.identifier, Bool):
            self.identifier = Bool(self.identifier)

        if self.designates_type is not None and not isinstance(self.designates_type, Bool):
            self.designates_type = Bool(self.designates_type)

        if self.alias is not None and not isinstance(self.alias, str):
            self.alias = str(self.alias)

        if self.owner is not None and not isinstance(self.owner, DefinitionName):
            self.owner = DefinitionName(self.owner)

        if not isinstance(self.domain_of, list):
            self.domain_of = [self.domain_of] if self.domain_of is not None else []
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

        if self.is_a is not None and not isinstance(self.is_a, SlotDefinitionName):
            self.is_a = SlotDefinitionName(self.is_a)

        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins] if self.mixins is not None else []
        self.mixins = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.mixins]

        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to] if self.apply_to is not None else []
        self.apply_to = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.apply_to]

        super().__post_init__(**kwargs)


@dataclass
class ClassDefinition(Definition):
    """
    the definition of a class or interface
    """
    _inherited_slots: ClassVar[List[str]] = ["defining_slots"]

    class_class_uri: ClassVar[URIRef] = LINKML.ClassDefinition
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "class_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.ClassDefinition

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
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ClassDefinitionName):
            self.name = ClassDefinitionName(self.name)

        if not isinstance(self.slots, list):
            self.slots = [self.slots] if self.slots is not None else []
        self.slots = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.slots]

        self._normalize_inlined_as_dict(slot_name="slot_usage", slot_type=SlotDefinition, key_name="name", keyed=True)

        self._normalize_inlined_as_dict(slot_name="attributes", slot_type=SlotDefinition, key_name="name", keyed=True)

        if self.class_uri is not None and not isinstance(self.class_uri, URIorCURIE):
            self.class_uri = URIorCURIE(self.class_uri)

        if self.subclass_of is not None and not isinstance(self.subclass_of, URIorCURIE):
            self.subclass_of = URIorCURIE(self.subclass_of)

        if not isinstance(self.union_of, list):
            self.union_of = [self.union_of] if self.union_of is not None else []
        self.union_of = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.union_of]

        if not isinstance(self.defining_slots, list):
            self.defining_slots = [self.defining_slots] if self.defining_slots is not None else []
        self.defining_slots = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.defining_slots]

        if self.tree_root is not None and not isinstance(self.tree_root, Bool):
            self.tree_root = Bool(self.tree_root)

        if self.is_a is not None and not isinstance(self.is_a, ClassDefinitionName):
            self.is_a = ClassDefinitionName(self.is_a)

        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins] if self.mixins is not None else []
        self.mixins = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.mixins]

        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to] if self.apply_to is not None else []
        self.apply_to = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.apply_to]

        super().__post_init__(**kwargs)


@dataclass
class Prefix(YAMLRoot):
    """
    prefix URI tuple
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Prefix
    class_class_curie: ClassVar[str] = "linkml:Prefix"
    class_name: ClassVar[str] = "prefix"
    class_model_uri: ClassVar[URIRef] = LINKML.Prefix

    prefix_prefix: Union[str, PrefixPrefixPrefix] = None
    prefix_reference: Union[str, URI] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.prefix_prefix):
            self.MissingRequiredField("prefix_prefix")
        if not isinstance(self.prefix_prefix, PrefixPrefixPrefix):
            self.prefix_prefix = PrefixPrefixPrefix(self.prefix_prefix)

        if self._is_empty(self.prefix_reference):
            self.MissingRequiredField("prefix_reference")
        if not isinstance(self.prefix_reference, URI):
            self.prefix_reference = URI(self.prefix_reference)

        super().__post_init__(**kwargs)


@dataclass
class LocalName(YAMLRoot):
    """
    an attributed label
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.LocalName
    class_class_curie: ClassVar[str] = "linkml:LocalName"
    class_name: ClassVar[str] = "local_name"
    class_model_uri: ClassVar[URIRef] = LINKML.LocalName

    local_name_source: Union[str, LocalNameLocalNameSource] = None
    local_name_value: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.local_name_source):
            self.MissingRequiredField("local_name_source")
        if not isinstance(self.local_name_source, LocalNameLocalNameSource):
            self.local_name_source = LocalNameLocalNameSource(self.local_name_source)

        if self._is_empty(self.local_name_value):
            self.MissingRequiredField("local_name_value")
        if not isinstance(self.local_name_value, str):
            self.local_name_value = str(self.local_name_value)

        super().__post_init__(**kwargs)


@dataclass
class Example(YAMLRoot):
    """
    usage example and description
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Example
    class_class_curie: ClassVar[str] = "linkml:Example"
    class_name: ClassVar[str] = "example"
    class_model_uri: ClassVar[URIRef] = LINKML.Example

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

    class_class_uri: ClassVar[URIRef] = LINKML.AltDescription
    class_class_curie: ClassVar[str] = "linkml:AltDescription"
    class_name: ClassVar[str] = "alt_description"
    class_model_uri: ClassVar[URIRef] = LINKML.AltDescription

    source: Union[str, AltDescriptionSource] = None
    description: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, AltDescriptionSource):
            self.source = AltDescriptionSource(self.source)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class PermissibleValue(YAMLRoot):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.PermissibleValue
    class_class_curie: ClassVar[str] = "linkml:PermissibleValue"
    class_name: ClassVar[str] = "permissible_value"
    class_model_uri: ClassVar[URIRef] = LINKML.PermissibleValue

    text: Union[str, PermissibleValueText] = None
    description: Optional[str] = None
    meaning: Optional[Union[str, URIorCURIE]] = None
    is_a: Optional[Union[str, PermissibleValueText]] = None
    mixins: Optional[Union[Union[str, PermissibleValueText], List[Union[str, PermissibleValueText]]]] = empty_list()
    extensions: Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]] = empty_list()
    annotations: Optional[Union[Union[dict, Annotation], List[Union[dict, Annotation]]]] = empty_list()
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

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, PermissibleValueText):
            self.text = PermissibleValueText(self.text)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.meaning is not None and not isinstance(self.meaning, URIorCURIE):
            self.meaning = URIorCURIE(self.meaning)

        if self.is_a is not None and not isinstance(self.is_a, PermissibleValueText):
            self.is_a = PermissibleValueText(self.is_a)

        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins] if self.mixins is not None else []
        self.mixins = [v if isinstance(v, PermissibleValueText) else PermissibleValueText(v) for v in self.mixins]

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=False)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=False)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.deprecated is not None and not isinstance(self.deprecated, str):
            self.deprecated = str(self.deprecated)

        if not isinstance(self.todos, list):
            self.todos = [self.todos] if self.todos is not None else []
        self.todos = [v if isinstance(v, str) else str(v) for v in self.todos]

        if not isinstance(self.notes, list):
            self.notes = [self.notes] if self.notes is not None else []
        self.notes = [v if isinstance(v, str) else str(v) for v in self.notes]

        if not isinstance(self.comments, list):
            self.comments = [self.comments] if self.comments is not None else []
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if not isinstance(self.examples, list):
            self.examples = [self.examples] if self.examples is not None else []
        self.examples = [v if isinstance(v, Example) else Example(**as_dict(v)) for v in self.examples]

        if not isinstance(self.in_subset, list):
            self.in_subset = [self.in_subset] if self.in_subset is not None else []
        self.in_subset = [v if isinstance(v, SubsetDefinitionName) else SubsetDefinitionName(v) for v in self.in_subset]

        if self.from_schema is not None and not isinstance(self.from_schema, URI):
            self.from_schema = URI(self.from_schema)

        if self.imported_from is not None and not isinstance(self.imported_from, str):
            self.imported_from = str(self.imported_from)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        super().__post_init__(**kwargs)


@dataclass
class UniqueKey(YAMLRoot):
    """
    a collection of slots whose values uniquely identify an instance of a class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.UniqueKey
    class_class_curie: ClassVar[str] = "linkml:UniqueKey"
    class_name: ClassVar[str] = "unique_key"
    class_model_uri: ClassVar[URIRef] = LINKML.UniqueKey

    unique_key_slots: Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]] = None
    extensions: Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]] = empty_list()
    annotations: Optional[Union[Union[dict, Annotation], List[Union[dict, Annotation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.unique_key_slots):
            self.MissingRequiredField("unique_key_slots")
        if not isinstance(self.unique_key_slots, list):
            self.unique_key_slots = [self.unique_key_slots] if self.unique_key_slots is not None else []
        self.unique_key_slots = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.unique_key_slots]

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=False)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=False)

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

