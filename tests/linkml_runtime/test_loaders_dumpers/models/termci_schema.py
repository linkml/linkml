# Auto generated from termci_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-04-22 12:19
# Schema: termci_schema
#
# id: https://w3id.org/termci_schema
# description: Terminology Code Index model
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.metamodelcore import empty_list, empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import URI, URIorCURIE

metamodel_version = "1.7.0"

# Namespaces
DC = CurieNamespace('dc', 'http://purl.org/dc/elements/1.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
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
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS.Concept
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "ConceptReference"
    class_model_uri: ClassVar[URIRef] = TERMCI.ConceptReference

    uri: Union[str, ConceptReferenceUri] = None
    code: str = None
    defined_in: Union[str, ConceptSystemNamespace] = None
    designation: Optional[str] = None
    definition: Optional[str] = None
    reference: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    narrower_than: Optional[Union[Union[str, ConceptReferenceUri], list[Union[str, ConceptReferenceUri]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS.ConceptScheme
    class_class_curie: ClassVar[str] = "skos:ConceptScheme"
    class_name: ClassVar[str] = "ConceptSystem"
    class_model_uri: ClassVar[URIRef] = TERMCI.ConceptSystem

    namespace: Union[str, ConceptSystemNamespace] = None
    prefix: str = None
    description: Optional[str] = None
    reference: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    root_concept: Optional[Union[Union[str, ConceptReferenceUri], list[Union[str, ConceptReferenceUri]]]] = empty_list()
    contents: Optional[Union[dict[Union[str, ConceptReferenceUri], Union[dict, ConceptReference]], list[Union[dict, ConceptReference]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
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
        if not isinstance(self.contents, (list, dict)):
            self.contents = [self.contents]
        self._normalize_inlined_slot(slot_name="contents", slot_type=ConceptReference, key_name="uri", inlined_as_list=True, keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Package(YAMLRoot):
    """
    A collection of ConceptSystems
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TERMCI.Package
    class_class_curie: ClassVar[str] = "termci:Package"
    class_name: ClassVar[str] = "Package"
    class_model_uri: ClassVar[URIRef] = TERMCI.Package

    system: Optional[Union[dict[Union[str, ConceptSystemNamespace], Union[dict, ConceptSystem]], list[Union[dict, ConceptSystem]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.system is None:
            self.system = []
        if not isinstance(self.system, (list, dict)):
            self.system = [self.system]
        self._normalize_inlined_slot(slot_name="system", slot_type=ConceptSystem, key_name="namespace", inlined_as_list=True, keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots

