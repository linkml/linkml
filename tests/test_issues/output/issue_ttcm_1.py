# Auto generated from resourcedescription.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: resourcedescription
#
# id: https://hotecosystem.org/tccm/resourcedescription
# description: ResourceDescription represents the shared characteristics common to both abstract and resource
#              version descriptions. ResourceDescription is an abstract type and, as such, cannot be directly
#              created. Resource descriptions are Changeable, meaning that they have identity and can be created,
#              updated, and deleted.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.annotations import Annotation
from linkml_runtime.linkml_model.extensions import Extension
from linkml_runtime.linkml_model.types import String
from linkml_runtime.utils.metamodelcore import Curie, NCName, URI, URIorCURIE, XSDDateTime

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TCCM = CurieNamespace('tccm', 'https://hotecosystem.org/tccm/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = TCCM


# Types
class DateAndTime(XSDDateTime):
    """ Represents an “Instant” as defined in the OWL Time Specification . Implementations must be able to support temporal units of second, minute, hour, day, month, and year, and be able to represent and compare instances represented in any of these units. DateAndTime can only provide a partial ordering and, as a consequence, i s never used as an index, unique identifier, or to sequence data or events. """
    type_class_uri = XSD.dateTime
    type_class_curie = "xsd:dateTime"
    type_name = "DateAndTime"
    type_model_uri = TCCM.DateAndTime


class NaturalNumber(int):
    """ A non-negative integer (N). NatrualNumber is used exclusively for representing quantities. """
    type_class_uri = XSD.nonNegativeInteger
    type_class_curie = "xsd:nonNegativeInteger"
    type_name = "NaturalNumber"
    type_model_uri = TCCM.NaturalNumber


class LocalIdentifier(String):
    """ An identifier that uniquely references a class, individual, property, or other resource within the context of a specific TCCM service implementation. LocalIdentifier syntax must match the PNAME production as defined in the SPARQL Query Specification . LocalIdentifiers may begin with leading digits, where XML Local Identifiers and NameSpaceIdentifiers may not. """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "LocalIdentifier"
    type_model_uri = TCCM.LocalIdentifier


class NamespaceIdentifier(NCName):
    """ An identifier that uniquely references the scoping namespace of an Entity (class, role, or individual) within the context of a TCCM service. NameSpaceIdentifier syntax must match the PNAME NS production as defined in the SPARQL Query Specification - meaning that it must begin with an alphabetic character """
    type_class_uri = XSD.NMTOKEN
    type_class_curie = "xsd:NMTOKEN"
    type_name = "NamespaceIdentifier"
    type_model_uri = TCCM.NamespaceIdentifier


class URI(URI):
    """ A Universal Resource Identifier (URI) as defined in IETF RFC 3986. TCCM implementations are encouraged to consider implementing this data type using the IRI (RFC3987) specification """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "URI"
    type_model_uri = TCCM.URI


class CURIE(Curie):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "CURIE"
    type_model_uri = TCCM.CURIE


class URIorCurie(URIorCURIE):
    """ a URI or a CURIE """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "URIorCurie"
    type_model_uri = TCCM.URIorCurie


class PersistentURI(URIorCurie):
    """ A Universal Resource Identifier (URI) that persists across service instances. PersistentURIs have enduring reference and meaning. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "PersistentURI"
    type_model_uri = TCCM.PersistentURI


class LocalURI(URIorCurie):
    """ A URI or handle whose scope is local to the implementing service. LocalURI cannot be used as a permanent identifier in a message or a data record. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "LocalURI"
    type_model_uri = TCCM.LocalURI


class ChangeSetURI(PersistentURI):
    """ The unique identifier of a set of change instructions that can potentially transform the contents of a TCCM service instance from one state to another. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ChangeSetURI"
    type_model_uri = TCCM.ChangeSetURI


class DocumentURI(PersistentURI):
    """ A reference to a “work” in the bibliographic sense. It is not necessary that a Document URI be directly or indirectly resolvable to a digital resource - it may simply be the name of a book, publication, or other abstraction. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "DocumentURI"
    type_model_uri = TCCM.DocumentURI


class ExternalURI(PersistentURI):
    """ A URI that names a unique resource. CTS2 implementations should never assume that ExternalURI is resolvable via an http: GET operation - ExternalURIs should always be passed as parameters to service implementations to get the sanctioned equivalent in a given service context. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ExternalURI"
    type_model_uri = TCCM.ExternalURI


class ServiceURI(LocalURI):
    """ The URI or CURIE of a service implementation """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ServiceURI"
    type_model_uri = TCCM.ServiceURI


class RenderingURI(LocalURI):
    """ A URI or handle that is directly readable by a specific instance of a TCCM service implementation. RenderingURI must resolve to Changeable CTS2 element. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "RenderingURI"
    type_model_uri = TCCM.RenderingURI


class DirectoryURI(LocalURI):
    """ The unique name of a query that when executed results in a list of resources that, in the context of a given service, satisfy the query. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "DirectoryURI"
    type_model_uri = TCCM.DirectoryURI


class ValueSet(URIorCurie):
    """ A URI that can be indirectly resolved to a set of entity descriptions """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ValueSet"
    type_model_uri = TCCM.ValueSet


class ASSOCIATION(ValueSet):
    """ A formal “semantic” assertion about a named entity, in the form of subject, predicate, and object including any provenance, qualifiers, or internal BNODEs. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ASSOCIATION"
    type_model_uri = TCCM.ASSOCIATION


class BINDINGQUALIFIER(ValueSet):
    """ An assertion about the semantics of a concept domain / value set binding. This model element exists specifically to address section 2.4.2.23 of the HL7 SFM14, which needs a qualifier that indicates whether the binding is “overall,” “minimal,” or “maximum.”
The TCCM specification does not formally define the semantics of the various possible BINDING_QUALIFIER elements: it is up to specific implementations and service clients to interpret the meaning of the specific binding qualifiers that may be represented in references of this type. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "BINDING_QUALIFIER"
    type_model_uri = TCCM.BINDINGQUALIFIER


class CASESIGNIFICANCE(ValueSet):
    """ Identifies the significance of case in a term or designation. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "CASE_SIGNIFICANCE"
    type_model_uri = TCCM.CASESIGNIFICANCE


class CODESYSTEMCATEGORY(ValueSet):
    """ The general category of a code system (flat list, subject heading system, taxonomy, thesaurus, classification, terminology, description logic ontology, first order predicate logic, etc.) (same as KnowledgeRepresentationParadigm: OMV 5.8). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "CODE_SYSTEM_CATEGORY"
    type_model_uri = TCCM.CODESYSTEMCATEGORY


class CODESYSTEM(ValueSet):
    """ A collection of metadata about the provenance, use, and distribution of a code system or ontology. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "CODE_SYSTEM"
    type_model_uri = TCCM.CODESYSTEM


class CODESYSTEMVERSION(ValueSet):
    """ A collection of metadata about content and distribution format of a particular version or release of a code system. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "CODE_SYSTEM_VERSION"
    type_model_uri = TCCM.CODESYSTEMVERSION


class CONCEPTDOMAIN(ValueSet):
    """ The description of the conceptual domain of a field in a message, column in a database, field on a form, etc. Equivalent to the ISO 11179-3 “Data Element Concept.” """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "CONCEPT_DOMAIN"
    type_model_uri = TCCM.CONCEPTDOMAIN


class CONTEXT(ValueSet):
    """ External and environmental factors that serve to discriminate among multiple possible selections. While it is assumed that the specific contexts referenced by CONTEXT are represented by entity descriptions contained in some ontology or coding scheme, the CTS2 specification does not recommend any targets. Note, however, the TCCM context is intended to represent the notion of “jurisdictional domain” or “realm” as described in the HL7 CTS2 SFM . """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "CONTEXT"
    type_model_uri = TCCM.CONTEXT


class DESIGNATIONFIDELITY(ValueSet):
    """ Identifies how well a particular designation represents the intended meaning of the referenced entity. TCCM implementations may consider using the SKOS16 semantic relations to represent this relationship. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "DESIGNATION_FIDELITY"
    type_model_uri = TCCM.DESIGNATIONFIDELITY


class DESIGNATIONTYPE(ValueSet):
    """ The particular form or type of a given designation: can be “short name,” “long name,” “abbreviation,” “eponym.” """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "DESIGNATION_TYPE"
    type_model_uri = TCCM.DESIGNATIONTYPE


class FORMALITYLEVEL(ValueSet):
    """ The level of formality of an ontology (OMV 5.9). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "FORMALITY_LEVEL"
    type_model_uri = TCCM.FORMALITYLEVEL


class FORMAT(ValueSet):
    """ A particular way that information is encoded for storage in a computer file """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "FORMAT"
    type_model_uri = TCCM.FORMAT


class LANGUAGE(ValueSet):
    """ A spoken or written language intended for human consumption. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "LANGUAGE"
    type_model_uri = TCCM.LANGUAGE


class MATCHALGORITHM(ValueSet):
    """ A predicate that determines whether an entity resource qualities for membership in a set based on supplied matching criteria. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "MATCH_ALGORITHM"
    type_model_uri = TCCM.MATCHALGORITHM


class MAP(ValueSet):
    """ A set of rules that associate a set of entity references from one domain into those in another. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "MAP"
    type_model_uri = TCCM.MAP


class MAPCORRELATION(ValueSet):
    """ An assertion about the strength or significance of a specific rule in a Map. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "MAP_CORRELATION"
    type_model_uri = TCCM.MAPCORRELATION


class MAPVERSION(ValueSet):
    """ The state of a Map at a given point in time. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "MAP_VERSION"
    type_model_uri = TCCM.MAPVERSION


class MODELATTRIBUTE(ValueSet):
    """ An attribute defined in CTS2 information model. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "MODEL_ATTRIBUTE"
    type_model_uri = TCCM.MODELATTRIBUTE


class NAMESPACE(ValueSet):
    """ A reference to a conceptual space that groups identifiers to avoid conflict with items that have the same name but different meanings. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "NAMESPACE"
    type_model_uri = TCCM.NAMESPACE


class ONTOLOGYENGINEERINGMETHODOLOGY(ValueSet):
    """ Information about the ontology engineering methodology (OMV 5.4) (sic). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ONTOLOGY_ENGINEERING_METHODOLOGY"
    type_model_uri = TCCM.ONTOLOGYENGINEERINGMETHODOLOGY


class ONTOLOGYENGINEERINGTOOL(ValueSet):
    """ A tool used to create the ontology (OMV 5.5). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ONTOLOGY_ENGINEERING_TOOL"
    type_model_uri = TCCM.ONTOLOGYENGINEERINGTOOL


class ONTOLOGYDOMAIN(ValueSet):
    """ While the domain can refer to any topic ontology it is advised to use one of the established general purpose topic hierarchy like DMOZ or domain specific topic like ACM for the computer science domain. Only this way it can be ensured that meaningful information about the relation of the domains of two separate ontologies can be deduced (OMV 5.1 1)(sic). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ONTOLOGY_DOMAIN"
    type_model_uri = TCCM.ONTOLOGYDOMAIN


class ONTOLOGYLANGUAGE(ValueSet):
    """ Information about the language in which the ontology is implemented (OMV 5.7). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ONTOLOGY_LANGUAGE"
    type_model_uri = TCCM.ONTOLOGYLANGUAGE


class ONTOLOGYSYNTAX(ValueSet):
    """ Information about the syntax used by an ontology (OMV 5.6). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ONTOLOGY_SYNTAX"
    type_model_uri = TCCM.ONTOLOGYSYNTAX


class ONTOLOGYTASK(ValueSet):
    """ Information about the task the ontology was intended to be used for (OMV 5.10). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ONTOLOGY_TASK"
    type_model_uri = TCCM.ONTOLOGYTASK


class ONTOLOGYTYPE(ValueSet):
    """ Categorizes ontologies (OMV 5.2). """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ONTOLOGY_TYPE"
    type_model_uri = TCCM.ONTOLOGYTYPE


class PREDICATE(ValueSet):
    """ A property or relation between entities. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "PREDICATE"
    type_model_uri = TCCM.PREDICATE


class REASONINGALGORITHM(ValueSet):
    """ A set of formal rules that allow the deduction of additional assertions from a supplied list of axioms. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "REASONING_ALGORITHM"
    type_model_uri = TCCM.REASONINGALGORITHM


class RESOURCETYPE(ValueSet):
    """ A class of which a referencing resource is an instance of. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "RESOURCE TYPE"
    type_model_uri = TCCM.RESOURCETYPE


class ROLE(ValueSet):
    """ A role that a SOURCE can play in the construction or dissemination of a terminological resource. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ROLE"
    type_model_uri = TCCM.ROLE


class SOURCE(ValueSet):
    """ An individual, organization, or bibliographic reference. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "SOURCE"
    type_model_uri = TCCM.SOURCE


class STATEMENT(ValueSet):
    """ An atomic assertion about a CTS2 resource. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "STATEMENT"
    type_model_uri = TCCM.STATEMENT


class STATUS(ValueSet):
    """ The state of a resource or other entry in an external workflow. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "STATUS"
    type_model_uri = TCCM.STATUS


class VALUESET(ValueSet):
    """ A set of entity references. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "VALUE_SET"
    type_model_uri = TCCM.VALUESET


class VALUESETDEFINITION(ValueSet):
    """ A set of rules that can be applied to specified versions or one or more code systems to yield a set of entity references. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "VALUE_SET_DEFINITION"
    type_model_uri = TCCM.VALUESETDEFINITION


class VERSIONTAG(ValueSet):
    """ An identifier that can be assigned to resource versions by a service implementation to identify their state in the service workflow. Examples might include “development,” “test,” “production,” etc. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "VERSION_TAG"
    type_model_uri = TCCM.VERSIONTAG


# Class references



@dataclass
class ResourceDescription(YAMLRoot):
    """
    ResourceDescription represents the shared characteristics common to both abstract and resource version
    descriptions. ResourceDescription is an abstract type and, as such, cannot be directly created. Resource
    descriptions are Changeable, meaning that they have identity and can be created, updated, and deleted.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ResourceDescription
    class_class_curie: ClassVar[str] = "tccm:ResourceDescription"
    class_name: ClassVar[str] = "ResourceDescription"
    class_model_uri: ClassVar[URIRef] = TCCM.ResourceDescription

    about: Union[str, ExternalURI] = None
    resourceID: Union[str, LocalIdentifier] = None
    formalName: Optional[str] = None
    keyword: Optional[Union[str, List[str]]] = empty_list()
    resourceSynopsis: Optional[str] = None
    additionalDocumentation: Optional[Union[Union[str, PersistentURI], List[Union[str, PersistentURI]]]] = empty_list()
    rights: Optional[str] = None
    alternateID: Optional[str] = None
    extensions: Optional[Union[Union[dict, Extension], List[Union[dict, Extension]]]] = empty_list()
    annotations: Optional[Union[Union[dict, Annotation], List[Union[dict, Annotation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.about):
            self.MissingRequiredField("about")
        if not isinstance(self.about, ExternalURI):
            self.about = ExternalURI(self.about)

        if self._is_empty(self.resourceID):
            self.MissingRequiredField("resourceID")
        if not isinstance(self.resourceID, LocalIdentifier):
            self.resourceID = LocalIdentifier(self.resourceID)

        if self.formalName is not None and not isinstance(self.formalName, str):
            self.formalName = str(self.formalName)

        if not isinstance(self.keyword, list):
            self.keyword = [self.keyword] if self.keyword is not None else []
        self.keyword = [v if isinstance(v, str) else str(v) for v in self.keyword]

        if self.resourceSynopsis is not None and not isinstance(self.resourceSynopsis, str):
            self.resourceSynopsis = str(self.resourceSynopsis)

        if not isinstance(self.additionalDocumentation, list):
            self.additionalDocumentation = [self.additionalDocumentation] if self.additionalDocumentation is not None else []
        self.additionalDocumentation = [v if isinstance(v, PersistentURI) else PersistentURI(v) for v in self.additionalDocumentation]

        if self.rights is not None and not isinstance(self.rights, str):
            self.rights = str(self.rights)

        if self.alternateID is not None and not isinstance(self.alternateID, str):
            self.alternateID = str(self.alternateID)

        self._normalize_inlined_as_dict(slot_name="extensions", slot_type=Extension, key_name="tag", keyed=False)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="tag", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class SourceAndNotation(YAMLRoot):
    """
    Format and notation that some or all the releases (versions) of this resource are published in
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.SourceAndNotation
    class_class_curie: ClassVar[str] = "tccm:SourceAndNotation"
    class_name: ClassVar[str] = "SourceAndNotation"
    class_model_uri: ClassVar[URIRef] = TCCM.SourceAndNotation

    sourceAndNotationDescription: Optional[str] = None
    sourceDocument: Optional[Union[str, PersistentURI]] = None
    sourceLanguage: Optional[Union[dict, "OntologyLanguageReference"]] = None
    sourceDocumentSyntax: Optional[Union[dict, "OntologySyntaxReference"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.sourceAndNotationDescription is not None and not isinstance(self.sourceAndNotationDescription, str):
            self.sourceAndNotationDescription = str(self.sourceAndNotationDescription)

        if self.sourceDocument is not None and not isinstance(self.sourceDocument, PersistentURI):
            self.sourceDocument = PersistentURI(self.sourceDocument)

        if self.sourceLanguage is not None and not isinstance(self.sourceLanguage, OntologyLanguageReference):
            self.sourceLanguage = OntologyLanguageReference(**as_dict(self.sourceLanguage))

        if self.sourceDocumentSyntax is not None and not isinstance(self.sourceDocumentSyntax, OntologySyntaxReference):
            self.sourceDocumentSyntax = OntologySyntaxReference(**as_dict(self.sourceDocumentSyntax))

        super().__post_init__(**kwargs)


@dataclass
class AbstractResourceDescription(ResourceDescription):
    """
    The description of the characteristics of a resource that are independent of the resource content.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.AbstractResourceDescription
    class_class_curie: ClassVar[str] = "tccm:AbstractResourceDescription"
    class_name: ClassVar[str] = "AbstractResourceDescription"
    class_model_uri: ClassVar[URIRef] = TCCM.AbstractResourceDescription

    about: Union[str, ExternalURI] = None
    resourceID: Union[str, LocalIdentifier] = None
    releaseDocumentation: Optional[str] = None
    releaseFormat: Optional[Union[Union[dict, SourceAndNotation], List[Union[dict, SourceAndNotation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.releaseDocumentation is not None and not isinstance(self.releaseDocumentation, str):
            self.releaseDocumentation = str(self.releaseDocumentation)

        if not isinstance(self.releaseFormat, list):
            self.releaseFormat = [self.releaseFormat] if self.releaseFormat is not None else []
        self.releaseFormat = [v if isinstance(v, SourceAndNotation) else SourceAndNotation(**as_dict(v)) for v in self.releaseFormat]

        super().__post_init__(**kwargs)


@dataclass
class ResourceVersionDescription(ResourceDescription):
    """
    Information about the source, format, release date, version identifier, etc. of a specific version of an abstract
    resource.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ResourceVersionDescription
    class_class_curie: ClassVar[str] = "tccm:ResourceVersionDescription"
    class_name: ClassVar[str] = "ResourceVersionDescription"
    class_model_uri: ClassVar[URIRef] = TCCM.ResourceVersionDescription

    about: Union[str, ExternalURI] = None
    resourceID: Union[str, LocalIdentifier] = None
    documentURI: Optional[Union[str, DocumentURI]] = None
    sourceAndNotation: Optional[Union[dict, SourceAndNotation]] = None
    predecessor: Optional[Union[dict, "NameAndMeaningReference"]] = None
    officialResourceVersionID: Optional[str] = None
    officialReleaseDate: Optional[Union[str, XSDDateTime]] = None
    officialActivationDate: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.documentURI is not None and not isinstance(self.documentURI, DocumentURI):
            self.documentURI = DocumentURI(self.documentURI)

        if self.sourceAndNotation is not None and not isinstance(self.sourceAndNotation, SourceAndNotation):
            self.sourceAndNotation = SourceAndNotation(**as_dict(self.sourceAndNotation))

        if self.predecessor is not None and not isinstance(self.predecessor, NameAndMeaningReference):
            self.predecessor = NameAndMeaningReference(**as_dict(self.predecessor))

        if self.officialResourceVersionID is not None and not isinstance(self.officialResourceVersionID, str):
            self.officialResourceVersionID = str(self.officialResourceVersionID)

        if self.officialReleaseDate is not None and not isinstance(self.officialReleaseDate, XSDDateTime):
            self.officialReleaseDate = XSDDateTime(self.officialReleaseDate)

        if self.officialActivationDate is not None and not isinstance(self.officialActivationDate, XSDDateTime):
            self.officialActivationDate = XSDDateTime(self.officialActivationDate)

        super().__post_init__(**kwargs)


@dataclass
class NameAndMeaningReference(YAMLRoot):
    """
    A NameAndMeaningReference consists of a local identifier that references a unique meaning within the context of a
    given domain in a TCCM service instance and a globally unique URI that identifies the intended meaning of the
    identifier.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.NameAndMeaningReference
    class_class_curie: ClassVar[str] = "tccm:NameAndMeaningReference"
    class_name: ClassVar[str] = "NameAndMeaningReference"
    class_model_uri: ClassVar[URIRef] = TCCM.NameAndMeaningReference

    name: Union[str, LocalIdentifier] = None
    uri: Optional[Union[str, ExternalURI]] = None
    href: Optional[Union[str, RenderingURI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, LocalIdentifier):
            self.name = LocalIdentifier(self.name)

        if self.uri is not None and not isinstance(self.uri, ExternalURI):
            self.uri = ExternalURI(self.uri)

        if self.href is not None and not isinstance(self.href, RenderingURI):
            self.href = RenderingURI(self.href)

        super().__post_init__(**kwargs)


@dataclass
class AssociationReference(NameAndMeaningReference):
    """
    A name or identifier that uniquely names an association instance in a code system.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.AssociationReference
    class_class_curie: ClassVar[str] = "tccm:AssociationReference"
    class_name: ClassVar[str] = "AssociationReference"
    class_model_uri: ClassVar[URIRef] = TCCM.AssociationReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class BindingQualifierReference(NameAndMeaningReference):
    """
    A reference to an entity that describes the role that a given value set binding plays for a concept domain. T
    ypical values represent “overall,” “minimum” or “maximum,” the significance of which can be found in H L7 Version
    3 documentation.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.BindingQualifierReference
    class_class_curie: ClassVar[str] = "tccm:BindingQualifierReference"
    class_name: ClassVar[str] = "BindingQualifierReference"
    class_model_uri: ClassVar[URIRef] = TCCM.BindingQualifierReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class CaseSignificanceReference(NameAndMeaningReference):
    """
    A reference to an entity that describes significance of the case in term or designation.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.CaseSignificanceReference
    class_class_curie: ClassVar[str] = "tccm:CaseSignificanceReference"
    class_name: ClassVar[str] = "CaseSignificanceReference"
    class_model_uri: ClassVar[URIRef] = TCCM.CaseSignificanceReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class CodeSystemCategoryReference(NameAndMeaningReference):
    """
    A reference to information about a paradigm model used to create an ontology (a.k.a. knowledge representation
    paradigm).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.CodeSystemCategoryReference
    class_class_curie: ClassVar[str] = "tccm:CodeSystemCategoryReference"
    class_name: ClassVar[str] = "CodeSystemCategoryReference"
    class_model_uri: ClassVar[URIRef] = TCCM.CodeSystemCategoryReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class CodeSystemReference(NameAndMeaningReference):
    """
    A reference to a code system or ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.CodeSystemReference
    class_class_curie: ClassVar[str] = "tccm:CodeSystemReference"
    class_name: ClassVar[str] = "CodeSystemReference"
    class_model_uri: ClassVar[URIRef] = TCCM.CodeSystemReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class CodeSystemVersionReference(NameAndMeaningReference):
    """
    A reference to a specific version of code system and, if known, the code system which it is a version of.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.CodeSystemVersionReference
    class_class_curie: ClassVar[str] = "tccm:CodeSystemVersionReference"
    class_name: ClassVar[str] = "CodeSystemVersionReference"
    class_model_uri: ClassVar[URIRef] = TCCM.CodeSystemVersionReference

    name: Union[str, LocalIdentifier] = None
    codeSystem: Optional[Union[dict, CodeSystemReference]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.codeSystem is not None and not isinstance(self.codeSystem, CodeSystemReference):
            self.codeSystem = CodeSystemReference(**as_dict(self.codeSystem))

        super().__post_init__(**kwargs)


@dataclass
class ConceptDomainReference(NameAndMeaningReference):
    """
    A reference to a concept domain.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ConceptDomainReference
    class_class_curie: ClassVar[str] = "tccm:ConceptDomainReference"
    class_name: ClassVar[str] = "ConceptDomainReference"
    class_model_uri: ClassVar[URIRef] = TCCM.ConceptDomainReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class ContextReference(NameAndMeaningReference):
    """
    A reference to a realm or context.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ContextReference
    class_class_curie: ClassVar[str] = "tccm:ContextReference"
    class_name: ClassVar[str] = "ContextReference"
    class_model_uri: ClassVar[URIRef] = TCCM.ContextReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class DesignationFidelityReference(NameAndMeaningReference):
    """
    A reference to a description about designation faithfulness or accuracy.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.DesignationFidelityReference
    class_class_curie: ClassVar[str] = "tccm:DesignationFidelityReference"
    class_name: ClassVar[str] = "DesignationFidelityReference"
    class_model_uri: ClassVar[URIRef] = TCCM.DesignationFidelityReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class DesignationTypeReference(NameAndMeaningReference):
    """
    A reference to a designation type or form such as “short name,” “abbreviation,” “eponym.”
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.DesignationTypeReference
    class_class_curie: ClassVar[str] = "tccm:DesignationTypeReference"
    class_name: ClassVar[str] = "DesignationTypeReference"
    class_model_uri: ClassVar[URIRef] = TCCM.DesignationTypeReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class FormalityLevelReference(NameAndMeaningReference):
    """
    A reference to a description of the relative formality an ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.FormalityLevelReference
    class_class_curie: ClassVar[str] = "tccm:FormalityLevelReference"
    class_name: ClassVar[str] = "FormalityLevelReference"
    class_model_uri: ClassVar[URIRef] = TCCM.FormalityLevelReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class FormatReference(NameAndMeaningReference):
    """
    A reference to a particular way that information is encoded for storage or transmission.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.FormatReference
    class_class_curie: ClassVar[str] = "tccm:FormatReference"
    class_name: ClassVar[str] = "FormatReference"
    class_model_uri: ClassVar[URIRef] = TCCM.FormatReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class LanguageReference(NameAndMeaningReference):
    """
    A reference to a spoken or written human language.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.LanguageReference
    class_class_curie: ClassVar[str] = "tccm:LanguageReference"
    class_name: ClassVar[str] = "LanguageReference"
    class_model_uri: ClassVar[URIRef] = TCCM.LanguageReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class MapCorrelationReference(NameAndMeaningReference):
    """
    A reference to a way that the source and target in a map can be related or assessed.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.MapCorrelationReference
    class_class_curie: ClassVar[str] = "tccm:MapCorrelationReference"
    class_name: ClassVar[str] = "MapCorrelationReference"
    class_model_uri: ClassVar[URIRef] = TCCM.MapCorrelationReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class MapReference(NameAndMeaningReference):
    """
    A reference to an abstract map.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.MapReference
    class_class_curie: ClassVar[str] = "tccm:MapReference"
    class_name: ClassVar[str] = "MapReference"
    class_model_uri: ClassVar[URIRef] = TCCM.MapReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class MapVersionReference(NameAndMeaningReference):
    """
    A reference to a map version and the corresponding map, if known.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.MapVersionReference
    class_class_curie: ClassVar[str] = "tccm:MapVersionReference"
    class_name: ClassVar[str] = "MapVersionReference"
    class_model_uri: ClassVar[URIRef] = TCCM.MapVersionReference

    name: Union[str, LocalIdentifier] = None
    map: Optional[Union[dict, MapReference]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.map is not None and not isinstance(self.map, MapReference):
            self.map = MapReference(**as_dict(self.map))

        super().__post_init__(**kwargs)


@dataclass
class MatchAlgorithmReference(NameAndMeaningReference):
    """
    A reference to an algorithm used for selecting and filtering data.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.MatchAlgorithmReference
    class_class_curie: ClassVar[str] = "tccm:MatchAlgorithmReference"
    class_name: ClassVar[str] = "MatchAlgorithmReference"
    class_model_uri: ClassVar[URIRef] = TCCM.MatchAlgorithmReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class ModelAttributeReference(NameAndMeaningReference):
    """
    A reference to an attribute defined in the CTS2 specification.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ModelAttributeReference
    class_class_curie: ClassVar[str] = "tccm:ModelAttributeReference"
    class_name: ClassVar[str] = "ModelAttributeReference"
    class_model_uri: ClassVar[URIRef] = TCCM.ModelAttributeReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class NamespaceReference(NameAndMeaningReference):
    """
    A reference to a conceptual space that groups identifiers to avoid conflict with items that have the same name but
    different meanings.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.NamespaceReference
    class_class_curie: ClassVar[str] = "tccm:NamespaceReference"
    class_name: ClassVar[str] = "NamespaceReference"
    class_model_uri: ClassVar[URIRef] = TCCM.NamespaceReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class OntologyDomainReference(NameAndMeaningReference):
    """
    A reference to a subject domain for an ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.OntologyDomainReference
    class_class_curie: ClassVar[str] = "tccm:OntologyDomainReference"
    class_name: ClassVar[str] = "OntologyDomainReference"
    class_model_uri: ClassVar[URIRef] = TCCM.OntologyDomainReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class OntologyEngineeringMethodologyReference(NameAndMeaningReference):
    """
    A reference to a method model that can be used to create an ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.OntologyEngineeringMethodologyReference
    class_class_curie: ClassVar[str] = "tccm:OntologyEngineeringMethodologyReference"
    class_name: ClassVar[str] = "OntologyEngineeringMethodologyReference"
    class_model_uri: ClassVar[URIRef] = TCCM.OntologyEngineeringMethodologyReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class OntologyEngineeringToolReference(NameAndMeaningReference):
    """
    A reference to a tool that can be used to create an ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.OntologyEngineeringToolReference
    class_class_curie: ClassVar[str] = "tccm:OntologyEngineeringToolReference"
    class_name: ClassVar[str] = "OntologyEngineeringToolReference"
    class_model_uri: ClassVar[URIRef] = TCCM.OntologyEngineeringToolReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class OntologyLanguageReference(NameAndMeaningReference):
    """
    A reference to a language in which an ontology may be implemented.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.OntologyLanguageReference
    class_class_curie: ClassVar[str] = "tccm:OntologyLanguageReference"
    class_name: ClassVar[str] = "OntologyLanguageReference"
    class_model_uri: ClassVar[URIRef] = TCCM.OntologyLanguageReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class OntologySyntaxReference(NameAndMeaningReference):
    """
    A reference to a syntax in which an ontology may be represented.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.OntologySyntaxReference
    class_class_curie: ClassVar[str] = "tccm:OntologySyntaxReference"
    class_name: ClassVar[str] = "OntologySyntaxReference"
    class_model_uri: ClassVar[URIRef] = TCCM.OntologySyntaxReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class OntologyTaskReference(NameAndMeaningReference):
    """
    A reference to a purpose for which an ontology can be designed.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.OntologyTaskReference
    class_class_curie: ClassVar[str] = "tccm:OntologyTaskReference"
    class_name: ClassVar[str] = "OntologyTaskReference"
    class_model_uri: ClassVar[URIRef] = TCCM.OntologyTaskReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class OntologyTypeReference(NameAndMeaningReference):
    """
    A reference to the nature of the content of an ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.OntologyTypeReference
    class_class_curie: ClassVar[str] = "tccm:OntologyTypeReference"
    class_name: ClassVar[str] = "OntologyTypeReference"
    class_model_uri: ClassVar[URIRef] = TCCM.OntologyTypeReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class PredicateReference(YAMLRoot):
    """
    An EntityReference that serves the role of predicate. Note that this varies slightly from the base class of
    NameAndMeaningReference because the name attribute is a namespace/name combination rather than a simple name
    scoped exclusively by the domain.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.PredicateReference
    class_class_curie: ClassVar[str] = "tccm:PredicateReference"
    class_name: ClassVar[str] = "PredicateReference"
    class_model_uri: ClassVar[URIRef] = TCCM.PredicateReference

    uri: Union[str, ExternalURI] = None
    name: Curie = None
    href: Optional[Union[str, RenderingURI]] = None
    designation: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.uri):
            self.MissingRequiredField("uri")
        if not isinstance(self.uri, ExternalURI):
            self.uri = ExternalURI(self.uri)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, Curie):
            self.name = Curie(self.name)

        if self.href is not None and not isinstance(self.href, RenderingURI):
            self.href = RenderingURI(self.href)

        if self.designation is not None and not isinstance(self.designation, str):
            self.designation = str(self.designation)

        super().__post_init__(**kwargs)


@dataclass
class ReasoningAlgorithmReference(NameAndMeaningReference):
    """
    A reference to a formal algorithm for making inferences about an ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ReasoningAlgorithmReference
    class_class_curie: ClassVar[str] = "tccm:ReasoningAlgorithmReference"
    class_name: ClassVar[str] = "ReasoningAlgorithmReference"
    class_model_uri: ClassVar[URIRef] = TCCM.ReasoningAlgorithmReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class RoleReference(NameAndMeaningReference):
    """
    A reference to a role that an individual, organization, or bibliographic reference can play in the construction of
    a resource or resource component.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.RoleReference
    class_class_curie: ClassVar[str] = "tccm:RoleReference"
    class_name: ClassVar[str] = "RoleReference"
    class_model_uri: ClassVar[URIRef] = TCCM.RoleReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class SourceAndRoleReference(NameAndMeaningReference):
    """
    A reference to a source that also includes the role that the source played and/or fixes the particular chapter,
    page, or other element within the reference.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.SourceAndRoleReference
    class_class_curie: ClassVar[str] = "tccm:SourceAndRoleReference"
    class_name: ClassVar[str] = "SourceAndRoleReference"
    class_model_uri: ClassVar[URIRef] = TCCM.SourceAndRoleReference

    name: Union[str, LocalIdentifier] = None
    role: Optional[Union[dict, RoleReference]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.role is not None and not isinstance(self.role, RoleReference):
            self.role = RoleReference(**as_dict(self.role))

        super().__post_init__(**kwargs)


@dataclass
class SourceReference(NameAndMeaningReference):
    """
    A reference to an individual, organization of bibliographic reference.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.SourceReference
    class_class_curie: ClassVar[str] = "tccm:SourceReference"
    class_name: ClassVar[str] = "SourceReference"
    class_model_uri: ClassVar[URIRef] = TCCM.SourceReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class StatusReference(NameAndMeaningReference):
    """
    A reference to a state in an external ontology authoring workflow.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.StatusReference
    class_class_curie: ClassVar[str] = "tccm:StatusReference"
    class_name: ClassVar[str] = "StatusReference"
    class_model_uri: ClassVar[URIRef] = TCCM.StatusReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class ValueSetDefinitionReference(NameAndMeaningReference):
    """
    A reference to a set of rules for constructing a value set along with the corresponding value set if known.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ValueSetDefinitionReference
    class_class_curie: ClassVar[str] = "tccm:ValueSetDefinitionReference"
    class_name: ClassVar[str] = "ValueSetDefinitionReference"
    class_model_uri: ClassVar[URIRef] = TCCM.ValueSetDefinitionReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class ValueSetReference(NameAndMeaningReference):
    """
    A reference to a named set of entity references.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.ValueSetReference
    class_class_curie: ClassVar[str] = "tccm:ValueSetReference"
    class_name: ClassVar[str] = "ValueSetReference"
    class_model_uri: ClassVar[URIRef] = TCCM.ValueSetReference

    name: Union[str, LocalIdentifier] = None

@dataclass
class VersionTagReference(NameAndMeaningReference):
    """
    A reference to a tag that can be assigned to versionable resources within the context of a service implementation.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.VersionTagReference
    class_class_curie: ClassVar[str] = "tccm:VersionTagReference"
    class_name: ClassVar[str] = "VersionTagReference"
    class_model_uri: ClassVar[URIRef] = TCCM.VersionTagReference

    name: Union[str, LocalIdentifier] = None

# Enumerations


# Slots
class slots:
    pass

slots.about = Slot(uri=TCCM.about, name="about", curie=TCCM.curie('about'),
                   model_uri=TCCM.about, domain=None, range=Union[str, ExternalURI])

slots.resourceID = Slot(uri=TCCM.resourceID, name="resourceID", curie=TCCM.curie('resourceID'),
                   model_uri=TCCM.resourceID, domain=None, range=Union[str, LocalIdentifier])

slots.formalName = Slot(uri=TCCM.formalName, name="formalName", curie=TCCM.curie('formalName'),
                   model_uri=TCCM.formalName, domain=None, range=Optional[str])

slots.keyword = Slot(uri=TCCM.keyword, name="keyword", curie=TCCM.curie('keyword'),
                   model_uri=TCCM.keyword, domain=None, range=Optional[Union[str, List[str]]])

slots.resourceSynopsis = Slot(uri=TCCM.resourceSynopsis, name="resourceSynopsis", curie=TCCM.curie('resourceSynopsis'),
                   model_uri=TCCM.resourceSynopsis, domain=None, range=Optional[str])

slots.additionalDocumentation = Slot(uri=TCCM.additionalDocumentation, name="additionalDocumentation", curie=TCCM.curie('additionalDocumentation'),
                   model_uri=TCCM.additionalDocumentation, domain=None, range=Optional[Union[Union[str, PersistentURI], List[Union[str, PersistentURI]]]])

slots.rights = Slot(uri=TCCM.rights, name="rights", curie=TCCM.curie('rights'),
                   model_uri=TCCM.rights, domain=None, range=Optional[str])

slots.alternateID = Slot(uri=TCCM.alternateID, name="alternateID", curie=TCCM.curie('alternateID'),
                   model_uri=TCCM.alternateID, domain=None, range=Optional[str])

slots.sourceAndNotationDescription = Slot(uri=TCCM.sourceAndNotationDescription, name="sourceAndNotationDescription", curie=TCCM.curie('sourceAndNotationDescription'),
                   model_uri=TCCM.sourceAndNotationDescription, domain=None, range=Optional[str])

slots.sourceDocument = Slot(uri=TCCM.sourceDocument, name="sourceDocument", curie=TCCM.curie('sourceDocument'),
                   model_uri=TCCM.sourceDocument, domain=None, range=Optional[Union[str, PersistentURI]])

slots.sourceLanguage = Slot(uri=TCCM.sourceLanguage, name="sourceLanguage", curie=TCCM.curie('sourceLanguage'),
                   model_uri=TCCM.sourceLanguage, domain=None, range=Optional[Union[dict, OntologyLanguageReference]])

slots.sourceDocumentSyntax = Slot(uri=TCCM.sourceDocumentSyntax, name="sourceDocumentSyntax", curie=TCCM.curie('sourceDocumentSyntax'),
                   model_uri=TCCM.sourceDocumentSyntax, domain=None, range=Optional[Union[dict, OntologySyntaxReference]])

slots.releaseDocumentation = Slot(uri=TCCM.releaseDocumentation, name="releaseDocumentation", curie=TCCM.curie('releaseDocumentation'),
                   model_uri=TCCM.releaseDocumentation, domain=None, range=Optional[str])

slots.releaseFormat = Slot(uri=TCCM.releaseFormat, name="releaseFormat", curie=TCCM.curie('releaseFormat'),
                   model_uri=TCCM.releaseFormat, domain=None, range=Optional[Union[Union[dict, SourceAndNotation], List[Union[dict, SourceAndNotation]]]])

slots.documentURI = Slot(uri=TCCM.documentURI, name="documentURI", curie=TCCM.curie('documentURI'),
                   model_uri=TCCM.documentURI, domain=None, range=Optional[Union[str, DocumentURI]])

slots.sourceAndNotation = Slot(uri=TCCM.sourceAndNotation, name="sourceAndNotation", curie=TCCM.curie('sourceAndNotation'),
                   model_uri=TCCM.sourceAndNotation, domain=None, range=Optional[Union[dict, SourceAndNotation]])

slots.predecessor = Slot(uri=TCCM.predecessor, name="predecessor", curie=TCCM.curie('predecessor'),
                   model_uri=TCCM.predecessor, domain=None, range=Optional[Union[dict, NameAndMeaningReference]])

slots.officialResourceVersionID = Slot(uri=TCCM.officialResourceVersionID, name="officialResourceVersionID", curie=TCCM.curie('officialResourceVersionID'),
                   model_uri=TCCM.officialResourceVersionID, domain=None, range=Optional[str])

slots.officialReleaseDate = Slot(uri=TCCM.officialReleaseDate, name="officialReleaseDate", curie=TCCM.curie('officialReleaseDate'),
                   model_uri=TCCM.officialReleaseDate, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.officialActivationDate = Slot(uri=TCCM.officialActivationDate, name="officialActivationDate", curie=TCCM.curie('officialActivationDate'),
                   model_uri=TCCM.officialActivationDate, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.name = Slot(uri=TCCM.name, name="name", curie=TCCM.curie('name'),
                   model_uri=TCCM.name, domain=None, range=Union[str, LocalIdentifier])

slots.uri = Slot(uri=TCCM.uri, name="uri", curie=TCCM.curie('uri'),
                   model_uri=TCCM.uri, domain=None, range=Optional[Union[str, ExternalURI]])

slots.href = Slot(uri=TCCM.href, name="href", curie=TCCM.curie('href'),
                   model_uri=TCCM.href, domain=None, range=Optional[Union[str, RenderingURI]])

slots.codeSystem = Slot(uri=TCCM.codeSystem, name="codeSystem", curie=TCCM.curie('codeSystem'),
                   model_uri=TCCM.codeSystem, domain=None, range=Optional[Union[dict, CodeSystemReference]])

slots.map = Slot(uri=TCCM.map, name="map", curie=TCCM.curie('map'),
                   model_uri=TCCM.map, domain=None, range=Optional[Union[dict, MapReference]])

slots.designation = Slot(uri=TCCM.designation, name="designation", curie=TCCM.curie('designation'),
                   model_uri=TCCM.designation, domain=None, range=Optional[str])

slots.role = Slot(uri=TCCM.role, name="role", curie=TCCM.curie('role'),
                   model_uri=TCCM.role, domain=None, range=Optional[Union[dict, RoleReference]])

slots.ResourceDescription_about = Slot(uri=TCCM.about, name="ResourceDescription_about", curie=TCCM.curie('about'),
                   model_uri=TCCM.ResourceDescription_about, domain=ResourceDescription, range=Union[str, ExternalURI])

slots.ResourceDescription_resourceID = Slot(uri=TCCM.resourceID, name="ResourceDescription_resourceID", curie=TCCM.curie('resourceID'),
                   model_uri=TCCM.ResourceDescription_resourceID, domain=ResourceDescription, range=Union[str, LocalIdentifier])

slots.ResourceDescription_formalName = Slot(uri=TCCM.formalName, name="ResourceDescription_formalName", curie=TCCM.curie('formalName'),
                   model_uri=TCCM.ResourceDescription_formalName, domain=ResourceDescription, range=Optional[str])

slots.ResourceDescription_keyword = Slot(uri=TCCM.keyword, name="ResourceDescription_keyword", curie=TCCM.curie('keyword'),
                   model_uri=TCCM.ResourceDescription_keyword, domain=ResourceDescription, range=Optional[Union[str, List[str]]])

slots.ResourceDescription_resourceSynopsis = Slot(uri=TCCM.resourceSynopsis, name="ResourceDescription_resourceSynopsis", curie=TCCM.curie('resourceSynopsis'),
                   model_uri=TCCM.ResourceDescription_resourceSynopsis, domain=ResourceDescription, range=Optional[str])

slots.ResourceDescription_additionalDocumentation = Slot(uri=TCCM.additionalDocumentation, name="ResourceDescription_additionalDocumentation", curie=TCCM.curie('additionalDocumentation'),
                   model_uri=TCCM.ResourceDescription_additionalDocumentation, domain=ResourceDescription, range=Optional[Union[Union[str, PersistentURI], List[Union[str, PersistentURI]]]])

slots.ResourceDescription_rights = Slot(uri=TCCM.rights, name="ResourceDescription_rights", curie=TCCM.curie('rights'),
                   model_uri=TCCM.ResourceDescription_rights, domain=ResourceDescription, range=Optional[str])

slots.ResourceDescription_alternateID = Slot(uri=TCCM.alternateID, name="ResourceDescription_alternateID", curie=TCCM.curie('alternateID'),
                   model_uri=TCCM.ResourceDescription_alternateID, domain=ResourceDescription, range=Optional[str])

slots.SourceAndNotation_sourceAndNotationDescription = Slot(uri=TCCM.sourceAndNotationDescription, name="SourceAndNotation_sourceAndNotationDescription", curie=TCCM.curie('sourceAndNotationDescription'),
                   model_uri=TCCM.SourceAndNotation_sourceAndNotationDescription, domain=SourceAndNotation, range=Optional[str])

slots.SourceAndNotation_sourceDocument = Slot(uri=TCCM.sourceDocument, name="SourceAndNotation_sourceDocument", curie=TCCM.curie('sourceDocument'),
                   model_uri=TCCM.SourceAndNotation_sourceDocument, domain=SourceAndNotation, range=Optional[Union[str, PersistentURI]])

slots.SourceAndNotation_sourceLanguage = Slot(uri=TCCM.sourceLanguage, name="SourceAndNotation_sourceLanguage", curie=TCCM.curie('sourceLanguage'),
                   model_uri=TCCM.SourceAndNotation_sourceLanguage, domain=SourceAndNotation, range=Optional[Union[dict, "OntologyLanguageReference"]])

slots.SourceAndNotation_sourceDocumentSyntax = Slot(uri=TCCM.sourceDocumentSyntax, name="SourceAndNotation_sourceDocumentSyntax", curie=TCCM.curie('sourceDocumentSyntax'),
                   model_uri=TCCM.SourceAndNotation_sourceDocumentSyntax, domain=SourceAndNotation, range=Optional[Union[dict, "OntologySyntaxReference"]])

slots.AbstractResourceDescription_releaseDocumentation = Slot(uri=TCCM.releaseDocumentation, name="AbstractResourceDescription_releaseDocumentation", curie=TCCM.curie('releaseDocumentation'),
                   model_uri=TCCM.AbstractResourceDescription_releaseDocumentation, domain=AbstractResourceDescription, range=Optional[str])

slots.AbstractResourceDescription_releaseFormat = Slot(uri=TCCM.releaseFormat, name="AbstractResourceDescription_releaseFormat", curie=TCCM.curie('releaseFormat'),
                   model_uri=TCCM.AbstractResourceDescription_releaseFormat, domain=AbstractResourceDescription, range=Optional[Union[Union[dict, SourceAndNotation], List[Union[dict, SourceAndNotation]]]])

slots.ResourceVersionDescription_documentURI = Slot(uri=TCCM.documentURI, name="ResourceVersionDescription_documentURI", curie=TCCM.curie('documentURI'),
                   model_uri=TCCM.ResourceVersionDescription_documentURI, domain=ResourceVersionDescription, range=Optional[Union[str, DocumentURI]])

slots.ResourceVersionDescription_sourceAndNotation = Slot(uri=TCCM.sourceAndNotation, name="ResourceVersionDescription_sourceAndNotation", curie=TCCM.curie('sourceAndNotation'),
                   model_uri=TCCM.ResourceVersionDescription_sourceAndNotation, domain=ResourceVersionDescription, range=Optional[Union[dict, SourceAndNotation]])

slots.ResourceVersionDescription_predecessor = Slot(uri=TCCM.predecessor, name="ResourceVersionDescription_predecessor", curie=TCCM.curie('predecessor'),
                   model_uri=TCCM.ResourceVersionDescription_predecessor, domain=ResourceVersionDescription, range=Optional[Union[dict, "NameAndMeaningReference"]])

slots.ResourceVersionDescription_officialResourceVersionID = Slot(uri=TCCM.officialResourceVersionID, name="ResourceVersionDescription_officialResourceVersionID", curie=TCCM.curie('officialResourceVersionID'),
                   model_uri=TCCM.ResourceVersionDescription_officialResourceVersionID, domain=ResourceVersionDescription, range=Optional[str])

slots.ResourceVersionDescription_officialReleaseDate = Slot(uri=TCCM.officialReleaseDate, name="ResourceVersionDescription_officialReleaseDate", curie=TCCM.curie('officialReleaseDate'),
                   model_uri=TCCM.ResourceVersionDescription_officialReleaseDate, domain=ResourceVersionDescription, range=Optional[Union[str, XSDDateTime]])

slots.ResourceVersionDescription_officialActivationDate = Slot(uri=TCCM.officialActivationDate, name="ResourceVersionDescription_officialActivationDate", curie=TCCM.curie('officialActivationDate'),
                   model_uri=TCCM.ResourceVersionDescription_officialActivationDate, domain=ResourceVersionDescription, range=Optional[Union[str, XSDDateTime]])

slots.NameAndMeaningReference_name = Slot(uri=TCCM.name, name="NameAndMeaningReference_name", curie=TCCM.curie('name'),
                   model_uri=TCCM.NameAndMeaningReference_name, domain=NameAndMeaningReference, range=Union[str, LocalIdentifier])

slots.NameAndMeaningReference_uri = Slot(uri=TCCM.uri, name="NameAndMeaningReference_uri", curie=TCCM.curie('uri'),
                   model_uri=TCCM.NameAndMeaningReference_uri, domain=NameAndMeaningReference, range=Optional[Union[str, ExternalURI]])

slots.NameAndMeaningReference_href = Slot(uri=TCCM.href, name="NameAndMeaningReference_href", curie=TCCM.curie('href'),
                   model_uri=TCCM.NameAndMeaningReference_href, domain=NameAndMeaningReference, range=Optional[Union[str, RenderingURI]])

slots.CodeSystemVersionReference_codeSystem = Slot(uri=TCCM.codeSystem, name="CodeSystemVersionReference_codeSystem", curie=TCCM.curie('codeSystem'),
                   model_uri=TCCM.CodeSystemVersionReference_codeSystem, domain=CodeSystemVersionReference, range=Optional[Union[dict, CodeSystemReference]])

slots.MapVersionReference_map = Slot(uri=TCCM.map, name="MapVersionReference_map", curie=TCCM.curie('map'),
                   model_uri=TCCM.MapVersionReference_map, domain=MapVersionReference, range=Optional[Union[dict, MapReference]])

slots.PredicateReference_uri = Slot(uri=TCCM.uri, name="PredicateReference_uri", curie=TCCM.curie('uri'),
                   model_uri=TCCM.PredicateReference_uri, domain=PredicateReference, range=Union[str, ExternalURI])

slots.PredicateReference_name = Slot(uri=TCCM.name, name="PredicateReference_name", curie=TCCM.curie('name'),
                   model_uri=TCCM.PredicateReference_name, domain=PredicateReference, range=Curie)

slots.PredicateReference_href = Slot(uri=TCCM.href, name="PredicateReference_href", curie=TCCM.curie('href'),
                   model_uri=TCCM.PredicateReference_href, domain=PredicateReference, range=Optional[Union[str, RenderingURI]])

slots.PredicateReference_designation = Slot(uri=TCCM.designation, name="PredicateReference_designation", curie=TCCM.curie('designation'),
                   model_uri=TCCM.PredicateReference_designation, domain=PredicateReference, range=Optional[str])

slots.SourceAndRoleReference_role = Slot(uri=TCCM.role, name="SourceAndRoleReference_role", curie=TCCM.curie('role'),
                   model_uri=TCCM.SourceAndRoleReference_role, domain=SourceAndRoleReference, range=Optional[Union[dict, RoleReference]])