# Auto generated from meta.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-07-13T17:59:08
# Schema: meta
#
# id: https://w3id.org/linkml/meta
# description: The metamodel for schemas defined using the Linked Data Modeling Language framework. For more
#              information on LinkML, see [linkml.io](https://linkml.io) Core metaclasses: *
#              [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition) *
#              [ClassDefinition](https://w3id.org/linkml/ClassDefinition) *
#              [SlotDefinition](https://w3id.org/linkml/SlotDefinition) *
#              [TypeDefinition](https://w3id.org/linkml/TypeDefinition) Every LinkML model instantiates
#              SchemaDefinition, all classes in the model instantiate ClassDefinition, and so on Note that the
#              LinkML metamodel instantiates itself. For a non-normative introduction to LinkML schemas, see the
#              tutorial and schema guide on [linkml.io/linkml]. For canonical reference documentation on any
#              metamodel construct, refer to the official URI for each construct, e.g.
#              [https://w3id.org/linkml/is_a](https://w3id.org/linkml/is_a)
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
from .annotations import Annotation, AnnotationTag
from .extensions import Extension, ExtensionTag
from .types import Boolean, Datetime, Integer, Ncname, String, Uri, Uriorcurie
from .units import UnitOfMeasure
from linkml_runtime.utils.metamodelcore import Bool, NCName, URI, URIorCURIE, XSDDateTime

metamodel_version = "1.7.0"
version = "2.0.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
NCIT = CurieNamespace('NCIT', 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')
OIO = CurieNamespace('OIO', 'http://www.geneontology.org/formats/oboInOwl#')
BIBO = CurieNamespace('bibo', 'http://purl.org/ontology/bibo/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OSLC = CurieNamespace('oslc', 'http://open-services.net/ns/core#')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
QB = CurieNamespace('qb', 'http://purl.org/linked-data/cube#')
QUDT = CurieNamespace('qudt', 'http://qudt.org/schema/qudt/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SKOSXL = CurieNamespace('skosxl', 'http://www.w3.org/2008/05/skos-xl#')
SWRL = CurieNamespace('swrl', 'http://www.w3.org/2003/11/swrl#')
VANN = CurieNamespace('vann', 'https://vocab.org/vann/')
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


class EnumDefinitionName(DefinitionName):
    pass


class SlotDefinitionName(DefinitionName):
    pass


class ClassDefinitionName(DefinitionName):
    pass


class SettingSettingKey(NCName):
    pass


class PrefixPrefixPrefix(NCName):
    pass


class LocalNameLocalNameSource(NCName):
    pass


class AltDescriptionSource(extended_str):
    pass


class PermissibleValueText(extended_str):
    pass


class UniqueKeyUniqueKeyName(extended_str):
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
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, "StructuredAlias"], List[Union[dict, "StructuredAlias"]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

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
    local_names: Optional[Union[Dict[Union[str, LocalNameLocalNameSource], Union[dict, "LocalName"]], List[Union[dict, "LocalName"]]]] = empty_dict()
    conforms_to: Optional[str] = None
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, "StructuredAlias"], List[Union[dict, "StructuredAlias"]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

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

        self._normalize_inlined_as_dict(slot_name="local_names", slot_type=LocalName, key_name="local_name_source", keyed=True)

        if self.conforms_to is not None and not isinstance(self.conforms_to, str):
            self.conforms_to = str(self.conforms_to)

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

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
    slot_names_unique: Optional[Union[bool, Bool]] = None
    settings: Optional[Union[Dict[Union[str, SettingSettingKey], Union[dict, "Setting"]], List[Union[dict, "Setting"]]]] = empty_dict()
    categories: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, List[str]]] = empty_list()

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

        if self.slot_names_unique is not None and not isinstance(self.slot_names_unique, Bool):
            self.slot_names_unique = Bool(self.slot_names_unique)

        self._normalize_inlined_as_dict(slot_name="settings", slot_type=Setting, key_name="setting_key", keyed=True)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass
class AnonymousTypeExpression(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = ["pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "minimum_value", "maximum_value"]

    class_class_uri: ClassVar[URIRef] = LINKML.AnonymousTypeExpression
    class_class_curie: ClassVar[str] = "linkml:AnonymousTypeExpression"
    class_name: ClassVar[str] = "anonymous_type_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousTypeExpression

    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, List[str]]] = empty_list()
    equals_number: Optional[int] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    none_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.minimum_value is not None and not isinstance(self.minimum_value, int):
            self.minimum_value = int(self.minimum_value)

        if self.maximum_value is not None and not isinstance(self.maximum_value, int):
            self.maximum_value = int(self.maximum_value)

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.all_of]

        super().__post_init__(**kwargs)


@dataclass
class TypeDefinition(Element):
    """
    A data type definition.
    """
    _inherited_slots: ClassVar[List[str]] = ["base", "uri", "repr", "pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "minimum_value", "maximum_value"]

    class_class_uri: ClassVar[URIRef] = LINKML.TypeDefinition
    class_class_curie: ClassVar[str] = "linkml:TypeDefinition"
    class_name: ClassVar[str] = "type_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.TypeDefinition

    name: Union[str, TypeDefinitionName] = None
    typeof: Optional[Union[str, TypeDefinitionName]] = None
    base: Optional[str] = None
    uri: Optional[Union[str, URIorCURIE]] = None
    repr: Optional[str] = None
    union_of: Optional[Union[Union[str, TypeDefinitionName], List[Union[str, TypeDefinitionName]]]] = empty_list()
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, List[str]]] = empty_list()
    equals_number: Optional[int] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    none_of: Optional[Union[Union[dict, AnonymousTypeExpression], List[Union[dict, AnonymousTypeExpression]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, AnonymousTypeExpression], List[Union[dict, AnonymousTypeExpression]]]] = empty_list()
    any_of: Optional[Union[Union[dict, AnonymousTypeExpression], List[Union[dict, AnonymousTypeExpression]]]] = empty_list()
    all_of: Optional[Union[Union[dict, AnonymousTypeExpression], List[Union[dict, AnonymousTypeExpression]]]] = empty_list()

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

        if not isinstance(self.union_of, list):
            self.union_of = [self.union_of] if self.union_of is not None else []
        self.union_of = [v if isinstance(v, TypeDefinitionName) else TypeDefinitionName(v) for v in self.union_of]

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.minimum_value is not None and not isinstance(self.minimum_value, int):
            self.minimum_value = int(self.minimum_value)

        if self.maximum_value is not None and not isinstance(self.maximum_value, int):
            self.maximum_value = int(self.maximum_value)

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.all_of]

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
class AnonymousEnumExpression(YAMLRoot):
    """
    An enum_expression that is not named
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.AnonymousEnumExpression
    class_class_curie: ClassVar[str] = "linkml:AnonymousEnumExpression"
    class_name: ClassVar[str] = "anonymous_enum_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousEnumExpression

    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[Dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], List[Union[dict, "PermissibleValue"]]]] = empty_dict()
    include: Optional[Union[Union[dict, "AnonymousEnumExpression"], List[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    minus: Optional[Union[Union[dict, "AnonymousEnumExpression"], List[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    inherits: Optional[Union[Union[str, EnumDefinitionName], List[Union[str, EnumDefinitionName]]]] = empty_list()
    reachable_from: Optional[Union[dict, "ReachabilityQuery"]] = None
    matches: Optional[Union[dict, "MatchQuery"]] = None
    concepts: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.code_set is not None and not isinstance(self.code_set, URIorCURIE):
            self.code_set = URIorCURIE(self.code_set)

        if self.code_set_tag is not None and not isinstance(self.code_set_tag, str):
            self.code_set_tag = str(self.code_set_tag)

        if self.code_set_version is not None and not isinstance(self.code_set_version, str):
            self.code_set_version = str(self.code_set_version)

        if self.pv_formula is not None and not isinstance(self.pv_formula, PvFormulaOptions):
            self.pv_formula = PvFormulaOptions(self.pv_formula)

        self._normalize_inlined_as_dict(slot_name="permissible_values", slot_type=PermissibleValue, key_name="text", keyed=True)

        if not isinstance(self.include, list):
            self.include = [self.include] if self.include is not None else []
        self.include = [v if isinstance(v, AnonymousEnumExpression) else AnonymousEnumExpression(**as_dict(v)) for v in self.include]

        if not isinstance(self.minus, list):
            self.minus = [self.minus] if self.minus is not None else []
        self.minus = [v if isinstance(v, AnonymousEnumExpression) else AnonymousEnumExpression(**as_dict(v)) for v in self.minus]

        if not isinstance(self.inherits, list):
            self.inherits = [self.inherits] if self.inherits is not None else []
        self.inherits = [v if isinstance(v, EnumDefinitionName) else EnumDefinitionName(v) for v in self.inherits]

        if self.reachable_from is not None and not isinstance(self.reachable_from, ReachabilityQuery):
            self.reachable_from = ReachabilityQuery(**as_dict(self.reachable_from))

        if self.matches is not None and not isinstance(self.matches, MatchQuery):
            self.matches = MatchQuery(**as_dict(self.matches))

        if not isinstance(self.concepts, list):
            self.concepts = [self.concepts] if self.concepts is not None else []
        self.concepts = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.concepts]

        super().__post_init__(**kwargs)


@dataclass
class EnumDefinition(Definition):
    """
    List of values that constrain the range of a slot
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.EnumDefinition
    class_class_curie: ClassVar[str] = "linkml:EnumDefinition"
    class_name: ClassVar[str] = "enum_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.EnumDefinition

    name: Union[str, EnumDefinitionName] = None
    enum_uri: Optional[Union[str, URIorCURIE]] = None
    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[Dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]],
                                       List[Union[dict, "PermissibleValue"]]]] = empty_dict()
    include: Optional[Union[Union[dict, AnonymousEnumExpression], List[Union[dict, AnonymousEnumExpression]]]] = empty_list()
    minus: Optional[Union[Union[dict, AnonymousEnumExpression], List[Union[dict, AnonymousEnumExpression]]]] = empty_list()
    inherits: Optional[Union[Union[str, EnumDefinitionName], List[Union[str, EnumDefinitionName]]]] = empty_list()
    reachable_from: Optional[Union[dict, "ReachabilityQuery"]] = None
    matches: Optional[Union[dict, "MatchQuery"]] = None
    concepts: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, EnumDefinitionName):
            self.name = EnumDefinitionName(self.name)

        if self.enum_uri is not None and not isinstance(self.enum_uri, URIorCURIE):
            self.enum_uri = URIorCURIE(self.enum_uri)

        if self.code_set is not None and not isinstance(self.code_set, URIorCURIE):
            self.code_set = URIorCURIE(self.code_set)

        if self.code_set_tag is not None and not isinstance(self.code_set_tag, str):
            self.code_set_tag = str(self.code_set_tag)

        if self.code_set_version is not None and not isinstance(self.code_set_version, str):
            self.code_set_version = str(self.code_set_version)

        if self.pv_formula is not None and not isinstance(self.pv_formula, PvFormulaOptions):
            self.pv_formula = PvFormulaOptions(self.pv_formula)

        self._normalize_inlined_as_dict(slot_name="permissible_values", slot_type=PermissibleValue, key_name="text", keyed=True)

        if not isinstance(self.include, list):
            self.include = [self.include] if self.include is not None else []
        self.include = [v if isinstance(v, AnonymousEnumExpression) else AnonymousEnumExpression(**as_dict(v)) for v in self.include]

        if not isinstance(self.minus, list):
            self.minus = [self.minus] if self.minus is not None else []
        self.minus = [v if isinstance(v, AnonymousEnumExpression) else AnonymousEnumExpression(**as_dict(v)) for v in self.minus]

        if not isinstance(self.inherits, list):
            self.inherits = [self.inherits] if self.inherits is not None else []
        self.inherits = [v if isinstance(v, EnumDefinitionName) else EnumDefinitionName(v) for v in self.inherits]

        if self.reachable_from is not None and not isinstance(self.reachable_from, ReachabilityQuery):
            self.reachable_from = ReachabilityQuery(**as_dict(self.reachable_from))

        if self.matches is not None and not isinstance(self.matches, MatchQuery):
            self.matches = MatchQuery(**as_dict(self.matches))

        if not isinstance(self.concepts, list):
            self.concepts = [self.concepts] if self.concepts is not None else []
        self.concepts = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.concepts]

        super().__post_init__(**kwargs)


@dataclass
class MatchQuery(YAMLRoot):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that
    matches on properties of the external concepts
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.MatchQuery
    class_class_curie: ClassVar[str] = "linkml:MatchQuery"
    class_name: ClassVar[str] = "match_query"
    class_model_uri: ClassVar[URIRef] = LINKML.MatchQuery

    identifier_pattern: Optional[str] = None
    source_ontology: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.identifier_pattern is not None and not isinstance(self.identifier_pattern, str):
            self.identifier_pattern = str(self.identifier_pattern)

        if self.source_ontology is not None and not isinstance(self.source_ontology, URIorCURIE):
            self.source_ontology = URIorCURIE(self.source_ontology)

        super().__post_init__(**kwargs)


@dataclass
class ReachabilityQuery(YAMLRoot):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a
    set of source nodes to a set of descendants or ancestors over a set of relationship types
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ReachabilityQuery
    class_class_curie: ClassVar[str] = "linkml:ReachabilityQuery"
    class_name: ClassVar[str] = "reachability_query"
    class_model_uri: ClassVar[URIRef] = LINKML.ReachabilityQuery

    source_ontology: Optional[Union[str, URIorCURIE]] = None
    source_nodes: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    relationship_types: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    is_direct: Optional[Union[bool, Bool]] = None
    include_self: Optional[Union[bool, Bool]] = None
    traverse_up: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.source_ontology is not None and not isinstance(self.source_ontology, URIorCURIE):
            self.source_ontology = URIorCURIE(self.source_ontology)

        if not isinstance(self.source_nodes, list):
            self.source_nodes = [self.source_nodes] if self.source_nodes is not None else []
        self.source_nodes = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.source_nodes]

        if not isinstance(self.relationship_types, list):
            self.relationship_types = [self.relationship_types] if self.relationship_types is not None else []
        self.relationship_types = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.relationship_types]

        if self.is_direct is not None and not isinstance(self.is_direct, Bool):
            self.is_direct = Bool(self.is_direct)

        if self.include_self is not None and not isinstance(self.include_self, Bool):
            self.include_self = Bool(self.include_self)

        if self.traverse_up is not None and not isinstance(self.traverse_up, Bool):
            self.traverse_up = Bool(self.traverse_up)

        super().__post_init__(**kwargs)


@dataclass
class StructuredAlias(YAMLRoot):
    """
    object that contains meta data about a synonym or alias including where it came from (source) and its scope
    (narrow, broad, etc.)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOSXL.Label
    class_class_curie: ClassVar[str] = "skosxl:Label"
    class_name: ClassVar[str] = "structured_alias"
    class_model_uri: ClassVar[URIRef] = LINKML.StructuredAlias

    literal_form: str = None
    predicate: Optional[Union[str, "AliasPredicateEnum"]] = None
    categories: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, "StructuredAlias"], List[Union[dict, "StructuredAlias"]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.literal_form):
            self.MissingRequiredField("literal_form")
        if not isinstance(self.literal_form, str):
            self.literal_form = str(self.literal_form)

        if self.predicate is not None and not isinstance(self.predicate, AliasPredicateEnum):
            self.predicate = AliasPredicateEnum(self.predicate)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        super().__post_init__(**kwargs)


class Expression(YAMLRoot):
    """
    general mixin for any class that can represent some form of expression
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Expression
    class_class_curie: ClassVar[str] = "linkml:Expression"
    class_name: ClassVar[str] = "expression"
    class_model_uri: ClassVar[URIRef] = LINKML.Expression


@dataclass
class TypeExpression(Expression):
    _inherited_slots: ClassVar[List[str]] = ["pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "minimum_value", "maximum_value"]

    class_class_uri: ClassVar[URIRef] = LINKML.TypeExpression
    class_class_curie: ClassVar[str] = "linkml:TypeExpression"
    class_name: ClassVar[str] = "type_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.TypeExpression

    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, List[str]]] = empty_list()
    equals_number: Optional[int] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    none_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], List[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.minimum_value is not None and not isinstance(self.minimum_value, int):
            self.minimum_value = int(self.minimum_value)

        if self.maximum_value is not None and not isinstance(self.maximum_value, int):
            self.maximum_value = int(self.maximum_value)

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousTypeExpression) else AnonymousTypeExpression(**as_dict(v)) for v in self.all_of]

        super().__post_init__(**kwargs)


@dataclass
class EnumExpression(Expression):
    """
    An expression that constrains the range of a slot
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.EnumExpression
    class_class_curie: ClassVar[str] = "linkml:EnumExpression"
    class_name: ClassVar[str] = "enum_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.EnumExpression

    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[Dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], List[Union[dict, "PermissibleValue"]]]] = empty_dict()
    include: Optional[Union[Union[dict, "AnonymousEnumExpression"], List[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    minus: Optional[Union[Union[dict, "AnonymousEnumExpression"], List[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    inherits: Optional[Union[Union[str, EnumDefinitionName], List[Union[str, EnumDefinitionName]]]] = empty_list()
    reachable_from: Optional[Union[dict, "ReachabilityQuery"]] = None
    matches: Optional[Union[dict, "MatchQuery"]] = None
    concepts: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.code_set is not None and not isinstance(self.code_set, URIorCURIE):
            self.code_set = URIorCURIE(self.code_set)

        if self.code_set_tag is not None and not isinstance(self.code_set_tag, str):
            self.code_set_tag = str(self.code_set_tag)

        if self.code_set_version is not None and not isinstance(self.code_set_version, str):
            self.code_set_version = str(self.code_set_version)

        if self.pv_formula is not None and not isinstance(self.pv_formula, PvFormulaOptions):
            self.pv_formula = PvFormulaOptions(self.pv_formula)

        self._normalize_inlined_as_dict(slot_name="permissible_values", slot_type=PermissibleValue, key_name="text", keyed=True)

        if not isinstance(self.include, list):
            self.include = [self.include] if self.include is not None else []
        self.include = [v if isinstance(v, AnonymousEnumExpression) else AnonymousEnumExpression(**as_dict(v)) for v in self.include]

        if not isinstance(self.minus, list):
            self.minus = [self.minus] if self.minus is not None else []
        self.minus = [v if isinstance(v, AnonymousEnumExpression) else AnonymousEnumExpression(**as_dict(v)) for v in self.minus]

        if not isinstance(self.inherits, list):
            self.inherits = [self.inherits] if self.inherits is not None else []
        self.inherits = [v if isinstance(v, EnumDefinitionName) else EnumDefinitionName(v) for v in self.inherits]

        if self.reachable_from is not None and not isinstance(self.reachable_from, ReachabilityQuery):
            self.reachable_from = ReachabilityQuery(**as_dict(self.reachable_from))

        if self.matches is not None and not isinstance(self.matches, MatchQuery):
            self.matches = MatchQuery(**as_dict(self.matches))

        if not isinstance(self.concepts, list):
            self.concepts = [self.concepts] if self.concepts is not None else []
        self.concepts = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.concepts]

        super().__post_init__(**kwargs)


@dataclass
class AnonymousExpression(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.AnonymousExpression
    class_class_curie: ClassVar[str] = "linkml:AnonymousExpression"
    class_name: ClassVar[str] = "anonymous_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousExpression

    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], List[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        super().__post_init__(**kwargs)


@dataclass
class PathExpression(YAMLRoot):
    """
    An expression that describes an abstract path from an object to another through a sequence of slot lookups
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.PathExpression
    class_class_curie: ClassVar[str] = "linkml:PathExpression"
    class_name: ClassVar[str] = "path_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.PathExpression

    followed_by: Optional[Union[dict, "PathExpression"]] = None
    none_of: Optional[Union[Union[dict, "PathExpression"], List[Union[dict, "PathExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "PathExpression"], List[Union[dict, "PathExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "PathExpression"], List[Union[dict, "PathExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "PathExpression"], List[Union[dict, "PathExpression"]]]] = empty_list()
    reversed: Optional[Union[bool, Bool]] = None
    traverse: Optional[Union[str, SlotDefinitionName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], List[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.followed_by is not None and not isinstance(self.followed_by, PathExpression):
            self.followed_by = PathExpression(**as_dict(self.followed_by))

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, PathExpression) else PathExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, PathExpression) else PathExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, PathExpression) else PathExpression(**as_dict(v)) for v in self.all_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, PathExpression) else PathExpression(**as_dict(v)) for v in self.exactly_one_of]

        if self.reversed is not None and not isinstance(self.reversed, Bool):
            self.reversed = Bool(self.reversed)

        if self.traverse is not None and not isinstance(self.traverse, SlotDefinitionName):
            self.traverse = SlotDefinitionName(self.traverse)

        if self.range_expression is not None and not isinstance(self.range_expression, AnonymousClassExpression):
            self.range_expression = AnonymousClassExpression(**as_dict(self.range_expression))

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        super().__post_init__(**kwargs)


@dataclass
class SlotExpression(Expression):
    """
    an expression that constrains the range of values a slot can take
    """
    _inherited_slots: ClassVar[List[str]] = ["range", "required", "recommended", "inlined", "inlined_as_list", "minimum_value", "maximum_value", "pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "equals_expression", "minimum_cardinality", "maximum_cardinality"]

    class_class_uri: ClassVar[URIRef] = LINKML.SlotExpression
    class_class_curie: ClassVar[str] = "linkml:SlotExpression"
    class_name: ClassVar[str] = "slot_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.SlotExpression

    range: Optional[Union[str, ElementName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    enum_range: Optional[Union[dict, EnumExpression]] = None
    required: Optional[Union[bool, Bool]] = None
    recommended: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, List[str]]] = empty_list()
    equals_number: Optional[int] = None
    equals_expression: Optional[str] = None
    minimum_cardinality: Optional[int] = None
    maximum_cardinality: Optional[int] = None
    has_member: Optional[Union[dict, "AnonymousSlotExpression"]] = None
    all_members: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, "SlotDefinition"]], List[Union[dict, "SlotDefinition"]]]] = empty_dict()
    none_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.range is not None and not isinstance(self.range, ElementName):
            self.range = ElementName(self.range)

        if self.range_expression is not None and not isinstance(self.range_expression, AnonymousClassExpression):
            self.range_expression = AnonymousClassExpression(**as_dict(self.range_expression))

        if self.enum_range is not None and not isinstance(self.enum_range, EnumExpression):
            self.enum_range = EnumExpression(**as_dict(self.enum_range))

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if self.recommended is not None and not isinstance(self.recommended, Bool):
            self.recommended = Bool(self.recommended)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.minimum_value is not None and not isinstance(self.minimum_value, int):
            self.minimum_value = int(self.minimum_value)

        if self.maximum_value is not None and not isinstance(self.maximum_value, int):
            self.maximum_value = int(self.maximum_value)

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.equals_expression is not None and not isinstance(self.equals_expression, str):
            self.equals_expression = str(self.equals_expression)

        if self.minimum_cardinality is not None and not isinstance(self.minimum_cardinality, int):
            self.minimum_cardinality = int(self.minimum_cardinality)

        if self.maximum_cardinality is not None and not isinstance(self.maximum_cardinality, int):
            self.maximum_cardinality = int(self.maximum_cardinality)

        if self.has_member is not None and not isinstance(self.has_member, AnonymousSlotExpression):
            self.has_member = AnonymousSlotExpression(**as_dict(self.has_member))

        self._normalize_inlined_as_dict(slot_name="all_members", slot_type=SlotDefinition, key_name="name", keyed=True)

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.all_of]

        super().__post_init__(**kwargs)


@dataclass
class AnonymousSlotExpression(AnonymousExpression):
    _inherited_slots: ClassVar[List[str]] = ["range", "required", "recommended", "inlined", "inlined_as_list", "minimum_value", "maximum_value", "pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "equals_expression", "minimum_cardinality", "maximum_cardinality"]

    class_class_uri: ClassVar[URIRef] = LINKML.AnonymousSlotExpression
    class_class_curie: ClassVar[str] = "linkml:AnonymousSlotExpression"
    class_name: ClassVar[str] = "anonymous_slot_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousSlotExpression

    range: Optional[Union[str, ElementName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    enum_range: Optional[Union[dict, EnumExpression]] = None
    required: Optional[Union[bool, Bool]] = None
    recommended: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, List[str]]] = empty_list()
    equals_number: Optional[int] = None
    equals_expression: Optional[str] = None
    minimum_cardinality: Optional[int] = None
    maximum_cardinality: Optional[int] = None
    has_member: Optional[Union[dict, "AnonymousSlotExpression"]] = None
    all_members: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, "SlotDefinition"]], List[Union[dict, "SlotDefinition"]]]] = empty_dict()
    none_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], List[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.range is not None and not isinstance(self.range, ElementName):
            self.range = ElementName(self.range)

        if self.range_expression is not None and not isinstance(self.range_expression, AnonymousClassExpression):
            self.range_expression = AnonymousClassExpression(**as_dict(self.range_expression))

        if self.enum_range is not None and not isinstance(self.enum_range, EnumExpression):
            self.enum_range = EnumExpression(**as_dict(self.enum_range))

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if self.recommended is not None and not isinstance(self.recommended, Bool):
            self.recommended = Bool(self.recommended)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.minimum_value is not None and not isinstance(self.minimum_value, int):
            self.minimum_value = int(self.minimum_value)

        if self.maximum_value is not None and not isinstance(self.maximum_value, int):
            self.maximum_value = int(self.maximum_value)

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.equals_expression is not None and not isinstance(self.equals_expression, str):
            self.equals_expression = str(self.equals_expression)

        if self.minimum_cardinality is not None and not isinstance(self.minimum_cardinality, int):
            self.minimum_cardinality = int(self.minimum_cardinality)

        if self.maximum_cardinality is not None and not isinstance(self.maximum_cardinality, int):
            self.maximum_cardinality = int(self.maximum_cardinality)

        if self.has_member is not None and not isinstance(self.has_member, AnonymousSlotExpression):
            self.has_member = AnonymousSlotExpression(**as_dict(self.has_member))

        self._normalize_inlined_as_dict(slot_name="all_members", slot_type=SlotDefinition, key_name="name", keyed=True)

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.all_of]

        super().__post_init__(**kwargs)


@dataclass
class SlotDefinition(Definition):
    """
    the definition of a property or a slot
    """
    _inherited_slots: ClassVar[List[str]] = ["domain", "multivalued", "inherited", "readonly", "ifabsent", "list_elements_unique", "list_elements_ordered", "shared", "key", "identifier", "designates_type", "role", "relational_role", "range", "required", "recommended", "inlined", "inlined_as_list", "minimum_value", "maximum_value", "pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "equals_expression", "minimum_cardinality", "maximum_cardinality"]

    class_class_uri: ClassVar[URIRef] = LINKML.SlotDefinition
    class_class_curie: ClassVar[str] = "linkml:SlotDefinition"
    class_name: ClassVar[str] = "slot_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.SlotDefinition

    name: Union[str, SlotDefinitionName] = None
    singular_name: Optional[str] = None
    domain: Optional[Union[str, ClassDefinitionName]] = None
    slot_uri: Optional[Union[str, URIorCURIE]] = None
    multivalued: Optional[Union[bool, Bool]] = None
    inherited: Optional[Union[bool, Bool]] = None
    readonly: Optional[str] = None
    ifabsent: Optional[str] = None
    list_elements_unique: Optional[Union[bool, Bool]] = None
    list_elements_ordered: Optional[Union[bool, Bool]] = None
    shared: Optional[Union[bool, Bool]] = None
    key: Optional[Union[bool, Bool]] = None
    identifier: Optional[Union[bool, Bool]] = None
    designates_type: Optional[Union[bool, Bool]] = None
    alias: Optional[str] = None
    owner: Optional[Union[str, DefinitionName]] = None
    domain_of: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()
    subproperty_of: Optional[Union[str, SlotDefinitionName]] = None
    symmetric: Optional[Union[bool, Bool]] = None
    reflexive: Optional[Union[bool, Bool]] = None
    locally_reflexive: Optional[Union[bool, Bool]] = None
    irreflexive: Optional[Union[bool, Bool]] = None
    asymmetric: Optional[Union[bool, Bool]] = None
    transitive: Optional[Union[bool, Bool]] = None
    inverse: Optional[Union[str, SlotDefinitionName]] = None
    is_class_field: Optional[Union[bool, Bool]] = None
    transitive_form_of: Optional[Union[str, SlotDefinitionName]] = None
    reflexive_transitive_form_of: Optional[Union[str, SlotDefinitionName]] = None
    role: Optional[str] = None
    is_usage_slot: Optional[Union[bool, Bool]] = None
    usage_slot_name: Optional[str] = None
    relational_role: Optional[Union[str, "RelationalRoleEnum"]] = None
    slot_group: Optional[Union[str, SlotDefinitionName]] = None
    is_grouping_slot: Optional[Union[bool, Bool]] = None
    path_rule: Optional[Union[dict, PathExpression]] = None
    disjoint_with: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()
    children_are_mutually_disjoint: Optional[Union[bool, Bool]] = None
    union_of: Optional[Union[Union[str, TypeDefinitionName], List[Union[str, TypeDefinitionName]]]] = empty_list()
    is_a: Optional[Union[str, SlotDefinitionName]] = None
    mixins: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]]] = empty_list()
    range: Optional[Union[str, ElementName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    enum_range: Optional[Union[dict, EnumExpression]] = None
    required: Optional[Union[bool, Bool]] = None
    recommended: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    minimum_value: Optional[int] = None
    maximum_value: Optional[int] = None
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, List[str]]] = empty_list()
    equals_number: Optional[int] = None
    equals_expression: Optional[str] = None
    minimum_cardinality: Optional[int] = None
    maximum_cardinality: Optional[int] = None
    has_member: Optional[Union[dict, AnonymousSlotExpression]] = None
    all_members: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, "SlotDefinition"]], List[Union[dict, "SlotDefinition"]]]] = empty_dict()
    none_of: Optional[Union[Union[dict, AnonymousSlotExpression], List[Union[dict, AnonymousSlotExpression]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, AnonymousSlotExpression], List[Union[dict, AnonymousSlotExpression]]]] = empty_list()
    any_of: Optional[Union[Union[dict, AnonymousSlotExpression], List[Union[dict, AnonymousSlotExpression]]]] = empty_list()
    all_of: Optional[Union[Union[dict, AnonymousSlotExpression], List[Union[dict, AnonymousSlotExpression]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SlotDefinitionName):
            self.name = SlotDefinitionName(self.name)

        if self.singular_name is not None and not isinstance(self.singular_name, str):
            self.singular_name = str(self.singular_name)

        if self.domain is not None and not isinstance(self.domain, ClassDefinitionName):
            self.domain = ClassDefinitionName(self.domain)

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

        if self.list_elements_unique is not None and not isinstance(self.list_elements_unique, Bool):
            self.list_elements_unique = Bool(self.list_elements_unique)

        if self.list_elements_ordered is not None and not isinstance(self.list_elements_ordered, Bool):
            self.list_elements_ordered = Bool(self.list_elements_ordered)

        if self.shared is not None and not isinstance(self.shared, Bool):
            self.shared = Bool(self.shared)

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

        if self.reflexive is not None and not isinstance(self.reflexive, Bool):
            self.reflexive = Bool(self.reflexive)

        if self.locally_reflexive is not None and not isinstance(self.locally_reflexive, Bool):
            self.locally_reflexive = Bool(self.locally_reflexive)

        if self.irreflexive is not None and not isinstance(self.irreflexive, Bool):
            self.irreflexive = Bool(self.irreflexive)

        if self.asymmetric is not None and not isinstance(self.asymmetric, Bool):
            self.asymmetric = Bool(self.asymmetric)

        if self.transitive is not None and not isinstance(self.transitive, Bool):
            self.transitive = Bool(self.transitive)

        if self.inverse is not None and not isinstance(self.inverse, SlotDefinitionName):
            self.inverse = SlotDefinitionName(self.inverse)

        if self.is_class_field is not None and not isinstance(self.is_class_field, Bool):
            self.is_class_field = Bool(self.is_class_field)

        if self.transitive_form_of is not None and not isinstance(self.transitive_form_of, SlotDefinitionName):
            self.transitive_form_of = SlotDefinitionName(self.transitive_form_of)

        if self.reflexive_transitive_form_of is not None and not isinstance(self.reflexive_transitive_form_of, SlotDefinitionName):
            self.reflexive_transitive_form_of = SlotDefinitionName(self.reflexive_transitive_form_of)

        if self.role is not None and not isinstance(self.role, str):
            self.role = str(self.role)

        if self.is_usage_slot is not None and not isinstance(self.is_usage_slot, Bool):
            self.is_usage_slot = Bool(self.is_usage_slot)

        if self.usage_slot_name is not None and not isinstance(self.usage_slot_name, str):
            self.usage_slot_name = str(self.usage_slot_name)

        if self.relational_role is not None and not isinstance(self.relational_role, RelationalRoleEnum):
            self.relational_role = RelationalRoleEnum(self.relational_role)

        if self.slot_group is not None and not isinstance(self.slot_group, SlotDefinitionName):
            self.slot_group = SlotDefinitionName(self.slot_group)

        if self.is_grouping_slot is not None and not isinstance(self.is_grouping_slot, Bool):
            self.is_grouping_slot = Bool(self.is_grouping_slot)

        if self.path_rule is not None and not isinstance(self.path_rule, PathExpression):
            self.path_rule = PathExpression(**as_dict(self.path_rule))

        if not isinstance(self.disjoint_with, list):
            self.disjoint_with = [self.disjoint_with] if self.disjoint_with is not None else []
        self.disjoint_with = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.disjoint_with]

        if self.children_are_mutually_disjoint is not None and not isinstance(self.children_are_mutually_disjoint, Bool):
            self.children_are_mutually_disjoint = Bool(self.children_are_mutually_disjoint)

        if not isinstance(self.union_of, list):
            self.union_of = [self.union_of] if self.union_of is not None else []
        self.union_of = [v if isinstance(v, TypeDefinitionName) else TypeDefinitionName(v) for v in self.union_of]

        if self.is_a is not None and not isinstance(self.is_a, SlotDefinitionName):
            self.is_a = SlotDefinitionName(self.is_a)

        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins] if self.mixins is not None else []
        self.mixins = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.mixins]

        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to] if self.apply_to is not None else []
        self.apply_to = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.apply_to]

        if self.range is not None and not isinstance(self.range, ElementName):
            self.range = ElementName(self.range)

        if self.range_expression is not None and not isinstance(self.range_expression, AnonymousClassExpression):
            self.range_expression = AnonymousClassExpression(**as_dict(self.range_expression))

        if self.enum_range is not None and not isinstance(self.enum_range, EnumExpression):
            self.enum_range = EnumExpression(**as_dict(self.enum_range))

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if self.recommended is not None and not isinstance(self.recommended, Bool):
            self.recommended = Bool(self.recommended)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.minimum_value is not None and not isinstance(self.minimum_value, int):
            self.minimum_value = int(self.minimum_value)

        if self.maximum_value is not None and not isinstance(self.maximum_value, int):
            self.maximum_value = int(self.maximum_value)

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.equals_expression is not None and not isinstance(self.equals_expression, str):
            self.equals_expression = str(self.equals_expression)

        if self.minimum_cardinality is not None and not isinstance(self.minimum_cardinality, int):
            self.minimum_cardinality = int(self.minimum_cardinality)

        if self.maximum_cardinality is not None and not isinstance(self.maximum_cardinality, int):
            self.maximum_cardinality = int(self.maximum_cardinality)

        if self.has_member is not None and not isinstance(self.has_member, AnonymousSlotExpression):
            self.has_member = AnonymousSlotExpression(**as_dict(self.has_member))

        self._normalize_inlined_as_dict(slot_name="all_members", slot_type=SlotDefinition, key_name="name", keyed=True)

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousSlotExpression) else AnonymousSlotExpression(**as_dict(v)) for v in self.all_of]

        super().__post_init__(**kwargs)


@dataclass
class ClassExpression(YAMLRoot):
    """
    A boolean expression that can be used to dynamically determine membership of a class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ClassExpression
    class_class_curie: ClassVar[str] = "linkml:ClassExpression"
    class_name: ClassVar[str] = "class_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.ClassExpression

    any_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    none_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    slot_conditions: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], List[Union[dict, SlotDefinition]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.all_of]

        self._normalize_inlined_as_dict(slot_name="slot_conditions", slot_type=SlotDefinition, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class AnonymousClassExpression(AnonymousExpression):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.AnonymousClassExpression
    class_class_curie: ClassVar[str] = "linkml:AnonymousClassExpression"
    class_name: ClassVar[str] = "anonymous_class_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousClassExpression

    is_a: Optional[Union[str, DefinitionName]] = None
    any_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    none_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousClassExpression"], List[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    slot_conditions: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], List[Union[dict, SlotDefinition]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.is_a is not None and not isinstance(self.is_a, DefinitionName):
            self.is_a = DefinitionName(self.is_a)

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.all_of]

        self._normalize_inlined_as_dict(slot_name="slot_conditions", slot_type=SlotDefinition, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class ClassDefinition(Definition):
    """
    the definition of a class or interface
    """
    _inherited_slots: ClassVar[List[str]] = ["defining_slots", "represents_relationship"]

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
    unique_keys: Optional[Union[Dict[Union[str, UniqueKeyUniqueKeyName], Union[dict, "UniqueKey"]], List[Union[dict, "UniqueKey"]]]] = empty_dict()
    rules: Optional[Union[Union[dict, "ClassRule"], List[Union[dict, "ClassRule"]]]] = empty_list()
    classification_rules: Optional[Union[Union[dict, AnonymousClassExpression], List[Union[dict, AnonymousClassExpression]]]] = empty_list()
    slot_names_unique: Optional[Union[bool, Bool]] = None
    represents_relationship: Optional[Union[bool, Bool]] = None
    disjoint_with: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()
    children_are_mutually_disjoint: Optional[Union[bool, Bool]] = None
    is_a: Optional[Union[str, ClassDefinitionName]] = None
    mixins: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, ClassDefinitionName], List[Union[str, ClassDefinitionName]]]] = empty_list()
    any_of: Optional[Union[Union[dict, AnonymousClassExpression], List[Union[dict, AnonymousClassExpression]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, AnonymousClassExpression], List[Union[dict, AnonymousClassExpression]]]] = empty_list()
    none_of: Optional[Union[Union[dict, AnonymousClassExpression], List[Union[dict, AnonymousClassExpression]]]] = empty_list()
    all_of: Optional[Union[Union[dict, AnonymousClassExpression], List[Union[dict, AnonymousClassExpression]]]] = empty_list()
    slot_conditions: Optional[Union[Dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], List[Union[dict, SlotDefinition]]]] = empty_dict()

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

        self._normalize_inlined_as_dict(slot_name="unique_keys", slot_type=UniqueKey, key_name="unique_key_name", keyed=True)

        if not isinstance(self.rules, list):
            self.rules = [self.rules] if self.rules is not None else []
        self.rules = [v if isinstance(v, ClassRule) else ClassRule(**as_dict(v)) for v in self.rules]

        if not isinstance(self.classification_rules, list):
            self.classification_rules = [self.classification_rules] if self.classification_rules is not None else []
        self.classification_rules = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.classification_rules]

        if self.slot_names_unique is not None and not isinstance(self.slot_names_unique, Bool):
            self.slot_names_unique = Bool(self.slot_names_unique)

        if self.represents_relationship is not None and not isinstance(self.represents_relationship, Bool):
            self.represents_relationship = Bool(self.represents_relationship)

        if not isinstance(self.disjoint_with, list):
            self.disjoint_with = [self.disjoint_with] if self.disjoint_with is not None else []
        self.disjoint_with = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.disjoint_with]

        if self.children_are_mutually_disjoint is not None and not isinstance(self.children_are_mutually_disjoint, Bool):
            self.children_are_mutually_disjoint = Bool(self.children_are_mutually_disjoint)

        if self.is_a is not None and not isinstance(self.is_a, ClassDefinitionName):
            self.is_a = ClassDefinitionName(self.is_a)

        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins] if self.mixins is not None else []
        self.mixins = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.mixins]

        if not isinstance(self.apply_to, list):
            self.apply_to = [self.apply_to] if self.apply_to is not None else []
        self.apply_to = [v if isinstance(v, ClassDefinitionName) else ClassDefinitionName(v) for v in self.apply_to]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.exactly_one_of, list):
            self.exactly_one_of = [self.exactly_one_of] if self.exactly_one_of is not None else []
        self.exactly_one_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.exactly_one_of]

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.none_of]

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, AnonymousClassExpression) else AnonymousClassExpression(**as_dict(v)) for v in self.all_of]

        self._normalize_inlined_as_dict(slot_name="slot_conditions", slot_type=SlotDefinition, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


class ClassLevelRule(YAMLRoot):
    """
    A rule that is applied to classes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ClassLevelRule
    class_class_curie: ClassVar[str] = "linkml:ClassLevelRule"
    class_name: ClassVar[str] = "class_level_rule"
    class_model_uri: ClassVar[URIRef] = LINKML.ClassLevelRule


@dataclass
class ClassRule(ClassLevelRule):
    """
    A rule that applies to instances of a class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ClassRule
    class_class_curie: ClassVar[str] = "linkml:ClassRule"
    class_name: ClassVar[str] = "class_rule"
    class_model_uri: ClassVar[URIRef] = LINKML.ClassRule

    preconditions: Optional[Union[dict, AnonymousClassExpression]] = None
    postconditions: Optional[Union[dict, AnonymousClassExpression]] = None
    elseconditions: Optional[Union[dict, AnonymousClassExpression]] = None
    bidirectional: Optional[Union[bool, Bool]] = None
    open_world: Optional[Union[bool, Bool]] = None
    rank: Optional[int] = None
    deactivated: Optional[Union[bool, Bool]] = None
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], List[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.preconditions is not None and not isinstance(self.preconditions, AnonymousClassExpression):
            self.preconditions = AnonymousClassExpression(**as_dict(self.preconditions))

        if self.postconditions is not None and not isinstance(self.postconditions, AnonymousClassExpression):
            self.postconditions = AnonymousClassExpression(**as_dict(self.postconditions))

        if self.elseconditions is not None and not isinstance(self.elseconditions, AnonymousClassExpression):
            self.elseconditions = AnonymousClassExpression(**as_dict(self.elseconditions))

        if self.bidirectional is not None and not isinstance(self.bidirectional, Bool):
            self.bidirectional = Bool(self.bidirectional)

        if self.open_world is not None and not isinstance(self.open_world, Bool):
            self.open_world = Bool(self.open_world)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if self.deactivated is not None and not isinstance(self.deactivated, Bool):
            self.deactivated = Bool(self.deactivated)

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        super().__post_init__(**kwargs)


@dataclass
class PatternExpression(YAMLRoot):
    """
    a regular expression pattern used to evaluate conformance of a string
    """
    _inherited_slots: ClassVar[List[str]] = ["syntax"]

    class_class_uri: ClassVar[URIRef] = LINKML.PatternExpression
    class_class_curie: ClassVar[str] = "linkml:PatternExpression"
    class_name: ClassVar[str] = "pattern_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.PatternExpression

    syntax: Optional[str] = None
    interpolated: Optional[Union[bool, Bool]] = None
    partial_match: Optional[Union[bool, Bool]] = None
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], List[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.syntax is not None and not isinstance(self.syntax, str):
            self.syntax = str(self.syntax)

        if self.interpolated is not None and not isinstance(self.interpolated, Bool):
            self.interpolated = Bool(self.interpolated)

        if self.partial_match is not None and not isinstance(self.partial_match, Bool):
            self.partial_match = Bool(self.partial_match)

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        super().__post_init__(**kwargs)


@dataclass
class ImportExpression(YAMLRoot):
    """
    an expression describing an import
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.ImportExpression
    class_class_curie: ClassVar[str] = "linkml:ImportExpression"
    class_name: ClassVar[str] = "import_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.ImportExpression

    import_from: Union[str, URIorCURIE] = None
    import_as: Optional[Union[str, NCName]] = None
    import_map: Optional[Union[Dict[Union[str, SettingSettingKey], Union[dict, "Setting"]], List[Union[dict, "Setting"]]]] = empty_dict()
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], List[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], List[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], List[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.import_from):
            self.MissingRequiredField("import_from")
        if not isinstance(self.import_from, URIorCURIE):
            self.import_from = URIorCURIE(self.import_from)

        if self.import_as is not None and not isinstance(self.import_as, NCName):
            self.import_as = NCName(self.import_as)

        self._normalize_inlined_as_dict(slot_name="import_map", slot_type=Setting, key_name="setting_key", keyed=True)

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        super().__post_init__(**kwargs)


@dataclass
class Setting(YAMLRoot):
    """
    assignment of a key to a value
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.Setting
    class_class_curie: ClassVar[str] = "linkml:Setting"
    class_name: ClassVar[str] = "setting"
    class_model_uri: ClassVar[URIRef] = LINKML.Setting

    setting_key: Union[str, SettingSettingKey] = None
    setting_value: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.setting_key):
            self.MissingRequiredField("setting_key")
        if not isinstance(self.setting_key, SettingSettingKey):
            self.setting_key = SettingSettingKey(self.setting_key)

        if self._is_empty(self.setting_value):
            self.MissingRequiredField("setting_value")
        if not isinstance(self.setting_value, str):
            self.setting_value = str(self.setting_value)

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
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    is_a: Optional[Union[str, PermissibleValueText]] = None
    mixins: Optional[Union[Union[str, PermissibleValueText], List[Union[str, PermissibleValueText]]]] = empty_list()
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, AltDescription]], List[Union[dict, AltDescription]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, Example], List[Union[dict, Example]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], List[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.text):
            self.MissingRequiredField("text")
        if not isinstance(self.text, PermissibleValueText):
            self.text = PermissibleValueText(self.text)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.meaning is not None and not isinstance(self.meaning, URIorCURIE):
            self.meaning = URIorCURIE(self.meaning)

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.is_a is not None and not isinstance(self.is_a, PermissibleValueText):
            self.is_a = PermissibleValueText(self.is_a)

        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins] if self.mixins is not None else []
        self.mixins = [v if isinstance(v, PermissibleValueText) else PermissibleValueText(v) for v in self.mixins]

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

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

    unique_key_name: Union[str, UniqueKeyUniqueKeyName] = None
    unique_key_slots: Union[Union[str, SlotDefinitionName], List[Union[str, SlotDefinitionName]]] = None
    extensions: Optional[Union[Dict[Union[str, ExtensionTag], Union[dict, Extension]], List[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[Dict[Union[str, AnnotationTag], Union[dict, Annotation]], List[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[Dict[Union[str, AltDescriptionSource], Union[dict, AltDescription]], List[Union[dict, AltDescription]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    examples: Optional[Union[Union[dict, Example], List[Union[dict, Example]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], List[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], List[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    rank: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.unique_key_name):
            self.MissingRequiredField("unique_key_name")
        if not isinstance(self.unique_key_name, UniqueKeyUniqueKeyName):
            self.unique_key_name = UniqueKeyUniqueKeyName(self.unique_key_name)

        if self._is_empty(self.unique_key_slots):
            self.MissingRequiredField("unique_key_slots")
        if not isinstance(self.unique_key_slots, list):
            self.unique_key_slots = [self.unique_key_slots] if self.unique_key_slots is not None else []
        self.unique_key_slots = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.unique_key_slots]

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=True)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=True)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="alt_descriptions", slot_type=AltDescription, key_name="source", keyed=True)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

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

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.in_language is not None and not isinstance(self.in_language, str):
            self.in_language = str(self.in_language)

        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also] if self.see_also is not None else []
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        self._normalize_inlined_as_dict(slot_name="structured_aliases", slot_type=StructuredAlias, key_name="literal_form", keyed=False)

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

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

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

class PresenceEnum(EnumDefinitionImpl):
    """
    enumeration of conditions by which a slot value should be set
    """
    UNCOMMITTED = PermissibleValue(text="UNCOMMITTED")
    PRESENT = PermissibleValue(text="PRESENT")
    ABSENT = PermissibleValue(text="ABSENT")

    _defn = EnumDefinition(
        name="PresenceEnum",
        description="enumeration of conditions by which a slot value should be set",
    )

class RelationalRoleEnum(EnumDefinitionImpl):
    """
    enumeration of roles a slot on a relationship class can play
    """
    SUBJECT = PermissibleValue(text="SUBJECT",
                                     description="a slot with this role connects a relationship to its subject/source node",
                                     meaning=RDF.subject)
    OBJECT = PermissibleValue(text="OBJECT",
                                   description="a slot with this role connects a relationship to its object/target node",
                                   meaning=RDF.object)
    PREDICATE = PermissibleValue(text="PREDICATE",
                                         description="a slot with this role connects a relationship to its predicate/property",
                                         meaning=RDF.predicate)
    NODE = PermissibleValue(text="NODE",
                               description="a slot with this role connects a symmetric relationship to a node that represents either subject or object node")
    OTHER_ROLE = PermissibleValue(text="OTHER_ROLE",
                                           description="a slot with this role connects a relationship to a node that is not subject/object/predicate")

    _defn = EnumDefinition(
        name="RelationalRoleEnum",
        description="enumeration of roles a slot on a relationship class can play",
    )

class AliasPredicateEnum(EnumDefinitionImpl):

    EXACT_SYNONYM = PermissibleValue(text="EXACT_SYNONYM",
                                                 meaning=SKOS.exactMatch)
    RELATED_SYNONYM = PermissibleValue(text="RELATED_SYNONYM",
                                                     meaning=SKOS.relatedMatch)
    BROAD_SYNONYM = PermissibleValue(text="BROAD_SYNONYM",
                                                 meaning=SKOS.broaderMatch)
    NARROW_SYNONYM = PermissibleValue(text="NARROW_SYNONYM",
                                                   meaning=SKOS.narrowerMatch)

    _defn = EnumDefinition(
        name="AliasPredicateEnum",
    )

# Slots

