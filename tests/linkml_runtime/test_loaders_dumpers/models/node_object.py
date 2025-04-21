# Auto generated from complex_range_example.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-11-25T10:11:03
# Schema: sparqlfun-RDF
#
# id: https://w3id.org/example/
# description: Abstractions for working with RDF and RDFS triples
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from jsonasobj2 import as_dict
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace

metamodel_version = "1.7.0"

# Namespaces
EX = CurieNamespace('ex', 'https://w3id.org/example/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
SH = CurieNamespace('sh', 'http://www.w3.org/ns/shacl#')
SPARQLFUN = CurieNamespace('sparqlfun', 'https://w3id.org/sparqlfun/')
DEFAULT_ = EX


# Types

# Class references
class NodeId(extended_str):
    pass


class NodeObjectId(NodeId):
    pass


@dataclass
class Triple(YAMLRoot):
    """
    Represents an RDF triple
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF.Statement
    class_class_curie: ClassVar[str] = "rdf:Statement"
    class_name: ClassVar[str] = "triple"
    class_model_uri: ClassVar[URIRef] = EX.Triple

    subject: Optional[Union[str, NodeId]] = None
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, str):
            self.object = str(self.object)

        super().__post_init__(**kwargs)


@dataclass
class Node(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Node
    class_class_curie: ClassVar[str] = "ex:Node"
    class_name: ClassVar[str] = "node"
    class_model_uri: ClassVar[URIRef] = EX.Node

    id: Union[str, NodeId] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class NodeObject(Node):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF.Resource
    class_class_curie: ClassVar[str] = "rdf:Resource"
    class_name: ClassVar[str] = "node object"
    class_model_uri: ClassVar[URIRef] = EX.NodeObject

    id: Union[str, NodeObjectId] = None
    statements: Optional[Union[Union[dict, Triple], list[Union[dict, Triple]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeObjectId):
            self.id = NodeObjectId(self.id)

        if not isinstance(self.statements, list):
            self.statements = [self.statements] if self.statements is not None else []
        self.statements = [v if isinstance(v, Triple) else Triple(**as_dict(v)) for v in self.statements]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=EX.id, name="id", curie=EX.curie('id'),
                   model_uri=EX.id, domain=None, range=URIRef)

slots.subject = Slot(uri=RDF.subject, name="subject", curie=RDF.curie('subject'),
                   model_uri=EX.subject, domain=None, range=Optional[Union[str, NodeId]])

slots.predicate = Slot(uri=RDF.predicate, name="predicate", curie=RDF.curie('predicate'),
                   model_uri=EX.predicate, domain=None, range=Optional[Union[str, NodeId]])

slots.object = Slot(uri=RDF.object, name="object", curie=RDF.curie('object'),
                   model_uri=EX.object, domain=None, range=Optional[str])

slots.graph = Slot(uri=EX.graph, name="graph", curie=EX.curie('graph'),
                   model_uri=EX.graph, domain=None, range=Optional[Union[str, NodeId]])

slots.statements = Slot(uri=SPARQLFUN.statements, name="statements", curie=SPARQLFUN.curie('statements'),
                   model_uri=EX.statements, domain=None, range=Optional[Union[Union[dict, Triple], list[Union[dict, Triple]]]])

slots.type = Slot(uri=EX.type, name="type", curie=EX.curie('type'),
                   model_uri=EX.type, domain=None, range=Optional[Union[str, NodeId]])
