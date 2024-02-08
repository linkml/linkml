# Auto generated from datasets.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-02-07T17:29:27
# Schema: datasets
#
# id: https://w3id.org/linkml/datasets
# description: A datamodel for datasets
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
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
from .types import Datetime, Integer, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import URI, URIorCURIE, XSDDateTime

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIBO = CurieNamespace('bibo', 'http://purl.org/ontology/bibo/')
CSVW = CurieNamespace('csvw', 'http://www.w3.org/ns/csvw#')
DATASETS = CurieNamespace('datasets', 'https://w3id.org/linkml/report')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
FORMATS = CurieNamespace('formats', 'http://www.w3.org/ns/formats/')
FRICTIONLESS = CurieNamespace('frictionless', 'https://specs.frictionlessdata.io/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MEDIATYPES = CurieNamespace('mediatypes', 'https://www.iana.org/assignments/media-types/')
OSLC = CurieNamespace('oslc', 'http://open-services.net/ns/core#')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
VOID = CurieNamespace('void', 'http://rdfs.org/ns/void#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = DATASETS


# Types

# Class references
class InformationId(extended_str):
    pass


class DataPackageId(InformationId):
    pass


class DataResourceId(InformationId):
    pass


@dataclass
class Information(YAMLRoot):
    """
    Grouping for datasets and data files
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = DATASETS["Information"]
    class_class_curie: ClassVar[str] = "datasets:Information"
    class_name: ClassVar[str] = "Information"
    class_model_uri: ClassVar[URIRef] = DATASETS.Information

    id: Union[str, InformationId] = None
    download_url: Optional[Union[str, URI]] = None
    license: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    conforms_to: Optional[Union[str, URIorCURIE]] = None
    conforms_to_schema: Optional[Union[str, URIorCURIE]] = None
    conforms_to_class: Optional[Union[str, URIorCURIE]] = None
    version: Optional[str] = None
    language: Optional[str] = None
    publisher: Optional[Union[str, URIorCURIE]] = None
    keywords: Optional[Union[str, List[str]]] = empty_list()
    issued: Optional[Union[str, XSDDateTime]] = None
    created_by: Optional[Union[str, URIorCURIE]] = None
    created_on: Optional[Union[str, XSDDateTime]] = None
    compression: Optional[str] = None
    was_derived_from: Optional[str] = None
    page: Optional[str] = None
    test_roles: Optional[Union[Union[str, "TestRole"], List[Union[str, "TestRole"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, InformationId):
            self.id = InformationId(self.id)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.conforms_to is not None and not isinstance(self.conforms_to, URIorCURIE):
            self.conforms_to = URIorCURIE(self.conforms_to)

        if self.conforms_to_schema is not None and not isinstance(self.conforms_to_schema, URIorCURIE):
            self.conforms_to_schema = URIorCURIE(self.conforms_to_schema)

        if self.conforms_to_class is not None and not isinstance(self.conforms_to_class, URIorCURIE):
            self.conforms_to_class = URIorCURIE(self.conforms_to_class)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        if self.publisher is not None and not isinstance(self.publisher, URIorCURIE):
            self.publisher = URIorCURIE(self.publisher)

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if self.issued is not None and not isinstance(self.issued, XSDDateTime):
            self.issued = XSDDateTime(self.issued)

        if self.created_by is not None and not isinstance(self.created_by, URIorCURIE):
            self.created_by = URIorCURIE(self.created_by)

        if self.created_on is not None and not isinstance(self.created_on, XSDDateTime):
            self.created_on = XSDDateTime(self.created_on)

        if self.compression is not None and not isinstance(self.compression, str):
            self.compression = str(self.compression)

        if self.was_derived_from is not None and not isinstance(self.was_derived_from, str):
            self.was_derived_from = str(self.was_derived_from)

        if self.page is not None and not isinstance(self.page, str):
            self.page = str(self.page)

        if not isinstance(self.test_roles, list):
            self.test_roles = [self.test_roles] if self.test_roles is not None else []
        self.test_roles = [v if isinstance(v, TestRole) else TestRole(v) for v in self.test_roles]

        super().__post_init__(**kwargs)


@dataclass
class DataPackage(Information):
    """
    A collection of data resources
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VOID["Dataset"]
    class_class_curie: ClassVar[str] = "void:Dataset"
    class_name: ClassVar[str] = "DataPackage"
    class_model_uri: ClassVar[URIRef] = DATASETS.DataPackage

    id: Union[str, DataPackageId] = None
    resources: Optional[Union[Union[str, DataResourceId], List[Union[str, DataResourceId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataPackageId):
            self.id = DataPackageId(self.id)

        if not isinstance(self.resources, list):
            self.resources = [self.resources] if self.resources is not None else []
        self.resources = [v if isinstance(v, DataResourceId) else DataResourceId(v) for v in self.resources]

        super().__post_init__(**kwargs)


@dataclass
class DataResource(Information):
    """
    An individual file or table
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Distribution"]
    class_class_curie: ClassVar[str] = "dcat:Distribution"
    class_name: ClassVar[str] = "DataResource"
    class_model_uri: ClassVar[URIRef] = DATASETS.DataResource

    id: Union[str, DataResourceId] = None
    path: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    format: Optional[Union[str, "FormatEnum"]] = None
    media_type: Optional[str] = None
    encoding: Optional[str] = None
    bytes: Optional[int] = None
    hash: Optional[str] = None
    md5: Optional[str] = None
    sha256: Optional[str] = None
    dialect: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataResourceId):
            self.id = DataResourceId(self.id)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.format is not None and not isinstance(self.format, FormatEnum):
            self.format = FormatEnum(self.format)

        if self.media_type is not None and not isinstance(self.media_type, str):
            self.media_type = str(self.media_type)

        if self.encoding is not None and not isinstance(self.encoding, str):
            self.encoding = str(self.encoding)

        if self.bytes is not None and not isinstance(self.bytes, int):
            self.bytes = int(self.bytes)

        if self.hash is not None and not isinstance(self.hash, str):
            self.hash = str(self.hash)

        if self.md5 is not None and not isinstance(self.md5, str):
            self.md5 = str(self.md5)

        if self.sha256 is not None and not isinstance(self.sha256, str):
            self.sha256 = str(self.sha256)

        if self.dialect is not None and not isinstance(self.dialect, str):
            self.dialect = str(self.dialect)

        super().__post_init__(**kwargs)


@dataclass
class FormatDialect(YAMLRoot):
    """
    Additional format information for a file
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = DATASETS["FormatDialect"]
    class_class_curie: ClassVar[str] = "datasets:FormatDialect"
    class_name: ClassVar[str] = "FormatDialect"
    class_model_uri: ClassVar[URIRef] = DATASETS.FormatDialect

    comment_prefix: Optional[str] = None
    delimiter: Optional[str] = None
    double_quote: Optional[str] = None
    header: Optional[str] = None
    quote_char: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.comment_prefix is not None and not isinstance(self.comment_prefix, str):
            self.comment_prefix = str(self.comment_prefix)

        if self.delimiter is not None and not isinstance(self.delimiter, str):
            self.delimiter = str(self.delimiter)

        if self.double_quote is not None and not isinstance(self.double_quote, str):
            self.double_quote = str(self.double_quote)

        if self.header is not None and not isinstance(self.header, str):
            self.header = str(self.header)

        if self.quote_char is not None and not isinstance(self.quote_char, str):
            self.quote_char = str(self.quote_char)

        super().__post_init__(**kwargs)


# Enumerations
class TestRole(EnumDefinitionImpl):

    Example = PermissibleValue(text="Example")
    CounterExample = PermissibleValue(text="CounterExample")

    _defn = EnumDefinition(
        name="TestRole",
    )

class MediaTypeEnum(EnumDefinitionImpl):

    csv = PermissibleValue(
        text="csv",
        meaning=MEDIATYPES["text/csv"])

    _defn = EnumDefinition(
        name="MediaTypeEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "rdf-xml",
            PermissibleValue(
                text="rdf-xml",
                meaning=MEDIATYPES["application/rdf+xml"]))

class FormatEnum(EnumDefinitionImpl):

    N3 = PermissibleValue(
        text="N3",
        meaning=FORMATS["N3"])
    Microdata = PermissibleValue(
        text="Microdata",
        meaning=FORMATS["microdata"])
    POWDER = PermissibleValue(
        text="POWDER",
        meaning=FORMATS["POWDER"])
    RDFa = PermissibleValue(
        text="RDFa",
        meaning=FORMATS["RDFa"])
    Turtle = PermissibleValue(
        text="Turtle",
        meaning=FORMATS["Turtle"])
    TriG = PermissibleValue(
        text="TriG",
        meaning=FORMATS["TriG"])
    YAML = PermissibleValue(text="YAML")
    JSON = PermissibleValue(text="JSON")

    _defn = EnumDefinition(
        name="FormatEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "JSON-LD",
            PermissibleValue(
                text="JSON-LD",
                meaning=FORMATS["JSON-LD"]))
        setattr(cls, "N-Triples",
            PermissibleValue(
                text="N-Triples",
                meaning=FORMATS["N-Triples"]))
        setattr(cls, "N-Quads",
            PermissibleValue(
                text="N-Quads",
                meaning=FORMATS["N-Quads"]))
        setattr(cls, "LD Patch",
            PermissibleValue(
                text="LD Patch",
                meaning=FORMATS["LD_Patch"]))
        setattr(cls, "OWL XML Serialization",
            PermissibleValue(
                text="OWL XML Serialization",
                meaning=FORMATS["OWL_XML"]))
        setattr(cls, "OWL Functional Syntax",
            PermissibleValue(
                text="OWL Functional Syntax",
                meaning=FORMATS["OWL_Functional"]))
        setattr(cls, "OWL Manchester Syntax",
            PermissibleValue(
                text="OWL Manchester Syntax",
                meaning=FORMATS["OWL_Manchester"]))
        setattr(cls, "POWDER-S",
            PermissibleValue(
                text="POWDER-S",
                meaning=FORMATS["POWDER-S"]))
        setattr(cls, "PROV-N",
            PermissibleValue(
                text="PROV-N",
                meaning=FORMATS["PROV-N"]))
        setattr(cls, "PROV-XML",
            PermissibleValue(
                text="PROV-XML",
                meaning=FORMATS["PROV-XML"]))
        setattr(cls, "RDF/JSON",
            PermissibleValue(
                text="RDF/JSON",
                meaning=FORMATS["RDF_JSON"]))
        setattr(cls, "RDF/XML",
            PermissibleValue(
                text="RDF/XML",
                meaning=FORMATS["RDF_XML"]))
        setattr(cls, "RIF XML Syntax",
            PermissibleValue(
                text="RIF XML Syntax",
                meaning=FORMATS["RIF_XML"]))
        setattr(cls, "SPARQL Results in XML",
            PermissibleValue(
                text="SPARQL Results in XML",
                meaning=FORMATS["SPARQL_Results_XML"]))
        setattr(cls, "SPARQL Results in JSON",
            PermissibleValue(
                text="SPARQL Results in JSON",
                meaning=FORMATS["SPARQL_Results_JSON"]))
        setattr(cls, "SPARQL Results in CSV",
            PermissibleValue(
                text="SPARQL Results in CSV",
                meaning=FORMATS["SPARQL_Results_CSV"]))
        setattr(cls, "SPARQL Results in TSV",
            PermissibleValue(
                text="SPARQL Results in TSV",
                meaning=FORMATS["SPARQL_Results_TSV"]))

# Slots
class slots:
    pass

slots.id = Slot(uri=DCTERMS.identifier, name="id", curie=DCTERMS.curie('identifier'),
                   model_uri=DATASETS.id, domain=None, range=URIRef)

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=DATASETS.title, domain=None, range=Optional[str])

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=DATASETS.description, domain=None, range=Optional[str])

slots.language = Slot(uri=DATASETS.language, name="language", curie=DATASETS.curie('language'),
                   model_uri=DATASETS.language, domain=None, range=Optional[str])

slots.publisher = Slot(uri=DCTERMS.publisher, name="publisher", curie=DCTERMS.curie('publisher'),
                   model_uri=DATASETS.publisher, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.issued = Slot(uri=DCTERMS.issued, name="issued", curie=DCTERMS.curie('issued'),
                   model_uri=DATASETS.issued, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.page = Slot(uri=DCAT.landingPage, name="page", curie=DCAT.curie('landingPage'),
                   model_uri=DATASETS.page, domain=None, range=Optional[str])

slots.dialect = Slot(uri=CSVW.dialect, name="dialect", curie=CSVW.curie('dialect'),
                   model_uri=DATASETS.dialect, domain=None, range=Optional[str])

slots.bytes = Slot(uri=DCAT.byteSize, name="bytes", curie=DCAT.curie('byteSize'),
                   model_uri=DATASETS.bytes, domain=None, range=Optional[int])

slots.path = Slot(uri=DATASETS.path, name="path", curie=DATASETS.curie('path'),
                   model_uri=DATASETS.path, domain=None, range=Optional[str])

slots.download_url = Slot(uri=DCAT.downloadURL, name="download_url", curie=DCAT.curie('downloadURL'),
                   model_uri=DATASETS.download_url, domain=None, range=Optional[Union[str, URI]])

slots.format = Slot(uri=DCTERMS.format, name="format", curie=DCTERMS.curie('format'),
                   model_uri=DATASETS.format, domain=None, range=Optional[Union[str, "FormatEnum"]])

slots.compression = Slot(uri=DATASETS.compression, name="compression", curie=DATASETS.curie('compression'),
                   model_uri=DATASETS.compression, domain=None, range=Optional[str])

slots.encoding = Slot(uri=DATASETS.encoding, name="encoding", curie=DATASETS.curie('encoding'),
                   model_uri=DATASETS.encoding, domain=None, range=Optional[str])

slots.hash = Slot(uri=DATASETS.hash, name="hash", curie=DATASETS.curie('hash'),
                   model_uri=DATASETS.hash, domain=None, range=Optional[str])

slots.sha256 = Slot(uri=DATASETS.sha256, name="sha256", curie=DATASETS.curie('sha256'),
                   model_uri=DATASETS.sha256, domain=None, range=Optional[str])

slots.md5 = Slot(uri=DATASETS.md5, name="md5", curie=DATASETS.curie('md5'),
                   model_uri=DATASETS.md5, domain=None, range=Optional[str])

slots.media_type = Slot(uri=DCAT.mediaType, name="media_type", curie=DCAT.curie('mediaType'),
                   model_uri=DATASETS.media_type, domain=None, range=Optional[str])

slots.conforms_to = Slot(uri=DCTERMS.conformsTo, name="conforms_to", curie=DCTERMS.curie('conformsTo'),
                   model_uri=DATASETS.conforms_to, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.conforms_to_schema = Slot(uri=DATASETS.conforms_to_schema, name="conforms_to_schema", curie=DATASETS.curie('conforms_to_schema'),
                   model_uri=DATASETS.conforms_to_schema, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.conforms_to_class = Slot(uri=DATASETS.conforms_to_class, name="conforms_to_class", curie=DATASETS.curie('conforms_to_class'),
                   model_uri=DATASETS.conforms_to_class, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.profile = Slot(uri=DATASETS.profile, name="profile", curie=DATASETS.curie('profile'),
                   model_uri=DATASETS.profile, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.keywords = Slot(uri=DCAT.keyword, name="keywords", curie=DCAT.curie('keyword'),
                   model_uri=DATASETS.keywords, domain=None, range=Optional[Union[str, List[str]]])

slots.themes = Slot(uri=DCAT.theme, name="themes", curie=DCAT.curie('theme'),
                   model_uri=DATASETS.themes, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.resources = Slot(uri=DCAT.distribution, name="resources", curie=DCAT.curie('distribution'),
                   model_uri=DATASETS.resources, domain=None, range=Optional[Union[Union[str, DataResourceId], List[Union[str, DataResourceId]]]])

slots.test_roles = Slot(uri=DATASETS.test_roles, name="test_roles", curie=DATASETS.curie('test_roles'),
                   model_uri=DATASETS.test_roles, domain=None, range=Optional[Union[Union[str, "TestRole"], List[Union[str, "TestRole"]]]])

slots.created_by = Slot(uri=PAV.createdBy, name="created_by", curie=PAV.curie('createdBy'),
                   model_uri=DATASETS.created_by, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.created_on = Slot(uri=PAV.createdOn, name="created_on", curie=PAV.curie('createdOn'),
                   model_uri=DATASETS.created_on, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.last_updated_on = Slot(uri=PAV.lastUpdatedOn, name="last_updated_on", curie=PAV.curie('lastUpdatedOn'),
                   model_uri=DATASETS.last_updated_on, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.modified_by = Slot(uri=OSLC.modifiedBy, name="modified_by", curie=OSLC.curie('modifiedBy'),
                   model_uri=DATASETS.modified_by, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.status = Slot(uri=BIBO.status, name="status", curie=BIBO.curie('status'),
                   model_uri=DATASETS.status, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.license = Slot(uri=DCTERMS.license, name="license", curie=DCTERMS.curie('license'),
                   model_uri=DATASETS.license, domain=None, range=Optional[str])

slots.version = Slot(uri=PAV.version, name="version", curie=PAV.curie('version'),
                   model_uri=DATASETS.version, domain=None, range=Optional[str])

slots.was_derived_from = Slot(uri=PROV.wasDerivedFrom, name="was_derived_from", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=DATASETS.was_derived_from, domain=None, range=Optional[str])

slots.formatDialect__comment_prefix = Slot(uri=DATASETS.comment_prefix, name="formatDialect__comment_prefix", curie=DATASETS.curie('comment_prefix'),
                   model_uri=DATASETS.formatDialect__comment_prefix, domain=None, range=Optional[str])

slots.formatDialect__delimiter = Slot(uri=DATASETS.delimiter, name="formatDialect__delimiter", curie=DATASETS.curie('delimiter'),
                   model_uri=DATASETS.formatDialect__delimiter, domain=None, range=Optional[str])

slots.formatDialect__double_quote = Slot(uri=DATASETS.double_quote, name="formatDialect__double_quote", curie=DATASETS.curie('double_quote'),
                   model_uri=DATASETS.formatDialect__double_quote, domain=None, range=Optional[str])

slots.formatDialect__header = Slot(uri=DATASETS.header, name="formatDialect__header", curie=DATASETS.curie('header'),
                   model_uri=DATASETS.formatDialect__header, domain=None, range=Optional[str])

slots.formatDialect__quote_char = Slot(uri=DATASETS.quote_char, name="formatDialect__quote_char", curie=DATASETS.curie('quote_char'),
                   model_uri=DATASETS.formatDialect__quote_char, domain=None, range=Optional[str])
