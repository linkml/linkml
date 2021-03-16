# Auto generated from uritypes.yaml by pythongen.py version: 0.4.0
# Generation date: 2020-09-01 13:08
# Schema: tccm
#
# id: https://hotecosystem.org/tccm
# description: Terminology Core Common Model Data Types
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
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
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace
from linkml.utils.metamodelcore import URIorCURIE

metamodel_version = "1.5.3"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
TCCM = CurieNamespace('tccm', 'https://hotecosystem.org/tccm/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = TCCM


# Types
class PersistentURI(URIorCURIE):
    """ A Universal Resource Identifier (URI) that persists across service instances. PersistentURIs have enduring
reference and meaning. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "PersistentURI"
    type_model_uri = TCCM.PersistentURI


class LocalURI(URIorCURIE):
    """ A URI or handle whose scope is local to the implementing service. LocalURI cannot be used as a permanent
identifier in a message or a data record. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "LocalURI"
    type_model_uri = TCCM.LocalURI


class ChangeSetURI(PersistentURI):
    """ The unique identifier of a set of change instructions that can potentially transform the contents of a TCCM
service instance from one state to another. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "ChangeSetURI"
    type_model_uri = TCCM.ChangeSetURI


class DocumentURI(PersistentURI):
    """ A reference to a “work” in the bibliographic sense. It is not necessary that a Document URI be directly or
indirectly resolvable to a digital resource - it may simply be the name of a book, publication, or other
abstraction. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "DocumentURI"
    type_model_uri = TCCM.DocumentURI


class ExternalURI(PersistentURI):
    """ A URI that names a unique resource. CTS2 implementations should never assume that ExternalURI is resolvable
via an http: GET operation - ExternalURIs should always be passed as parameters to service implementations
to get the sanctioned equivalent in a given service context. """
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
    """ A URI or handle that is directly readable by a specific instance of a TCCM service implementation. RenderingURI
must resolve to Changeable CTS2 element. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "RenderingURI"
    type_model_uri = TCCM.RenderingURI


class DirectoryURI(LocalURI):
    """ The unique name of a query that when executed results in a list of resources that, in the context of a given
service, satisfy the query. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "DirectoryURI"
    type_model_uri = TCCM.DirectoryURI


# Class references





# Slots
class slots:
    pass


