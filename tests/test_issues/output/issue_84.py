# Auto generated from issue_84.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: nmdc_schema
#
# id: https://microbiomedata/schema
# description: Schema for NMDC. Alpha. Currently focuses on samples
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
from linkml_runtime.linkml_model.types import Double, Float, String
from linkml_runtime.utils.metamodelcore import ElementIdentifier

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
DCTERMS = CurieNamespace('dcterms', 'http://example.org/UNKNOWN/dcterms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
NMDC = CurieNamespace('nmdc', 'https://microbiomedata/meta/')
QUD = CurieNamespace('qud', 'http://qudt.org/1.1/schema/qudt#')
RDF = CurieNamespace('rdf', 'http://example.org/UNKNOWN/rdf/')
RDFS = CurieNamespace('rdfs', 'http://example.org/UNKNOWN/rdfs/')
SKOS = CurieNamespace('skos', 'http://example.org/UNKNOWN/skos/')
WGS = CurieNamespace('wgs', 'http://www.w3.org/2003/01/geo/wgs84_pos')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = NMDC


# Types
class IdentifierType(ElementIdentifier):
    """ A string that is intended to uniquely identify a thing May be URI in full or compact (CURIE) form """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "identifier type"
    type_model_uri = NMDC.IdentifierType


# Class references
class BiosampleId(ElementIdentifier):
    pass


class CharacteristicId(ElementIdentifier):
    pass


class OntologyClassId(ElementIdentifier):
    pass


@dataclass
class Biosample(YAMLRoot):
    """
    A material sample. May be environmental (encompassing many organisms) or isolate or tissue
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.Biosample
    class_class_curie: ClassVar[str] = "nmdc:Biosample"
    class_name: ClassVar[str] = "biosample"
    class_model_uri: ClassVar[URIRef] = NMDC.Biosample

    id: Union[ElementIdentifier, BiosampleId] = None
    name: Optional[str] = None
    annotations: Optional[Union[Union[dict, "Annotation"], List[Union[dict, "Annotation"]]]] = empty_list()
    alternate_identifiers: Optional[Union[ElementIdentifier, List[ElementIdentifier]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BiosampleId):
            self.id = BiosampleId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=Annotation, key_name="has raw value", keyed=False)

        if not isinstance(self.alternate_identifiers, list):
            self.alternate_identifiers = [self.alternate_identifiers] if self.alternate_identifiers is not None else []
        self.alternate_identifiers = [v if isinstance(v, ElementIdentifier) else ElementIdentifier(v) for v in self.alternate_identifiers]

        super().__post_init__(**kwargs)


@dataclass
class BiosampleProcessing(YAMLRoot):
    """
    A process that takes one or more biosamples as inputs and generates one or more as output
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.BiosampleProcessing
    class_class_curie: ClassVar[str] = "nmdc:BiosampleProcessing"
    class_name: ClassVar[str] = "biosample processing"
    class_model_uri: ClassVar[URIRef] = NMDC.BiosampleProcessing

    input: Optional[Union[Union[ElementIdentifier, BiosampleId], List[Union[ElementIdentifier, BiosampleId]]]] = empty_list()
    output: Optional[Union[Union[ElementIdentifier, BiosampleId], List[Union[ElementIdentifier, BiosampleId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.input, list):
            self.input = [self.input] if self.input is not None else []
        self.input = [v if isinstance(v, BiosampleId) else BiosampleId(v) for v in self.input]

        if not isinstance(self.output, list):
            self.output = [self.output] if self.output is not None else []
        self.output = [v if isinstance(v, BiosampleId) else BiosampleId(v) for v in self.output]

        super().__post_init__(**kwargs)


@dataclass
class Annotation(YAMLRoot):
    """
    An annotation on a sample. This is essentially a key value pair
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.Annotation
    class_class_curie: ClassVar[str] = "nmdc:Annotation"
    class_name: ClassVar[str] = "annotation"
    class_model_uri: ClassVar[URIRef] = NMDC.Annotation

    has_raw_value: str = None
    has_characteristic: Optional[Union[ElementIdentifier, CharacteristicId]] = None
    has_normalized_value: Optional[Union[dict, "NormalizedValue"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_raw_value):
            self.MissingRequiredField("has_raw_value")
        if not isinstance(self.has_raw_value, str):
            self.has_raw_value = str(self.has_raw_value)

        if self.has_characteristic is not None and not isinstance(self.has_characteristic, CharacteristicId):
            self.has_characteristic = CharacteristicId(self.has_characteristic)

        if self.has_normalized_value is not None and not isinstance(self.has_normalized_value, NormalizedValue):
            self.has_normalized_value = NormalizedValue()

        super().__post_init__(**kwargs)


@dataclass
class Characteristic(YAMLRoot):
    """
    A characteristic of a biosample. Examples: depth, habitat, material, ... For NMDC, characteristics SHOULD be
    mapped to fields within a MIxS template
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.Characteristic
    class_class_curie: ClassVar[str] = "nmdc:Characteristic"
    class_name: ClassVar[str] = "characteristic"
    class_model_uri: ClassVar[URIRef] = NMDC.Characteristic

    id: Union[ElementIdentifier, CharacteristicId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    alternate_identifiers: Optional[Union[ElementIdentifier, List[ElementIdentifier]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CharacteristicId):
            self.id = CharacteristicId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.alternate_identifiers, list):
            self.alternate_identifiers = [self.alternate_identifiers] if self.alternate_identifiers is not None else []
        self.alternate_identifiers = [v if isinstance(v, ElementIdentifier) else ElementIdentifier(v) for v in self.alternate_identifiers]

        super().__post_init__(**kwargs)


class NormalizedValue(YAMLRoot):
    """
    The value that was specified for an annotation in parsed/normalized form. This could be a range of different types
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.NormalizedValue
    class_class_curie: ClassVar[str] = "nmdc:NormalizedValue"
    class_name: ClassVar[str] = "normalized value"
    class_model_uri: ClassVar[URIRef] = NMDC.NormalizedValue


@dataclass
class QuantityValue(NormalizedValue):
    """
    A simple quantity, e.g. 2cm
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.QuantityValue
    class_class_curie: ClassVar[str] = "nmdc:QuantityValue"
    class_name: ClassVar[str] = "quantity value"
    class_model_uri: ClassVar[URIRef] = NMDC.QuantityValue

    has_unit: Optional[Union[dict, "Unit"]] = None
    has_numeric_value: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_unit is not None and not isinstance(self.has_unit, Unit):
            self.has_unit = Unit()

        if self.has_numeric_value is not None and not isinstance(self.has_numeric_value, float):
            self.has_numeric_value = float(self.has_numeric_value)

        super().__post_init__(**kwargs)


@dataclass
class ControlledTermValue(NormalizedValue):
    """
    A controlled term or class from an ontology
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.ControlledTermValue
    class_class_curie: ClassVar[str] = "nmdc:ControlledTermValue"
    class_name: ClassVar[str] = "controlled term value"
    class_model_uri: ClassVar[URIRef] = NMDC.ControlledTermValue

    instance_of: Optional[Union[ElementIdentifier, OntologyClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.instance_of is not None and not isinstance(self.instance_of, OntologyClassId):
            self.instance_of = OntologyClassId(self.instance_of)

        super().__post_init__(**kwargs)


@dataclass
class GeolocationValue(NormalizedValue):
    """
    A normalized value for a location on the earth's surface
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.GeolocationValue
    class_class_curie: ClassVar[str] = "nmdc:GeolocationValue"
    class_name: ClassVar[str] = "geolocation value"
    class_model_uri: ClassVar[URIRef] = NMDC.GeolocationValue

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.latitude is not None and not isinstance(self.latitude, float):
            self.latitude = float(self.latitude)

        if self.longitude is not None and not isinstance(self.longitude, float):
            self.longitude = float(self.longitude)

        super().__post_init__(**kwargs)


class Unit(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.Unit
    class_class_curie: ClassVar[str] = "nmdc:Unit"
    class_name: ClassVar[str] = "unit"
    class_model_uri: ClassVar[URIRef] = NMDC.Unit


@dataclass
class OntologyClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC.OntologyClass
    class_class_curie: ClassVar[str] = "nmdc:OntologyClass"
    class_name: ClassVar[str] = "ontology class"
    class_model_uri: ClassVar[URIRef] = NMDC.OntologyClass

    id: Union[ElementIdentifier, OntologyClassId] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyClassId):
            self.id = OntologyClassId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=NMDC.id, name="id", curie=NMDC.curie('id'),
                   model_uri=NMDC.id, domain=None, range=URIRef)

slots.name = Slot(uri=NMDC.name, name="name", curie=NMDC.curie('name'),
                   model_uri=NMDC.name, domain=None, range=Optional[str])

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=NMDC.description, domain=None, range=Optional[str])

slots.has_characteristic = Slot(uri=NMDC.has_characteristic, name="has characteristic", curie=NMDC.curie('has_characteristic'),
                   model_uri=NMDC.has_characteristic, domain=Annotation, range=Optional[Union[ElementIdentifier, CharacteristicId]])

slots.instance_of = Slot(uri=NMDC.instance_of, name="instance of", curie=NMDC.curie('instance_of'),
                   model_uri=NMDC.instance_of, domain=None, range=Optional[Union[ElementIdentifier, OntologyClassId]])

slots.has_raw_value = Slot(uri=NMDC.has_raw_value, name="has raw value", curie=NMDC.curie('has_raw_value'),
                   model_uri=NMDC.has_raw_value, domain=Annotation, range=str)

slots.has_normalized_value = Slot(uri=NMDC.has_normalized_value, name="has normalized value", curie=NMDC.curie('has_normalized_value'),
                   model_uri=NMDC.has_normalized_value, domain=Annotation, range=Optional[Union[dict, "NormalizedValue"]])

slots.has_unit = Slot(uri=NMDC.has_unit, name="has unit", curie=NMDC.curie('has_unit'),
                   model_uri=NMDC.has_unit, domain=None, range=Optional[Union[dict, Unit]], mappings = [QUD.unit])

slots.has_numeric_value = Slot(uri=NMDC.has_numeric_value, name="has numeric value", curie=NMDC.curie('has_numeric_value'),
                   model_uri=NMDC.has_numeric_value, domain=None, range=Optional[float], mappings = [QUD.quantityValue])

slots.alternate_identifiers = Slot(uri=NMDC.alternate_identifiers, name="alternate identifiers", curie=NMDC.curie('alternate_identifiers'),
                   model_uri=NMDC.alternate_identifiers, domain=None, range=Optional[Union[ElementIdentifier, List[ElementIdentifier]]])

slots.annotations = Slot(uri=NMDC.annotations, name="annotations", curie=NMDC.curie('annotations'),
                   model_uri=NMDC.annotations, domain=Biosample, range=Optional[Union[Union[dict, "Annotation"], List[Union[dict, "Annotation"]]]])

slots.latitude = Slot(uri=WGS.lat, name="latitude", curie=WGS.curie('lat'),
                   model_uri=NMDC.latitude, domain=None, range=Optional[float])

slots.longitude = Slot(uri=WGS.long, name="longitude", curie=WGS.curie('long'),
                   model_uri=NMDC.longitude, domain=None, range=Optional[float])

slots.input = Slot(uri=NMDC.input, name="input", curie=NMDC.curie('input'),
                   model_uri=NMDC.input, domain=None, range=Optional[Union[Union[ElementIdentifier, BiosampleId], List[Union[ElementIdentifier, BiosampleId]]]])

slots.output = Slot(uri=NMDC.output, name="output", curie=NMDC.curie('output'),
                   model_uri=NMDC.output, domain=None, range=Optional[Union[Union[ElementIdentifier, BiosampleId], List[Union[ElementIdentifier, BiosampleId]]]])

slots.biosample_id = Slot(uri=NMDC.id, name="biosample_id", curie=NMDC.curie('id'),
                   model_uri=NMDC.biosample_id, domain=Biosample, range=Union[ElementIdentifier, BiosampleId])

slots.biosample_name = Slot(uri=NMDC.name, name="biosample_name", curie=NMDC.curie('name'),
                   model_uri=NMDC.biosample_name, domain=Biosample, range=Optional[str])

slots.biosample_alternate_identifiers = Slot(uri=NMDC.alternate_identifiers, name="biosample_alternate identifiers", curie=NMDC.curie('alternate_identifiers'),
                   model_uri=NMDC.biosample_alternate_identifiers, domain=Biosample, range=Optional[Union[ElementIdentifier, List[ElementIdentifier]]])