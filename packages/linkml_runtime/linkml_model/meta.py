# Auto generated from meta.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-06-27T23:15:25
# Schema: meta
#
# id: https://w3id.org/linkml/meta
# description: The metamodel for schemas defined using the Linked Data Modeling Language framework.
#
#   For more information on LinkML:
#
#   * [linkml.io](https://linkml.io) main website
#   * [specification](https://w3id.org/linkml/docs/specification/)
#
#   LinkML is self-describing. Every LinkML schema consists of elements
#   that instantiate classes in this metamodel.
#
#   Core metaclasses:
#
#   * [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)
#   * [ClassDefinition](https://w3id.org/linkml/ClassDefinition)
#   * [SlotDefinition](https://w3id.org/linkml/SlotDefinition)
#   * [TypeDefinition](https://w3id.org/linkml/TypeDefinition)
#
#   There are many subsets of *profiles* of the metamodel, for different purposes:
#
#   * [MinimalSubset](https://w3id.org/linkml/MinimalSubset)
#   * [BasicSubset](https://w3id.org/linkml/BasicSubset)
#
#   For canonical reference documentation on any metamodel construct,
#   refer to the official URI for each construct, e.g.
#   [https://w3id.org/linkml/is_a](https://w3id.org/linkml/is_a)
# license: https://creativecommons.org/publicdomain/zero/1.0/

from jsonasobj2 import as_dict
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from linkml_runtime.utils.formatutils import sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from .annotations import Annotation, AnnotationTag
from .extensions import Extension, ExtensionTag
from .units import UnitOfMeasure
from linkml_runtime.utils.metamodelcore import Bool, NCName, URI, URIorCURIE, XSDDateTime

metamodel_version = "1.7.0"
version = None

# Namespaces
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
NCIT = CurieNamespace('NCIT', 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#')
OIO = CurieNamespace('OIO', 'http://www.geneontology.org/formats/oboInOwl#')
SIO = CurieNamespace('SIO', 'http://semanticscience.org/resource/SIO_')
BIBO = CurieNamespace('bibo', 'http://purl.org/ontology/bibo/')
CDISC = CurieNamespace('cdisc', 'http://rdf.cdisc.org/mms#')
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
SH = CurieNamespace('sh', 'http://www.w3.org/ns/shacl#')
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


class TypeMappingFramework(extended_str):
    pass


Anything = Any

@dataclass(repr=False)
class CommonMetadata(YAMLRoot):
    """
    Generic metadata shared across definitions
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["CommonMetadata"]
    class_class_curie: ClassVar[str] = "linkml:CommonMetadata"
    class_name: ClassVar[str] = "common_metadata"
    class_model_uri: ClassVar[URIRef] = LINKML.CommonMetadata

    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, "StructuredAlias"], list[Union[dict, "StructuredAlias"]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Element(YAMLRoot):
    """
    A named element in the model
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Element"]
    class_class_curie: ClassVar[str] = "linkml:Element"
    class_name: ClassVar[str] = "element"
    class_model_uri: ClassVar[URIRef] = LINKML.Element

    name: Union[str, ElementName] = None
    id_prefixes: Optional[Union[Union[str, NCName], list[Union[str, NCName]]]] = empty_list()
    id_prefixes_are_closed: Optional[Union[bool, Bool]] = None
    definition_uri: Optional[Union[str, URIorCURIE]] = None
    local_names: Optional[Union[dict[Union[str, LocalNameLocalNameSource], Union[dict, "LocalName"]], list[Union[dict, "LocalName"]]]] = empty_dict()
    conforms_to: Optional[str] = None
    implements: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    instantiates: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, "StructuredAlias"], list[Union[dict, "StructuredAlias"]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ElementName):
            self.name = ElementName(self.name)

        if not isinstance(self.id_prefixes, list):
            self.id_prefixes = [self.id_prefixes] if self.id_prefixes is not None else []
        self.id_prefixes = [v if isinstance(v, NCName) else NCName(v) for v in self.id_prefixes]

        if self.id_prefixes_are_closed is not None and not isinstance(self.id_prefixes_are_closed, Bool):
            self.id_prefixes_are_closed = Bool(self.id_prefixes_are_closed)

        if self.definition_uri is not None and not isinstance(self.definition_uri, URIorCURIE):
            self.definition_uri = URIorCURIE(self.definition_uri)

        self._normalize_inlined_as_dict(slot_name="local_names", slot_type=LocalName, key_name="local_name_source", keyed=True)

        if self.conforms_to is not None and not isinstance(self.conforms_to, str):
            self.conforms_to = str(self.conforms_to)

        if not isinstance(self.implements, list):
            self.implements = [self.implements] if self.implements is not None else []
        self.implements = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.implements]

        if not isinstance(self.instantiates, list):
            self.instantiates = [self.instantiates] if self.instantiates is not None else []
        self.instantiates = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.instantiates]

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SchemaDefinition(Element):
    """
    A collection of definitions that make up a schema or a data model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["SchemaDefinition"]
    class_class_curie: ClassVar[str] = "linkml:SchemaDefinition"
    class_name: ClassVar[str] = "schema_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.SchemaDefinition

    name: Union[str, SchemaDefinitionName] = None
    id: Union[str, URI] = None
    version: Optional[str] = None
    imports: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    license: Optional[str] = None
    prefixes: Optional[Union[dict[Union[str, PrefixPrefixPrefix], Union[dict, "Prefix"]], list[Union[dict, "Prefix"]]]] = empty_dict()
    emit_prefixes: Optional[Union[Union[str, NCName], list[Union[str, NCName]]]] = empty_list()
    default_curi_maps: Optional[Union[str, list[str]]] = empty_list()
    default_prefix: Optional[str] = None
    default_range: Optional[Union[str, TypeDefinitionName]] = None
    subsets: Optional[Union[dict[Union[str, SubsetDefinitionName], Union[dict, "SubsetDefinition"]], list[Union[dict, "SubsetDefinition"]]]] = empty_dict()
    types: Optional[Union[dict[Union[str, TypeDefinitionName], Union[dict, "TypeDefinition"]], list[Union[dict, "TypeDefinition"]]]] = empty_dict()
    enums: Optional[Union[dict[Union[str, EnumDefinitionName], Union[dict, "EnumDefinition"]], list[Union[dict, "EnumDefinition"]]]] = empty_dict()
    slots: Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, "SlotDefinition"]], list[Union[dict, "SlotDefinition"]]]] = empty_dict()
    classes: Optional[Union[dict[Union[str, ClassDefinitionName], Union[dict, "ClassDefinition"]], list[Union[dict, "ClassDefinition"]]]] = empty_dict()
    metamodel_version: Optional[str] = None
    source_file: Optional[str] = None
    source_file_date: Optional[Union[str, XSDDateTime]] = None
    source_file_size: Optional[int] = None
    generation_date: Optional[Union[str, XSDDateTime]] = None
    slot_names_unique: Optional[Union[bool, Bool]] = None
    settings: Optional[Union[dict[Union[str, SettingSettingKey], Union[dict, "Setting"]], list[Union[dict, "Setting"]]]] = empty_dict()
    bindings: Optional[Union[Union[dict, "EnumBinding"], list[Union[dict, "EnumBinding"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if not isinstance(self.bindings, list):
            self.bindings = [self.bindings] if self.bindings is not None else []
        self.bindings = [v if isinstance(v, EnumBinding) else EnumBinding(**as_dict(v)) for v in self.bindings]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnonymousTypeExpression(YAMLRoot):
    """
    A type expression that is not a top-level named type definition. Used for nesting.
    """
    _inherited_slots: ClassVar[list[str]] = ["pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "minimum_value", "maximum_value"]

    class_class_uri: ClassVar[URIRef] = LINKML["AnonymousTypeExpression"]
    class_class_curie: ClassVar[str] = "linkml:AnonymousTypeExpression"
    class_name: ClassVar[str] = "anonymous_type_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousTypeExpression

    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, list[str]]] = empty_list()
    equals_number: Optional[int] = None
    minimum_value: Optional[Union[dict, Anything]] = None
    maximum_value: Optional[Union[dict, Anything]] = None
    none_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class TypeDefinition(Element):
    """
    an element that whose instances are atomic scalar values that can be mapped to primitive types
    """
    _inherited_slots: ClassVar[list[str]] = ["base", "uri", "repr", "pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "minimum_value", "maximum_value"]

    class_class_uri: ClassVar[URIRef] = LINKML["TypeDefinition"]
    class_class_curie: ClassVar[str] = "linkml:TypeDefinition"
    class_name: ClassVar[str] = "type_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.TypeDefinition

    name: Union[str, TypeDefinitionName] = None
    typeof: Optional[Union[str, TypeDefinitionName]] = None
    base: Optional[str] = None
    uri: Optional[Union[str, URIorCURIE]] = None
    repr: Optional[str] = None
    union_of: Optional[Union[Union[str, TypeDefinitionName], list[Union[str, TypeDefinitionName]]]] = empty_list()
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, list[str]]] = empty_list()
    equals_number: Optional[int] = None
    minimum_value: Optional[Union[dict, Anything]] = None
    maximum_value: Optional[Union[dict, Anything]] = None
    none_of: Optional[Union[Union[dict, AnonymousTypeExpression], list[Union[dict, AnonymousTypeExpression]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, AnonymousTypeExpression], list[Union[dict, AnonymousTypeExpression]]]] = empty_list()
    any_of: Optional[Union[Union[dict, AnonymousTypeExpression], list[Union[dict, AnonymousTypeExpression]]]] = empty_list()
    all_of: Optional[Union[Union[dict, AnonymousTypeExpression], list[Union[dict, AnonymousTypeExpression]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class SubsetDefinition(Element):
    """
    an element that can be used to group other metamodel elements
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["SubsetDefinition"]
    class_class_curie: ClassVar[str] = "linkml:SubsetDefinition"
    class_name: ClassVar[str] = "subset_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.SubsetDefinition

    name: Union[str, SubsetDefinitionName] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, SubsetDefinitionName):
            self.name = SubsetDefinitionName(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Definition(Element):
    """
    abstract base class for core metaclasses
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Definition"]
    class_class_curie: ClassVar[str] = "linkml:Definition"
    class_name: ClassVar[str] = "definition"
    class_model_uri: ClassVar[URIRef] = LINKML.Definition

    name: Union[str, DefinitionName] = None
    is_a: Optional[Union[str, DefinitionName]] = None
    abstract: Optional[Union[bool, Bool]] = None
    mixin: Optional[Union[bool, Bool]] = None
    mixins: Optional[Union[Union[str, DefinitionName], list[Union[str, DefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, DefinitionName], list[Union[str, DefinitionName]]]] = empty_list()
    values_from: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    string_serialization: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.string_serialization is not None and not isinstance(self.string_serialization, str):
            self.string_serialization = str(self.string_serialization)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnonymousEnumExpression(YAMLRoot):
    """
    An enum_expression that is not named
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["AnonymousEnumExpression"]
    class_class_curie: ClassVar[str] = "linkml:AnonymousEnumExpression"
    class_name: ClassVar[str] = "anonymous_enum_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousEnumExpression

    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], list[Union[dict, "PermissibleValue"]]]] = empty_dict()
    include: Optional[Union[Union[dict, "AnonymousEnumExpression"], list[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    minus: Optional[Union[Union[dict, "AnonymousEnumExpression"], list[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    inherits: Optional[Union[Union[str, EnumDefinitionName], list[Union[str, EnumDefinitionName]]]] = empty_list()
    reachable_from: Optional[Union[dict, "ReachabilityQuery"]] = None
    matches: Optional[Union[dict, "MatchQuery"]] = None
    concepts: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class EnumDefinition(Definition):
    """
    an element whose instances must be drawn from a specified set of permissible values
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["EnumDefinition"]
    class_class_curie: ClassVar[str] = "linkml:EnumDefinition"
    class_name: ClassVar[str] = "enum_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.EnumDefinition

    name: Union[str, EnumDefinitionName] = None
    enum_uri: Optional[Union[str, URIorCURIE]] = None
    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], list[Union[dict, "PermissibleValue"]]]] = empty_dict()
    include: Optional[Union[Union[dict, AnonymousEnumExpression], list[Union[dict, AnonymousEnumExpression]]]] = empty_list()
    minus: Optional[Union[Union[dict, AnonymousEnumExpression], list[Union[dict, AnonymousEnumExpression]]]] = empty_list()
    inherits: Optional[Union[Union[str, EnumDefinitionName], list[Union[str, EnumDefinitionName]]]] = empty_list()
    reachable_from: Optional[Union[dict, "ReachabilityQuery"]] = None
    matches: Optional[Union[dict, "MatchQuery"]] = None
    concepts: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class EnumBinding(YAMLRoot):
    """
    A binding of a slot or a class to a permissible value from an enumeration.
    """
    _inherited_slots: ClassVar[list[str]] = ["range"]

    class_class_uri: ClassVar[URIRef] = LINKML["EnumBinding"]
    class_class_curie: ClassVar[str] = "linkml:EnumBinding"
    class_name: ClassVar[str] = "enum_binding"
    class_model_uri: ClassVar[URIRef] = LINKML.EnumBinding

    range: Optional[Union[str, EnumDefinitionName]] = None
    obligation_level: Optional[Union[str, "ObligationLevelEnum"]] = None
    binds_value_of: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, "StructuredAlias"], list[Union[dict, "StructuredAlias"]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.range is not None and not isinstance(self.range, EnumDefinitionName):
            self.range = EnumDefinitionName(self.range)

        if self.obligation_level is not None and not isinstance(self.obligation_level, ObligationLevelEnum):
            self.obligation_level = ObligationLevelEnum(self.obligation_level)

        if self.binds_value_of is not None and not isinstance(self.binds_value_of, str):
            self.binds_value_of = str(self.binds_value_of)

        if self.pv_formula is not None and not isinstance(self.pv_formula, PvFormulaOptions):
            self.pv_formula = PvFormulaOptions(self.pv_formula)

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MatchQuery(YAMLRoot):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that
    matches on properties of the external concepts.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["MatchQuery"]
    class_class_curie: ClassVar[str] = "linkml:MatchQuery"
    class_name: ClassVar[str] = "match_query"
    class_model_uri: ClassVar[URIRef] = LINKML.MatchQuery

    identifier_pattern: Optional[str] = None
    source_ontology: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.identifier_pattern is not None and not isinstance(self.identifier_pattern, str):
            self.identifier_pattern = str(self.identifier_pattern)

        if self.source_ontology is not None and not isinstance(self.source_ontology, URIorCURIE):
            self.source_ontology = URIorCURIE(self.source_ontology)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReachabilityQuery(YAMLRoot):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a
    set of source nodes to a set of descendants or ancestors over a set of relationship types.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ReachabilityQuery"]
    class_class_curie: ClassVar[str] = "linkml:ReachabilityQuery"
    class_name: ClassVar[str] = "reachability_query"
    class_model_uri: ClassVar[URIRef] = LINKML.ReachabilityQuery

    source_ontology: Optional[Union[str, URIorCURIE]] = None
    source_nodes: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    relationship_types: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    is_direct: Optional[Union[bool, Bool]] = None
    include_self: Optional[Union[bool, Bool]] = None
    traverse_up: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class StructuredAlias(YAMLRoot):
    """
    object that contains meta data about a synonym or alias including where it came from (source) and its scope
    (narrow, broad, etc.)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOSXL["Label"]
    class_class_curie: ClassVar[str] = "skosxl:Label"
    class_name: ClassVar[str] = "structured_alias"
    class_model_uri: ClassVar[URIRef] = LINKML.StructuredAlias

    literal_form: str = None
    predicate: Optional[Union[str, "AliasPredicateEnum"]] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    contexts: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, "StructuredAlias"], list[Union[dict, "StructuredAlias"]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.literal_form):
            self.MissingRequiredField("literal_form")
        if not isinstance(self.literal_form, str):
            self.literal_form = str(self.literal_form)

        if self.predicate is not None and not isinstance(self.predicate, AliasPredicateEnum):
            self.predicate = AliasPredicateEnum(self.predicate)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.contexts, list):
            self.contexts = [self.contexts] if self.contexts is not None else []
        self.contexts = [v if isinstance(v, URI) else URI(v) for v in self.contexts]

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


class Expression(YAMLRoot):
    """
    general mixin for any class that can represent some form of expression
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Expression"]
    class_class_curie: ClassVar[str] = "linkml:Expression"
    class_name: ClassVar[str] = "expression"
    class_model_uri: ClassVar[URIRef] = LINKML.Expression


@dataclass(repr=False)
class TypeExpression(Expression):
    """
    An abstract class grouping named types and anonymous type expressions
    """
    _inherited_slots: ClassVar[list[str]] = ["pattern", "structured_pattern", "equals_string", "equals_string_in", "equals_number", "minimum_value", "maximum_value"]

    class_class_uri: ClassVar[URIRef] = LINKML["TypeExpression"]
    class_class_curie: ClassVar[str] = "linkml:TypeExpression"
    class_name: ClassVar[str] = "type_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.TypeExpression

    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, list[str]]] = empty_list()
    equals_number: Optional[int] = None
    minimum_value: Optional[Union[dict, Anything]] = None
    maximum_value: Optional[Union[dict, Anything]] = None
    none_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class EnumExpression(Expression):
    """
    An expression that constrains the range of a slot
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["EnumExpression"]
    class_class_curie: ClassVar[str] = "linkml:EnumExpression"
    class_name: ClassVar[str] = "enum_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.EnumExpression

    code_set: Optional[Union[str, URIorCURIE]] = None
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None
    permissible_values: Optional[Union[dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], list[Union[dict, "PermissibleValue"]]]] = empty_dict()
    include: Optional[Union[Union[dict, "AnonymousEnumExpression"], list[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    minus: Optional[Union[Union[dict, "AnonymousEnumExpression"], list[Union[dict, "AnonymousEnumExpression"]]]] = empty_list()
    inherits: Optional[Union[Union[str, EnumDefinitionName], list[Union[str, EnumDefinitionName]]]] = empty_list()
    reachable_from: Optional[Union[dict, "ReachabilityQuery"]] = None
    matches: Optional[Union[dict, "MatchQuery"]] = None
    concepts: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class AnonymousExpression(YAMLRoot):
    """
    An abstract parent class for any nested expression
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["AnonymousExpression"]
    class_class_curie: ClassVar[str] = "linkml:AnonymousExpression"
    class_name: ClassVar[str] = "anonymous_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousExpression

    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PathExpression(YAMLRoot):
    """
    An expression that describes an abstract path from an object to another through a sequence of slot lookups
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["PathExpression"]
    class_class_curie: ClassVar[str] = "linkml:PathExpression"
    class_name: ClassVar[str] = "path_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.PathExpression

    followed_by: Optional[Union[dict, "PathExpression"]] = None
    none_of: Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]] = empty_list()
    reversed: Optional[Union[bool, Bool]] = None
    traverse: Optional[Union[str, SlotDefinitionName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SlotExpression(Expression):
    """
    an expression that constrains the range of values a slot can take
    """
    _inherited_slots: ClassVar[list[str]] = ["range", "required", "recommended", "multivalued", "inlined", "inlined_as_list", "minimum_value", "maximum_value", "pattern", "structured_pattern", "value_presence", "equals_string", "equals_string_in", "equals_number", "equals_expression", "exact_cardinality", "minimum_cardinality", "maximum_cardinality"]

    class_class_uri: ClassVar[URIRef] = LINKML["SlotExpression"]
    class_class_curie: ClassVar[str] = "linkml:SlotExpression"
    class_name: ClassVar[str] = "slot_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.SlotExpression

    range: Optional[Union[str, ElementName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    enum_range: Optional[Union[dict, EnumExpression]] = None
    bindings: Optional[Union[Union[dict, EnumBinding], list[Union[dict, EnumBinding]]]] = empty_list()
    required: Optional[Union[bool, Bool]] = None
    recommended: Optional[Union[bool, Bool]] = None
    multivalued: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    minimum_value: Optional[Union[dict, Anything]] = None
    maximum_value: Optional[Union[dict, Anything]] = None
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    value_presence: Optional[Union[str, "PresenceEnum"]] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, list[str]]] = empty_list()
    equals_number: Optional[int] = None
    equals_expression: Optional[str] = None
    exact_cardinality: Optional[int] = None
    minimum_cardinality: Optional[int] = None
    maximum_cardinality: Optional[int] = None
    has_member: Optional[Union[dict, "AnonymousSlotExpression"]] = None
    all_members: Optional[Union[dict, "AnonymousSlotExpression"]] = None
    none_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.range is not None and not isinstance(self.range, ElementName):
            self.range = ElementName(self.range)

        if self.range_expression is not None and not isinstance(self.range_expression, AnonymousClassExpression):
            self.range_expression = AnonymousClassExpression(**as_dict(self.range_expression))

        if self.enum_range is not None and not isinstance(self.enum_range, EnumExpression):
            self.enum_range = EnumExpression(**as_dict(self.enum_range))

        if not isinstance(self.bindings, list):
            self.bindings = [self.bindings] if self.bindings is not None else []
        self.bindings = [v if isinstance(v, EnumBinding) else EnumBinding(**as_dict(v)) for v in self.bindings]

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if self.recommended is not None and not isinstance(self.recommended, Bool):
            self.recommended = Bool(self.recommended)

        if self.multivalued is not None and not isinstance(self.multivalued, Bool):
            self.multivalued = Bool(self.multivalued)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.value_presence is not None and not isinstance(self.value_presence, PresenceEnum):
            self.value_presence = PresenceEnum(self.value_presence)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.equals_expression is not None and not isinstance(self.equals_expression, str):
            self.equals_expression = str(self.equals_expression)

        if self.exact_cardinality is not None and not isinstance(self.exact_cardinality, int):
            self.exact_cardinality = int(self.exact_cardinality)

        if self.minimum_cardinality is not None and not isinstance(self.minimum_cardinality, int):
            self.minimum_cardinality = int(self.minimum_cardinality)

        if self.maximum_cardinality is not None and not isinstance(self.maximum_cardinality, int):
            self.maximum_cardinality = int(self.maximum_cardinality)

        if self.has_member is not None and not isinstance(self.has_member, AnonymousSlotExpression):
            self.has_member = AnonymousSlotExpression(**as_dict(self.has_member))

        if self.all_members is not None and not isinstance(self.all_members, AnonymousSlotExpression):
            self.all_members = AnonymousSlotExpression(**as_dict(self.all_members))

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


@dataclass(repr=False)
class AnonymousSlotExpression(AnonymousExpression):
    _inherited_slots: ClassVar[list[str]] = ["range", "required", "recommended", "multivalued", "inlined", "inlined_as_list", "minimum_value", "maximum_value", "pattern", "structured_pattern", "value_presence", "equals_string", "equals_string_in", "equals_number", "equals_expression", "exact_cardinality", "minimum_cardinality", "maximum_cardinality"]

    class_class_uri: ClassVar[URIRef] = LINKML["AnonymousSlotExpression"]
    class_class_curie: ClassVar[str] = "linkml:AnonymousSlotExpression"
    class_name: ClassVar[str] = "anonymous_slot_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousSlotExpression

    range: Optional[Union[str, ElementName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    enum_range: Optional[Union[dict, EnumExpression]] = None
    bindings: Optional[Union[Union[dict, EnumBinding], list[Union[dict, EnumBinding]]]] = empty_list()
    required: Optional[Union[bool, Bool]] = None
    recommended: Optional[Union[bool, Bool]] = None
    multivalued: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    minimum_value: Optional[Union[dict, Anything]] = None
    maximum_value: Optional[Union[dict, Anything]] = None
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    value_presence: Optional[Union[str, "PresenceEnum"]] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, list[str]]] = empty_list()
    equals_number: Optional[int] = None
    equals_expression: Optional[str] = None
    exact_cardinality: Optional[int] = None
    minimum_cardinality: Optional[int] = None
    maximum_cardinality: Optional[int] = None
    has_member: Optional[Union[dict, "AnonymousSlotExpression"]] = None
    all_members: Optional[Union[dict, "AnonymousSlotExpression"]] = None
    none_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.range is not None and not isinstance(self.range, ElementName):
            self.range = ElementName(self.range)

        if self.range_expression is not None and not isinstance(self.range_expression, AnonymousClassExpression):
            self.range_expression = AnonymousClassExpression(**as_dict(self.range_expression))

        if self.enum_range is not None and not isinstance(self.enum_range, EnumExpression):
            self.enum_range = EnumExpression(**as_dict(self.enum_range))

        if not isinstance(self.bindings, list):
            self.bindings = [self.bindings] if self.bindings is not None else []
        self.bindings = [v if isinstance(v, EnumBinding) else EnumBinding(**as_dict(v)) for v in self.bindings]

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if self.recommended is not None and not isinstance(self.recommended, Bool):
            self.recommended = Bool(self.recommended)

        if self.multivalued is not None and not isinstance(self.multivalued, Bool):
            self.multivalued = Bool(self.multivalued)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.value_presence is not None and not isinstance(self.value_presence, PresenceEnum):
            self.value_presence = PresenceEnum(self.value_presence)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.equals_expression is not None and not isinstance(self.equals_expression, str):
            self.equals_expression = str(self.equals_expression)

        if self.exact_cardinality is not None and not isinstance(self.exact_cardinality, int):
            self.exact_cardinality = int(self.exact_cardinality)

        if self.minimum_cardinality is not None and not isinstance(self.minimum_cardinality, int):
            self.minimum_cardinality = int(self.minimum_cardinality)

        if self.maximum_cardinality is not None and not isinstance(self.maximum_cardinality, int):
            self.maximum_cardinality = int(self.maximum_cardinality)

        if self.has_member is not None and not isinstance(self.has_member, AnonymousSlotExpression):
            self.has_member = AnonymousSlotExpression(**as_dict(self.has_member))

        if self.all_members is not None and not isinstance(self.all_members, AnonymousSlotExpression):
            self.all_members = AnonymousSlotExpression(**as_dict(self.all_members))

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


@dataclass(repr=False)
class SlotDefinition(Definition):
    """
    an element that describes how instances are related to other instances
    """
    _inherited_slots: ClassVar[list[str]] = ["domain", "array", "inherited", "readonly", "ifabsent", "list_elements_unique", "list_elements_ordered", "shared", "key", "identifier", "designates_type", "role", "relational_role", "range", "required", "recommended", "multivalued", "inlined", "inlined_as_list", "minimum_value", "maximum_value", "pattern", "structured_pattern", "value_presence", "equals_string", "equals_string_in", "equals_number", "equals_expression", "exact_cardinality", "minimum_cardinality", "maximum_cardinality"]

    class_class_uri: ClassVar[URIRef] = LINKML["SlotDefinition"]
    class_class_curie: ClassVar[str] = "linkml:SlotDefinition"
    class_name: ClassVar[str] = "slot_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.SlotDefinition

    name: Union[str, SlotDefinitionName] = None
    singular_name: Optional[str] = None
    domain: Optional[Union[str, ClassDefinitionName]] = None
    slot_uri: Optional[Union[str, URIorCURIE]] = None
    array: Optional[Union[dict, "ArrayExpression"]] = None
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
    domain_of: Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]] = empty_list()
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
    disjoint_with: Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]] = empty_list()
    children_are_mutually_disjoint: Optional[Union[bool, Bool]] = None
    union_of: Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]] = empty_list()
    type_mappings: Optional[Union[Union[str, TypeMappingFramework], list[Union[str, TypeMappingFramework]]]] = empty_list()
    is_a: Optional[Union[str, SlotDefinitionName]] = None
    mixins: Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]] = empty_list()
    range: Optional[Union[str, ElementName]] = None
    range_expression: Optional[Union[dict, "AnonymousClassExpression"]] = None
    enum_range: Optional[Union[dict, EnumExpression]] = None
    bindings: Optional[Union[Union[dict, EnumBinding], list[Union[dict, EnumBinding]]]] = empty_list()
    required: Optional[Union[bool, Bool]] = None
    recommended: Optional[Union[bool, Bool]] = None
    multivalued: Optional[Union[bool, Bool]] = None
    inlined: Optional[Union[bool, Bool]] = None
    inlined_as_list: Optional[Union[bool, Bool]] = None
    minimum_value: Optional[Union[dict, Anything]] = None
    maximum_value: Optional[Union[dict, Anything]] = None
    pattern: Optional[str] = None
    structured_pattern: Optional[Union[dict, "PatternExpression"]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    implicit_prefix: Optional[str] = None
    value_presence: Optional[Union[str, "PresenceEnum"]] = None
    equals_string: Optional[str] = None
    equals_string_in: Optional[Union[str, list[str]]] = empty_list()
    equals_number: Optional[int] = None
    equals_expression: Optional[str] = None
    exact_cardinality: Optional[int] = None
    minimum_cardinality: Optional[int] = None
    maximum_cardinality: Optional[int] = None
    has_member: Optional[Union[dict, AnonymousSlotExpression]] = None
    all_members: Optional[Union[dict, AnonymousSlotExpression]] = None
    none_of: Optional[Union[Union[dict, AnonymousSlotExpression], list[Union[dict, AnonymousSlotExpression]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, AnonymousSlotExpression], list[Union[dict, AnonymousSlotExpression]]]] = empty_list()
    any_of: Optional[Union[Union[dict, AnonymousSlotExpression], list[Union[dict, AnonymousSlotExpression]]]] = empty_list()
    all_of: Optional[Union[Union[dict, AnonymousSlotExpression], list[Union[dict, AnonymousSlotExpression]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.array is not None and not isinstance(self.array, ArrayExpression):
            self.array = ArrayExpression(**as_dict(self.array))

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
        self.union_of = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.union_of]

        if not isinstance(self.type_mappings, list):
            self.type_mappings = [self.type_mappings] if self.type_mappings is not None else []
        self.type_mappings = [v if isinstance(v, TypeMappingFramework) else TypeMappingFramework(v) for v in self.type_mappings]

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

        if not isinstance(self.bindings, list):
            self.bindings = [self.bindings] if self.bindings is not None else []
        self.bindings = [v if isinstance(v, EnumBinding) else EnumBinding(**as_dict(v)) for v in self.bindings]

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if self.recommended is not None and not isinstance(self.recommended, Bool):
            self.recommended = Bool(self.recommended)

        if self.multivalued is not None and not isinstance(self.multivalued, Bool):
            self.multivalued = Bool(self.multivalued)

        if self.inlined is not None and not isinstance(self.inlined, Bool):
            self.inlined = Bool(self.inlined)

        if self.inlined_as_list is not None and not isinstance(self.inlined_as_list, Bool):
            self.inlined_as_list = Bool(self.inlined_as_list)

        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.structured_pattern is not None and not isinstance(self.structured_pattern, PatternExpression):
            self.structured_pattern = PatternExpression(**as_dict(self.structured_pattern))

        if self.unit is not None and not isinstance(self.unit, UnitOfMeasure):
            self.unit = UnitOfMeasure(**as_dict(self.unit))

        if self.implicit_prefix is not None and not isinstance(self.implicit_prefix, str):
            self.implicit_prefix = str(self.implicit_prefix)

        if self.value_presence is not None and not isinstance(self.value_presence, PresenceEnum):
            self.value_presence = PresenceEnum(self.value_presence)

        if self.equals_string is not None and not isinstance(self.equals_string, str):
            self.equals_string = str(self.equals_string)

        if not isinstance(self.equals_string_in, list):
            self.equals_string_in = [self.equals_string_in] if self.equals_string_in is not None else []
        self.equals_string_in = [v if isinstance(v, str) else str(v) for v in self.equals_string_in]

        if self.equals_number is not None and not isinstance(self.equals_number, int):
            self.equals_number = int(self.equals_number)

        if self.equals_expression is not None and not isinstance(self.equals_expression, str):
            self.equals_expression = str(self.equals_expression)

        if self.exact_cardinality is not None and not isinstance(self.exact_cardinality, int):
            self.exact_cardinality = int(self.exact_cardinality)

        if self.minimum_cardinality is not None and not isinstance(self.minimum_cardinality, int):
            self.minimum_cardinality = int(self.minimum_cardinality)

        if self.maximum_cardinality is not None and not isinstance(self.maximum_cardinality, int):
            self.maximum_cardinality = int(self.maximum_cardinality)

        if self.has_member is not None and not isinstance(self.has_member, AnonymousSlotExpression):
            self.has_member = AnonymousSlotExpression(**as_dict(self.has_member))

        if self.all_members is not None and not isinstance(self.all_members, AnonymousSlotExpression):
            self.all_members = AnonymousSlotExpression(**as_dict(self.all_members))

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


@dataclass(repr=False)
class ClassExpression(YAMLRoot):
    """
    A boolean expression that can be used to dynamically determine membership of a class
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassExpression"]
    class_class_curie: ClassVar[str] = "linkml:ClassExpression"
    class_name: ClassVar[str] = "class_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.ClassExpression

    any_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    none_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    slot_conditions: Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class AnonymousClassExpression(AnonymousExpression):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["AnonymousClassExpression"]
    class_class_curie: ClassVar[str] = "linkml:AnonymousClassExpression"
    class_name: ClassVar[str] = "anonymous_class_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.AnonymousClassExpression

    is_a: Optional[Union[str, DefinitionName]] = None
    any_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    none_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    all_of: Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]] = empty_list()
    slot_conditions: Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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


@dataclass(repr=False)
class ClassDefinition(Definition):
    """
    an element whose instances are complex objects that may have slot-value assignments
    """
    _inherited_slots: ClassVar[list[str]] = ["defining_slots", "represents_relationship"]

    class_class_uri: ClassVar[URIRef] = LINKML["ClassDefinition"]
    class_class_curie: ClassVar[str] = "linkml:ClassDefinition"
    class_name: ClassVar[str] = "class_definition"
    class_model_uri: ClassVar[URIRef] = LINKML.ClassDefinition

    name: Union[str, ClassDefinitionName] = None
    slots: Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]] = empty_list()
    slot_usage: Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]] = empty_dict()
    attributes: Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]] = empty_dict()
    class_uri: Optional[Union[str, URIorCURIE]] = None
    subclass_of: Optional[Union[str, URIorCURIE]] = None
    union_of: Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]] = empty_list()
    defining_slots: Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]] = empty_list()
    tree_root: Optional[Union[bool, Bool]] = None
    unique_keys: Optional[Union[dict[Union[str, UniqueKeyUniqueKeyName], Union[dict, "UniqueKey"]], list[Union[dict, "UniqueKey"]]]] = empty_dict()
    rules: Optional[Union[Union[dict, "ClassRule"], list[Union[dict, "ClassRule"]]]] = empty_list()
    classification_rules: Optional[Union[Union[dict, AnonymousClassExpression], list[Union[dict, AnonymousClassExpression]]]] = empty_list()
    slot_names_unique: Optional[Union[bool, Bool]] = None
    represents_relationship: Optional[Union[bool, Bool]] = None
    disjoint_with: Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]] = empty_list()
    children_are_mutually_disjoint: Optional[Union[bool, Bool]] = None
    is_a: Optional[Union[str, ClassDefinitionName]] = None
    mixins: Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]] = empty_list()
    apply_to: Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]] = empty_list()
    any_of: Optional[Union[Union[dict, AnonymousClassExpression], list[Union[dict, AnonymousClassExpression]]]] = empty_list()
    exactly_one_of: Optional[Union[Union[dict, AnonymousClassExpression], list[Union[dict, AnonymousClassExpression]]]] = empty_list()
    none_of: Optional[Union[Union[dict, AnonymousClassExpression], list[Union[dict, AnonymousClassExpression]]]] = empty_list()
    all_of: Optional[Union[Union[dict, AnonymousClassExpression], list[Union[dict, AnonymousClassExpression]]]] = empty_list()
    slot_conditions: Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassLevelRule"]
    class_class_curie: ClassVar[str] = "linkml:ClassLevelRule"
    class_name: ClassVar[str] = "class_level_rule"
    class_model_uri: ClassVar[URIRef] = LINKML.ClassLevelRule


@dataclass(repr=False)
class ClassRule(ClassLevelRule):
    """
    A rule that applies to instances of a class
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ClassRule"]
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
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ArrayExpression(YAMLRoot):
    """
    defines the dimensions of an array
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ArrayExpression"]
    class_class_curie: ClassVar[str] = "linkml:ArrayExpression"
    class_name: ClassVar[str] = "array_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.ArrayExpression

    exact_number_dimensions: Optional[int] = None
    minimum_number_dimensions: Optional[int] = None
    maximum_number_dimensions: Optional[Union[dict, Anything]] = None
    dimensions: Optional[Union[Union[dict, "DimensionExpression"], list[Union[dict, "DimensionExpression"]]]] = empty_list()
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.exact_number_dimensions is not None and not isinstance(self.exact_number_dimensions, int):
            self.exact_number_dimensions = int(self.exact_number_dimensions)

        if self.minimum_number_dimensions is not None and not isinstance(self.minimum_number_dimensions, int):
            self.minimum_number_dimensions = int(self.minimum_number_dimensions)

        if not isinstance(self.dimensions, list):
            self.dimensions = [self.dimensions] if self.dimensions is not None else []
        self.dimensions = [v if isinstance(v, DimensionExpression) else DimensionExpression(**as_dict(v)) for v in self.dimensions]

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DimensionExpression(YAMLRoot):
    """
    defines one of the dimensions of an array
    """
    _inherited_slots: ClassVar[list[str]] = ["maximum_cardinality", "minimum_cardinality", "exact_cardinality"]

    class_class_uri: ClassVar[URIRef] = LINKML["DimensionExpression"]
    class_class_curie: ClassVar[str] = "linkml:DimensionExpression"
    class_name: ClassVar[str] = "dimension_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.DimensionExpression

    alias: Optional[str] = None
    maximum_cardinality: Optional[int] = None
    minimum_cardinality: Optional[int] = None
    exact_cardinality: Optional[int] = None
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.alias is not None and not isinstance(self.alias, str):
            self.alias = str(self.alias)

        if self.maximum_cardinality is not None and not isinstance(self.maximum_cardinality, int):
            self.maximum_cardinality = int(self.maximum_cardinality)

        if self.minimum_cardinality is not None and not isinstance(self.minimum_cardinality, int):
            self.minimum_cardinality = int(self.minimum_cardinality)

        if self.exact_cardinality is not None and not isinstance(self.exact_cardinality, int):
            self.exact_cardinality = int(self.exact_cardinality)

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PatternExpression(YAMLRoot):
    """
    a regular expression pattern used to evaluate conformance of a string
    """
    _inherited_slots: ClassVar[list[str]] = ["syntax"]

    class_class_uri: ClassVar[URIRef] = LINKML["PatternExpression"]
    class_class_curie: ClassVar[str] = "linkml:PatternExpression"
    class_name: ClassVar[str] = "pattern_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.PatternExpression

    syntax: Optional[str] = None
    interpolated: Optional[Union[bool, Bool]] = None
    partial_match: Optional[Union[bool, Bool]] = None
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ImportExpression(YAMLRoot):
    """
    an expression describing an import
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["ImportExpression"]
    class_class_curie: ClassVar[str] = "linkml:ImportExpression"
    class_name: ClassVar[str] = "import_expression"
    class_model_uri: ClassVar[URIRef] = LINKML.ImportExpression

    import_from: Union[str, URIorCURIE] = None
    import_as: Optional[Union[str, NCName]] = None
    import_map: Optional[Union[dict[Union[str, SettingSettingKey], Union[dict, "Setting"]], list[Union[dict, "Setting"]]]] = empty_dict()
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Setting(YAMLRoot):
    """
    assignment of a key to a value
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Setting"]
    class_class_curie: ClassVar[str] = "linkml:Setting"
    class_name: ClassVar[str] = "setting"
    class_model_uri: ClassVar[URIRef] = LINKML.Setting

    setting_key: Union[str, SettingSettingKey] = None
    setting_value: str = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.setting_key):
            self.MissingRequiredField("setting_key")
        if not isinstance(self.setting_key, SettingSettingKey):
            self.setting_key = SettingSettingKey(self.setting_key)

        if self._is_empty(self.setting_value):
            self.MissingRequiredField("setting_value")
        if not isinstance(self.setting_value, str):
            self.setting_value = str(self.setting_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Prefix(YAMLRoot):
    """
    prefix URI tuple
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Prefix"]
    class_class_curie: ClassVar[str] = "linkml:Prefix"
    class_name: ClassVar[str] = "prefix"
    class_model_uri: ClassVar[URIRef] = LINKML.Prefix

    prefix_prefix: Union[str, PrefixPrefixPrefix] = None
    prefix_reference: Union[str, URI] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.prefix_prefix):
            self.MissingRequiredField("prefix_prefix")
        if not isinstance(self.prefix_prefix, PrefixPrefixPrefix):
            self.prefix_prefix = PrefixPrefixPrefix(self.prefix_prefix)

        if self._is_empty(self.prefix_reference):
            self.MissingRequiredField("prefix_reference")
        if not isinstance(self.prefix_reference, URI):
            self.prefix_reference = URI(self.prefix_reference)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LocalName(YAMLRoot):
    """
    an attributed label
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["LocalName"]
    class_class_curie: ClassVar[str] = "linkml:LocalName"
    class_name: ClassVar[str] = "local_name"
    class_model_uri: ClassVar[URIRef] = LINKML.LocalName

    local_name_source: Union[str, LocalNameLocalNameSource] = None
    local_name_value: str = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.local_name_source):
            self.MissingRequiredField("local_name_source")
        if not isinstance(self.local_name_source, LocalNameLocalNameSource):
            self.local_name_source = LocalNameLocalNameSource(self.local_name_source)

        if self._is_empty(self.local_name_value):
            self.MissingRequiredField("local_name_value")
        if not isinstance(self.local_name_value, str):
            self.local_name_value = str(self.local_name_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Example(YAMLRoot):
    """
    usage example and description
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["Example"]
    class_class_curie: ClassVar[str] = "linkml:Example"
    class_name: ClassVar[str] = "example"
    class_model_uri: ClassVar[URIRef] = LINKML.Example

    value: Optional[str] = None
    description: Optional[str] = None
    object: Optional[Union[dict, Anything]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AltDescription(YAMLRoot):
    """
    an attributed description
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["AltDescription"]
    class_class_curie: ClassVar[str] = "linkml:AltDescription"
    class_name: ClassVar[str] = "alt_description"
    class_model_uri: ClassVar[URIRef] = LINKML.AltDescription

    source: Union[str, AltDescriptionSource] = None
    description: str = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, AltDescriptionSource):
            self.source = AltDescriptionSource(self.source)

        if self._is_empty(self.description):
            self.MissingRequiredField("description")
        if not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PermissibleValue(YAMLRoot):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["PermissibleValue"]
    class_class_curie: ClassVar[str] = "linkml:PermissibleValue"
    class_name: ClassVar[str] = "permissible_value"
    class_model_uri: ClassVar[URIRef] = LINKML.PermissibleValue

    text: Union[str, PermissibleValueText] = None
    description: Optional[str] = None
    meaning: Optional[Union[str, URIorCURIE]] = None
    unit: Optional[Union[dict, UnitOfMeasure]] = None
    instantiates: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    implements: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    is_a: Optional[Union[str, PermissibleValueText]] = None
    mixins: Optional[Union[Union[str, PermissibleValueText], list[Union[str, PermissibleValueText]]]] = empty_list()
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, AltDescription]], list[Union[dict, AltDescription]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, Example], list[Union[dict, Example]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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

        if not isinstance(self.instantiates, list):
            self.instantiates = [self.instantiates] if self.instantiates is not None else []
        self.instantiates = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.instantiates]

        if not isinstance(self.implements, list):
            self.implements = [self.implements] if self.implements is not None else []
        self.implements = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.implements]

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UniqueKey(YAMLRoot):
    """
    a collection of slots whose values uniquely identify an instance of a class
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["UniqueKey"]
    class_class_curie: ClassVar[str] = "linkml:UniqueKey"
    class_name: ClassVar[str] = "unique_key"
    class_model_uri: ClassVar[URIRef] = LINKML.UniqueKey

    unique_key_name: Union[str, UniqueKeyUniqueKeyName] = None
    unique_key_slots: Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]] = None
    consider_nulls_inequal: Optional[Union[bool, Bool]] = None
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, AltDescription]], list[Union[dict, AltDescription]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, Example], list[Union[dict, Example]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.unique_key_name):
            self.MissingRequiredField("unique_key_name")
        if not isinstance(self.unique_key_name, UniqueKeyUniqueKeyName):
            self.unique_key_name = UniqueKeyUniqueKeyName(self.unique_key_name)

        if self._is_empty(self.unique_key_slots):
            self.MissingRequiredField("unique_key_slots")
        if not isinstance(self.unique_key_slots, list):
            self.unique_key_slots = [self.unique_key_slots] if self.unique_key_slots is not None else []
        self.unique_key_slots = [v if isinstance(v, SlotDefinitionName) else SlotDefinitionName(v) for v in self.unique_key_slots]

        if self.consider_nulls_inequal is not None and not isinstance(self.consider_nulls_inequal, Bool):
            self.consider_nulls_inequal = Bool(self.consider_nulls_inequal)

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


@dataclass
class TypeMapping(YAMLRoot):
    """
    Represents how a slot or type can be serialized to a format.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["TypeMapping"]
    class_class_curie: ClassVar[str] = "linkml:TypeMapping"
    class_name: ClassVar[str] = "type_mapping"
    class_model_uri: ClassVar[URIRef] = LINKML.TypeMapping

    framework: Union[str, TypeMappingFramework] = None
    type: Optional[Union[str, TypeDefinitionName]] = None
    string_serialization: Optional[str] = None
    extensions: Optional[Union[dict[Union[str, ExtensionTag], Union[dict, Extension]], list[Union[dict, Extension]]]] = empty_dict()
    annotations: Optional[Union[dict[Union[str, AnnotationTag], Union[dict, Annotation]], list[Union[dict, Annotation]]]] = empty_dict()
    description: Optional[str] = None
    alt_descriptions: Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, AltDescription]], list[Union[dict, AltDescription]]]] = empty_dict()
    title: Optional[str] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[Union[str, list[str]]] = empty_list()
    comments: Optional[Union[str, list[str]]] = empty_list()
    examples: Optional[Union[Union[dict, Example], list[Union[dict, Example]]]] = empty_list()
    in_subset: Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    in_language: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    aliases: Optional[Union[str, list[str]]] = empty_list()
    structured_aliases: Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]] = empty_list()
    mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    exact_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    close_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    related_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    narrow_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    broad_mappings: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_by: Optional[Union[str, URIorCURIE]] = None
    contributors: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    created_on: Optional[Union[str, XSDDateTime]] = None
    last_updated_on: Optional[Union[str, XSDDateTime]] = None
    modified_by: Optional[Union[str, URIorCURIE]] = None
    status: Optional[Union[str, URIorCURIE]] = None
    rank: Optional[int] = None
    categories: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.framework):
            self.MissingRequiredField("framework")
        if not isinstance(self.framework, TypeMappingFramework):
            self.framework = TypeMappingFramework(self.framework)

        if self.type is not None and not isinstance(self.type, TypeDefinitionName):
            self.type = TypeDefinitionName(self.type)

        if self.string_serialization is not None and not isinstance(self.string_serialization, str):
            self.string_serialization = str(self.string_serialization)

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

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if not isinstance(self.contributors, list):
            self.contributors = [self.contributors] if self.contributors is not None else []
        self.contributors = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.contributors]

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.last_updated_on is not None and not isinstance(self.last_updated_on, XSDDateTime):
            self.last_updated_on = XSDDateTime(self.last_updated_on)

        if self.modified_by is not None and not isinstance(self.modified_by, URIorCURIE):
            self.modified_by = URIorCURIE(self.modified_by)

        if self.status is not None and not isinstance(self.status, URIorCURIE):
            self.status = URIorCURIE(self.status)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        super().__post_init__(**kwargs)


# Enumerations
class PvFormulaOptions(EnumDefinitionImpl):
    """
    The formula used to generate the set of permissible values from the code_set values
    """
    CODE = PermissibleValue(
        text="CODE",
        description="The permissible values are the set of possible codes in the code set")
    CURIE = PermissibleValue(
        text="CURIE",
        description="The permissible values are the set of CURIES in the code set")
    URI = PermissibleValue(
        text="URI",
        description="The permissible values are the set of code URIs in the code set")
    FHIR_CODING = PermissibleValue(
        text="FHIR_CODING",
        description="The permissible values are the set of FHIR coding elements derived from the code set")
    LABEL = PermissibleValue(
        text="LABEL",
        description="The permissible values are the set of human readable labels in the code set")

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
    SUBJECT = PermissibleValue(
        text="SUBJECT",
        description="a slot with this role connects a relationship to its subject/source node",
        meaning=RDF["subject"])
    OBJECT = PermissibleValue(
        text="OBJECT",
        description="a slot with this role connects a relationship to its object/target node",
        meaning=RDF["object"])
    PREDICATE = PermissibleValue(
        text="PREDICATE",
        description="a slot with this role connects a relationship to its predicate/property",
        meaning=RDF["predicate"])
    NODE = PermissibleValue(
        text="NODE",
        description="""a slot with this role connects a symmetric relationship to a node that represents either subject or object node""")
    OTHER_ROLE = PermissibleValue(
        text="OTHER_ROLE",
        description="a slot with this role connects a relationship to a node that is not subject/object/predicate")

    _defn = EnumDefinition(
        name="RelationalRoleEnum",
        description="enumeration of roles a slot on a relationship class can play",
    )

class AliasPredicateEnum(EnumDefinitionImpl):
    """
    permissible values for the relationship between an element and an alias
    """
    EXACT_SYNONYM = PermissibleValue(
        text="EXACT_SYNONYM",
        meaning=SKOS["exactMatch"])
    RELATED_SYNONYM = PermissibleValue(
        text="RELATED_SYNONYM",
        meaning=SKOS["relatedMatch"])
    BROAD_SYNONYM = PermissibleValue(
        text="BROAD_SYNONYM",
        meaning=SKOS["broaderMatch"])
    NARROW_SYNONYM = PermissibleValue(
        text="NARROW_SYNONYM",
        meaning=SKOS["narrowerMatch"])

    _defn = EnumDefinition(
        name="AliasPredicateEnum",
        description="permissible values for the relationship between an element and an alias",
    )

class ObligationLevelEnum(EnumDefinitionImpl):
    """
    The level of obligation or recommendation strength for a metadata element
    """
    REQUIRED = PermissibleValue(
        text="REQUIRED",
        description="The metadata element is required to be present in the model")
    RECOMMENDED = PermissibleValue(
        text="RECOMMENDED",
        description="The metadata element is recommended to be present in the model")
    OPTIONAL = PermissibleValue(
        text="OPTIONAL",
        description="The metadata element is optional to be present in the model")
    EXAMPLE = PermissibleValue(
        text="EXAMPLE",
        description="The metadata element is an example of how to use the model")
    DISCOURAGED = PermissibleValue(
        text="DISCOURAGED",
        description="The metadata element is allowed but discouraged to be present in the model")

    _defn = EnumDefinition(
        name="ObligationLevelEnum",
        description="The level of obligation or recommendation strength for a metadata element",
    )

# Slots
class slots:
    pass

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=LINKML.name, domain=Element, range=Union[str, ElementName])

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=LINKML.title, domain=Element, range=Optional[str])

slots.conforms_to = Slot(uri=DCTERMS.conformsTo, name="conforms_to", curie=DCTERMS.curie('conformsTo'),
                   model_uri=LINKML.conforms_to, domain=Element, range=Optional[str])

slots.implements = Slot(uri=LINKML.implements, name="implements", curie=LINKML.curie('implements'),
                   model_uri=LINKML.implements, domain=Element, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.instantiates = Slot(uri=LINKML.instantiates, name="instantiates", curie=LINKML.curie('instantiates'),
                   model_uri=LINKML.instantiates, domain=Element, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.categories = Slot(uri=DCTERMS.subject, name="categories", curie=DCTERMS.curie('subject'),
                   model_uri=LINKML.categories, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.keywords = Slot(uri=SCHEMA.keywords, name="keywords", curie=SCHEMA.curie('keywords'),
                   model_uri=LINKML.keywords, domain=Element, range=Optional[Union[str, list[str]]])

slots.definition_uri = Slot(uri=LINKML.definition_uri, name="definition_uri", curie=LINKML.curie('definition_uri'),
                   model_uri=LINKML.definition_uri, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.id_prefixes = Slot(uri=LINKML.id_prefixes, name="id_prefixes", curie=LINKML.curie('id_prefixes'),
                   model_uri=LINKML.id_prefixes, domain=Element, range=Optional[Union[Union[str, NCName], list[Union[str, NCName]]]])

slots.id_prefixes_are_closed = Slot(uri=LINKML.id_prefixes_are_closed, name="id_prefixes_are_closed", curie=LINKML.curie('id_prefixes_are_closed'),
                   model_uri=LINKML.id_prefixes_are_closed, domain=Element, range=Optional[Union[bool, Bool]])

slots.description = Slot(uri=SKOS.definition, name="description", curie=SKOS.curie('definition'),
                   model_uri=LINKML.description, domain=Element, range=Optional[str])

slots.structured_aliases = Slot(uri=SKOSXL.altLabel, name="structured_aliases", curie=SKOSXL.curie('altLabel'),
                   model_uri=LINKML.structured_aliases, domain=None, range=Optional[Union[Union[dict, StructuredAlias], list[Union[dict, StructuredAlias]]]])

slots.aliases = Slot(uri=SKOS.altLabel, name="aliases", curie=SKOS.curie('altLabel'),
                   model_uri=LINKML.aliases, domain=Element, range=Optional[Union[str, list[str]]])

slots.deprecated = Slot(uri=LINKML.deprecated, name="deprecated", curie=LINKML.curie('deprecated'),
                   model_uri=LINKML.deprecated, domain=Element, range=Optional[str])

slots.todos = Slot(uri=LINKML.todos, name="todos", curie=LINKML.curie('todos'),
                   model_uri=LINKML.todos, domain=Element, range=Optional[Union[str, list[str]]])

slots.notes = Slot(uri=SKOS.editorialNote, name="notes", curie=SKOS.curie('editorialNote'),
                   model_uri=LINKML.notes, domain=Element, range=Optional[Union[str, list[str]]])

slots.comments = Slot(uri=SKOS.note, name="comments", curie=SKOS.curie('note'),
                   model_uri=LINKML.comments, domain=Element, range=Optional[Union[str, list[str]]])

slots.in_subset = Slot(uri=OIO.inSubset, name="in_subset", curie=OIO.curie('inSubset'),
                   model_uri=LINKML.in_subset, domain=Element, range=Optional[Union[Union[str, SubsetDefinitionName], list[Union[str, SubsetDefinitionName]]]])

slots.from_schema = Slot(uri=SKOS.inScheme, name="from_schema", curie=SKOS.curie('inScheme'),
                   model_uri=LINKML.from_schema, domain=Element, range=Optional[Union[str, URI]])

slots.imported_from = Slot(uri=LINKML.imported_from, name="imported_from", curie=LINKML.curie('imported_from'),
                   model_uri=LINKML.imported_from, domain=Element, range=Optional[str])

slots.see_also = Slot(uri=RDFS.seeAlso, name="see_also", curie=RDFS.curie('seeAlso'),
                   model_uri=LINKML.see_also, domain=Element, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.owned_by = Slot(uri=LINKML.owned_by, name="owned_by", curie=LINKML.curie('owned_by'),
                   model_uri=LINKML.owned_by, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.created_by = Slot(uri=PAV.createdBy, name="created_by", curie=PAV.curie('createdBy'),
                   model_uri=LINKML.created_by, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.contributors = Slot(uri=DCTERMS.contributor, name="contributors", curie=DCTERMS.curie('contributor'),
                   model_uri=LINKML.contributors, domain=Element, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.created_on = Slot(uri=PAV.createdOn, name="created_on", curie=PAV.curie('createdOn'),
                   model_uri=LINKML.created_on, domain=Element, range=Optional[Union[str, XSDDateTime]])

slots.last_updated_on = Slot(uri=PAV.lastUpdatedOn, name="last_updated_on", curie=PAV.curie('lastUpdatedOn'),
                   model_uri=LINKML.last_updated_on, domain=Element, range=Optional[Union[str, XSDDateTime]])

slots.modified_by = Slot(uri=OSLC.modifiedBy, name="modified_by", curie=OSLC.curie('modifiedBy'),
                   model_uri=LINKML.modified_by, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.status = Slot(uri=BIBO.status, name="status", curie=BIBO.curie('status'),
                   model_uri=LINKML.status, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.literal_form = Slot(uri=SKOSXL.literalForm, name="literal_form", curie=SKOSXL.curie('literalForm'),
                   model_uri=LINKML.literal_form, domain=StructuredAlias, range=str)

slots.alias_predicate = Slot(uri=RDF.predicate, name="alias_predicate", curie=RDF.curie('predicate'),
                   model_uri=LINKML.alias_predicate, domain=StructuredAlias, range=Optional[Union[str, "AliasPredicateEnum"]])

slots.alias_contexts = Slot(uri=LINKML.contexts, name="alias_contexts", curie=LINKML.curie('contexts'),
                   model_uri=LINKML.alias_contexts, domain=StructuredAlias, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.in_language = Slot(uri=SCHEMA.inLanguage, name="in_language", curie=SCHEMA.curie('inLanguage'),
                   model_uri=LINKML.in_language, domain=None, range=Optional[str])

slots.source = Slot(uri=DCTERMS.source, name="source", curie=DCTERMS.curie('source'),
                   model_uri=LINKML.source, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.publisher = Slot(uri=DCTERMS.publisher, name="publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=LINKML.publisher, domain=Element, range=Optional[Union[str, URIorCURIE]])

slots.is_a = Slot(uri=LINKML.is_a, name="is_a", curie=LINKML.curie('is_a'),
                   model_uri=LINKML.is_a, domain=None, range=Optional[Union[str, DefinitionName]])

slots.abstract = Slot(uri=LINKML.abstract, name="abstract", curie=LINKML.curie('abstract'),
                   model_uri=LINKML.abstract, domain=Definition, range=Optional[Union[bool, Bool]])

slots.mixin = Slot(uri=LINKML.mixin, name="mixin", curie=LINKML.curie('mixin'),
                   model_uri=LINKML.mixin, domain=Definition, range=Optional[Union[bool, Bool]])

slots.mixins = Slot(uri=LINKML.mixins, name="mixins", curie=LINKML.curie('mixins'),
                   model_uri=LINKML.mixins, domain=None, range=Optional[Union[Union[str, DefinitionName], list[Union[str, DefinitionName]]]])

slots.apply_to = Slot(uri=LINKML.apply_to, name="apply_to", curie=LINKML.curie('apply_to'),
                   model_uri=LINKML.apply_to, domain=Definition, range=Optional[Union[Union[str, DefinitionName], list[Union[str, DefinitionName]]]])

slots.values_from = Slot(uri=LINKML.values_from, name="values_from", curie=LINKML.curie('values_from'),
                   model_uri=LINKML.values_from, domain=Definition, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.code_set = Slot(uri=LINKML.code_set, name="code_set", curie=LINKML.curie('code_set'),
                   model_uri=LINKML.code_set, domain=EnumExpression, range=Optional[Union[str, URIorCURIE]])

slots.code_set_version = Slot(uri=LINKML.code_set_version, name="code_set_version", curie=LINKML.curie('code_set_version'),
                   model_uri=LINKML.code_set_version, domain=EnumExpression, range=Optional[str])

slots.code_set_tag = Slot(uri=LINKML.code_set_tag, name="code_set_tag", curie=LINKML.curie('code_set_tag'),
                   model_uri=LINKML.code_set_tag, domain=EnumExpression, range=Optional[str])

slots.pv_formula = Slot(uri=LINKML.pv_formula, name="pv_formula", curie=LINKML.curie('pv_formula'),
                   model_uri=LINKML.pv_formula, domain=None, range=Optional[Union[str, "PvFormulaOptions"]])

slots.permissible_values = Slot(uri=LINKML.permissible_values, name="permissible_values", curie=LINKML.curie('permissible_values'),
                   model_uri=LINKML.permissible_values, domain=EnumExpression, range=Optional[Union[dict[Union[str, PermissibleValueText], Union[dict, "PermissibleValue"]], list[Union[dict, "PermissibleValue"]]]])

slots.enum_uri = Slot(uri=LINKML.enum_uri, name="enum_uri", curie=LINKML.curie('enum_uri'),
                   model_uri=LINKML.enum_uri, domain=EnumDefinition, range=Optional[Union[str, URIorCURIE]])

slots.include = Slot(uri=LINKML.include, name="include", curie=LINKML.curie('include'),
                   model_uri=LINKML.include, domain=EnumExpression, range=Optional[Union[Union[dict, "AnonymousEnumExpression"], list[Union[dict, "AnonymousEnumExpression"]]]])

slots.minus = Slot(uri=LINKML.minus, name="minus", curie=LINKML.curie('minus'),
                   model_uri=LINKML.minus, domain=EnumExpression, range=Optional[Union[Union[dict, "AnonymousEnumExpression"], list[Union[dict, "AnonymousEnumExpression"]]]])

slots.inherits = Slot(uri=LINKML.inherits, name="inherits", curie=LINKML.curie('inherits'),
                   model_uri=LINKML.inherits, domain=EnumExpression, range=Optional[Union[Union[str, EnumDefinitionName], list[Union[str, EnumDefinitionName]]]])

slots.matches = Slot(uri=LINKML.matches, name="matches", curie=LINKML.curie('matches'),
                   model_uri=LINKML.matches, domain=EnumExpression, range=Optional[Union[dict, "MatchQuery"]])

slots.identifier_pattern = Slot(uri=LINKML.identifier_pattern, name="identifier_pattern", curie=LINKML.curie('identifier_pattern'),
                   model_uri=LINKML.identifier_pattern, domain=MatchQuery, range=Optional[str])

slots.concepts = Slot(uri=LINKML.concepts, name="concepts", curie=LINKML.curie('concepts'),
                   model_uri=LINKML.concepts, domain=EnumExpression, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.reachable_from = Slot(uri=LINKML.reachable_from, name="reachable_from", curie=LINKML.curie('reachable_from'),
                   model_uri=LINKML.reachable_from, domain=EnumExpression, range=Optional[Union[dict, "ReachabilityQuery"]])

slots.source_ontology = Slot(uri=LINKML.source_ontology, name="source_ontology", curie=LINKML.curie('source_ontology'),
                   model_uri=LINKML.source_ontology, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.is_direct = Slot(uri=LINKML.is_direct, name="is_direct", curie=LINKML.curie('is_direct'),
                   model_uri=LINKML.is_direct, domain=ReachabilityQuery, range=Optional[Union[bool, Bool]])

slots.traverse_up = Slot(uri=LINKML.traverse_up, name="traverse_up", curie=LINKML.curie('traverse_up'),
                   model_uri=LINKML.traverse_up, domain=ReachabilityQuery, range=Optional[Union[bool, Bool]])

slots.include_self = Slot(uri=LINKML.include_self, name="include_self", curie=LINKML.curie('include_self'),
                   model_uri=LINKML.include_self, domain=ReachabilityQuery, range=Optional[Union[bool, Bool]])

slots.relationship_types = Slot(uri=LINKML.relationship_types, name="relationship_types", curie=LINKML.curie('relationship_types'),
                   model_uri=LINKML.relationship_types, domain=ReachabilityQuery, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.source_nodes = Slot(uri=LINKML.source_nodes, name="source_nodes", curie=LINKML.curie('source_nodes'),
                   model_uri=LINKML.source_nodes, domain=ReachabilityQuery, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.text = Slot(uri=LINKML.text, name="text", curie=LINKML.curie('text'),
                   model_uri=LINKML.text, domain=PermissibleValue, range=Union[str, PermissibleValueText])

slots.meaning = Slot(uri=LINKML.meaning, name="meaning", curie=LINKML.curie('meaning'),
                   model_uri=LINKML.meaning, domain=PermissibleValue, range=Optional[Union[str, URIorCURIE]])

slots.id = Slot(uri=LINKML.id, name="id", curie=LINKML.curie('id'),
                   model_uri=LINKML.id, domain=SchemaDefinition, range=Union[str, URI])

slots.emit_prefixes = Slot(uri=LINKML.emit_prefixes, name="emit_prefixes", curie=LINKML.curie('emit_prefixes'),
                   model_uri=LINKML.emit_prefixes, domain=SchemaDefinition, range=Optional[Union[Union[str, NCName], list[Union[str, NCName]]]])

slots.version = Slot(uri=PAV.version, name="version", curie=PAV.curie('version'),
                   model_uri=LINKML.version, domain=SchemaDefinition, range=Optional[str])

slots.imports = Slot(uri=LINKML.imports, name="imports", curie=LINKML.curie('imports'),
                   model_uri=LINKML.imports, domain=SchemaDefinition, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.structured_imports = Slot(uri=LINKML.structured_imports, name="structured_imports", curie=LINKML.curie('structured_imports'),
                   model_uri=LINKML.structured_imports, domain=SchemaDefinition, range=Optional[Union[Union[dict, "ImportExpression"], list[Union[dict, "ImportExpression"]]]])

slots.license = Slot(uri=DCTERMS.license, name="license", curie=DCTERMS.curie('license'),
                   model_uri=LINKML.license, domain=SchemaDefinition, range=Optional[str])

slots.default_curi_maps = Slot(uri=LINKML.default_curi_maps, name="default_curi_maps", curie=LINKML.curie('default_curi_maps'),
                   model_uri=LINKML.default_curi_maps, domain=SchemaDefinition, range=Optional[Union[str, list[str]]])

slots.default_prefix = Slot(uri=LINKML.default_prefix, name="default_prefix", curie=LINKML.curie('default_prefix'),
                   model_uri=LINKML.default_prefix, domain=SchemaDefinition, range=Optional[str])

slots.default_range = Slot(uri=LINKML.default_range, name="default_range", curie=LINKML.curie('default_range'),
                   model_uri=LINKML.default_range, domain=SchemaDefinition, range=Optional[Union[str, TypeDefinitionName]])

slots.subsets = Slot(uri=LINKML.subsets, name="subsets", curie=LINKML.curie('subsets'),
                   model_uri=LINKML.subsets, domain=SchemaDefinition, range=Optional[Union[dict[Union[str, SubsetDefinitionName], Union[dict, "SubsetDefinition"]], list[Union[dict, "SubsetDefinition"]]]])

slots.types = Slot(uri=LINKML.types, name="types", curie=LINKML.curie('types'),
                   model_uri=LINKML.types, domain=SchemaDefinition, range=Optional[Union[dict[Union[str, TypeDefinitionName], Union[dict, "TypeDefinition"]], list[Union[dict, "TypeDefinition"]]]])

slots.enums = Slot(uri=LINKML.enums, name="enums", curie=LINKML.curie('enums'),
                   model_uri=LINKML.enums, domain=SchemaDefinition, range=Optional[Union[dict[Union[str, EnumDefinitionName], Union[dict, "EnumDefinition"]], list[Union[dict, "EnumDefinition"]]]])

slots.slot_definitions = Slot(uri=LINKML.slots, name="slot_definitions", curie=LINKML.curie('slots'),
                   model_uri=LINKML.slot_definitions, domain=SchemaDefinition, range=Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, "SlotDefinition"]], list[Union[dict, "SlotDefinition"]]]])

slots.classes = Slot(uri=LINKML.classes, name="classes", curie=LINKML.curie('classes'),
                   model_uri=LINKML.classes, domain=SchemaDefinition, range=Optional[Union[dict[Union[str, ClassDefinitionName], Union[dict, "ClassDefinition"]], list[Union[dict, "ClassDefinition"]]]])

slots.metamodel_version = Slot(uri=LINKML.metamodel_version, name="metamodel_version", curie=LINKML.curie('metamodel_version'),
                   model_uri=LINKML.metamodel_version, domain=SchemaDefinition, range=Optional[str])

slots.source_file = Slot(uri=LINKML.source_file, name="source_file", curie=LINKML.curie('source_file'),
                   model_uri=LINKML.source_file, domain=SchemaDefinition, range=Optional[str])

slots.source_file_date = Slot(uri=LINKML.source_file_date, name="source_file_date", curie=LINKML.curie('source_file_date'),
                   model_uri=LINKML.source_file_date, domain=SchemaDefinition, range=Optional[Union[str, XSDDateTime]])

slots.source_file_size = Slot(uri=LINKML.source_file_size, name="source_file_size", curie=LINKML.curie('source_file_size'),
                   model_uri=LINKML.source_file_size, domain=SchemaDefinition, range=Optional[int])

slots.generation_date = Slot(uri=LINKML.generation_date, name="generation_date", curie=LINKML.curie('generation_date'),
                   model_uri=LINKML.generation_date, domain=SchemaDefinition, range=Optional[Union[str, XSDDateTime]])

slots.slots = Slot(uri=LINKML.slots, name="slots", curie=LINKML.curie('slots'),
                   model_uri=LINKML.slots, domain=ClassDefinition, range=Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]])

slots.slot_usage = Slot(uri=LINKML.slot_usage, name="slot_usage", curie=LINKML.curie('slot_usage'),
                   model_uri=LINKML.slot_usage, domain=ClassDefinition, range=Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]])

slots.enum_range = Slot(uri=LINKML.enum_range, name="enum_range", curie=LINKML.curie('enum_range'),
                   model_uri=LINKML.enum_range, domain=None, range=Optional[Union[dict, EnumExpression]])

slots.range_expression = Slot(uri=LINKML.range_expression, name="range_expression", curie=LINKML.curie('range_expression'),
                   model_uri=LINKML.range_expression, domain=None, range=Optional[Union[dict, "AnonymousClassExpression"]])

slots.boolean_slot = Slot(uri=LINKML.boolean_slot, name="boolean_slot", curie=LINKML.curie('boolean_slot'),
                   model_uri=LINKML.boolean_slot, domain=None, range=Optional[Union[Union[dict, Expression], list[Union[dict, Expression]]]])

slots.any_of = Slot(uri=LINKML.any_of, name="any_of", curie=LINKML.curie('any_of'),
                   model_uri=LINKML.any_of, domain=None, range=Optional[Union[Union[dict, Expression], list[Union[dict, Expression]]]])

slots.exactly_one_of = Slot(uri=LINKML.exactly_one_of, name="exactly_one_of", curie=LINKML.curie('exactly_one_of'),
                   model_uri=LINKML.exactly_one_of, domain=None, range=Optional[Union[Union[dict, Expression], list[Union[dict, Expression]]]])

slots.none_of = Slot(uri=LINKML.none_of, name="none_of", curie=LINKML.curie('none_of'),
                   model_uri=LINKML.none_of, domain=None, range=Optional[Union[Union[dict, Expression], list[Union[dict, Expression]]]])

slots.all_of = Slot(uri=LINKML.all_of, name="all_of", curie=LINKML.curie('all_of'),
                   model_uri=LINKML.all_of, domain=None, range=Optional[Union[Union[dict, Expression], list[Union[dict, Expression]]]])

slots.preconditions = Slot(uri=SH.condition, name="preconditions", curie=SH.curie('condition'),
                   model_uri=LINKML.preconditions, domain=None, range=Optional[Union[dict, AnonymousClassExpression]])

slots.postconditions = Slot(uri=LINKML.postconditions, name="postconditions", curie=LINKML.curie('postconditions'),
                   model_uri=LINKML.postconditions, domain=None, range=Optional[Union[dict, AnonymousClassExpression]])

slots.elseconditions = Slot(uri=LINKML.elseconditions, name="elseconditions", curie=LINKML.curie('elseconditions'),
                   model_uri=LINKML.elseconditions, domain=None, range=Optional[Union[dict, AnonymousClassExpression]])

slots.bidirectional = Slot(uri=LINKML.bidirectional, name="bidirectional", curie=LINKML.curie('bidirectional'),
                   model_uri=LINKML.bidirectional, domain=None, range=Optional[Union[bool, Bool]])

slots.open_world = Slot(uri=LINKML.open_world, name="open_world", curie=LINKML.curie('open_world'),
                   model_uri=LINKML.open_world, domain=None, range=Optional[Union[bool, Bool]])

slots.rank = Slot(uri=SH.order, name="rank", curie=SH.curie('order'),
                   model_uri=LINKML.rank, domain=None, range=Optional[int])

slots.deactivated = Slot(uri=SH.deactivated, name="deactivated", curie=SH.curie('deactivated'),
                   model_uri=LINKML.deactivated, domain=None, range=Optional[Union[bool, Bool]])

slots.rules = Slot(uri=SH.rule, name="rules", curie=SH.curie('rule'),
                   model_uri=LINKML.rules, domain=ClassDefinition, range=Optional[Union[Union[dict, "ClassRule"], list[Union[dict, "ClassRule"]]]])

slots.classification_rules = Slot(uri=LINKML.classification_rules, name="classification_rules", curie=LINKML.curie('classification_rules'),
                   model_uri=LINKML.classification_rules, domain=ClassDefinition, range=Optional[Union[Union[dict, AnonymousClassExpression], list[Union[dict, AnonymousClassExpression]]]])

slots.slot_conditions = Slot(uri=LINKML.slot_conditions, name="slot_conditions", curie=LINKML.curie('slot_conditions'),
                   model_uri=LINKML.slot_conditions, domain=None, range=Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]])

slots.attributes = Slot(uri=LINKML.attributes, name="attributes", curie=LINKML.curie('attributes'),
                   model_uri=LINKML.attributes, domain=ClassDefinition, range=Optional[Union[dict[Union[str, SlotDefinitionName], Union[dict, SlotDefinition]], list[Union[dict, SlotDefinition]]]])

slots.class_uri = Slot(uri=LINKML.class_uri, name="class_uri", curie=LINKML.curie('class_uri'),
                   model_uri=LINKML.class_uri, domain=ClassDefinition, range=Optional[Union[str, URIorCURIE]])

slots.subclass_of = Slot(uri=LINKML.subclass_of, name="subclass_of", curie=LINKML.curie('subclass_of'),
                   model_uri=LINKML.subclass_of, domain=ClassDefinition, range=Optional[Union[str, URIorCURIE]])

slots.defining_slots = Slot(uri=LINKML.defining_slots, name="defining_slots", curie=LINKML.curie('defining_slots'),
                   model_uri=LINKML.defining_slots, domain=ClassDefinition, range=Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]])

slots.union_of = Slot(uri=LINKML.union_of, name="union_of", curie=LINKML.curie('union_of'),
                   model_uri=LINKML.union_of, domain=Element, range=Optional[Union[Union[str, ElementName], list[Union[str, ElementName]]]])

slots.tree_root = Slot(uri=LINKML.tree_root, name="tree_root", curie=LINKML.curie('tree_root'),
                   model_uri=LINKML.tree_root, domain=ClassDefinition, range=Optional[Union[bool, Bool]])

slots.unique_keys = Slot(uri=LINKML.unique_keys, name="unique_keys", curie=LINKML.curie('unique_keys'),
                   model_uri=LINKML.unique_keys, domain=ClassDefinition, range=Optional[Union[dict[Union[str, UniqueKeyUniqueKeyName], Union[dict, "UniqueKey"]], list[Union[dict, "UniqueKey"]]]])

slots.unique_key_name = Slot(uri=LINKML.unique_key_name, name="unique_key_name", curie=LINKML.curie('unique_key_name'),
                   model_uri=LINKML.unique_key_name, domain=UniqueKey, range=Union[str, UniqueKeyUniqueKeyName])

slots.consider_nulls_inequal = Slot(uri=LINKML.consider_nulls_inequal, name="consider_nulls_inequal", curie=LINKML.curie('consider_nulls_inequal'),
                   model_uri=LINKML.consider_nulls_inequal, domain=UniqueKey, range=Optional[Union[bool, Bool]])

slots.unique_key_slots = Slot(uri=LINKML.unique_key_slots, name="unique_key_slots", curie=LINKML.curie('unique_key_slots'),
                   model_uri=LINKML.unique_key_slots, domain=UniqueKey, range=Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]])

slots.slot_names_unique = Slot(uri=LINKML.slot_names_unique, name="slot_names_unique", curie=LINKML.curie('slot_names_unique'),
                   model_uri=LINKML.slot_names_unique, domain=Definition, range=Optional[Union[bool, Bool]])

slots.domain = Slot(uri=LINKML.domain, name="domain", curie=LINKML.curie('domain'),
                   model_uri=LINKML.domain, domain=SlotDefinition, range=Optional[Union[str, ClassDefinitionName]])

slots.range = Slot(uri=LINKML.range, name="range", curie=LINKML.curie('range'),
                   model_uri=LINKML.range, domain=SlotDefinition, range=Optional[Union[str, ElementName]])

slots.slot_uri = Slot(uri=LINKML.slot_uri, name="slot_uri", curie=LINKML.curie('slot_uri'),
                   model_uri=LINKML.slot_uri, domain=SlotDefinition, range=Optional[Union[str, URIorCURIE]])

slots.multivalued = Slot(uri=LINKML.multivalued, name="multivalued", curie=LINKML.curie('multivalued'),
                   model_uri=LINKML.multivalued, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.array = Slot(uri=LINKML.array, name="array", curie=LINKML.curie('array'),
                   model_uri=LINKML.array, domain=SlotDefinition, range=Optional[Union[dict, "ArrayExpression"]])

slots.dimensions = Slot(uri=LINKML.dimensions, name="dimensions", curie=LINKML.curie('dimensions'),
                   model_uri=LINKML.dimensions, domain=ArrayExpression, range=Optional[Union[Union[dict, "DimensionExpression"], list[Union[dict, "DimensionExpression"]]]])

slots.minimum_number_dimensions = Slot(uri=LINKML.minimum_number_dimensions, name="minimum_number_dimensions", curie=LINKML.curie('minimum_number_dimensions'),
                   model_uri=LINKML.minimum_number_dimensions, domain=ArrayExpression, range=Optional[int])

slots.maximum_number_dimensions = Slot(uri=LINKML.maximum_number_dimensions, name="maximum_number_dimensions", curie=LINKML.curie('maximum_number_dimensions'),
                   model_uri=LINKML.maximum_number_dimensions, domain=ArrayExpression, range=Optional[Union[dict, Anything]])

slots.exact_number_dimensions = Slot(uri=LINKML.exact_number_dimensions, name="exact_number_dimensions", curie=LINKML.curie('exact_number_dimensions'),
                   model_uri=LINKML.exact_number_dimensions, domain=ArrayExpression, range=Optional[int])

slots.inherited = Slot(uri=LINKML.inherited, name="inherited", curie=LINKML.curie('inherited'),
                   model_uri=LINKML.inherited, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.readonly = Slot(uri=LINKML.readonly, name="readonly", curie=LINKML.curie('readonly'),
                   model_uri=LINKML.readonly, domain=SlotDefinition, range=Optional[str])

slots.ifabsent = Slot(uri=LINKML.ifabsent, name="ifabsent", curie=LINKML.curie('ifabsent'),
                   model_uri=LINKML.ifabsent, domain=SlotDefinition, range=Optional[str])

slots.implicit_prefix = Slot(uri=LINKML.implicit_prefix, name="implicit_prefix", curie=LINKML.curie('implicit_prefix'),
                   model_uri=LINKML.implicit_prefix, domain=None, range=Optional[str])

slots.value_specification_constant = Slot(uri=LINKML.value_specification_constant, name="value_specification_constant", curie=LINKML.curie('value_specification_constant'),
                   model_uri=LINKML.value_specification_constant, domain=None, range=Optional[str])

slots.list_value_specification_constant = Slot(uri=LINKML.list_value_specification_constant, name="list_value_specification_constant", curie=LINKML.curie('list_value_specification_constant'),
                   model_uri=LINKML.list_value_specification_constant, domain=None, range=Optional[str])

slots.value_presence = Slot(uri=LINKML.value_presence, name="value_presence", curie=LINKML.curie('value_presence'),
                   model_uri=LINKML.value_presence, domain=SlotDefinition, range=Optional[Union[str, "PresenceEnum"]])

slots.equals_string = Slot(uri=LINKML.equals_string, name="equals_string", curie=LINKML.curie('equals_string'),
                   model_uri=LINKML.equals_string, domain=None, range=Optional[str])

slots.equals_number = Slot(uri=LINKML.equals_number, name="equals_number", curie=LINKML.curie('equals_number'),
                   model_uri=LINKML.equals_number, domain=None, range=Optional[int])

slots.equals_expression = Slot(uri=LINKML.equals_expression, name="equals_expression", curie=LINKML.curie('equals_expression'),
                   model_uri=LINKML.equals_expression, domain=None, range=Optional[str])

slots.exact_cardinality = Slot(uri=LINKML.exact_cardinality, name="exact_cardinality", curie=LINKML.curie('exact_cardinality'),
                   model_uri=LINKML.exact_cardinality, domain=None, range=Optional[int])

slots.minimum_cardinality = Slot(uri=LINKML.minimum_cardinality, name="minimum_cardinality", curie=LINKML.curie('minimum_cardinality'),
                   model_uri=LINKML.minimum_cardinality, domain=None, range=Optional[int])

slots.maximum_cardinality = Slot(uri=LINKML.maximum_cardinality, name="maximum_cardinality", curie=LINKML.curie('maximum_cardinality'),
                   model_uri=LINKML.maximum_cardinality, domain=None, range=Optional[int])

slots.equals_string_in = Slot(uri=LINKML.equals_string_in, name="equals_string_in", curie=LINKML.curie('equals_string_in'),
                   model_uri=LINKML.equals_string_in, domain=None, range=Optional[Union[str, list[str]]])

slots.equals_number_in = Slot(uri=LINKML.equals_number_in, name="equals_number_in", curie=LINKML.curie('equals_number_in'),
                   model_uri=LINKML.equals_number_in, domain=None, range=Optional[Union[int, list[int]]])

slots.has_member = Slot(uri=LINKML.has_member, name="has_member", curie=LINKML.curie('has_member'),
                   model_uri=LINKML.has_member, domain=None, range=Optional[Union[dict, AnonymousSlotExpression]])

slots.all_members = Slot(uri=LINKML.all_members, name="all_members", curie=LINKML.curie('all_members'),
                   model_uri=LINKML.all_members, domain=None, range=Optional[Union[dict, AnonymousSlotExpression]])

slots.singular_name = Slot(uri=LINKML.singular_name, name="singular_name", curie=LINKML.curie('singular_name'),
                   model_uri=LINKML.singular_name, domain=SlotDefinition, range=Optional[str])

slots.required = Slot(uri=LINKML.required, name="required", curie=LINKML.curie('required'),
                   model_uri=LINKML.required, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.recommended = Slot(uri=LINKML.recommended, name="recommended", curie=LINKML.curie('recommended'),
                   model_uri=LINKML.recommended, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inapplicable = Slot(uri=LINKML.inapplicable, name="inapplicable", curie=LINKML.curie('inapplicable'),
                   model_uri=LINKML.inapplicable, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inlined = Slot(uri=LINKML.inlined, name="inlined", curie=LINKML.curie('inlined'),
                   model_uri=LINKML.inlined, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inlined_as_list = Slot(uri=LINKML.inlined_as_list, name="inlined_as_list", curie=LINKML.curie('inlined_as_list'),
                   model_uri=LINKML.inlined_as_list, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.inlined_as_simple_dict = Slot(uri=LINKML.inlined_as_simple_dict, name="inlined_as_simple_dict", curie=LINKML.curie('inlined_as_simple_dict'),
                   model_uri=LINKML.inlined_as_simple_dict, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.list_elements_ordered = Slot(uri=LINKML.list_elements_ordered, name="list_elements_ordered", curie=LINKML.curie('list_elements_ordered'),
                   model_uri=LINKML.list_elements_ordered, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.list_elements_unique = Slot(uri=LINKML.list_elements_unique, name="list_elements_unique", curie=LINKML.curie('list_elements_unique'),
                   model_uri=LINKML.list_elements_unique, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.shared = Slot(uri=LINKML.shared, name="shared", curie=LINKML.curie('shared'),
                   model_uri=LINKML.shared, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.key = Slot(uri=LINKML.key, name="key", curie=LINKML.curie('key'),
                   model_uri=LINKML.key, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.identifier = Slot(uri=LINKML.identifier, name="identifier", curie=LINKML.curie('identifier'),
                   model_uri=LINKML.identifier, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.designates_type = Slot(uri=LINKML.designates_type, name="designates_type", curie=LINKML.curie('designates_type'),
                   model_uri=LINKML.designates_type, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.alias = Slot(uri=SKOS.prefLabel, name="alias", curie=SKOS.curie('prefLabel'),
                   model_uri=LINKML.alias, domain=SlotDefinition, range=Optional[str])

slots.owner = Slot(uri=LINKML.owner, name="owner", curie=LINKML.curie('owner'),
                   model_uri=LINKML.owner, domain=SlotDefinition, range=Optional[Union[str, DefinitionName]])

slots.domain_of = Slot(uri=LINKML.domain_of, name="domain_of", curie=LINKML.curie('domain_of'),
                   model_uri=LINKML.domain_of, domain=SlotDefinition, range=Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]])

slots.is_usage_slot = Slot(uri=LINKML.is_usage_slot, name="is_usage_slot", curie=LINKML.curie('is_usage_slot'),
                   model_uri=LINKML.is_usage_slot, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.usage_slot_name = Slot(uri=LINKML.usage_slot_name, name="usage_slot_name", curie=LINKML.curie('usage_slot_name'),
                   model_uri=LINKML.usage_slot_name, domain=SlotDefinition, range=Optional[str])

slots.subproperty_of = Slot(uri=RDFS.subPropertyOf, name="subproperty_of", curie=RDFS.curie('subPropertyOf'),
                   model_uri=LINKML.subproperty_of, domain=SlotDefinition, range=Optional[Union[str, SlotDefinitionName]])

slots.disjoint_with = Slot(uri=LINKML.disjoint_with, name="disjoint_with", curie=LINKML.curie('disjoint_with'),
                   model_uri=LINKML.disjoint_with, domain=Definition, range=Optional[Union[Union[str, DefinitionName], list[Union[str, DefinitionName]]]])

slots.children_are_mutually_disjoint = Slot(uri=LINKML.children_are_mutually_disjoint, name="children_are_mutually_disjoint", curie=LINKML.curie('children_are_mutually_disjoint'),
                   model_uri=LINKML.children_are_mutually_disjoint, domain=Definition, range=Optional[Union[bool, Bool]])

slots.relational_logical_characteristic = Slot(uri=LINKML.relational_logical_characteristic, name="relational_logical_characteristic", curie=LINKML.curie('relational_logical_characteristic'),
                   model_uri=LINKML.relational_logical_characteristic, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.symmetric = Slot(uri=LINKML.symmetric, name="symmetric", curie=LINKML.curie('symmetric'),
                   model_uri=LINKML.symmetric, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.asymmetric = Slot(uri=LINKML.asymmetric, name="asymmetric", curie=LINKML.curie('asymmetric'),
                   model_uri=LINKML.asymmetric, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.reflexive = Slot(uri=LINKML.reflexive, name="reflexive", curie=LINKML.curie('reflexive'),
                   model_uri=LINKML.reflexive, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.irreflexive = Slot(uri=LINKML.irreflexive, name="irreflexive", curie=LINKML.curie('irreflexive'),
                   model_uri=LINKML.irreflexive, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.locally_reflexive = Slot(uri=LINKML.locally_reflexive, name="locally_reflexive", curie=LINKML.curie('locally_reflexive'),
                   model_uri=LINKML.locally_reflexive, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.transitive = Slot(uri=LINKML.transitive, name="transitive", curie=LINKML.curie('transitive'),
                   model_uri=LINKML.transitive, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.transitive_form_of = Slot(uri=LINKML.transitive_form_of, name="transitive_form_of", curie=LINKML.curie('transitive_form_of'),
                   model_uri=LINKML.transitive_form_of, domain=None, range=Optional[Union[str, SlotDefinitionName]])

slots.reflexive_transitive_form_of = Slot(uri=LINKML.reflexive_transitive_form_of, name="reflexive_transitive_form_of", curie=LINKML.curie('reflexive_transitive_form_of'),
                   model_uri=LINKML.reflexive_transitive_form_of, domain=None, range=Optional[Union[str, SlotDefinitionName]])

slots.inverse = Slot(uri=OWL.inverseOf, name="inverse", curie=OWL.curie('inverseOf'),
                   model_uri=LINKML.inverse, domain=SlotDefinition, range=Optional[Union[str, SlotDefinitionName]])

slots.is_class_field = Slot(uri=LINKML.is_class_field, name="is_class_field", curie=LINKML.curie('is_class_field'),
                   model_uri=LINKML.is_class_field, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.role = Slot(uri=LINKML.role, name="role", curie=LINKML.curie('role'),
                   model_uri=LINKML.role, domain=SlotDefinition, range=Optional[str])

slots.minimum_value = Slot(uri=LINKML.minimum_value, name="minimum_value", curie=LINKML.curie('minimum_value'),
                   model_uri=LINKML.minimum_value, domain=SlotDefinition, range=Optional[Union[dict, Anything]])

slots.maximum_value = Slot(uri=LINKML.maximum_value, name="maximum_value", curie=LINKML.curie('maximum_value'),
                   model_uri=LINKML.maximum_value, domain=SlotDefinition, range=Optional[Union[dict, Anything]])

slots.interpolated = Slot(uri=LINKML.interpolated, name="interpolated", curie=LINKML.curie('interpolated'),
                   model_uri=LINKML.interpolated, domain=PatternExpression, range=Optional[Union[bool, Bool]])

slots.partial_match = Slot(uri=LINKML.partial_match, name="partial_match", curie=LINKML.curie('partial_match'),
                   model_uri=LINKML.partial_match, domain=PatternExpression, range=Optional[Union[bool, Bool]])

slots.pattern = Slot(uri=LINKML.pattern, name="pattern", curie=LINKML.curie('pattern'),
                   model_uri=LINKML.pattern, domain=Definition, range=Optional[str])

slots.syntax = Slot(uri=LINKML.syntax, name="syntax", curie=LINKML.curie('syntax'),
                   model_uri=LINKML.syntax, domain=PatternExpression, range=Optional[str])

slots.structured_pattern = Slot(uri=LINKML.structured_pattern, name="structured_pattern", curie=LINKML.curie('structured_pattern'),
                   model_uri=LINKML.structured_pattern, domain=Definition, range=Optional[Union[dict, "PatternExpression"]])

slots.string_serialization = Slot(uri=LINKML.string_serialization, name="string_serialization", curie=LINKML.curie('string_serialization'),
                   model_uri=LINKML.string_serialization, domain=Definition, range=Optional[str])

slots.bindings = Slot(uri=LINKML.bindings, name="bindings", curie=LINKML.curie('bindings'),
                   model_uri=LINKML.bindings, domain=Element, range=Optional[Union[Union[dict, "EnumBinding"], list[Union[dict, "EnumBinding"]]]])

slots.binds_value_of = Slot(uri=LINKML.binds_value_of, name="binds_value_of", curie=LINKML.curie('binds_value_of'),
                   model_uri=LINKML.binds_value_of, domain=EnumBinding, range=Optional[str])

slots.obligation_level = Slot(uri=LINKML.obligation_level, name="obligation_level", curie=LINKML.curie('obligation_level'),
                   model_uri=LINKML.obligation_level, domain=None, range=Optional[Union[str, "ObligationLevelEnum"]])

slots.type_mappings = Slot(uri=LINKML.type_mappings, name="type_mappings", curie=LINKML.curie('type_mappings'),
                   model_uri=LINKML.type_mappings, domain=None, range=Optional[Union[Union[str, TypeMappingFramework], list[Union[str, TypeMappingFramework]]]])

slots.framework_key = Slot(uri=LINKML.framework, name="framework_key", curie=LINKML.curie('framework'),
                   model_uri=LINKML.framework_key, domain=None, range=URIRef)

slots.mapped_type = Slot(uri=LINKML.type, name="mapped_type", curie=LINKML.curie('type'),
                   model_uri=LINKML.mapped_type, domain=None, range=Optional[Union[str, TypeDefinitionName]])

slots.typeof = Slot(uri=LINKML.typeof, name="typeof", curie=LINKML.curie('typeof'),
                   model_uri=LINKML.typeof, domain=TypeDefinition, range=Optional[Union[str, TypeDefinitionName]])

slots.base = Slot(uri=LINKML.base, name="base", curie=LINKML.curie('base'),
                   model_uri=LINKML.base, domain=TypeDefinition, range=Optional[str])

slots.type_uri = Slot(uri=LINKML.uri, name="type_uri", curie=LINKML.curie('uri'),
                   model_uri=LINKML.type_uri, domain=TypeDefinition, range=Optional[Union[str, URIorCURIE]])

slots.repr = Slot(uri=LINKML.repr, name="repr", curie=LINKML.curie('repr'),
                   model_uri=LINKML.repr, domain=TypeDefinition, range=Optional[str])

slots.alt_description_text = Slot(uri=LINKML.description, name="alt_description_text", curie=LINKML.curie('description'),
                   model_uri=LINKML.alt_description_text, domain=AltDescription, range=str)

slots.alt_description_source = Slot(uri=LINKML.source, name="alt_description_source", curie=LINKML.curie('source'),
                   model_uri=LINKML.alt_description_source, domain=AltDescription, range=Union[str, AltDescriptionSource])

slots.alt_descriptions = Slot(uri=LINKML.alt_descriptions, name="alt_descriptions", curie=LINKML.curie('alt_descriptions'),
                   model_uri=LINKML.alt_descriptions, domain=Element, range=Optional[Union[dict[Union[str, AltDescriptionSource], Union[dict, "AltDescription"]], list[Union[dict, "AltDescription"]]]])

slots.value = Slot(uri=SKOS.example, name="value", curie=SKOS.curie('example'),
                   model_uri=LINKML.value, domain=Example, range=Optional[str])

slots.value_description = Slot(uri=LINKML.description, name="value_description", curie=LINKML.curie('description'),
                   model_uri=LINKML.value_description, domain=Example, range=Optional[str])

slots.value_object = Slot(uri=LINKML.object, name="value_object", curie=LINKML.curie('object'),
                   model_uri=LINKML.value_object, domain=Example, range=Optional[Union[dict, Anything]])

slots.examples = Slot(uri=LINKML.examples, name="examples", curie=LINKML.curie('examples'),
                   model_uri=LINKML.examples, domain=Element, range=Optional[Union[Union[dict, "Example"], list[Union[dict, "Example"]]]])

slots.prefix_prefix = Slot(uri=SH.prefix, name="prefix_prefix", curie=SH.curie('prefix'),
                   model_uri=LINKML.prefix_prefix, domain=Prefix, range=Union[str, PrefixPrefixPrefix])

slots.prefix_reference = Slot(uri=SH.namespace, name="prefix_reference", curie=SH.curie('namespace'),
                   model_uri=LINKML.prefix_reference, domain=Prefix, range=Union[str, URI])

slots.prefixes = Slot(uri=SH.declare, name="prefixes", curie=SH.curie('declare'),
                   model_uri=LINKML.prefixes, domain=SchemaDefinition, range=Optional[Union[dict[Union[str, PrefixPrefixPrefix], Union[dict, "Prefix"]], list[Union[dict, "Prefix"]]]])

slots.setting_key = Slot(uri=LINKML.setting_key, name="setting_key", curie=LINKML.curie('setting_key'),
                   model_uri=LINKML.setting_key, domain=Setting, range=Union[str, SettingSettingKey])

slots.setting_value = Slot(uri=LINKML.setting_value, name="setting_value", curie=LINKML.curie('setting_value'),
                   model_uri=LINKML.setting_value, domain=Setting, range=str)

slots.settings = Slot(uri=LINKML.settings, name="settings", curie=LINKML.curie('settings'),
                   model_uri=LINKML.settings, domain=SchemaDefinition, range=Optional[Union[dict[Union[str, SettingSettingKey], Union[dict, "Setting"]], list[Union[dict, "Setting"]]]])

slots.import_from = Slot(uri=LINKML.import_from, name="import_from", curie=LINKML.curie('import_from'),
                   model_uri=LINKML.import_from, domain=ImportExpression, range=Union[str, URIorCURIE])

slots.import_as = Slot(uri=LINKML.import_as, name="import_as", curie=LINKML.curie('import_as'),
                   model_uri=LINKML.import_as, domain=ImportExpression, range=Optional[Union[str, NCName]])

slots.import_map = Slot(uri=LINKML.import_map, name="import_map", curie=LINKML.curie('import_map'),
                   model_uri=LINKML.import_map, domain=ImportExpression, range=Optional[Union[dict[Union[str, SettingSettingKey], Union[dict, "Setting"]], list[Union[dict, "Setting"]]]])

slots.local_name_source = Slot(uri=LINKML.local_name_source, name="local_name_source", curie=LINKML.curie('local_name_source'),
                   model_uri=LINKML.local_name_source, domain=LocalName, range=Union[str, LocalNameLocalNameSource])

slots.local_name_value = Slot(uri=SKOS.altLabel, name="local_name_value", curie=SKOS.curie('altLabel'),
                   model_uri=LINKML.local_name_value, domain=LocalName, range=str)

slots.local_names = Slot(uri=LINKML.local_names, name="local_names", curie=LINKML.curie('local_names'),
                   model_uri=LINKML.local_names, domain=Element, range=Optional[Union[dict[Union[str, LocalNameLocalNameSource], Union[dict, "LocalName"]], list[Union[dict, "LocalName"]]]])

slots.slot_group = Slot(uri=SH.group, name="slot_group", curie=SH.curie('group'),
                   model_uri=LINKML.slot_group, domain=SlotDefinition, range=Optional[Union[str, SlotDefinitionName]])

slots.is_grouping_slot = Slot(uri=LINKML.is_grouping_slot, name="is_grouping_slot", curie=LINKML.curie('is_grouping_slot'),
                   model_uri=LINKML.is_grouping_slot, domain=SlotDefinition, range=Optional[Union[bool, Bool]])

slots.followed_by = Slot(uri=LINKML.followed_by, name="followed_by", curie=LINKML.curie('followed_by'),
                   model_uri=LINKML.followed_by, domain=None, range=Optional[Union[dict, Expression]])

slots.reversed = Slot(uri=LINKML.reversed, name="reversed", curie=LINKML.curie('reversed'),
                   model_uri=LINKML.reversed, domain=None, range=Optional[Union[bool, Bool]])

slots.traverse = Slot(uri=LINKML.traverse, name="traverse", curie=LINKML.curie('traverse'),
                   model_uri=LINKML.traverse, domain=None, range=Optional[Union[str, SlotDefinitionName]])

slots.path_rule = Slot(uri=LINKML.path_rule, name="path_rule", curie=LINKML.curie('path_rule'),
                   model_uri=LINKML.path_rule, domain=SlotDefinition, range=Optional[Union[dict, PathExpression]])

slots.represents_relationship = Slot(uri=LINKML.represents_relationship, name="represents_relationship", curie=LINKML.curie('represents_relationship'),
                   model_uri=LINKML.represents_relationship, domain=ClassDefinition, range=Optional[Union[bool, Bool]])

slots.relational_role = Slot(uri=LINKML.relational_role, name="relational_role", curie=LINKML.curie('relational_role'),
                   model_uri=LINKML.relational_role, domain=SlotDefinition, range=Optional[Union[str, "RelationalRoleEnum"]])

slots.schema_definition_name = Slot(uri=RDFS.label, name="schema_definition_name", curie=RDFS.curie('label'),
                   model_uri=LINKML.schema_definition_name, domain=SchemaDefinition, range=Union[str, SchemaDefinitionName])

slots.type_expression_any_of = Slot(uri=LINKML.any_of, name="type_expression_any_of", curie=LINKML.curie('any_of'),
                   model_uri=LINKML.type_expression_any_of, domain=None, range=Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]])

slots.type_expression_all_of = Slot(uri=LINKML.all_of, name="type_expression_all_of", curie=LINKML.curie('all_of'),
                   model_uri=LINKML.type_expression_all_of, domain=None, range=Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]])

slots.type_expression_exactly_one_of = Slot(uri=LINKML.exactly_one_of, name="type_expression_exactly_one_of", curie=LINKML.curie('exactly_one_of'),
                   model_uri=LINKML.type_expression_exactly_one_of, domain=None, range=Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]])

slots.type_expression_none_of = Slot(uri=LINKML.none_of, name="type_expression_none_of", curie=LINKML.curie('none_of'),
                   model_uri=LINKML.type_expression_none_of, domain=None, range=Optional[Union[Union[dict, "AnonymousTypeExpression"], list[Union[dict, "AnonymousTypeExpression"]]]])

slots.type_definition_union_of = Slot(uri=LINKML.union_of, name="type_definition_union_of", curie=LINKML.curie('union_of'),
                   model_uri=LINKML.type_definition_union_of, domain=TypeDefinition, range=Optional[Union[Union[str, TypeDefinitionName], list[Union[str, TypeDefinitionName]]]])

slots.enum_binding_range = Slot(uri=LINKML.range, name="enum_binding_range", curie=LINKML.curie('range'),
                   model_uri=LINKML.enum_binding_range, domain=EnumBinding, range=Optional[Union[str, EnumDefinitionName]])

slots.structured_alias_categories = Slot(uri=DCTERMS.subject, name="structured_alias_categories", curie=DCTERMS.curie('subject'),
                   model_uri=LINKML.structured_alias_categories, domain=StructuredAlias, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.path_expression_followed_by = Slot(uri=LINKML.followed_by, name="path_expression_followed_by", curie=LINKML.curie('followed_by'),
                   model_uri=LINKML.path_expression_followed_by, domain=PathExpression, range=Optional[Union[dict, "PathExpression"]])

slots.path_expression_any_of = Slot(uri=LINKML.any_of, name="path_expression_any_of", curie=LINKML.curie('any_of'),
                   model_uri=LINKML.path_expression_any_of, domain=PathExpression, range=Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]])

slots.path_expression_exactly_one_of = Slot(uri=LINKML.exactly_one_of, name="path_expression_exactly_one_of", curie=LINKML.curie('exactly_one_of'),
                   model_uri=LINKML.path_expression_exactly_one_of, domain=PathExpression, range=Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]])

slots.path_expression_none_of = Slot(uri=LINKML.none_of, name="path_expression_none_of", curie=LINKML.curie('none_of'),
                   model_uri=LINKML.path_expression_none_of, domain=PathExpression, range=Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]])

slots.path_expression_all_of = Slot(uri=LINKML.all_of, name="path_expression_all_of", curie=LINKML.curie('all_of'),
                   model_uri=LINKML.path_expression_all_of, domain=PathExpression, range=Optional[Union[Union[dict, "PathExpression"], list[Union[dict, "PathExpression"]]]])

slots.slot_expression_any_of = Slot(uri=LINKML.any_of, name="slot_expression_any_of", curie=LINKML.curie('any_of'),
                   model_uri=LINKML.slot_expression_any_of, domain=None, range=Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]])

slots.slot_expression_all_of = Slot(uri=LINKML.all_of, name="slot_expression_all_of", curie=LINKML.curie('all_of'),
                   model_uri=LINKML.slot_expression_all_of, domain=None, range=Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]])

slots.slot_expression_exactly_one_of = Slot(uri=LINKML.exactly_one_of, name="slot_expression_exactly_one_of", curie=LINKML.curie('exactly_one_of'),
                   model_uri=LINKML.slot_expression_exactly_one_of, domain=None, range=Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]])

slots.slot_expression_none_of = Slot(uri=LINKML.none_of, name="slot_expression_none_of", curie=LINKML.curie('none_of'),
                   model_uri=LINKML.slot_expression_none_of, domain=None, range=Optional[Union[Union[dict, "AnonymousSlotExpression"], list[Union[dict, "AnonymousSlotExpression"]]]])

slots.slot_definition_is_a = Slot(uri=LINKML.is_a, name="slot_definition_is_a", curie=LINKML.curie('is_a'),
                   model_uri=LINKML.slot_definition_is_a, domain=SlotDefinition, range=Optional[Union[str, SlotDefinitionName]])

slots.slot_definition_mixins = Slot(uri=LINKML.mixins, name="slot_definition_mixins", curie=LINKML.curie('mixins'),
                   model_uri=LINKML.slot_definition_mixins, domain=SlotDefinition, range=Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]])

slots.slot_definition_apply_to = Slot(uri=LINKML.apply_to, name="slot_definition_apply_to", curie=LINKML.curie('apply_to'),
                   model_uri=LINKML.slot_definition_apply_to, domain=SlotDefinition, range=Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]])

slots.slot_definition_disjoint_with = Slot(uri=LINKML.disjoint_with, name="slot_definition_disjoint_with", curie=LINKML.curie('disjoint_with'),
                   model_uri=LINKML.slot_definition_disjoint_with, domain=SlotDefinition, range=Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]])

slots.slot_definition_union_of = Slot(uri=LINKML.union_of, name="slot_definition_union_of", curie=LINKML.curie('union_of'),
                   model_uri=LINKML.slot_definition_union_of, domain=SlotDefinition, range=Optional[Union[Union[str, SlotDefinitionName], list[Union[str, SlotDefinitionName]]]])

slots.class_expression_any_of = Slot(uri=LINKML.any_of, name="class_expression_any_of", curie=LINKML.curie('any_of'),
                   model_uri=LINKML.class_expression_any_of, domain=None, range=Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]])

slots.class_expression_all_of = Slot(uri=LINKML.all_of, name="class_expression_all_of", curie=LINKML.curie('all_of'),
                   model_uri=LINKML.class_expression_all_of, domain=None, range=Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]])

slots.class_expression_exactly_one_of = Slot(uri=LINKML.exactly_one_of, name="class_expression_exactly_one_of", curie=LINKML.curie('exactly_one_of'),
                   model_uri=LINKML.class_expression_exactly_one_of, domain=None, range=Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]])

slots.class_expression_none_of = Slot(uri=LINKML.none_of, name="class_expression_none_of", curie=LINKML.curie('none_of'),
                   model_uri=LINKML.class_expression_none_of, domain=None, range=Optional[Union[Union[dict, "AnonymousClassExpression"], list[Union[dict, "AnonymousClassExpression"]]]])

slots.class_definition_is_a = Slot(uri=LINKML.is_a, name="class_definition_is_a", curie=LINKML.curie('is_a'),
                   model_uri=LINKML.class_definition_is_a, domain=ClassDefinition, range=Optional[Union[str, ClassDefinitionName]])

slots.class_definition_mixins = Slot(uri=LINKML.mixins, name="class_definition_mixins", curie=LINKML.curie('mixins'),
                   model_uri=LINKML.class_definition_mixins, domain=ClassDefinition, range=Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]])

slots.class_definition_apply_to = Slot(uri=LINKML.apply_to, name="class_definition_apply_to", curie=LINKML.curie('apply_to'),
                   model_uri=LINKML.class_definition_apply_to, domain=ClassDefinition, range=Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]])

slots.class_definition_rules = Slot(uri=SH.rule, name="class_definition_rules", curie=SH.curie('rule'),
                   model_uri=LINKML.class_definition_rules, domain=ClassDefinition, range=Optional[Union[Union[dict, "ClassRule"], list[Union[dict, "ClassRule"]]]])

slots.class_definition_disjoint_with = Slot(uri=LINKML.disjoint_with, name="class_definition_disjoint_with", curie=LINKML.curie('disjoint_with'),
                   model_uri=LINKML.class_definition_disjoint_with, domain=ClassDefinition, range=Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]])

slots.class_definition_union_of = Slot(uri=LINKML.union_of, name="class_definition_union_of", curie=LINKML.curie('union_of'),
                   model_uri=LINKML.class_definition_union_of, domain=ClassDefinition, range=Optional[Union[Union[str, ClassDefinitionName], list[Union[str, ClassDefinitionName]]]])

slots.permissible_value_is_a = Slot(uri=LINKML.is_a, name="permissible_value_is_a", curie=LINKML.curie('is_a'),
                   model_uri=LINKML.permissible_value_is_a, domain=PermissibleValue, range=Optional[Union[str, PermissibleValueText]])

slots.permissible_value_mixins = Slot(uri=LINKML.mixins, name="permissible_value_mixins", curie=LINKML.curie('mixins'),
                   model_uri=LINKML.permissible_value_mixins, domain=PermissibleValue, range=Optional[Union[Union[str, PermissibleValueText], list[Union[str, PermissibleValueText]]]])
