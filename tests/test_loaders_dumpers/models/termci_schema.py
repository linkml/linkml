# Auto generated from termci_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-02-12 11:22
# Schema: termci_schema
#
# id: https://w3id.org/termci_schema
# description: Terminology Code Index model
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

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
from linkml.utils.metamodelcore import URI, URIorCURIE
from linkml_model.types import String, Uri, Uriorcurie

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DC = CurieNamespace('dc', 'http://purl.org/dc/elements/1.1/')
SCT = CurieNamespace('sct', 'http://snomed.info/id/')
SH = CurieNamespace('sh', 'http://www.w3.org/ns/shacl#')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
TERMCI = CurieNamespace('termci', 'https://hotecosystem.org/termci/')
DEFAULT_ = TERMCI


# Types

# Class references
class ConceptReferenceUri(URIorCURIE):
    pass


class ConceptSystemNamespace(URI):
    pass


@dataclass
class ConceptReference(YAMLRoot):
    """
    A minimal description of a class, individual, term or similar construct
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS.Concept
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "ConceptReference"
    class_model_uri: ClassVar[URIRef] = TERMCI.ConceptReference

    uri: Union[str, ConceptReferenceUri] = None
    code: str = None
    defined_in: Union[str, ConceptSystemNamespace] = None
    designation: Optional[str] = None
    definition: Optional[str] = None
    reference: Optional[Union[Union[str, URI], List[Union[str, URI]]]] = empty_list()
    narrower_than: Optional[Union[Union[str, ConceptReferenceUri], List[Union[str, ConceptReferenceUri]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.uri is None:
            raise ValueError("uri must be supplied")
        if not isinstance(self.uri, ConceptReferenceUri):
            self.uri = ConceptReferenceUri(self.uri)

        if self.code is None:
            raise ValueError("code must be supplied")
        if not isinstance(self.code, str):
            self.code = str(self.code)

        if self.defined_in is None:
            raise ValueError("defined_in must be supplied")
        if not isinstance(self.defined_in, ConceptSystemNamespace):
            self.defined_in = ConceptSystemNamespace(self.defined_in)

        if self.designation is not None and not isinstance(self.designation, str):
            self.designation = str(self.designation)

        if self.definition is not None and not isinstance(self.definition, str):
            self.definition = str(self.definition)

        if self.reference is None:
            self.reference = []
        if not isinstance(self.reference, list):
            self.reference = [self.reference]
        self.reference = [v if isinstance(v, URI) else URI(v) for v in self.reference]

        if self.narrower_than is None:
            self.narrower_than = []
        if not isinstance(self.narrower_than, list):
            self.narrower_than = [self.narrower_than]
        self.narrower_than = [v if isinstance(v, ConceptReferenceUri) else ConceptReferenceUri(v) for v in self.narrower_than]

        super().__post_init__(**kwargs)


@dataclass
class ConceptSystem(YAMLRoot):
    """
    A terminological resource (ontology, classification scheme, concept system, etc.)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS.ConceptScheme
    class_class_curie: ClassVar[str] = "skos:ConceptScheme"
    class_name: ClassVar[str] = "ConceptSystem"
    class_model_uri: ClassVar[URIRef] = TERMCI.ConceptSystem

    namespace: Union[str, ConceptSystemNamespace] = None
    prefix: str = None
    description: Optional[str] = None
    reference: Optional[Union[Union[str, URI], List[Union[str, URI]]]] = empty_list()
    root_concept: Optional[Union[Union[str, ConceptReferenceUri], List[Union[str, ConceptReferenceUri]]]] = empty_list()
    contents: Optional[Union[Dict[Union[str, ConceptReferenceUri], Union[dict, ConceptReference]], List[Union[dict, ConceptReference]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.namespace is None:
            raise ValueError("namespace must be supplied")
        if not isinstance(self.namespace, ConceptSystemNamespace):
            self.namespace = ConceptSystemNamespace(self.namespace)

        if self.prefix is None:
            raise ValueError("prefix must be supplied")
        if not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.reference is None:
            self.reference = []
        if not isinstance(self.reference, list):
            self.reference = [self.reference]
        self.reference = [v if isinstance(v, URI) else URI(v) for v in self.reference]

        if self.root_concept is None:
            self.root_concept = []
        if not isinstance(self.root_concept, list):
            self.root_concept = [self.root_concept]
        self.root_concept = [v if isinstance(v, ConceptReferenceUri) else ConceptReferenceUri(v) for v in self.root_concept]

        if self.contents is None:
            self.contents = []
        if not isinstance(self.contents, (list)):
            self.contents = [self.contents]
        self._normalize_inlined_slot(slot_name="contents", slot_type=ConceptReference, key_name="uri", inlined_as_list=True, keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Package(YAMLRoot):
    """
    A collection of ConceptSystems
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TERMCI.Package
    class_class_curie: ClassVar[str] = "termci:Package"
    class_name: ClassVar[str] = "Package"
    class_model_uri: ClassVar[URIRef] = TERMCI.Package

    system: Optional[Union[Dict[Union[str, ConceptSystemNamespace], Union[dict, ConceptSystem]], List[Union[dict, ConceptSystem]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.system is None:
            self.system = []
        if not isinstance(self.system, (list)):
            self.system = [self.system]
        self._normalize_inlined_slot(slot_name="system", slot_type=ConceptSystem, key_name="namespace", inlined_as_list=True, keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.code = Slot(uri=SKOS.notation, name="code", curie=SKOS.curie('notation'),
                   model_uri=TERMCI.code, domain=None, range=str)

slots.designation = Slot(uri=SKOS.prefLabel, name="designation", curie=SKOS.curie('prefLabel'),
                   model_uri=TERMCI.designation, domain=None, range=Optional[str])

slots.definition = Slot(uri=SKOS.definition, name="definition", curie=SKOS.curie('definition'),
                   model_uri=TERMCI.definition, domain=None, range=Optional[str])

slots.reference = Slot(uri=SKOS.seeAlso, name="reference", curie=SKOS.curie('seeAlso'),
                   model_uri=TERMCI.reference, domain=None, range=Optional[Union[Union[str, URI], List[Union[str, URI]]]])

slots.defined_in = Slot(uri=SKOS.inScheme, name="defined_in", curie=SKOS.curie('inScheme'),
                   model_uri=TERMCI.defined_in, domain=None, range=Union[str, ConceptSystemNamespace])

slots.narrower_than = Slot(uri=SKOS.broader, name="narrower_than", curie=SKOS.curie('broader'),
                   model_uri=TERMCI.narrower_than, domain=None, range=Optional[Union[Union[str, ConceptReferenceUri], List[Union[str, ConceptReferenceUri]]]])

slots.prefix = Slot(uri=SH.prefix, name="prefix", curie=SH.curie('prefix'),
                   model_uri=TERMCI.prefix, domain=None, range=str)

slots.namespace = Slot(uri=SH.namespace, name="namespace", curie=SH.curie('namespace'),
                   model_uri=TERMCI.namespace, domain=None, range=URIRef)

slots.root_concept = Slot(uri=SKOS.hasTopConcept, name="root_concept", curie=SKOS.curie('hasTopConcept'),
                   model_uri=TERMCI.root_concept, domain=None, range=Optional[Union[Union[str, ConceptReferenceUri], List[Union[str, ConceptReferenceUri]]]])

slots.description = Slot(uri=DC.description, name="description", curie=DC.curie('description'),
                   model_uri=TERMCI.description, domain=None, range=Optional[str])

slots.concept_uri = Slot(uri=TERMCI.uri, name="concept_uri", curie=TERMCI.curie('uri'),
                   model_uri=TERMCI.concept_uri, domain=None, range=URIRef)

slots.contents = Slot(uri=TERMCI.contents, name="contents", curie=TERMCI.curie('contents'),
                   model_uri=TERMCI.contents, domain=None, range=Optional[Union[Dict[Union[str, ConceptReferenceUri], Union[dict, ConceptReference]], List[Union[dict, ConceptReference]]]])

slots.package__system = Slot(uri=TERMCI.system, name="package__system", curie=TERMCI.curie('system'),
                   model_uri=TERMCI.package__system, domain=None, range=Optional[Union[Dict[Union[str, ConceptSystemNamespace], Union[dict, ConceptSystem]], List[Union[dict, ConceptSystem]]]])
