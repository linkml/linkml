# Auto generated from phenopackets.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-01-17T12:56:45
# Schema: phenopackets
#
# id: https://w3id.org/linkml/phenopackets/phenopackets
# description: Automatic translation of phenopackets protobuf to LinkML. Status: EXPERIMENTAL.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from jsonasobj2 import as_dict
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Namespaces
ARGO = CurieNamespace('ARGO', 'https://docs.icgc-argo.org/dictionary/')
GENO = CurieNamespace('GENO', 'http://purl.obolibrary.org/obo/GENO_')
HP = CurieNamespace('HP', 'http://purl.obolibrary.org/obo/HP_')
LOINC = CurieNamespace('LOINC', 'https://loinc.org/')
MONDO = CurieNamespace('MONDO', 'http://purl.obolibrary.org/obo/MONDO_')
NCIT = CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_')
UBERON = CurieNamespace('UBERON', 'http://purl.obolibrary.org/obo/UBERON_')
UCUM = CurieNamespace('UCUM', 'http://unitsofmeasure.org/')
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
ANY = CurieNamespace('any', 'https://w3id.org/linkml/phenopackets/any/')
ARGO = CurieNamespace('argo', 'https://docs.icgc-argo.org/dictionary/')
BASE = CurieNamespace('base', 'https://w3id.org/linkml/phenopackets/base/')
BIOSAMPLE = CurieNamespace('biosample', 'https://w3id.org/linkml/phenopackets/biosample/')
DISEASE = CurieNamespace('disease', 'https://w3id.org/linkml/phenopackets/disease/')
INDIVIDUAL = CurieNamespace('individual', 'https://w3id.org/linkml/phenopackets/individual/')
INTERPRETATION = CurieNamespace('interpretation', 'https://w3id.org/linkml/phenopackets/interpretation/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MEASUREMENT = CurieNamespace('measurement', 'https://w3id.org/linkml/phenopackets/measurement/')
MEDICAL_ACTION = CurieNamespace('medical_action', 'https://w3id.org/linkml/phenopackets/medical_action/')
META_DATA = CurieNamespace('meta_data', 'https://w3id.org/linkml/phenopackets/meta_data/')
PEDIGREE = CurieNamespace('pedigree', 'https://w3id.org/linkml/phenopackets/pedigree/')
PHENOPACKETS = CurieNamespace('phenopackets', 'https://w3id.org/linkml/phenopackets/phenopackets/')
PHENOTYPIC_FEATURE = CurieNamespace('phenotypic_feature', 'https://w3id.org/linkml/phenopackets/phenotypic_feature/')
TIMESTAMP = CurieNamespace('timestamp', 'https://w3id.org/linkml/phenopackets/timestamp/')
VRS = CurieNamespace('vrs', 'https://w3id.org/linkml/phenopackets/vrs/')
VRSATILE = CurieNamespace('vrsatile', 'https://w3id.org/linkml/phenopackets/vrsatile/')
DEFAULT_ = PHENOPACKETS


# Types

# Class references
class OntologyClassId(extended_str):
    pass


@dataclass
class Cohort(YAMLRoot):
    """
    A group of individuals related in some phenotypic or genotypic aspect.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PHENOPACKETS.Cohort
    class_class_curie: ClassVar[str] = "phenopackets:Cohort"
    class_name: ClassVar[str] = "Cohort"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Cohort

    metaData: Union[dict, "MetaData"] = None
    description: Optional[str] = None
    files: Optional[Union[Union[dict, "File"], list[Union[dict, "File"]]]] = empty_list()
    id: Optional[str] = None
    members: Optional[Union[Union[dict, "Phenopacket"], list[Union[dict, "Phenopacket"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.metaData):
            self.MissingRequiredField("metaData")
        if not isinstance(self.metaData, MetaData):
            self.metaData = MetaData(**as_dict(self.metaData))

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.files, list):
            self.files = [self.files] if self.files is not None else []
        self.files = [v if isinstance(v, File) else File(**as_dict(v)) for v in self.files]

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        self._normalize_inlined_as_dict(slot_name="members", slot_type=Phenopacket, key_name="metaData", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Family(YAMLRoot):
    """
    Phenotype, sample and pedigree data required for a genomic diagnosis. Equivalent to the Genomics England
    InterpretationRequestRD
    https://github.com/genomicsengland/GelReportModels/blob/master/schemas/IDLs/org.gel.models.report.avro/5.0.0/InterpretationRequestRD.avdl
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PHENOPACKETS.Family
    class_class_curie: ClassVar[str] = "phenopackets:Family"
    class_name: ClassVar[str] = "Family"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Family

    metaData: Union[dict, "MetaData"] = None
    consanguinousParents: Optional[Union[bool, Bool]] = None
    files: Optional[Union[Union[dict, "File"], list[Union[dict, "File"]]]] = empty_list()
    id: Optional[str] = None
    pedigree: Optional[Union[dict, "Pedigree"]] = None
    proband: Optional[Union[dict, "Phenopacket"]] = None
    relatives: Optional[Union[Union[dict, "Phenopacket"], list[Union[dict, "Phenopacket"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.metaData):
            self.MissingRequiredField("metaData")
        if not isinstance(self.metaData, MetaData):
            self.metaData = MetaData(**as_dict(self.metaData))

        if self.consanguinousParents is not None and not isinstance(self.consanguinousParents, Bool):
            self.consanguinousParents = Bool(self.consanguinousParents)

        if not isinstance(self.files, list):
            self.files = [self.files] if self.files is not None else []
        self.files = [v if isinstance(v, File) else File(**as_dict(v)) for v in self.files]

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.pedigree is not None and not isinstance(self.pedigree, Pedigree):
            self.pedigree = Pedigree(**as_dict(self.pedigree))

        if self.proband is not None and not isinstance(self.proband, Phenopacket):
            self.proband = Phenopacket(**as_dict(self.proband))

        self._normalize_inlined_as_dict(slot_name="relatives", slot_type=Phenopacket, key_name="metaData", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Phenopacket(YAMLRoot):
    """
    An anonymous phenotypic description of an individual or biosample with potential genes of interest and/or
    diagnoses. This is a bundle of high-level concepts with no specifically defined relational concepts. It is
    expected that the resources sharing the phenopackets will define and enforce their own semantics and level of
    requirements for included fields.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PHENOPACKETS.Phenopacket
    class_class_curie: ClassVar[str] = "phenopackets:Phenopacket"
    class_name: ClassVar[str] = "Phenopacket"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Phenopacket

    metaData: Union[dict, "MetaData"] = None
    biosamples: Optional[Union[Union[dict, "Biosample"], list[Union[dict, "Biosample"]]]] = empty_list()
    diseases: Optional[Union[Union[dict, "Disease"], list[Union[dict, "Disease"]]]] = empty_list()
    files: Optional[Union[Union[dict, "File"], list[Union[dict, "File"]]]] = empty_list()
    id: Optional[str] = None
    interpretations: Optional[Union[Union[dict, "Interpretation"], list[Union[dict, "Interpretation"]]]] = empty_list()
    measurements: Optional[Union[Union[dict, "Measurement"], list[Union[dict, "Measurement"]]]] = empty_list()
    medicalActions: Optional[Union[Union[dict, "MedicalAction"], list[Union[dict, "MedicalAction"]]]] = empty_list()
    phenotypicFeatures: Optional[Union[Union[dict, "PhenotypicFeature"], list[Union[dict, "PhenotypicFeature"]]]] = empty_list()
    subject: Optional[Union[dict, "Individual"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.metaData):
            self.MissingRequiredField("metaData")
        if not isinstance(self.metaData, MetaData):
            self.metaData = MetaData(**as_dict(self.metaData))

        if not isinstance(self.biosamples, list):
            self.biosamples = [self.biosamples] if self.biosamples is not None else []
        self.biosamples = [v if isinstance(v, Biosample) else Biosample(**as_dict(v)) for v in self.biosamples]

        if not isinstance(self.diseases, list):
            self.diseases = [self.diseases] if self.diseases is not None else []
        self.diseases = [v if isinstance(v, Disease) else Disease(**as_dict(v)) for v in self.diseases]

        if not isinstance(self.files, list):
            self.files = [self.files] if self.files is not None else []
        self.files = [v if isinstance(v, File) else File(**as_dict(v)) for v in self.files]

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if not isinstance(self.interpretations, list):
            self.interpretations = [self.interpretations] if self.interpretations is not None else []
        self.interpretations = [v if isinstance(v, Interpretation) else Interpretation(**as_dict(v)) for v in self.interpretations]

        if not isinstance(self.measurements, list):
            self.measurements = [self.measurements] if self.measurements is not None else []
        self.measurements = [v if isinstance(v, Measurement) else Measurement(**as_dict(v)) for v in self.measurements]

        if not isinstance(self.medicalActions, list):
            self.medicalActions = [self.medicalActions] if self.medicalActions is not None else []
        self.medicalActions = [v if isinstance(v, MedicalAction) else MedicalAction(**as_dict(v)) for v in self.medicalActions]

        if not isinstance(self.phenotypicFeatures, list):
            self.phenotypicFeatures = [self.phenotypicFeatures] if self.phenotypicFeatures is not None else []
        self.phenotypicFeatures = [v if isinstance(v, PhenotypicFeature) else PhenotypicFeature(**as_dict(v)) for v in self.phenotypicFeatures]

        if self.subject is not None and not isinstance(self.subject, Individual):
            self.subject = Individual(**as_dict(self.subject))

        super().__post_init__(**kwargs)


@dataclass
class Age(YAMLRoot):
    """
    See http://build.fhir.org/datatypes and http://build.fhir.org/condition-definitions.html#Condition.onset_x_ In
    FHIR this is represented as a UCUM measurement - http://unitsofmeasure.org/trac/
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.Age
    class_class_curie: ClassVar[str] = "base:Age"
    class_name: ClassVar[str] = "Age"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Age

    iso8601duration: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.iso8601duration is not None and not isinstance(self.iso8601duration, str):
            self.iso8601duration = str(self.iso8601duration)

        super().__post_init__(**kwargs)


@dataclass
class AgeRange(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.AgeRange
    class_class_curie: ClassVar[str] = "base:AgeRange"
    class_name: ClassVar[str] = "AgeRange"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.AgeRange

    end: Optional[Union[dict, Age]] = None
    start: Optional[Union[dict, Age]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.end is not None and not isinstance(self.end, Age):
            self.end = Age(**as_dict(self.end))

        if self.start is not None and not isinstance(self.start, Age):
            self.start = Age(**as_dict(self.start))

        super().__post_init__(**kwargs)


class Dictionary(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.Dictionary
    class_class_curie: ClassVar[str] = "base:Dictionary"
    class_name: ClassVar[str] = "Dictionary"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Dictionary


@dataclass
class Evidence(YAMLRoot):
    """
    FHIR mapping: Condition.evidence (https://www.hl7.org/fhir/condition-definitions.html#Condition.evidence)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.Evidence
    class_class_curie: ClassVar[str] = "base:Evidence"
    class_name: ClassVar[str] = "Evidence"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Evidence

    evidenceCode: Optional[Union[dict, "OntologyClass"]] = None
    reference: Optional[Union[dict, "ExternalReference"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.evidenceCode is not None and not isinstance(self.evidenceCode, OntologyClass):
            self.evidenceCode = OntologyClass(**as_dict(self.evidenceCode))

        if self.reference is not None and not isinstance(self.reference, ExternalReference):
            self.reference = ExternalReference(**as_dict(self.reference))

        super().__post_init__(**kwargs)


@dataclass
class ExternalReference(YAMLRoot):
    """
    FHIR mapping: Reference (https://www.hl7.org/fhir/references.html)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.ExternalReference
    class_class_curie: ClassVar[str] = "base:ExternalReference"
    class_name: ClassVar[str] = "ExternalReference"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.ExternalReference

    description: Optional[str] = None
    id: Optional[str] = None
    reference: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.reference is not None and not isinstance(self.reference, str):
            self.reference = str(self.reference)

        super().__post_init__(**kwargs)


@dataclass
class File(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.File
    class_class_curie: ClassVar[str] = "base:File"
    class_name: ClassVar[str] = "File"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.File

    fileAttributes: Optional[Union[dict, Dictionary]] = None
    individualToFileIdentifiers: Optional[Union[dict, Dictionary]] = None
    uri: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.fileAttributes is not None and not isinstance(self.fileAttributes, Dictionary):
            self.fileAttributes = Dictionary()

        if self.individualToFileIdentifiers is not None and not isinstance(self.individualToFileIdentifiers, Dictionary):
            self.individualToFileIdentifiers = Dictionary()

        if self.uri is not None and not isinstance(self.uri, str):
            self.uri = str(self.uri)

        super().__post_init__(**kwargs)


@dataclass
class GestationalAge(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.GestationalAge
    class_class_curie: ClassVar[str] = "base:GestationalAge"
    class_name: ClassVar[str] = "GestationalAge"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.GestationalAge

    days: Optional[int] = None
    weeks: Optional[int] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.days is not None and not isinstance(self.days, int):
            self.days = int(self.days)

        if self.weeks is not None and not isinstance(self.weeks, int):
            self.weeks = int(self.weeks)

        super().__post_init__(**kwargs)


@dataclass
class OntologyClass(YAMLRoot):
    """
    A class (aka term, concept) in an ontology. FHIR mapping: CodeableConcept
    (http://www.hl7.org/fhir/datatypes.html#CodeableConcept) see also Coding
    (http://www.hl7.org/fhir/datatypes.html#Coding)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.OntologyClass
    class_class_curie: ClassVar[str] = "base:OntologyClass"
    class_name: ClassVar[str] = "OntologyClass"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.OntologyClass

    id: Union[str, OntologyClassId] = None
    label: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyClassId):
            self.id = OntologyClassId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass
class Procedure(YAMLRoot):
    """
    A clinical procedure performed on a subject. By preference a single concept to indicate both the procedure and the
    body site should be used. In cases where this is not possible, the body site should be indicated using a separate
    ontology class. e.g. {"code":{"NCIT:C51585": "Biopsy of Soft Palate"}} {"code":{"NCIT:C28743": "Punch Biopsy"},
    "body_site":{"UBERON:0003403": "skin of forearm"}} - a punch biopsy of the skin from the forearm FHIR mapping:
    Procedure (https://www.hl7.org/fhir/procedure.html)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.Procedure
    class_class_curie: ClassVar[str] = "base:Procedure"
    class_name: ClassVar[str] = "Procedure"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Procedure

    bodySite: Optional[Union[dict, OntologyClass]] = None
    code: Optional[Union[dict, OntologyClass]] = None
    performed: Optional[Union[dict, "TimeElement"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.bodySite is not None and not isinstance(self.bodySite, OntologyClass):
            self.bodySite = OntologyClass(**as_dict(self.bodySite))

        if self.code is not None and not isinstance(self.code, OntologyClass):
            self.code = OntologyClass(**as_dict(self.code))

        if self.performed is not None and not isinstance(self.performed, TimeElement):
            self.performed = TimeElement(**as_dict(self.performed))

        super().__post_init__(**kwargs)


@dataclass
class TimeElement(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.TimeElement
    class_class_curie: ClassVar[str] = "base:TimeElement"
    class_name: ClassVar[str] = "TimeElement"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.TimeElement

    age: Optional[Union[dict, Age]] = None
    ageRange: Optional[Union[dict, AgeRange]] = None
    gestationalAge: Optional[Union[dict, GestationalAge]] = None
    interval: Optional[Union[dict, "TimeInterval"]] = None
    ontologyClass: Optional[Union[dict, OntologyClass]] = None
    timestamp: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.age is not None and not isinstance(self.age, Age):
            self.age = Age(**as_dict(self.age))

        if self.ageRange is not None and not isinstance(self.ageRange, AgeRange):
            self.ageRange = AgeRange(**as_dict(self.ageRange))

        if self.gestationalAge is not None and not isinstance(self.gestationalAge, GestationalAge):
            self.gestationalAge = GestationalAge(**as_dict(self.gestationalAge))

        if self.interval is not None and not isinstance(self.interval, TimeInterval):
            self.interval = TimeInterval(**as_dict(self.interval))

        if self.ontologyClass is not None and not isinstance(self.ontologyClass, OntologyClass):
            self.ontologyClass = OntologyClass(**as_dict(self.ontologyClass))

        if self.timestamp is not None and not isinstance(self.timestamp, str):
            self.timestamp = str(self.timestamp)

        super().__post_init__(**kwargs)


@dataclass
class TimeInterval(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BASE.TimeInterval
    class_class_curie: ClassVar[str] = "base:TimeInterval"
    class_name: ClassVar[str] = "TimeInterval"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.TimeInterval

    end: Optional[str] = None
    start: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.end is not None and not isinstance(self.end, str):
            self.end = str(self.end)

        if self.start is not None and not isinstance(self.start, str):
            self.start = str(self.start)

        super().__post_init__(**kwargs)


@dataclass
class Biosample(YAMLRoot):
    """
    A Biosample refers to a unit of biological material from which the substrate molecules (e.g. genomic DNA, RNA,
    proteins) for molecular analyses (e.g. sequencing, array hybridisation, mass-spectrometry) are extracted. Examples
    would be a tissue biopsy, a single cell from a culture for single cell genome sequencing or a protein fraction
    from a gradient centrifugation. Several instances (e.g. technical replicates) or types of experiments (e.g.
    genomic array as well as RNA-seq experiments) may refer to the same Biosample. FHIR mapping: Specimen
    (http://www.hl7.org/fhir/specimen.html).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOSAMPLE.Biosample
    class_class_curie: ClassVar[str] = "biosample:Biosample"
    class_name: ClassVar[str] = "Biosample"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Biosample

    derivedFromId: Optional[str] = None
    description: Optional[str] = None
    diagnosticMarkers: Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]] = empty_dict()
    files: Optional[Union[Union[dict, File], list[Union[dict, File]]]] = empty_list()
    histologicalDiagnosis: Optional[Union[dict, OntologyClass]] = None
    id: Optional[str] = None
    individualId: Optional[str] = None
    materialSample: Optional[Union[dict, OntologyClass]] = None
    measurements: Optional[Union[Union[dict, "Measurement"], list[Union[dict, "Measurement"]]]] = empty_list()
    pathologicalStage: Optional[Union[dict, OntologyClass]] = None
    pathologicalTnmFinding: Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]] = empty_dict()
    phenotypicFeatures: Optional[Union[Union[dict, "PhenotypicFeature"], list[Union[dict, "PhenotypicFeature"]]]] = empty_list()
    procedure: Optional[Union[dict, Procedure]] = None
    sampleProcessing: Optional[Union[dict, OntologyClass]] = None
    sampleStorage: Optional[Union[dict, OntologyClass]] = None
    sampleType: Optional[Union[dict, OntologyClass]] = None
    sampledTissue: Optional[Union[dict, OntologyClass]] = None
    taxonomy: Optional[Union[dict, OntologyClass]] = None
    timeOfCollection: Optional[Union[dict, TimeElement]] = None
    tumorGrade: Optional[Union[dict, OntologyClass]] = None
    tumorProgression: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.derivedFromId is not None and not isinstance(self.derivedFromId, str):
            self.derivedFromId = str(self.derivedFromId)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="diagnosticMarkers", slot_type=OntologyClass, key_name="id", keyed=True)

        if not isinstance(self.files, list):
            self.files = [self.files] if self.files is not None else []
        self.files = [v if isinstance(v, File) else File(**as_dict(v)) for v in self.files]

        if self.histologicalDiagnosis is not None and not isinstance(self.histologicalDiagnosis, OntologyClass):
            self.histologicalDiagnosis = OntologyClass(**as_dict(self.histologicalDiagnosis))

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.individualId is not None and not isinstance(self.individualId, str):
            self.individualId = str(self.individualId)

        if self.materialSample is not None and not isinstance(self.materialSample, OntologyClass):
            self.materialSample = OntologyClass(**as_dict(self.materialSample))

        if not isinstance(self.measurements, list):
            self.measurements = [self.measurements] if self.measurements is not None else []
        self.measurements = [v if isinstance(v, Measurement) else Measurement(**as_dict(v)) for v in self.measurements]

        if self.pathologicalStage is not None and not isinstance(self.pathologicalStage, OntologyClass):
            self.pathologicalStage = OntologyClass(**as_dict(self.pathologicalStage))

        self._normalize_inlined_as_dict(slot_name="pathologicalTnmFinding", slot_type=OntologyClass, key_name="id", keyed=True)

        if not isinstance(self.phenotypicFeatures, list):
            self.phenotypicFeatures = [self.phenotypicFeatures] if self.phenotypicFeatures is not None else []
        self.phenotypicFeatures = [v if isinstance(v, PhenotypicFeature) else PhenotypicFeature(**as_dict(v)) for v in self.phenotypicFeatures]

        if self.procedure is not None and not isinstance(self.procedure, Procedure):
            self.procedure = Procedure(**as_dict(self.procedure))

        if self.sampleProcessing is not None and not isinstance(self.sampleProcessing, OntologyClass):
            self.sampleProcessing = OntologyClass(**as_dict(self.sampleProcessing))

        if self.sampleStorage is not None and not isinstance(self.sampleStorage, OntologyClass):
            self.sampleStorage = OntologyClass(**as_dict(self.sampleStorage))

        if self.sampleType is not None and not isinstance(self.sampleType, OntologyClass):
            self.sampleType = OntologyClass(**as_dict(self.sampleType))

        if self.sampledTissue is not None and not isinstance(self.sampledTissue, OntologyClass):
            self.sampledTissue = OntologyClass(**as_dict(self.sampledTissue))

        if self.taxonomy is not None and not isinstance(self.taxonomy, OntologyClass):
            self.taxonomy = OntologyClass(**as_dict(self.taxonomy))

        if self.timeOfCollection is not None and not isinstance(self.timeOfCollection, TimeElement):
            self.timeOfCollection = TimeElement(**as_dict(self.timeOfCollection))

        if self.tumorGrade is not None and not isinstance(self.tumorGrade, OntologyClass):
            self.tumorGrade = OntologyClass(**as_dict(self.tumorGrade))

        if self.tumorProgression is not None and not isinstance(self.tumorProgression, OntologyClass):
            self.tumorProgression = OntologyClass(**as_dict(self.tumorProgression))

        super().__post_init__(**kwargs)


@dataclass
class Disease(YAMLRoot):
    """
    Message to indicate a disease (diagnosis) and its recorded onset.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DISEASE.Disease
    class_class_curie: ClassVar[str] = "disease:Disease"
    class_name: ClassVar[str] = "Disease"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Disease

    clinicalTnmFinding: Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]] = empty_dict()
    diseaseStage: Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]] = empty_dict()
    excluded: Optional[Union[bool, Bool]] = None
    laterality: Optional[Union[dict, OntologyClass]] = None
    onset: Optional[Union[dict, TimeElement]] = None
    primarySite: Optional[Union[dict, OntologyClass]] = None
    resolution: Optional[Union[dict, TimeElement]] = None
    term: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="clinicalTnmFinding", slot_type=OntologyClass, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="diseaseStage", slot_type=OntologyClass, key_name="id", keyed=True)

        if self.excluded is not None and not isinstance(self.excluded, Bool):
            self.excluded = Bool(self.excluded)

        if self.laterality is not None and not isinstance(self.laterality, OntologyClass):
            self.laterality = OntologyClass(**as_dict(self.laterality))

        if self.onset is not None and not isinstance(self.onset, TimeElement):
            self.onset = TimeElement(**as_dict(self.onset))

        if self.primarySite is not None and not isinstance(self.primarySite, OntologyClass):
            self.primarySite = OntologyClass(**as_dict(self.primarySite))

        if self.resolution is not None and not isinstance(self.resolution, TimeElement):
            self.resolution = TimeElement(**as_dict(self.resolution))

        if self.term is not None and not isinstance(self.term, OntologyClass):
            self.term = OntologyClass(**as_dict(self.term))

        super().__post_init__(**kwargs)


@dataclass
class Diagnosis(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = INTERPRETATION.Diagnosis
    class_class_curie: ClassVar[str] = "interpretation:Diagnosis"
    class_name: ClassVar[str] = "Diagnosis"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Diagnosis

    disease: Optional[Union[dict, OntologyClass]] = None
    genomicInterpretations: Optional[Union[Union[dict, "GenomicInterpretation"], list[Union[dict, "GenomicInterpretation"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.disease is not None and not isinstance(self.disease, OntologyClass):
            self.disease = OntologyClass(**as_dict(self.disease))

        if not isinstance(self.genomicInterpretations, list):
            self.genomicInterpretations = [self.genomicInterpretations] if self.genomicInterpretations is not None else []
        self.genomicInterpretations = [v if isinstance(v, GenomicInterpretation) else GenomicInterpretation(**as_dict(v)) for v in self.genomicInterpretations]

        super().__post_init__(**kwargs)


@dataclass
class GenomicInterpretation(YAMLRoot):
    """
    A statement about the contribution of a genomic element towards the observed phenotype. Note that this does not
    intend to encode any knowledge or results of specific computations.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = INTERPRETATION.GenomicInterpretation
    class_class_curie: ClassVar[str] = "interpretation:GenomicInterpretation"
    class_name: ClassVar[str] = "GenomicInterpretation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.GenomicInterpretation

    gene: Optional[Union[dict, "GeneDescriptor"]] = None
    interpretationStatus: Optional[Union[str, "InterpretationStatus"]] = None
    subjectOrBiosampleId: Optional[str] = None
    variantInterpretation: Optional[Union[dict, "VariantInterpretation"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.gene is not None and not isinstance(self.gene, GeneDescriptor):
            self.gene = GeneDescriptor(**as_dict(self.gene))

        if self.interpretationStatus is not None and not isinstance(self.interpretationStatus, InterpretationStatus):
            self.interpretationStatus = InterpretationStatus(self.interpretationStatus)

        if self.subjectOrBiosampleId is not None and not isinstance(self.subjectOrBiosampleId, str):
            self.subjectOrBiosampleId = str(self.subjectOrBiosampleId)

        if self.variantInterpretation is not None and not isinstance(self.variantInterpretation, VariantInterpretation):
            self.variantInterpretation = VariantInterpretation(**as_dict(self.variantInterpretation))

        super().__post_init__(**kwargs)


@dataclass
class Interpretation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = INTERPRETATION.Interpretation
    class_class_curie: ClassVar[str] = "interpretation:Interpretation"
    class_name: ClassVar[str] = "Interpretation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Interpretation

    diagnosis: Optional[Union[dict, Diagnosis]] = None
    id: Optional[str] = None
    progressStatus: Optional[Union[str, "ProgressStatus"]] = None
    summary: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.diagnosis is not None and not isinstance(self.diagnosis, Diagnosis):
            self.diagnosis = Diagnosis(**as_dict(self.diagnosis))

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.progressStatus is not None and not isinstance(self.progressStatus, ProgressStatus):
            self.progressStatus = ProgressStatus(self.progressStatus)

        if self.summary is not None and not isinstance(self.summary, str):
            self.summary = str(self.summary)

        super().__post_init__(**kwargs)


@dataclass
class VariantInterpretation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = INTERPRETATION.VariantInterpretation
    class_class_curie: ClassVar[str] = "interpretation:VariantInterpretation"
    class_name: ClassVar[str] = "VariantInterpretation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.VariantInterpretation

    acmgPathogenicityClassification: Optional[Union[str, "AcmgPathogenicityClassification"]] = None
    therapeuticActionability: Optional[Union[str, "TherapeuticActionability"]] = None
    variationDescriptor: Optional[Union[dict, "VariationDescriptor"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.acmgPathogenicityClassification is not None and not isinstance(self.acmgPathogenicityClassification, AcmgPathogenicityClassification):
            self.acmgPathogenicityClassification = AcmgPathogenicityClassification(self.acmgPathogenicityClassification)

        if self.therapeuticActionability is not None and not isinstance(self.therapeuticActionability, TherapeuticActionability):
            self.therapeuticActionability = TherapeuticActionability(self.therapeuticActionability)

        if self.variationDescriptor is not None and not isinstance(self.variationDescriptor, VariationDescriptor):
            self.variationDescriptor = VariationDescriptor(**as_dict(self.variationDescriptor))

        super().__post_init__(**kwargs)


@dataclass
class Individual(YAMLRoot):
    """
    An individual (or subject) typically corresponds to an individual human or another organism. FHIR mapping: Patient
    (https://www.hl7.org/fhir/patient.html).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = INDIVIDUAL.Individual
    class_class_curie: ClassVar[str] = "individual:Individual"
    class_name: ClassVar[str] = "Individual"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Individual

    alternateIds: Optional[Union[str, list[str]]] = empty_list()
    dateOfBirth: Optional[str] = None
    gender: Optional[Union[dict, OntologyClass]] = None
    id: Optional[str] = None
    karyotypicSex: Optional[Union[str, "KaryotypicSex"]] = None
    sex: Optional[Union[str, "Sex"]] = None
    taxonomy: Optional[Union[dict, OntologyClass]] = None
    timeAtLastEncounter: Optional[Union[dict, TimeElement]] = None
    vitalStatus: Optional[Union[dict, "VitalStatus"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if not isinstance(self.alternateIds, list):
            self.alternateIds = [self.alternateIds] if self.alternateIds is not None else []
        self.alternateIds = [v if isinstance(v, str) else str(v) for v in self.alternateIds]

        if self.dateOfBirth is not None and not isinstance(self.dateOfBirth, str):
            self.dateOfBirth = str(self.dateOfBirth)

        if self.gender is not None and not isinstance(self.gender, OntologyClass):
            self.gender = OntologyClass(**as_dict(self.gender))

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.karyotypicSex is not None and not isinstance(self.karyotypicSex, KaryotypicSex):
            self.karyotypicSex = KaryotypicSex(self.karyotypicSex)

        if self.sex is not None and not isinstance(self.sex, Sex):
            self.sex = Sex(self.sex)

        if self.taxonomy is not None and not isinstance(self.taxonomy, OntologyClass):
            self.taxonomy = OntologyClass(**as_dict(self.taxonomy))

        if self.timeAtLastEncounter is not None and not isinstance(self.timeAtLastEncounter, TimeElement):
            self.timeAtLastEncounter = TimeElement(**as_dict(self.timeAtLastEncounter))

        if self.vitalStatus is not None and not isinstance(self.vitalStatus, VitalStatus):
            self.vitalStatus = VitalStatus(**as_dict(self.vitalStatus))

        super().__post_init__(**kwargs)


@dataclass
class VitalStatus(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = INDIVIDUAL.VitalStatus
    class_class_curie: ClassVar[str] = "individual:VitalStatus"
    class_name: ClassVar[str] = "VitalStatus"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.VitalStatus

    causeOfDeath: Optional[Union[dict, OntologyClass]] = None
    status: Optional[Union[str, "Status"]] = None
    survivalTimeInDays: Optional[int] = None
    timeOfDeath: Optional[Union[dict, TimeElement]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.causeOfDeath is not None and not isinstance(self.causeOfDeath, OntologyClass):
            self.causeOfDeath = OntologyClass(**as_dict(self.causeOfDeath))

        if self.status is not None and not isinstance(self.status, Status):
            self.status = Status(self.status)

        if self.survivalTimeInDays is not None and not isinstance(self.survivalTimeInDays, int):
            self.survivalTimeInDays = int(self.survivalTimeInDays)

        if self.timeOfDeath is not None and not isinstance(self.timeOfDeath, TimeElement):
            self.timeOfDeath = TimeElement(**as_dict(self.timeOfDeath))

        super().__post_init__(**kwargs)


@dataclass
class ComplexValue(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEASUREMENT.ComplexValue
    class_class_curie: ClassVar[str] = "measurement:ComplexValue"
    class_name: ClassVar[str] = "ComplexValue"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.ComplexValue

    typedQuantities: Optional[Union[Union[dict, "TypedQuantity"], list[Union[dict, "TypedQuantity"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if not isinstance(self.typedQuantities, list):
            self.typedQuantities = [self.typedQuantities] if self.typedQuantities is not None else []
        self.typedQuantities = [v if isinstance(v, TypedQuantity) else TypedQuantity(**as_dict(v)) for v in self.typedQuantities]

        super().__post_init__(**kwargs)


@dataclass
class Measurement(YAMLRoot):
    """
    FHIR mapping: Observation (https://www.hl7.org/fhir/observation.html)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEASUREMENT.Measurement
    class_class_curie: ClassVar[str] = "measurement:Measurement"
    class_name: ClassVar[str] = "Measurement"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Measurement

    assay: Optional[Union[dict, OntologyClass]] = None
    complexValue: Optional[Union[dict, ComplexValue]] = None
    description: Optional[str] = None
    procedure: Optional[Union[dict, Procedure]] = None
    timeObserved: Optional[Union[dict, TimeElement]] = None
    value: Optional[Union[dict, "Value"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.assay is not None and not isinstance(self.assay, OntologyClass):
            self.assay = OntologyClass(**as_dict(self.assay))

        if self.complexValue is not None and not isinstance(self.complexValue, ComplexValue):
            self.complexValue = ComplexValue(**as_dict(self.complexValue))

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.procedure is not None and not isinstance(self.procedure, Procedure):
            self.procedure = Procedure(**as_dict(self.procedure))

        if self.timeObserved is not None and not isinstance(self.timeObserved, TimeElement):
            self.timeObserved = TimeElement(**as_dict(self.timeObserved))

        if self.value is not None and not isinstance(self.value, Value):
            self.value = Value(**as_dict(self.value))

        super().__post_init__(**kwargs)


@dataclass
class Quantity(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEASUREMENT.Quantity
    class_class_curie: ClassVar[str] = "measurement:Quantity"
    class_name: ClassVar[str] = "Quantity"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Quantity

    referenceRange: Optional[Union[dict, "ReferenceRange"]] = None
    unit: Optional[Union[dict, OntologyClass]] = None
    value: Optional[float] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.referenceRange is not None and not isinstance(self.referenceRange, ReferenceRange):
            self.referenceRange = ReferenceRange(**as_dict(self.referenceRange))

        if self.unit is not None and not isinstance(self.unit, OntologyClass):
            self.unit = OntologyClass(**as_dict(self.unit))

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        super().__post_init__(**kwargs)


@dataclass
class ReferenceRange(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEASUREMENT.ReferenceRange
    class_class_curie: ClassVar[str] = "measurement:ReferenceRange"
    class_name: ClassVar[str] = "ReferenceRange"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.ReferenceRange

    high: Optional[float] = None
    low: Optional[float] = None
    unit: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.high is not None and not isinstance(self.high, float):
            self.high = float(self.high)

        if self.low is not None and not isinstance(self.low, float):
            self.low = float(self.low)

        if self.unit is not None and not isinstance(self.unit, OntologyClass):
            self.unit = OntologyClass(**as_dict(self.unit))

        super().__post_init__(**kwargs)


@dataclass
class TypedQuantity(YAMLRoot):
    """
    For complex measurements, such as blood pressure where more than one component quantity is required to describe
    the measurement
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEASUREMENT.TypedQuantity
    class_class_curie: ClassVar[str] = "measurement:TypedQuantity"
    class_name: ClassVar[str] = "TypedQuantity"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.TypedQuantity

    quantity: Optional[Union[dict, Quantity]] = None
    type: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.quantity is not None and not isinstance(self.quantity, Quantity):
            self.quantity = Quantity(**as_dict(self.quantity))

        if self.type is not None and not isinstance(self.type, OntologyClass):
            self.type = OntologyClass(**as_dict(self.type))

        super().__post_init__(**kwargs)


@dataclass
class Value(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEASUREMENT.Value
    class_class_curie: ClassVar[str] = "measurement:Value"
    class_name: ClassVar[str] = "Value"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Value

    ontologyClass: Optional[Union[dict, OntologyClass]] = None
    quantity: Optional[Union[dict, Quantity]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.ontologyClass is not None and not isinstance(self.ontologyClass, OntologyClass):
            self.ontologyClass = OntologyClass(**as_dict(self.ontologyClass))

        if self.quantity is not None and not isinstance(self.quantity, Quantity):
            self.quantity = Quantity(**as_dict(self.quantity))

        super().__post_init__(**kwargs)


@dataclass
class DoseInterval(YAMLRoot):
    """
    e.g. 50mg/ml 3 times daily for two weeks
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEDICAL_ACTION.DoseInterval
    class_class_curie: ClassVar[str] = "medical_action:DoseInterval"
    class_name: ClassVar[str] = "DoseInterval"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.DoseInterval

    interval: Optional[Union[dict, TimeInterval]] = None
    quantity: Optional[Union[dict, Quantity]] = None
    scheduleFrequency: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.interval is not None and not isinstance(self.interval, TimeInterval):
            self.interval = TimeInterval(**as_dict(self.interval))

        if self.quantity is not None and not isinstance(self.quantity, Quantity):
            self.quantity = Quantity(**as_dict(self.quantity))

        if self.scheduleFrequency is not None and not isinstance(self.scheduleFrequency, OntologyClass):
            self.scheduleFrequency = OntologyClass(**as_dict(self.scheduleFrequency))

        super().__post_init__(**kwargs)


@dataclass
class MedicalAction(YAMLRoot):
    """
    medication, procedure, other actions taken for clinical management
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEDICAL_ACTION.MedicalAction
    class_class_curie: ClassVar[str] = "medical_action:MedicalAction"
    class_name: ClassVar[str] = "MedicalAction"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.MedicalAction

    adverseEvents: Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]] = empty_dict()
    procedure: Optional[Union[dict, Procedure]] = None
    radiationTherapy: Optional[Union[dict, "RadiationTherapy"]] = None
    responseToTreatment: Optional[Union[dict, OntologyClass]] = None
    therapeuticRegimen: Optional[Union[dict, "TherapeuticRegimen"]] = None
    treatment: Optional[Union[dict, "Treatment"]] = None
    treatmentIntent: Optional[Union[dict, OntologyClass]] = None
    treatmentTarget: Optional[Union[dict, OntologyClass]] = None
    treatmentTerminationReason: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="adverseEvents", slot_type=OntologyClass, key_name="id", keyed=True)

        if self.procedure is not None and not isinstance(self.procedure, Procedure):
            self.procedure = Procedure(**as_dict(self.procedure))

        if self.radiationTherapy is not None and not isinstance(self.radiationTherapy, RadiationTherapy):
            self.radiationTherapy = RadiationTherapy(**as_dict(self.radiationTherapy))

        if self.responseToTreatment is not None and not isinstance(self.responseToTreatment, OntologyClass):
            self.responseToTreatment = OntologyClass(**as_dict(self.responseToTreatment))

        if self.therapeuticRegimen is not None and not isinstance(self.therapeuticRegimen, TherapeuticRegimen):
            self.therapeuticRegimen = TherapeuticRegimen(**as_dict(self.therapeuticRegimen))

        if self.treatment is not None and not isinstance(self.treatment, Treatment):
            self.treatment = Treatment(**as_dict(self.treatment))

        if self.treatmentIntent is not None and not isinstance(self.treatmentIntent, OntologyClass):
            self.treatmentIntent = OntologyClass(**as_dict(self.treatmentIntent))

        if self.treatmentTarget is not None and not isinstance(self.treatmentTarget, OntologyClass):
            self.treatmentTarget = OntologyClass(**as_dict(self.treatmentTarget))

        if self.treatmentTerminationReason is not None and not isinstance(self.treatmentTerminationReason, OntologyClass):
            self.treatmentTerminationReason = OntologyClass(**as_dict(self.treatmentTerminationReason))

        super().__post_init__(**kwargs)


@dataclass
class RadiationTherapy(YAMLRoot):
    """
    RadiationTherapy
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEDICAL_ACTION.RadiationTherapy
    class_class_curie: ClassVar[str] = "medical_action:RadiationTherapy"
    class_name: ClassVar[str] = "RadiationTherapy"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.RadiationTherapy

    bodySite: Union[dict, OntologyClass] = None
    dosage: int = None
    fractions: int = None
    modality: Union[dict, OntologyClass] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.bodySite):
            self.MissingRequiredField("bodySite")
        if not isinstance(self.bodySite, OntologyClass):
            self.bodySite = OntologyClass(**as_dict(self.bodySite))

        if self._is_empty(self.dosage):
            self.MissingRequiredField("dosage")
        if not isinstance(self.dosage, int):
            self.dosage = int(self.dosage)

        if self._is_empty(self.fractions):
            self.MissingRequiredField("fractions")
        if not isinstance(self.fractions, int):
            self.fractions = int(self.fractions)

        if self._is_empty(self.modality):
            self.MissingRequiredField("modality")
        if not isinstance(self.modality, OntologyClass):
            self.modality = OntologyClass(**as_dict(self.modality))

        super().__post_init__(**kwargs)


@dataclass
class TherapeuticRegimen(YAMLRoot):
    """
    ARGO mapping radiation::radiation_therapy_type (missing)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEDICAL_ACTION.TherapeuticRegimen
    class_class_curie: ClassVar[str] = "medical_action:TherapeuticRegimen"
    class_name: ClassVar[str] = "TherapeuticRegimen"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.TherapeuticRegimen

    endTime: Optional[Union[dict, TimeElement]] = None
    externalReference: Optional[Union[dict, ExternalReference]] = None
    ontologyClass: Optional[Union[dict, OntologyClass]] = None
    regimenStatus: Optional[Union[str, "RegimenStatus"]] = None
    startTime: Optional[Union[dict, TimeElement]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.endTime is not None and not isinstance(self.endTime, TimeElement):
            self.endTime = TimeElement(**as_dict(self.endTime))

        if self.externalReference is not None and not isinstance(self.externalReference, ExternalReference):
            self.externalReference = ExternalReference(**as_dict(self.externalReference))

        if self.ontologyClass is not None and not isinstance(self.ontologyClass, OntologyClass):
            self.ontologyClass = OntologyClass(**as_dict(self.ontologyClass))

        if self.regimenStatus is not None and not isinstance(self.regimenStatus, RegimenStatus):
            self.regimenStatus = RegimenStatus(self.regimenStatus)

        if self.startTime is not None and not isinstance(self.startTime, TimeElement):
            self.startTime = TimeElement(**as_dict(self.startTime))

        super().__post_init__(**kwargs)


@dataclass
class Treatment(YAMLRoot):
    """
    ARGO mapping treatment::is_primary_treatment (missing) treatment with an agent, such as a drug
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = MEDICAL_ACTION.Treatment
    class_class_curie: ClassVar[str] = "medical_action:Treatment"
    class_name: ClassVar[str] = "Treatment"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Treatment

    agent: Optional[Union[dict, OntologyClass]] = None
    cumulativeDose: Optional[Union[dict, Quantity]] = None
    doseIntervals: Optional[Union[Union[dict, DoseInterval], list[Union[dict, DoseInterval]]]] = empty_list()
    drugType: Optional[Union[str, "DrugType"]] = None
    routeOfAdministration: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.agent is not None and not isinstance(self.agent, OntologyClass):
            self.agent = OntologyClass(**as_dict(self.agent))

        if self.cumulativeDose is not None and not isinstance(self.cumulativeDose, Quantity):
            self.cumulativeDose = Quantity(**as_dict(self.cumulativeDose))

        if not isinstance(self.doseIntervals, list):
            self.doseIntervals = [self.doseIntervals] if self.doseIntervals is not None else []
        self.doseIntervals = [v if isinstance(v, DoseInterval) else DoseInterval(**as_dict(v)) for v in self.doseIntervals]

        if self.drugType is not None and not isinstance(self.drugType, DrugType):
            self.drugType = DrugType(self.drugType)

        if self.routeOfAdministration is not None and not isinstance(self.routeOfAdministration, OntologyClass):
            self.routeOfAdministration = OntologyClass(**as_dict(self.routeOfAdministration))

        super().__post_init__(**kwargs)


@dataclass
class MetaData(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = META_DATA.MetaData
    class_class_curie: ClassVar[str] = "meta_data:MetaData"
    class_name: ClassVar[str] = "MetaData"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.MetaData

    created: Optional[str] = None
    createdBy: Optional[str] = None
    externalReferences: Optional[Union[Union[dict, ExternalReference], list[Union[dict, ExternalReference]]]] = empty_list()
    phenopacketSchemaVersion: Optional[str] = None
    resources: Optional[Union[Union[dict, "Resource"], list[Union[dict, "Resource"]]]] = empty_list()
    submittedBy: Optional[str] = None
    updates: Optional[Union[Union[dict, "Update"], list[Union[dict, "Update"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.created is not None and not isinstance(self.created, str):
            self.created = str(self.created)

        if self.createdBy is not None and not isinstance(self.createdBy, str):
            self.createdBy = str(self.createdBy)

        if not isinstance(self.externalReferences, list):
            self.externalReferences = [self.externalReferences] if self.externalReferences is not None else []
        self.externalReferences = [v if isinstance(v, ExternalReference) else ExternalReference(**as_dict(v)) for v in self.externalReferences]

        if self.phenopacketSchemaVersion is not None and not isinstance(self.phenopacketSchemaVersion, str):
            self.phenopacketSchemaVersion = str(self.phenopacketSchemaVersion)

        if not isinstance(self.resources, list):
            self.resources = [self.resources] if self.resources is not None else []
        self.resources = [v if isinstance(v, Resource) else Resource(**as_dict(v)) for v in self.resources]

        if self.submittedBy is not None and not isinstance(self.submittedBy, str):
            self.submittedBy = str(self.submittedBy)

        self._normalize_inlined_as_dict(slot_name="updates", slot_type=Update, key_name="timestamp", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Resource(YAMLRoot):
    """
    Description of an external resource used for referencing an object. For example the resource may be an ontology
    such as the HPO or SNOMED. FHIR mapping: CodeSystem (http://www.hl7.org/fhir/codesystem.html)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = META_DATA.Resource
    class_class_curie: ClassVar[str] = "meta_data:Resource"
    class_name: ClassVar[str] = "Resource"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Resource

    id: Optional[str] = None
    iriPrefix: Optional[str] = None
    name: Optional[str] = None
    namespacePrefix: Optional[str] = None
    url: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.iriPrefix is not None and not isinstance(self.iriPrefix, str):
            self.iriPrefix = str(self.iriPrefix)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.namespacePrefix is not None and not isinstance(self.namespacePrefix, str):
            self.namespacePrefix = str(self.namespacePrefix)

        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        super().__post_init__(**kwargs)


@dataclass
class Update(YAMLRoot):
    """
    Information about when an update to a record occurred, who or what made the update and any pertinent information
    regarding the content and/or reason for the update
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = META_DATA.Update
    class_class_curie: ClassVar[str] = "meta_data:Update"
    class_name: ClassVar[str] = "Update"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Update

    timestamp: str = None
    comment: Optional[str] = None
    updatedBy: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.timestamp):
            self.MissingRequiredField("timestamp")
        if not isinstance(self.timestamp, str):
            self.timestamp = str(self.timestamp)

        if self.comment is not None and not isinstance(self.comment, str):
            self.comment = str(self.comment)

        if self.updatedBy is not None and not isinstance(self.updatedBy, str):
            self.updatedBy = str(self.updatedBy)

        super().__post_init__(**kwargs)


@dataclass
class Pedigree(YAMLRoot):
    """
    https://software.broadinstitute.org/gatk/documentation/article?id=11016
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEDIGREE.Pedigree
    class_class_curie: ClassVar[str] = "pedigree:Pedigree"
    class_name: ClassVar[str] = "Pedigree"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Pedigree

    persons: Optional[Union[Union[dict, "Person"], list[Union[dict, "Person"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if not isinstance(self.persons, list):
            self.persons = [self.persons] if self.persons is not None else []
        self.persons = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.persons]

        super().__post_init__(**kwargs)


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PEDIGREE.Person
    class_class_curie: ClassVar[str] = "pedigree:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Person

    affectedStatus: Optional[Union[str, "AffectedStatus"]] = None
    familyId: Optional[str] = None
    individualId: Optional[str] = None
    maternalId: Optional[str] = None
    paternalId: Optional[str] = None
    sex: Optional[Union[str, "Sex"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.affectedStatus is not None and not isinstance(self.affectedStatus, AffectedStatus):
            self.affectedStatus = AffectedStatus(self.affectedStatus)

        if self.familyId is not None and not isinstance(self.familyId, str):
            self.familyId = str(self.familyId)

        if self.individualId is not None and not isinstance(self.individualId, str):
            self.individualId = str(self.individualId)

        if self.maternalId is not None and not isinstance(self.maternalId, str):
            self.maternalId = str(self.maternalId)

        if self.paternalId is not None and not isinstance(self.paternalId, str):
            self.paternalId = str(self.paternalId)

        if self.sex is not None and not isinstance(self.sex, Sex):
            self.sex = Sex(self.sex)

        super().__post_init__(**kwargs)


@dataclass
class PhenotypicFeature(YAMLRoot):
    """
    An individual phenotypic feature, observed as either present or absent (negated), with possible onset, modifiers
    and frequency FHIR mapping: Condition (https://www.hl7.org/fhir/condition.html) or Observation
    (https://www.hl7.org/fhir/observation.html)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PHENOTYPIC_FEATURE.PhenotypicFeature
    class_class_curie: ClassVar[str] = "phenotypic_feature:PhenotypicFeature"
    class_name: ClassVar[str] = "PhenotypicFeature"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.PhenotypicFeature

    description: Optional[str] = None
    evidence: Optional[Union[Union[dict, Evidence], list[Union[dict, Evidence]]]] = empty_list()
    excluded: Optional[Union[bool, Bool]] = None
    modifiers: Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]] = empty_dict()
    onset: Optional[Union[dict, TimeElement]] = None
    resolution: Optional[Union[dict, TimeElement]] = None
    severity: Optional[Union[dict, OntologyClass]] = None
    type: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.evidence, list):
            self.evidence = [self.evidence] if self.evidence is not None else []
        self.evidence = [v if isinstance(v, Evidence) else Evidence(**as_dict(v)) for v in self.evidence]

        if self.excluded is not None and not isinstance(self.excluded, Bool):
            self.excluded = Bool(self.excluded)

        self._normalize_inlined_as_dict(slot_name="modifiers", slot_type=OntologyClass, key_name="id", keyed=True)

        if self.onset is not None and not isinstance(self.onset, TimeElement):
            self.onset = TimeElement(**as_dict(self.onset))

        if self.resolution is not None and not isinstance(self.resolution, TimeElement):
            self.resolution = TimeElement(**as_dict(self.resolution))

        if self.severity is not None and not isinstance(self.severity, OntologyClass):
            self.severity = OntologyClass(**as_dict(self.severity))

        if self.type is not None and not isinstance(self.type, OntologyClass):
            self.type = OntologyClass(**as_dict(self.type))

        super().__post_init__(**kwargs)


@dataclass
class Timestamp(YAMLRoot):
    """
    A Timestamp represents a point in time independent of any time zone or local calendar, encoded as a count of
    seconds and fractions of seconds at nanosecond resolution. The count is relative to an epoch at UTC midnight on
    January 1, 1970, in the proleptic Gregorian calendar which extends the Gregorian calendar backwards to year one.
    All minutes are 60 seconds long. Leap seconds are "smeared" so that no leap second table is needed for
    interpretation, using a [24-hour linear smear](https://developers.google.com/time/smear). The range is from
    0001-01-01T00:00:00Z to 9999-12-31T23:59:59.999999999Z. By restricting to that range, we ensure that we can
    convert to and from [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) date strings. # Examples Example 1: Compute
    Timestamp from POSIX `time()`. Timestamp timestamp; timestamp.set_seconds(time(NULL)); timestamp.set_nanos(0);
    Example 2: Compute Timestamp from POSIX `gettimeofday()`. struct timeval tv; gettimeofday(&tv, NULL); Timestamp
    timestamp; timestamp.set_seconds(tv.tv_sec); timestamp.set_nanos(tv.tv_usec * 1000); Example 3: Compute Timestamp
    from Win32 `GetSystemTimeAsFileTime()`. FILETIME ft; GetSystemTimeAsFileTime(&ft); UINT64 ticks =
    (((UINT64)ft.dwHighDateTime) << 32) | ft.dwLowDateTime; // A Windows tick is 100 nanoseconds. Windows epoch
    1601-01-01T00:00:00Z // is 11644473600 seconds before Unix epoch 1970-01-01T00:00:00Z. Timestamp timestamp;
    timestamp.set_seconds((INT64) ((ticks / 10000000) - 11644473600LL)); timestamp.set_nanos((INT32) ((ticks %
    10000000) * 100)); Example 4: Compute Timestamp from Java `System.currentTimeMillis()`. long millis =
    System.currentTimeMillis(); Timestamp timestamp = Timestamp.newBuilder().setSeconds(millis / 1000) .setNanos((int)
    ((millis % 1000) * 1000000)).build(); Example 5: Compute Timestamp from Java `Instant.now()`. Instant now =
    Instant.now(); Timestamp timestamp = Timestamp.newBuilder().setSeconds(now.getEpochSecond())
    .setNanos(now.getNano()).build(); Example 6: Compute Timestamp from current time in Python. timestamp =
    Timestamp() timestamp.GetCurrentTime() # JSON Mapping In JSON format, the Timestamp type is encoded as a string in
    the [RFC 3339](https://www.ietf.org/rfc/rfc3339.txt) format. That is, the format is
    "{year}-{month}-{day}T{hour}:{min}:{sec}[.{frac_sec}]Z" where {year} is always expressed using four digits while
    {month}, {day}, {hour}, {min}, and {sec} are zero-padded to two digits each. The fractional seconds, which can go
    up to 9 digits (i.e. up to 1 nanosecond resolution), are optional. The "Z" suffix indicates the timezone ("UTC");
    the timezone is required. A proto3 JSON serializer should always use UTC (as indicated by "Z") when printing the
    Timestamp type and a proto3 JSON parser should be able to accept both UTC and other timezones (as indicated by an
    offset). For example, "2017-01-15T01:30:15.01Z" encodes 15.01 seconds past 01:30 UTC on January 15, 2017. In
    JavaScript, one can convert a Date object to this format using the standard
    [toISOString()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString)
    method. In Python, a standard `datetime.datetime` object can be converted to this format using
    [`strftime`](https://docs.python.org/2/library/time.html#time.strftime) with the time format spec
    '%Y-%m-%dT%H:%M:%S.%fZ'. Likewise, in Java, one can use the Joda Time's [`ISODateTimeFormat.dateTime()`](
    http://www.joda.org/joda-time/apidocs/org/joda/time/format/ISODateTimeFormat.html#dateTime%2D%2D ) to obtain a
    formatter capable of generating timestamps in this format.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = TIMESTAMP.Timestamp
    class_class_curie: ClassVar[str] = "timestamp:Timestamp"
    class_name: ClassVar[str] = "Timestamp"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Timestamp

    nanos: Optional[int] = None
    seconds: Optional[int] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.nanos is not None and not isinstance(self.nanos, int):
            self.nanos = int(self.nanos)

        if self.seconds is not None and not isinstance(self.seconds, int):
            self.seconds = int(self.seconds)

        super().__post_init__(**kwargs)


@dataclass
class Expression(YAMLRoot):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#expression
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRSATILE.Expression
    class_class_curie: ClassVar[str] = "vrsatile:Expression"
    class_name: ClassVar[str] = "Expression"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Expression

    syntax: Optional[str] = None
    value: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.syntax is not None and not isinstance(self.syntax, str):
            self.syntax = str(self.syntax)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        super().__post_init__(**kwargs)


@dataclass
class Extension(YAMLRoot):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#extension
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRSATILE.Extension
    class_class_curie: ClassVar[str] = "vrsatile:Extension"
    class_name: ClassVar[str] = "Extension"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Extension

    name: Optional[str] = None
    value: Optional[Union[Union[dict, "Any"], list[Union[dict, "Any"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.value, list):
            self.value = [self.value] if self.value is not None else []
        self.value = [v if isinstance(v, Any) else Any(**as_dict(v)) for v in self.value]

        super().__post_init__(**kwargs)


@dataclass
class GeneDescriptor(YAMLRoot):
    """
    https://vrsatile.readthedocs.io/en/latest/value_object_descriptor/vod_index.html#gene-descriptor
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRSATILE.GeneDescriptor
    class_class_curie: ClassVar[str] = "vrsatile:GeneDescriptor"
    class_name: ClassVar[str] = "GeneDescriptor"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.GeneDescriptor

    alternateIds: Optional[Union[str, list[str]]] = empty_list()
    alternateSymbols: Optional[Union[str, list[str]]] = empty_list()
    description: Optional[str] = None
    symbol: Optional[str] = None
    valueId: Optional[str] = None
    xrefs: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if not isinstance(self.alternateIds, list):
            self.alternateIds = [self.alternateIds] if self.alternateIds is not None else []
        self.alternateIds = [v if isinstance(v, str) else str(v) for v in self.alternateIds]

        if not isinstance(self.alternateSymbols, list):
            self.alternateSymbols = [self.alternateSymbols] if self.alternateSymbols is not None else []
        self.alternateSymbols = [v if isinstance(v, str) else str(v) for v in self.alternateSymbols]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.symbol is not None and not isinstance(self.symbol, str):
            self.symbol = str(self.symbol)

        if self.valueId is not None and not isinstance(self.valueId, str):
            self.valueId = str(self.valueId)

        if not isinstance(self.xrefs, list):
            self.xrefs = [self.xrefs] if self.xrefs is not None else []
        self.xrefs = [v if isinstance(v, str) else str(v) for v in self.xrefs]

        super().__post_init__(**kwargs)


@dataclass
class VariationDescriptor(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRSATILE.VariationDescriptor
    class_class_curie: ClassVar[str] = "vrsatile:VariationDescriptor"
    class_name: ClassVar[str] = "VariationDescriptor"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.VariationDescriptor

    allelicState: Optional[Union[dict, OntologyClass]] = None
    alternateLabels: Optional[Union[str, list[str]]] = empty_list()
    description: Optional[str] = None
    expressions: Optional[Union[Union[dict, Expression], list[Union[dict, Expression]]]] = empty_list()
    extensions: Optional[Union[Union[dict, Extension], list[Union[dict, Extension]]]] = empty_list()
    geneContext: Optional[Union[dict, GeneDescriptor]] = None
    id: Optional[str] = None
    label: Optional[str] = None
    moleculeContext: Optional[Union[str, "MoleculeContext"]] = None
    structuralType: Optional[Union[dict, OntologyClass]] = None
    variation: Optional[Union[dict, "Variation"]] = None
    vcfRecord: Optional[Union[dict, "VcfRecord"]] = None
    vrsRefAlleleSeq: Optional[str] = None
    xrefs: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.allelicState is not None and not isinstance(self.allelicState, OntologyClass):
            self.allelicState = OntologyClass(**as_dict(self.allelicState))

        if not isinstance(self.alternateLabels, list):
            self.alternateLabels = [self.alternateLabels] if self.alternateLabels is not None else []
        self.alternateLabels = [v if isinstance(v, str) else str(v) for v in self.alternateLabels]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.expressions, list):
            self.expressions = [self.expressions] if self.expressions is not None else []
        self.expressions = [v if isinstance(v, Expression) else Expression(**as_dict(v)) for v in self.expressions]

        if not isinstance(self.extensions, list):
            self.extensions = [self.extensions] if self.extensions is not None else []
        self.extensions = [v if isinstance(v, Extension) else Extension(**as_dict(v)) for v in self.extensions]

        if self.geneContext is not None and not isinstance(self.geneContext, GeneDescriptor):
            self.geneContext = GeneDescriptor(**as_dict(self.geneContext))

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.moleculeContext is not None and not isinstance(self.moleculeContext, MoleculeContext):
            self.moleculeContext = MoleculeContext(self.moleculeContext)

        if self.structuralType is not None and not isinstance(self.structuralType, OntologyClass):
            self.structuralType = OntologyClass(**as_dict(self.structuralType))

        if self.variation is not None and not isinstance(self.variation, Variation):
            self.variation = Variation(**as_dict(self.variation))

        if self.vcfRecord is not None and not isinstance(self.vcfRecord, VcfRecord):
            self.vcfRecord = VcfRecord(**as_dict(self.vcfRecord))

        if self.vrsRefAlleleSeq is not None and not isinstance(self.vrsRefAlleleSeq, str):
            self.vrsRefAlleleSeq = str(self.vrsRefAlleleSeq)

        if not isinstance(self.xrefs, list):
            self.xrefs = [self.xrefs] if self.xrefs is not None else []
        self.xrefs = [v if isinstance(v, str) else str(v) for v in self.xrefs]

        super().__post_init__(**kwargs)


@dataclass
class VcfRecord(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRSATILE.VcfRecord
    class_class_curie: ClassVar[str] = "vrsatile:VcfRecord"
    class_name: ClassVar[str] = "VcfRecord"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.VcfRecord

    alt: Optional[str] = None
    chrom: Optional[str] = None
    filter: Optional[str] = None
    genomeAssembly: Optional[str] = None
    id: Optional[str] = None
    info: Optional[str] = None
    pos: Optional[int] = None
    qual: Optional[str] = None
    ref: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.alt is not None and not isinstance(self.alt, str):
            self.alt = str(self.alt)

        if self.chrom is not None and not isinstance(self.chrom, str):
            self.chrom = str(self.chrom)

        if self.filter is not None and not isinstance(self.filter, str):
            self.filter = str(self.filter)

        if self.genomeAssembly is not None and not isinstance(self.genomeAssembly, str):
            self.genomeAssembly = str(self.genomeAssembly)

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        if self.pos is not None and not isinstance(self.pos, int):
            self.pos = int(self.pos)

        if self.qual is not None and not isinstance(self.qual, str):
            self.qual = str(self.qual)

        if self.ref is not None and not isinstance(self.ref, str):
            self.ref = str(self.ref)

        super().__post_init__(**kwargs)


@dataclass
class Any(YAMLRoot):
    """
    `Any` contains an arbitrary serialized protocol buffer message along with a URL that describes the type of the
    serialized message. Protobuf library provides support to pack/unpack Any values in the form of utility functions
    or additional generated methods of the Any type. Example 1: Pack and unpack a message in C++. Foo foo = ...; Any
    any; any.PackFrom(foo); ... if (any.UnpackTo(&foo)) { ... } Example 2: Pack and unpack a message in Java. Foo foo
    = ...; Any any = Any.pack(foo); ... if (any.is(Foo.class)) { foo = any.unpack(Foo.class); } Example 3: Pack and
    unpack a message in Python. foo = Foo(...) any = Any() any.Pack(foo) ... if any.Is(Foo.DESCRIPTOR):
    any.Unpack(foo) ... Example 4: Pack and unpack a message in Go foo := &pb.Foo{...} any, err := anypb.New(foo) if
    err != nil { ... } ... foo := &pb.Foo{} if err := any.UnmarshalTo(foo); err != nil { ... } The pack methods
    provided by protobuf library will by default use 'type.googleapis.com/full.type.name' as the type URL and the
    unpack methods only use the fully qualified type name after the last '/' in the type URL, for example
    "foo.bar.com/x/y.z" will yield type name "y.z". JSON ==== The JSON representation of an `Any` value uses the
    regular representation of the deserialized, embedded message, with an additional field `@type` which contains the
    type URL. Example: package google.profile; message Person { string first_name = 1; string last_name = 2; } {
    "@type": "type.googleapis.com/google.profile.Person", "firstName": <string>, "lastName": <string> } If the
    embedded message type is well-known and has a custom JSON representation, that representation will be embedded
    adding a field `value` which holds the custom JSON in addition to the `@type` field. Example (for message
    [google.protobuf.Duration][]): { "@type": "type.googleapis.com/google.protobuf.Duration", "value": "1.212s" }
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ANY.Any
    class_class_curie: ClassVar[str] = "any:Any"
    class_name: ClassVar[str] = "Any"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Any

    typeUrl: Optional[str] = None
    value: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.typeUrl is not None and not isinstance(self.typeUrl, str):
            self.typeUrl = str(self.typeUrl)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass
class Abundance(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Abundance
    class_class_curie: ClassVar[str] = "vrs:Abundance"
    class_name: ClassVar[str] = "Abundance"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Abundance

    copyNumber: Optional[Union[dict, "CopyNumber"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.copyNumber is not None and not isinstance(self.copyNumber, CopyNumber):
            self.copyNumber = CopyNumber(**as_dict(self.copyNumber))

        super().__post_init__(**kwargs)


@dataclass
class Allele(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Allele
    class_class_curie: ClassVar[str] = "vrs:Allele"
    class_name: ClassVar[str] = "Allele"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Allele

    chromosomeLocation: Optional[Union[dict, "ChromosomeLocation"]] = None
    curie: Optional[str] = None
    derivedSequenceExpression: Optional[Union[dict, "DerivedSequenceExpression"]] = None
    id: Optional[str] = None
    literalSequenceExpression: Optional[Union[dict, "LiteralSequenceExpression"]] = None
    repeatedSequenceExpression: Optional[Union[dict, "RepeatedSequenceExpression"]] = None
    sequenceLocation: Optional[Union[dict, "SequenceLocation"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.chromosomeLocation is not None and not isinstance(self.chromosomeLocation, ChromosomeLocation):
            self.chromosomeLocation = ChromosomeLocation(**as_dict(self.chromosomeLocation))

        if self.curie is not None and not isinstance(self.curie, str):
            self.curie = str(self.curie)

        if self.derivedSequenceExpression is not None and not isinstance(self.derivedSequenceExpression, DerivedSequenceExpression):
            self.derivedSequenceExpression = DerivedSequenceExpression(**as_dict(self.derivedSequenceExpression))

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.literalSequenceExpression is not None and not isinstance(self.literalSequenceExpression, LiteralSequenceExpression):
            self.literalSequenceExpression = LiteralSequenceExpression(**as_dict(self.literalSequenceExpression))

        if self.repeatedSequenceExpression is not None and not isinstance(self.repeatedSequenceExpression, RepeatedSequenceExpression):
            self.repeatedSequenceExpression = RepeatedSequenceExpression(**as_dict(self.repeatedSequenceExpression))

        if self.sequenceLocation is not None and not isinstance(self.sequenceLocation, SequenceLocation):
            self.sequenceLocation = SequenceLocation(**as_dict(self.sequenceLocation))

        super().__post_init__(**kwargs)


@dataclass
class ChromosomeLocation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.ChromosomeLocation
    class_class_curie: ClassVar[str] = "vrs:ChromosomeLocation"
    class_name: ClassVar[str] = "ChromosomeLocation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.ChromosomeLocation

    chr: Optional[str] = None
    id: Optional[str] = None
    interval: Optional[Union[dict, "CytobandInterval"]] = None
    speciesId: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.chr is not None and not isinstance(self.chr, str):
            self.chr = str(self.chr)

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.interval is not None and not isinstance(self.interval, CytobandInterval):
            self.interval = CytobandInterval(**as_dict(self.interval))

        if self.speciesId is not None and not isinstance(self.speciesId, str):
            self.speciesId = str(self.speciesId)

        super().__post_init__(**kwargs)


@dataclass
class CopyNumber(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.CopyNumber
    class_class_curie: ClassVar[str] = "vrs:CopyNumber"
    class_name: ClassVar[str] = "CopyNumber"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.CopyNumber

    allele: Optional[Union[dict, Allele]] = None
    curie: Optional[str] = None
    definiteRange: Optional[Union[dict, "DefiniteRange"]] = None
    derivedSequenceExpression: Optional[Union[dict, "DerivedSequenceExpression"]] = None
    gene: Optional[Union[dict, "Gene"]] = None
    haplotype: Optional[Union[dict, "Haplotype"]] = None
    id: Optional[str] = None
    indefiniteRange: Optional[Union[dict, "IndefiniteRange"]] = None
    literalSequenceExpression: Optional[Union[dict, "LiteralSequenceExpression"]] = None
    number: Optional[Union[dict, "Number"]] = None
    repeatedSequenceExpression: Optional[Union[dict, "RepeatedSequenceExpression"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.allele is not None and not isinstance(self.allele, Allele):
            self.allele = Allele(**as_dict(self.allele))

        if self.curie is not None and not isinstance(self.curie, str):
            self.curie = str(self.curie)

        if self.definiteRange is not None and not isinstance(self.definiteRange, DefiniteRange):
            self.definiteRange = DefiniteRange(**as_dict(self.definiteRange))

        if self.derivedSequenceExpression is not None and not isinstance(self.derivedSequenceExpression, DerivedSequenceExpression):
            self.derivedSequenceExpression = DerivedSequenceExpression(**as_dict(self.derivedSequenceExpression))

        if self.gene is not None and not isinstance(self.gene, Gene):
            self.gene = Gene(**as_dict(self.gene))

        if self.haplotype is not None and not isinstance(self.haplotype, Haplotype):
            self.haplotype = Haplotype()

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.indefiniteRange is not None and not isinstance(self.indefiniteRange, IndefiniteRange):
            self.indefiniteRange = IndefiniteRange(**as_dict(self.indefiniteRange))

        if self.literalSequenceExpression is not None and not isinstance(self.literalSequenceExpression, LiteralSequenceExpression):
            self.literalSequenceExpression = LiteralSequenceExpression(**as_dict(self.literalSequenceExpression))

        if self.number is not None and not isinstance(self.number, Number):
            self.number = Number(**as_dict(self.number))

        if self.repeatedSequenceExpression is not None and not isinstance(self.repeatedSequenceExpression, RepeatedSequenceExpression):
            self.repeatedSequenceExpression = RepeatedSequenceExpression(**as_dict(self.repeatedSequenceExpression))

        super().__post_init__(**kwargs)


@dataclass
class CytobandInterval(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.CytobandInterval
    class_class_curie: ClassVar[str] = "vrs:CytobandInterval"
    class_name: ClassVar[str] = "CytobandInterval"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.CytobandInterval

    end: Optional[str] = None
    start: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.end is not None and not isinstance(self.end, str):
            self.end = str(self.end)

        if self.start is not None and not isinstance(self.start, str):
            self.start = str(self.start)

        super().__post_init__(**kwargs)


@dataclass
class DefiniteRange(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.DefiniteRange
    class_class_curie: ClassVar[str] = "vrs:DefiniteRange"
    class_name: ClassVar[str] = "DefiniteRange"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.DefiniteRange

    max: Optional[int] = None
    min: Optional[int] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.max is not None and not isinstance(self.max, int):
            self.max = int(self.max)

        if self.min is not None and not isinstance(self.min, int):
            self.min = int(self.min)

        super().__post_init__(**kwargs)


@dataclass
class DerivedSequenceExpression(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.DerivedSequenceExpression
    class_class_curie: ClassVar[str] = "vrs:DerivedSequenceExpression"
    class_name: ClassVar[str] = "DerivedSequenceExpression"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.DerivedSequenceExpression

    location: Optional[Union[dict, "SequenceLocation"]] = None
    reverseComplement: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.location is not None and not isinstance(self.location, SequenceLocation):
            self.location = SequenceLocation(**as_dict(self.location))

        if self.reverseComplement is not None and not isinstance(self.reverseComplement, Bool):
            self.reverseComplement = Bool(self.reverseComplement)

        super().__post_init__(**kwargs)


@dataclass
class Feature(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Feature
    class_class_curie: ClassVar[str] = "vrs:Feature"
    class_name: ClassVar[str] = "Feature"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Feature

    gene: Optional[Union[dict, "Gene"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.gene is not None and not isinstance(self.gene, Gene):
            self.gene = Gene(**as_dict(self.gene))

        super().__post_init__(**kwargs)


@dataclass
class Gene(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Gene
    class_class_curie: ClassVar[str] = "vrs:Gene"
    class_name: ClassVar[str] = "Gene"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Gene

    geneId: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.geneId is not None and not isinstance(self.geneId, str):
            self.geneId = str(self.geneId)

        super().__post_init__(**kwargs)


class Haplotype(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Haplotype
    class_class_curie: ClassVar[str] = "vrs:Haplotype"
    class_name: ClassVar[str] = "Haplotype"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Haplotype


@dataclass
class IndefiniteRange(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.IndefiniteRange
    class_class_curie: ClassVar[str] = "vrs:IndefiniteRange"
    class_name: ClassVar[str] = "IndefiniteRange"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.IndefiniteRange

    comparator: Optional[str] = None
    value: Optional[int] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.comparator is not None and not isinstance(self.comparator, str):
            self.comparator = str(self.comparator)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        super().__post_init__(**kwargs)


@dataclass
class LiteralSequenceExpression(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.LiteralSequenceExpression
    class_class_curie: ClassVar[str] = "vrs:LiteralSequenceExpression"
    class_name: ClassVar[str] = "LiteralSequenceExpression"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.LiteralSequenceExpression

    sequence: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.sequence is not None and not isinstance(self.sequence, str):
            self.sequence = str(self.sequence)

        super().__post_init__(**kwargs)


@dataclass
class Location(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Location
    class_class_curie: ClassVar[str] = "vrs:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Location

    chromosomeLocation: Optional[Union[dict, ChromosomeLocation]] = None
    sequenceLocation: Optional[Union[dict, "SequenceLocation"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.chromosomeLocation is not None and not isinstance(self.chromosomeLocation, ChromosomeLocation):
            self.chromosomeLocation = ChromosomeLocation(**as_dict(self.chromosomeLocation))

        if self.sequenceLocation is not None and not isinstance(self.sequenceLocation, SequenceLocation):
            self.sequenceLocation = SequenceLocation(**as_dict(self.sequenceLocation))

        super().__post_init__(**kwargs)


@dataclass
class Member(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Member
    class_class_curie: ClassVar[str] = "vrs:Member"
    class_name: ClassVar[str] = "Member"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Member

    allele: Optional[Union[dict, Allele]] = None
    copyNumber: Optional[Union[dict, CopyNumber]] = None
    curie: Optional[str] = None
    haplotype: Optional[Union[dict, Haplotype]] = None
    id: Optional[str] = None
    members: Optional[Union[Union[dict, "Member"], list[Union[dict, "Member"]]]] = empty_list()
    text: Optional[Union[dict, "Text"]] = None
    variationSet: Optional[Union[dict, "VariationSet"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.allele is not None and not isinstance(self.allele, Allele):
            self.allele = Allele(**as_dict(self.allele))

        if self.copyNumber is not None and not isinstance(self.copyNumber, CopyNumber):
            self.copyNumber = CopyNumber(**as_dict(self.copyNumber))

        if self.curie is not None and not isinstance(self.curie, str):
            self.curie = str(self.curie)

        if self.haplotype is not None and not isinstance(self.haplotype, Haplotype):
            self.haplotype = Haplotype()

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if not isinstance(self.members, list):
            self.members = [self.members] if self.members is not None else []
        self.members = [v if isinstance(v, Member) else Member(**as_dict(v)) for v in self.members]

        if self.text is not None and not isinstance(self.text, Text):
            self.text = Text(**as_dict(self.text))

        if self.variationSet is not None and not isinstance(self.variationSet, VariationSet):
            self.variationSet = VariationSet()

        super().__post_init__(**kwargs)


@dataclass
class MolecularVariation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.MolecularVariation
    class_class_curie: ClassVar[str] = "vrs:MolecularVariation"
    class_name: ClassVar[str] = "MolecularVariation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.MolecularVariation

    allele: Optional[Union[dict, Allele]] = None
    haplotype: Optional[Union[dict, Haplotype]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.allele is not None and not isinstance(self.allele, Allele):
            self.allele = Allele(**as_dict(self.allele))

        if self.haplotype is not None and not isinstance(self.haplotype, Haplotype):
            self.haplotype = Haplotype()

        super().__post_init__(**kwargs)


@dataclass
class Number(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Number
    class_class_curie: ClassVar[str] = "vrs:Number"
    class_name: ClassVar[str] = "Number"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Number

    value: Optional[int] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        super().__post_init__(**kwargs)


@dataclass
class RepeatedSequenceExpression(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.RepeatedSequenceExpression
    class_class_curie: ClassVar[str] = "vrs:RepeatedSequenceExpression"
    class_name: ClassVar[str] = "RepeatedSequenceExpression"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.RepeatedSequenceExpression

    definiteRange: Optional[Union[dict, DefiniteRange]] = None
    derivedSequenceExpression: Optional[Union[dict, DerivedSequenceExpression]] = None
    indefiniteRange: Optional[Union[dict, IndefiniteRange]] = None
    literalSequenceExpression: Optional[Union[dict, LiteralSequenceExpression]] = None
    number: Optional[Union[dict, Number]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.definiteRange is not None and not isinstance(self.definiteRange, DefiniteRange):
            self.definiteRange = DefiniteRange(**as_dict(self.definiteRange))

        if self.derivedSequenceExpression is not None and not isinstance(self.derivedSequenceExpression, DerivedSequenceExpression):
            self.derivedSequenceExpression = DerivedSequenceExpression(**as_dict(self.derivedSequenceExpression))

        if self.indefiniteRange is not None and not isinstance(self.indefiniteRange, IndefiniteRange):
            self.indefiniteRange = IndefiniteRange(**as_dict(self.indefiniteRange))

        if self.literalSequenceExpression is not None and not isinstance(self.literalSequenceExpression, LiteralSequenceExpression):
            self.literalSequenceExpression = LiteralSequenceExpression(**as_dict(self.literalSequenceExpression))

        if self.number is not None and not isinstance(self.number, Number):
            self.number = Number(**as_dict(self.number))

        super().__post_init__(**kwargs)


@dataclass
class SequenceExpression(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.SequenceExpression
    class_class_curie: ClassVar[str] = "vrs:SequenceExpression"
    class_name: ClassVar[str] = "SequenceExpression"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.SequenceExpression

    derivedSequenceExpression: Optional[Union[dict, DerivedSequenceExpression]] = None
    literalSequenceExpression: Optional[Union[dict, LiteralSequenceExpression]] = None
    repeatedSequenceExpression: Optional[Union[dict, RepeatedSequenceExpression]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.derivedSequenceExpression is not None and not isinstance(self.derivedSequenceExpression, DerivedSequenceExpression):
            self.derivedSequenceExpression = DerivedSequenceExpression(**as_dict(self.derivedSequenceExpression))

        if self.literalSequenceExpression is not None and not isinstance(self.literalSequenceExpression, LiteralSequenceExpression):
            self.literalSequenceExpression = LiteralSequenceExpression(**as_dict(self.literalSequenceExpression))

        if self.repeatedSequenceExpression is not None and not isinstance(self.repeatedSequenceExpression, RepeatedSequenceExpression):
            self.repeatedSequenceExpression = RepeatedSequenceExpression(**as_dict(self.repeatedSequenceExpression))

        super().__post_init__(**kwargs)


@dataclass
class SequenceInterval(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.SequenceInterval
    class_class_curie: ClassVar[str] = "vrs:SequenceInterval"
    class_name: ClassVar[str] = "SequenceInterval"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.SequenceInterval

    endDefiniteRange: Optional[Union[dict, DefiniteRange]] = None
    endIndefiniteRange: Optional[Union[dict, IndefiniteRange]] = None
    endNumber: Optional[Union[dict, Number]] = None
    startDefiniteRange: Optional[Union[dict, DefiniteRange]] = None
    startIndefiniteRange: Optional[Union[dict, IndefiniteRange]] = None
    startNumber: Optional[Union[dict, Number]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.endDefiniteRange is not None and not isinstance(self.endDefiniteRange, DefiniteRange):
            self.endDefiniteRange = DefiniteRange(**as_dict(self.endDefiniteRange))

        if self.endIndefiniteRange is not None and not isinstance(self.endIndefiniteRange, IndefiniteRange):
            self.endIndefiniteRange = IndefiniteRange(**as_dict(self.endIndefiniteRange))

        if self.endNumber is not None and not isinstance(self.endNumber, Number):
            self.endNumber = Number(**as_dict(self.endNumber))

        if self.startDefiniteRange is not None and not isinstance(self.startDefiniteRange, DefiniteRange):
            self.startDefiniteRange = DefiniteRange(**as_dict(self.startDefiniteRange))

        if self.startIndefiniteRange is not None and not isinstance(self.startIndefiniteRange, IndefiniteRange):
            self.startIndefiniteRange = IndefiniteRange(**as_dict(self.startIndefiniteRange))

        if self.startNumber is not None and not isinstance(self.startNumber, Number):
            self.startNumber = Number(**as_dict(self.startNumber))

        super().__post_init__(**kwargs)


@dataclass
class SequenceLocation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.SequenceLocation
    class_class_curie: ClassVar[str] = "vrs:SequenceLocation"
    class_name: ClassVar[str] = "SequenceLocation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.SequenceLocation

    id: Optional[str] = None
    sequenceId: Optional[str] = None
    sequenceInterval: Optional[Union[dict, SequenceInterval]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.sequenceId is not None and not isinstance(self.sequenceId, str):
            self.sequenceId = str(self.sequenceId)

        if self.sequenceInterval is not None and not isinstance(self.sequenceInterval, SequenceInterval):
            self.sequenceInterval = SequenceInterval(**as_dict(self.sequenceInterval))

        super().__post_init__(**kwargs)


@dataclass
class SequenceState(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.SequenceState
    class_class_curie: ClassVar[str] = "vrs:SequenceState"
    class_name: ClassVar[str] = "SequenceState"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.SequenceState

    sequence: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.sequence is not None and not isinstance(self.sequence, str):
            self.sequence = str(self.sequence)

        super().__post_init__(**kwargs)


@dataclass
class SimpleInterval(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.SimpleInterval
    class_class_curie: ClassVar[str] = "vrs:SimpleInterval"
    class_name: ClassVar[str] = "SimpleInterval"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.SimpleInterval

    end: Optional[int] = None
    start: Optional[int] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.end is not None and not isinstance(self.end, int):
            self.end = int(self.end)

        if self.start is not None and not isinstance(self.start, int):
            self.start = int(self.start)

        super().__post_init__(**kwargs)


@dataclass
class SystemicVariation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.SystemicVariation
    class_class_curie: ClassVar[str] = "vrs:SystemicVariation"
    class_name: ClassVar[str] = "SystemicVariation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.SystemicVariation

    copyNumber: Optional[Union[dict, CopyNumber]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.copyNumber is not None and not isinstance(self.copyNumber, CopyNumber):
            self.copyNumber = CopyNumber(**as_dict(self.copyNumber))

        super().__post_init__(**kwargs)


@dataclass
class Text(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Text
    class_class_curie: ClassVar[str] = "vrs:Text"
    class_name: ClassVar[str] = "Text"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Text

    definition: Optional[str] = None
    id: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.definition is not None and not isinstance(self.definition, str):
            self.definition = str(self.definition)

        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)


@dataclass
class UtilityVariation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.UtilityVariation
    class_class_curie: ClassVar[str] = "vrs:UtilityVariation"
    class_name: ClassVar[str] = "UtilityVariation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.UtilityVariation

    text: Optional[Union[dict, Text]] = None
    variationSet: Optional[Union[dict, "VariationSet"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.text is not None and not isinstance(self.text, Text):
            self.text = Text(**as_dict(self.text))

        if self.variationSet is not None and not isinstance(self.variationSet, VariationSet):
            self.variationSet = VariationSet()

        super().__post_init__(**kwargs)


@dataclass
class Variation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.Variation
    class_class_curie: ClassVar[str] = "vrs:Variation"
    class_name: ClassVar[str] = "Variation"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.Variation

    allele: Optional[Union[dict, Allele]] = None
    copyNumber: Optional[Union[dict, CopyNumber]] = None
    haplotype: Optional[Union[dict, Haplotype]] = None
    text: Optional[Union[dict, Text]] = None
    variationSet: Optional[Union[dict, "VariationSet"]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.allele is not None and not isinstance(self.allele, Allele):
            self.allele = Allele(**as_dict(self.allele))

        if self.copyNumber is not None and not isinstance(self.copyNumber, CopyNumber):
            self.copyNumber = CopyNumber(**as_dict(self.copyNumber))

        if self.haplotype is not None and not isinstance(self.haplotype, Haplotype):
            self.haplotype = Haplotype()

        if self.text is not None and not isinstance(self.text, Text):
            self.text = Text(**as_dict(self.text))

        if self.variationSet is not None and not isinstance(self.variationSet, VariationSet):
            self.variationSet = VariationSet()

        super().__post_init__(**kwargs)


class VariationSet(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = VRS.VariationSet
    class_class_curie: ClassVar[str] = "vrs:VariationSet"
    class_name: ClassVar[str] = "VariationSet"
    class_model_uri: ClassVar[URIRef] = PHENOPACKETS.VariationSet


# Enumerations
class MondoDiseaseTerms(EnumDefinitionImpl):
    """
    Mondo Disease Ontology provides a comprehensive logically structured ontology of diseases that integrates multiple
    other disease ontologies.
    """
    _defn = EnumDefinition(
        name="MondoDiseaseTerms",
        description="Mondo Disease Ontology provides a comprehensive logically structured ontology of diseases that integrates multiple other disease ontologies.",
    )

class NCITDiseaseTerms(EnumDefinitionImpl):
    """
    All disease terms from the NCI Thesaurus
    """
    _defn = EnumDefinition(
        name="NCITDiseaseTerms",
        description="All disease terms from the NCI Thesaurus",
    )

class NCITNeoplasmTerms(EnumDefinitionImpl):
    """
    All neoplasm terms from the NCI Thesaurus
    """
    _defn = EnumDefinition(
        name="NCITNeoplasmTerms",
        description="All neoplasm terms from the NCI Thesaurus",
    )

class HPOAbnormalityTerms(EnumDefinitionImpl):
    """
    The Human Phenotype Ontology (HPO) provides a comprehensive logical standard to describe and computationally
    analyze phenotypic abnormalities found in human disease.
    """
    _defn = EnumDefinition(
        name="HPOAbnormalityTerms",
        description="The Human Phenotype Ontology (HPO) provides a comprehensive logical standard to describe and computationally analyze phenotypic abnormalities found in human disease.",
    )

class UberonAnatomicalEntityTerms(EnumDefinitionImpl):
    """
    UBERON is an integrated cross-species ontology with classes representing a variety of anatomical entities.
    """
    _defn = EnumDefinition(
        name="UberonAnatomicalEntityTerms",
        description="UBERON is an integrated cross-species ontology with classes representing a variety of anatomical entities.",
    )

class HGNCGeneTerms(EnumDefinitionImpl):
    """
    The HUGO Gene Nomenclature Committee (HGNC) provides standard names, symbols, and IDs for human genes.
    """
    _defn = EnumDefinition(
        name="HGNCGeneTerms",
        description="The HUGO Gene Nomenclature Committee (HGNC) provides standard names, symbols, and IDs for human genes.",
    )

class UOUnitTerms(EnumDefinitionImpl):
    """
    The Units of measurement ontology (denoted UO) provides terms for units commonly encountered in medical data. The
    following table shows some typical examples.
    """
    _defn = EnumDefinition(
        name="UOUnitTerms",
        description="The Units of measurement ontology (denoted UO) provides terms for units commonly encountered in medical data. The following table shows some typical examples.",
    )

class GENOZygosityTerms(EnumDefinitionImpl):
    """
    GENO is an ontology of genotypes their more fundamental sequence components. This enum refers to the zygosity
    subset of GENO
    """
    _defn = EnumDefinition(
        name="GENOZygosityTerms",
        description="GENO is an ontology of genotypes their more fundamental sequence components. This enum refers to the zygosity subset of GENO",
    )

class LOINCMeasurementTerms(EnumDefinitionImpl):
    """
    Logical Observation Identifiers Names and Codes (LOINC) is a database and universal standard for identifying
    medical laboratory observations. It can be used to denote clinical assays in the Measurement element. examples:
    """
    _defn = EnumDefinition(
        name="LOINCMeasurementTerms",
        description="Logical Observation Identifiers Names and Codes (LOINC) is a database and universal standard for identifying medical laboratory observations. It can be used to denote clinical assays in the Measurement element.    examples:",
    )

class AcmgPathogenicityClassification(EnumDefinitionImpl):

    BENIGN = PermissibleValue(text="BENIGN")
    LIKELY_BENIGN = PermissibleValue(text="LIKELY_BENIGN")
    LIKELY_PATHOGENIC = PermissibleValue(text="LIKELY_PATHOGENIC")
    NOT_PROVIDED = PermissibleValue(text="NOT_PROVIDED")
    PATHOGENIC = PermissibleValue(text="PATHOGENIC")
    UNCERTAIN_SIGNIFICANCE = PermissibleValue(text="UNCERTAIN_SIGNIFICANCE")

    _defn = EnumDefinition(
        name="AcmgPathogenicityClassification",
    )

class InterpretationStatus(EnumDefinitionImpl):

    CANDIDATE = PermissibleValue(text="CANDIDATE")
    CAUSATIVE = PermissibleValue(text="CAUSATIVE")
    CONTRIBUTORY = PermissibleValue(text="CONTRIBUTORY")
    REJECTED = PermissibleValue(text="REJECTED")
    UNKNOWN_STATUS = PermissibleValue(text="UNKNOWN_STATUS")

    _defn = EnumDefinition(
        name="InterpretationStatus",
    )

class ProgressStatus(EnumDefinitionImpl):

    COMPLETED = PermissibleValue(text="COMPLETED")
    IN_PROGRESS = PermissibleValue(text="IN_PROGRESS")
    SOLVED = PermissibleValue(text="SOLVED")
    UNKNOWN_PROGRESS = PermissibleValue(text="UNKNOWN_PROGRESS")
    UNSOLVED = PermissibleValue(text="UNSOLVED")

    _defn = EnumDefinition(
        name="ProgressStatus",
    )

class TherapeuticActionability(EnumDefinitionImpl):

    ACTIONABLE = PermissibleValue(text="ACTIONABLE")
    NOT_ACTIONABLE = PermissibleValue(text="NOT_ACTIONABLE")
    UNKNOWN_ACTIONABILITY = PermissibleValue(text="UNKNOWN_ACTIONABILITY")

    _defn = EnumDefinition(
        name="TherapeuticActionability",
    )

class KaryotypicSex(EnumDefinitionImpl):
    """
    Karyotypic sex of the individual
    """
    OTHER_KARYOTYPE = PermissibleValue(text="OTHER_KARYOTYPE")
    UNKNOWN_KARYOTYPE = PermissibleValue(text="UNKNOWN_KARYOTYPE")
    XO = PermissibleValue(text="XO")
    XX = PermissibleValue(text="XX")
    XXX = PermissibleValue(text="XXX")
    XXXX = PermissibleValue(text="XXXX")
    XXXY = PermissibleValue(text="XXXY")
    XXY = PermissibleValue(text="XXY")
    XXYY = PermissibleValue(text="XXYY")
    XY = PermissibleValue(text="XY")
    XYY = PermissibleValue(text="XYY")

    _defn = EnumDefinition(
        name="KaryotypicSex",
        description="Karyotypic sex of the individual",
    )

class Sex(EnumDefinitionImpl):
    """
    Sex of an individual FHIR mapping: AdministrativeGender
    (https://www.hl7.org/fhir/codesystem-administrative-gender.html)
    """
    FEMALE = PermissibleValue(text="FEMALE",
                                   description="Female")
    MALE = PermissibleValue(text="MALE",
                               description="Male")
    OTHER_SEX = PermissibleValue(text="OTHER_SEX",
                                         description="It is not possible, to accurately assess the applicability of MALE/FEMALE.")
    UNKNOWN_SEX = PermissibleValue(text="UNKNOWN_SEX",
                                             description="Not assessed / available.")

    _defn = EnumDefinition(
        name="Sex",
        description="Sex of an individual FHIR mapping: AdministrativeGender (https://www.hl7.org/fhir/codesystem-administrative-gender.html)",
    )

class Status(EnumDefinitionImpl):
    """
    Default = false i.e. the individual is alive. MUST be true if
    """
    ALIVE = PermissibleValue(text="ALIVE")
    DECEASED = PermissibleValue(text="DECEASED")
    UNKNOWN_STATUS = PermissibleValue(text="UNKNOWN_STATUS")

    _defn = EnumDefinition(
        name="Status",
        description="Default = false i.e. the individual is alive. MUST be true if",
    )

class DrugType(EnumDefinitionImpl):
    """
    A simplified version of ODHSI-DRUG_EXPOSURE
    """
    ADMINISTRATION_RELATED_TO_PROCEDURE = PermissibleValue(text="ADMINISTRATION_RELATED_TO_PROCEDURE")
    EHR_MEDICATION_LIST = PermissibleValue(text="EHR_MEDICATION_LIST")
    PRESCRIPTION = PermissibleValue(text="PRESCRIPTION")
    UNKNOWN_DRUG_TYPE = PermissibleValue(text="UNKNOWN_DRUG_TYPE")

    _defn = EnumDefinition(
        name="DrugType",
        description="A simplified version of ODHSI-DRUG_EXPOSURE",
    )

class RegimenStatus(EnumDefinitionImpl):

    COMPLETED = PermissibleValue(text="COMPLETED")
    DISCONTINUED = PermissibleValue(text="DISCONTINUED")
    STARTED = PermissibleValue(text="STARTED")
    UNKNOWN_STATUS = PermissibleValue(text="UNKNOWN_STATUS")

    _defn = EnumDefinition(
        name="RegimenStatus",
    )

class AffectedStatus(EnumDefinitionImpl):

    AFFECTED = PermissibleValue(text="AFFECTED")
    MISSING = PermissibleValue(text="MISSING")
    UNAFFECTED = PermissibleValue(text="UNAFFECTED")

    _defn = EnumDefinition(
        name="AffectedStatus",
    )

class AllelicStateTerms(EnumDefinitionImpl):

    HETEROZYGOUS = PermissibleValue(text="HETEROZYGOUS",
                                               description="heterozygous",
                                               meaning=GENO["0000135"])
    HOMOZYGOUS = PermissibleValue(text="HOMOZYGOUS",
                                           description="homozygous",
                                           meaning=GENO["0000136"])
    HEMIZYGOUS = PermissibleValue(text="HEMIZYGOUS",
                                           description="hemizygous",
                                           meaning=GENO["0000134"])

    _defn = EnumDefinition(
        name="AllelicStateTerms",
    )

class AssaysTerms(EnumDefinitionImpl):

    CREATINE_KINASE = PermissibleValue(text="CREATINE_KINASE",
                                                     description="Creatine kinase [Enzymatic activity/volume] in Serum or Plasma",
                                                     meaning=LOINC["2157-6"])

    _defn = EnumDefinition(
        name="AssaysTerms",
    )

class GenderTerms(EnumDefinitionImpl):

    IDENTIFIES_AS_MALE = PermissibleValue(text="IDENTIFIES_AS_MALE",
                                                           description="Identifies as male",
                                                           meaning=LOINC["LA22878-5"])
    IDENTIFIES_AS_FEMALE = PermissibleValue(text="IDENTIFIES_AS_FEMALE",
                                                               description="Identifies as female",
                                                               meaning=LOINC["LA22879-3"])
    FEMALE_TO_MALE_TRANSSEXUAL = PermissibleValue(text="FEMALE_TO_MALE_TRANSSEXUAL",
                                                                           description="Female-to-male transsexual",
                                                                           meaning=LOINC["LA22880-1"])
    MALE_TO_FEMALE_TRANSSEXUAL = PermissibleValue(text="MALE_TO_FEMALE_TRANSSEXUAL",
                                                                           description="Male-to-female transsexual",
                                                                           meaning=LOINC["LA22881-9"])
    IDENTIFIES_AS_NON_CONFORMING = PermissibleValue(text="IDENTIFIES_AS_NON_CONFORMING",
                                                                               description="Identifies as non-conforming",
                                                                               meaning=LOINC["LA22882-7"])
    OTHER_GENDER = PermissibleValue(text="OTHER_GENDER",
                                               description="other",
                                               meaning=LOINC["LA46-8"])
    ASKED_BUT_UNKNOWN = PermissibleValue(text="ASKED_BUT_UNKNOWN",
                                                         description="Asked but unknown",
                                                         meaning=LOINC["LA20384-6"])

    _defn = EnumDefinition(
        name="GenderTerms",
    )

class LateralityTerms(EnumDefinitionImpl):

    RIGHT = PermissibleValue(text="RIGHT",
                                 description="Right",
                                 meaning=HP["0012834"])
    LEFT = PermissibleValue(text="LEFT",
                               description="Left",
                               meaning=HP["0012835"])
    UNILATERAL = PermissibleValue(text="UNILATERAL",
                                           description="Unilateral",
                                           meaning=HP["0012833"])
    BILATERAL = PermissibleValue(text="BILATERAL",
                                         description="Bilateral",
                                         meaning=HP["0012832"])

    _defn = EnumDefinition(
        name="LateralityTerms",
    )

class MedicalActionsTerms(EnumDefinitionImpl):

    ADVERSE_EVENT = PermissibleValue(text="ADVERSE_EVENT",
                                                 description="Adverse Event",
                                                 meaning=NCIT.C41331)
    FOUR_TIMES_DAILY = PermissibleValue(text="FOUR_TIMES_DAILY",
                                                       description="Four Times Daily",
                                                       meaning=NCIT.C64530)
    INTRA_ARTERIAL = PermissibleValue(text="INTRA_ARTERIAL",
                                                   description="Intraarterial Route of Administration",
                                                   meaning=NCIT.C38222)
    IV_ADMINISTRATION = PermissibleValue(text="IV_ADMINISTRATION",
                                                         description="Intravenous Route of Administration",
                                                         meaning=NCIT.C38276)
    ORAL_ADMINISTRATION = PermissibleValue(text="ORAL_ADMINISTRATION",
                                                             description="Oral Route of Administration",
                                                             meaning=NCIT.C38288)
    ONCE = PermissibleValue(text="ONCE",
                               description="Once",
                               meaning=NCIT.C64576)
    ONCE_DAILY = PermissibleValue(text="ONCE_DAILY",
                                           description="Once Daily",
                                           meaning=NCIT.C125004)
    THREE_TIMES_DAILY = PermissibleValue(text="THREE_TIMES_DAILY",
                                                         description="Three Times Daily",
                                                         meaning=NCIT.C64527)
    TWICE_DAILY = PermissibleValue(text="TWICE_DAILY",
                                             description="Twice Daily",
                                             meaning=NCIT.C64496)

    _defn = EnumDefinition(
        name="MedicalActionsTerms",
    )

class OnsetTerms(EnumDefinitionImpl):

    ANTENATAL_ONSET = PermissibleValue(text="ANTENATAL_ONSET",
                                                     description="Antenatal onset",
                                                     meaning=HP["0030674"])
    EMBRYONAL_ONSET = PermissibleValue(text="EMBRYONAL_ONSET",
                                                     description="Embryonal onset",
                                                     meaning=HP["0011460"])
    FETAL_ONSET = PermissibleValue(text="FETAL_ONSET",
                                             description="Fetal onset",
                                             meaning=HP["0011461"])
    LATE_FIRST_TRIMESTER_ONSET = PermissibleValue(text="LATE_FIRST_TRIMESTER_ONSET",
                                                                           description="Late first trimester onset",
                                                                           meaning=HP["0034199"])
    SECOND_TRIMESTER_ONSET = PermissibleValue(text="SECOND_TRIMESTER_ONSET",
                                                                   description="Second trimester onset",
                                                                   meaning=HP["0034198"])
    THIRD_TRIMESTER_ONSET = PermissibleValue(text="THIRD_TRIMESTER_ONSET",
                                                                 description="Third trimester onset",
                                                                 meaning=HP["0034197"])
    CONGENITAL_ONSET = PermissibleValue(text="CONGENITAL_ONSET",
                                                       description="Congenital onset",
                                                       meaning=HP["0003577"])
    NEONATAL_ONSET = PermissibleValue(text="NEONATAL_ONSET",
                                                   description="Neonatal onset",
                                                   meaning=HP["0003623"])
    INFANTILE_ONSET = PermissibleValue(text="INFANTILE_ONSET",
                                                     description="Infantile onset",
                                                     meaning=HP["0003593"])
    CHILDHOOD_ONSET = PermissibleValue(text="CHILDHOOD_ONSET",
                                                     description="Childhood onset",
                                                     meaning=HP["0011463"])
    JUVENILE_ONSET = PermissibleValue(text="JUVENILE_ONSET",
                                                   description="Juvenile onset",
                                                   meaning=HP["0003621"])
    ADULT_ONSET = PermissibleValue(text="ADULT_ONSET",
                                             description="Adult onset",
                                             meaning=HP["0003581"])
    YOUNG_ADULT_ONSET = PermissibleValue(text="YOUNG_ADULT_ONSET",
                                                         description="Young adult onset",
                                                         meaning=HP["0011462"])
    EARLY_YOUNG_ADULT_ONSET = PermissibleValue(text="EARLY_YOUNG_ADULT_ONSET",
                                                                     description="Early young adult onset",
                                                                     meaning=HP["0025708"])
    INTERMEDIATE_YOUNG_ADULT_ONSET = PermissibleValue(text="INTERMEDIATE_YOUNG_ADULT_ONSET",
                                                                                   description="Intermediate young adult onset",
                                                                                   meaning=HP["0025709"])
    LATE_YOUNG_ADULT_ONSET = PermissibleValue(text="LATE_YOUNG_ADULT_ONSET",
                                                                   description="Late young adult onset",
                                                                   meaning=HP["0025710"])
    MIDDLE_AGE_ONSET = PermissibleValue(text="MIDDLE_AGE_ONSET",
                                                       description="Middle age onset",
                                                       meaning=HP["0003596"])
    LATE_ONSET = PermissibleValue(text="LATE_ONSET",
                                           description="Late onset",
                                           meaning=HP["0003584"])

    _defn = EnumDefinition(
        name="OnsetTerms",
    )

class OrganTerms(EnumDefinitionImpl):

    BRAIN = PermissibleValue(text="BRAIN",
                                 description="brain",
                                 meaning=UBERON["0000955"])
    CEREBELLUM = PermissibleValue(text="CEREBELLUM",
                                           description="cerebellum",
                                           meaning=UBERON["0002037"])
    EAR = PermissibleValue(text="EAR",
                             description="ear",
                             meaning=UBERON["0001690"])
    EYE = PermissibleValue(text="EYE",
                             description="eye",
                             meaning=UBERON["0000970"])
    HEART = PermissibleValue(text="HEART",
                                 description="heart",
                                 meaning=UBERON["0002107"])
    KIDNEY = PermissibleValue(text="KIDNEY",
                                   description="kidney",
                                   meaning=UBERON["0002113"])
    LARGE_INTESTINE = PermissibleValue(text="LARGE_INTESTINE",
                                                     description="large intestine",
                                                     meaning=UBERON["0000059"])
    LIVER = PermissibleValue(text="LIVER",
                                 description="liver",
                                 meaning=UBERON["0002107"])
    LUNG = PermissibleValue(text="LUNG",
                               description="lung",
                               meaning=UBERON["0002048"])
    NOSE = PermissibleValue(text="NOSE",
                               description="nose",
                               meaning=UBERON["0000004"])
    SMALL_INTESTINE = PermissibleValue(text="SMALL_INTESTINE",
                                                     description="small intestine",
                                                     meaning=UBERON["0002108"])
    SPINAL_CORD = PermissibleValue(text="SPINAL_CORD",
                                             description="spinal cord",
                                             meaning=UBERON["0002240"])
    SPLEEN = PermissibleValue(text="SPLEEN",
                                   description="spleen",
                                   meaning=UBERON["0002106"])
    TONGUE = PermissibleValue(text="TONGUE",
                                   description="tongue",
                                   meaning=UBERON["0001723"])
    THYMUS = PermissibleValue(text="THYMUS",
                                   description="thymus",
                                   meaning=UBERON["0002370"])

    _defn = EnumDefinition(
        name="OrganTerms",
    )

class ResponseTerms(EnumDefinitionImpl):

    FAVORABLE = PermissibleValue(text="FAVORABLE",
                                         description="Favorable",
                                         meaning=NCIT.C102560)
    UNFAVORABLE = PermissibleValue(text="UNFAVORABLE",
                                             description="Unfavorable",
                                             meaning=NCIT.C102561)

    _defn = EnumDefinition(
        name="ResponseTerms",
    )

class SpatialPatternTerms(EnumDefinitionImpl):

    PREDOMINANT_SMALL_JOINT_LOCALIZATION = PermissibleValue(text="PREDOMINANT_SMALL_JOINT_LOCALIZATION",
                                                                                               description="Predominant small joint localization",
                                                                                               meaning=HP["0032544"])
    POLYCYCLIC = PermissibleValue(text="POLYCYCLIC",
                                           description="Polycyclic",
                                           meaning=HP["0031450"])
    AXIAL = PermissibleValue(text="AXIAL",
                                 description="Axial",
                                 meaning=HP["0025287"])
    PERILOBULAR = PermissibleValue(text="PERILOBULAR",
                                             description="Perilobular",
                                             meaning=HP["0033813"])
    PARASEPTAL = PermissibleValue(text="PARASEPTAL",
                                           description="Paraseptal",
                                           meaning=HP["0033814"])
    BRONCHOCENTRIC = PermissibleValue(text="BRONCHOCENTRIC",
                                                   description="Bronchocentric",
                                                   meaning=HP["0033815"])
    CENTRILOBULAR = PermissibleValue(text="CENTRILOBULAR",
                                                 description="Centrilobular",
                                                 meaning=HP["0033816"])
    MILIARY = PermissibleValue(text="MILIARY",
                                     description="Miliary",
                                     meaning=HP["0033817"])
    GENERALIZED = PermissibleValue(text="GENERALIZED",
                                             description="Generalized",
                                             meaning=HP["0012837"])
    PERILYMPHATIC = PermissibleValue(text="PERILYMPHATIC",
                                                 description="Perilymphatic",
                                                 meaning=HP["0033819"])
    LOCALIZED = PermissibleValue(text="LOCALIZED",
                                         description="Localized",
                                         meaning=HP["0012838"])
    RETICULAR = PermissibleValue(text="RETICULAR",
                                         description="Reticular",
                                         meaning=HP["0033818"])
    DISTAL = PermissibleValue(text="DISTAL",
                                   description="Distal",
                                   meaning=HP["0012839"])
    CENTRAL = PermissibleValue(text="CENTRAL",
                                     description="Central",
                                     meaning=HP["0030645"])
    UPPER_BODY_PREDOMINANCE = PermissibleValue(text="UPPER_BODY_PREDOMINANCE",
                                                                     description="Upper-body predominance",
                                                                     meaning=HP["0025290"])
    JOINT_EXTENSOR_SURFACE_LOCALIZATION = PermissibleValue(text="JOINT_EXTENSOR_SURFACE_LOCALIZATION",
                                                                                             description="Joint extensor surface localization",
                                                                                             meaning=HP["0032539"])
    HERPETIFORM = PermissibleValue(text="HERPETIFORM",
                                             description="Herpetiform",
                                             meaning=HP["0025295"])
    MORBILLIFORM = PermissibleValue(text="MORBILLIFORM",
                                               description="Morbilliform",
                                               meaning=HP["0025296"])
    PERICENTRAL = PermissibleValue(text="PERICENTRAL",
                                             description="Pericentral",
                                             meaning=HP["0030649"])
    DERMATOMAL = PermissibleValue(text="DERMATOMAL",
                                           description="Dermatomal",
                                           meaning=HP["0025294"])
    MIDPERIPHERAL = PermissibleValue(text="MIDPERIPHERAL",
                                                 description="Midperipheral",
                                                 meaning=HP["0030648"])
    DISTRIBUTED_ALONG_BLASCHKO_LINES = PermissibleValue(text="DISTRIBUTED_ALONG_BLASCHKO_LINES",
                                                                                       description="Distributed along Blaschko lines",
                                                                                       meaning=HP["0025293"])
    ACRAL = PermissibleValue(text="ACRAL",
                                 description="Acral",
                                 meaning=HP["0025292"])
    PARACENTRAL = PermissibleValue(text="PARACENTRAL",
                                             description="Paracentral",
                                             meaning=HP["0030647"])
    LATERAL = PermissibleValue(text="LATERAL",
                                     description="Lateral",
                                     meaning=HP["0025275"])
    PERIPHERAL = PermissibleValue(text="PERIPHERAL",
                                           description="Peripheral",
                                           meaning=HP["0030646"])
    LOWER_BODY_PREDOMINANCE = PermissibleValue(text="LOWER_BODY_PREDOMINANCE",
                                                                     description="Lower-body predominance",
                                                                     meaning=HP["0025291"])
    DIFFUSE = PermissibleValue(text="DIFFUSE",
                                     description="Diffuse",
                                     meaning=HP["0020034"])
    PROXIMAL = PermissibleValue(text="PROXIMAL",
                                       description="Proximal",
                                       meaning=HP["0012840"])
    APICAL = PermissibleValue(text="APICAL",
                                   description="Apical",
                                   meaning=HP["0033820"])
    FOCAL = PermissibleValue(text="FOCAL",
                                 description="Focal",
                                 meaning=HP["0030650"])
    MULTIFOCAL = PermissibleValue(text="MULTIFOCAL",
                                           description="Multifocal",
                                           meaning=HP["0030651"])
    JOINT_FLEXOR_SURFACE_LOCALIZATION = PermissibleValue(text="JOINT_FLEXOR_SURFACE_LOCALIZATION",
                                                                                         description="Jointflexorsurfacelocalization",
                                                                                         meaning=HP["0032540"])

    _defn = EnumDefinition(
        name="SpatialPatternTerms",
    )

class UnitTerms(EnumDefinitionImpl):

    DEGREE = PermissibleValue(text="DEGREE",
                                   description="degree (plane angle)",
                                   meaning=UCUM.degree)
    DIOPTER = PermissibleValue(text="DIOPTER",
                                     description="diopter",
                                     meaning=UCUM["%5Bdiop%5D"])
    GRAM = PermissibleValue(text="GRAM",
                               description="gram",
                               meaning=UCUM.g)
    GRAM_PER_KG = PermissibleValue(text="GRAM_PER_KG",
                                             description="gram per kilogram",
                                             meaning=UCUM["g/kg"])
    KILIGRAM = PermissibleValue(text="KILIGRAM",
                                       description="kiligram",
                                       meaning=UCUM.kg)
    LITER = PermissibleValue(text="LITER",
                                 description="liter",
                                 meaning=UCUM.L)
    METER = PermissibleValue(text="METER",
                                 description="meter",
                                 meaning=UCUM.m)
    MICROGRAM = PermissibleValue(text="MICROGRAM",
                                         description="microgram",
                                         meaning=UCUM.ug)
    MICROGRAM_PER_DECILITER = PermissibleValue(text="MICROGRAM_PER_DECILITER",
                                                                     description="microgram per deciliter",
                                                                     meaning=UCUM["ug/dL"])
    MICROGRAM_PER_LITER = PermissibleValue(text="MICROGRAM_PER_LITER",
                                                             description="microgram per liter",
                                                             meaning=UCUM["ug/L"])
    MICROLITER = PermissibleValue(text="MICROLITER",
                                           description="microliter",
                                           meaning=UCUM.uL)
    MICROMETER = PermissibleValue(text="MICROMETER",
                                           description="micrometer",
                                           meaning=UCUM.um)
    MILLIGRAM = PermissibleValue(text="MILLIGRAM",
                                         description="milligram",
                                         meaning=UCUM.mg)
    MILLIGRAM_PER_DAY = PermissibleValue(text="MILLIGRAM_PER_DAY",
                                                         description="milligram per day",
                                                         meaning=UCUM["mg/dL"])
    MILLIGRAM_PER_DL = PermissibleValue(text="MILLIGRAM_PER_DL",
                                                       description="milligram per deciliter",
                                                       meaning=UCUM["mg/dL"])
    MILLIGRAM_PER_KG = PermissibleValue(text="MILLIGRAM_PER_KG",
                                                       description="milligram per kilogram",
                                                       meaning=UCUM["mg.kg-1"])
    MILLILITER = PermissibleValue(text="MILLILITER",
                                           description="milliliter",
                                           meaning=UCUM.mL)
    MILLIMETER = PermissibleValue(text="MILLIMETER",
                                           description="millimeter",
                                           meaning=UCUM.mm)
    MILLIMETRES_OF_MERCURY = PermissibleValue(text="MILLIMETRES_OF_MERCURY",
                                                                   description="millimetres of mercury",
                                                                   meaning=UCUM["mm%5BHg%5D"])
    MILLIMOLE = PermissibleValue(text="MILLIMOLE",
                                         description="millimole",
                                         meaning=UCUM.mmol)
    MOLE = PermissibleValue(text="MOLE",
                               description="mole",
                               meaning=UCUM.mol)
    MOLE_PER_LITER = PermissibleValue(text="MOLE_PER_LITER",
                                                   description="mole per liter",
                                                   meaning=UCUM["mol/L"])
    MOLE_PER_MILLILITER = PermissibleValue(text="MOLE_PER_MILLILITER",
                                                             description="mole per milliliter",
                                                             meaning=UCUM["mol/mL"])
    ENZYME_UNIT_PER_LITER = PermissibleValue(text="ENZYME_UNIT_PER_LITER",
                                                                 description="enzyme unit per liter",
                                                                 meaning=UCUM["U/L"])

    _defn = EnumDefinition(
        name="UnitTerms",
    )

class MoleculeContext(EnumDefinitionImpl):

    genomic = PermissibleValue(text="genomic")
    protein = PermissibleValue(text="protein")
    transcript = PermissibleValue(text="transcript")
    unspecified_molecule_context = PermissibleValue(text="unspecified_molecule_context")

    _defn = EnumDefinition(
        name="MoleculeContext",
    )

# Slots
class slots:
    pass

slots.cohort__description = Slot(uri=PHENOPACKETS.description, name="cohort__description", curie=PHENOPACKETS.curie('description'),
                   model_uri=PHENOPACKETS.cohort__description, domain=None, range=Optional[str])

slots.cohort__files = Slot(uri=PHENOPACKETS.files, name="cohort__files", curie=PHENOPACKETS.curie('files'),
                   model_uri=PHENOPACKETS.cohort__files, domain=None, range=Optional[Union[Union[dict, File], list[Union[dict, File]]]])

slots.cohort__id = Slot(uri=PHENOPACKETS.id, name="cohort__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.cohort__id, domain=None, range=Optional[str])

slots.cohort__members = Slot(uri=PHENOPACKETS.members, name="cohort__members", curie=PHENOPACKETS.curie('members'),
                   model_uri=PHENOPACKETS.cohort__members, domain=None, range=Optional[Union[Union[dict, Phenopacket], list[Union[dict, Phenopacket]]]])

slots.cohort__metaData = Slot(uri=PHENOPACKETS.metaData, name="cohort__metaData", curie=PHENOPACKETS.curie('metaData'),
                   model_uri=PHENOPACKETS.cohort__metaData, domain=None, range=Union[dict, MetaData])

slots.family__consanguinousParents = Slot(uri=PHENOPACKETS.consanguinousParents, name="family__consanguinousParents", curie=PHENOPACKETS.curie('consanguinousParents'),
                   model_uri=PHENOPACKETS.family__consanguinousParents, domain=None, range=Optional[Union[bool, Bool]])

slots.family__files = Slot(uri=PHENOPACKETS.files, name="family__files", curie=PHENOPACKETS.curie('files'),
                   model_uri=PHENOPACKETS.family__files, domain=None, range=Optional[Union[Union[dict, File], list[Union[dict, File]]]])

slots.family__id = Slot(uri=PHENOPACKETS.id, name="family__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.family__id, domain=None, range=Optional[str])

slots.family__metaData = Slot(uri=PHENOPACKETS.metaData, name="family__metaData", curie=PHENOPACKETS.curie('metaData'),
                   model_uri=PHENOPACKETS.family__metaData, domain=None, range=Union[dict, MetaData])

slots.family__pedigree = Slot(uri=PHENOPACKETS.pedigree, name="family__pedigree", curie=PHENOPACKETS.curie('pedigree'),
                   model_uri=PHENOPACKETS.family__pedigree, domain=None, range=Optional[Union[dict, Pedigree]])

slots.family__proband = Slot(uri=PHENOPACKETS.proband, name="family__proband", curie=PHENOPACKETS.curie('proband'),
                   model_uri=PHENOPACKETS.family__proband, domain=None, range=Optional[Union[dict, Phenopacket]])

slots.family__relatives = Slot(uri=PHENOPACKETS.relatives, name="family__relatives", curie=PHENOPACKETS.curie('relatives'),
                   model_uri=PHENOPACKETS.family__relatives, domain=None, range=Optional[Union[Union[dict, Phenopacket], list[Union[dict, Phenopacket]]]])

slots.phenopacket__biosamples = Slot(uri=PHENOPACKETS.biosamples, name="phenopacket__biosamples", curie=PHENOPACKETS.curie('biosamples'),
                   model_uri=PHENOPACKETS.phenopacket__biosamples, domain=None, range=Optional[Union[Union[dict, Biosample], list[Union[dict, Biosample]]]])

slots.phenopacket__diseases = Slot(uri=PHENOPACKETS.diseases, name="phenopacket__diseases", curie=PHENOPACKETS.curie('diseases'),
                   model_uri=PHENOPACKETS.phenopacket__diseases, domain=None, range=Optional[Union[Union[dict, Disease], list[Union[dict, Disease]]]])

slots.phenopacket__files = Slot(uri=PHENOPACKETS.files, name="phenopacket__files", curie=PHENOPACKETS.curie('files'),
                   model_uri=PHENOPACKETS.phenopacket__files, domain=None, range=Optional[Union[Union[dict, File], list[Union[dict, File]]]])

slots.phenopacket__id = Slot(uri=PHENOPACKETS.id, name="phenopacket__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.phenopacket__id, domain=None, range=Optional[str])

slots.phenopacket__interpretations = Slot(uri=PHENOPACKETS.interpretations, name="phenopacket__interpretations", curie=PHENOPACKETS.curie('interpretations'),
                   model_uri=PHENOPACKETS.phenopacket__interpretations, domain=None, range=Optional[Union[Union[dict, Interpretation], list[Union[dict, Interpretation]]]])

slots.phenopacket__measurements = Slot(uri=PHENOPACKETS.measurements, name="phenopacket__measurements", curie=PHENOPACKETS.curie('measurements'),
                   model_uri=PHENOPACKETS.phenopacket__measurements, domain=None, range=Optional[Union[Union[dict, Measurement], list[Union[dict, Measurement]]]])

slots.phenopacket__medicalActions = Slot(uri=PHENOPACKETS.medicalActions, name="phenopacket__medicalActions", curie=PHENOPACKETS.curie('medicalActions'),
                   model_uri=PHENOPACKETS.phenopacket__medicalActions, domain=None, range=Optional[Union[Union[dict, MedicalAction], list[Union[dict, MedicalAction]]]])

slots.phenopacket__metaData = Slot(uri=PHENOPACKETS.metaData, name="phenopacket__metaData", curie=PHENOPACKETS.curie('metaData'),
                   model_uri=PHENOPACKETS.phenopacket__metaData, domain=None, range=Union[dict, MetaData])

slots.phenopacket__phenotypicFeatures = Slot(uri=PHENOPACKETS.phenotypicFeatures, name="phenopacket__phenotypicFeatures", curie=PHENOPACKETS.curie('phenotypicFeatures'),
                   model_uri=PHENOPACKETS.phenopacket__phenotypicFeatures, domain=None, range=Optional[Union[Union[dict, PhenotypicFeature], list[Union[dict, PhenotypicFeature]]]])

slots.phenopacket__subject = Slot(uri=PHENOPACKETS.subject, name="phenopacket__subject", curie=PHENOPACKETS.curie('subject'),
                   model_uri=PHENOPACKETS.phenopacket__subject, domain=None, range=Optional[Union[dict, Individual]])

slots.age__iso8601duration = Slot(uri=PHENOPACKETS.iso8601duration, name="age__iso8601duration", curie=PHENOPACKETS.curie('iso8601duration'),
                   model_uri=PHENOPACKETS.age__iso8601duration, domain=None, range=Optional[str])

slots.ageRange__end = Slot(uri=PHENOPACKETS.end, name="ageRange__end", curie=PHENOPACKETS.curie('end'),
                   model_uri=PHENOPACKETS.ageRange__end, domain=None, range=Optional[Union[dict, Age]])

slots.ageRange__start = Slot(uri=PHENOPACKETS.start, name="ageRange__start", curie=PHENOPACKETS.curie('start'),
                   model_uri=PHENOPACKETS.ageRange__start, domain=None, range=Optional[Union[dict, Age]])

slots.evidence__evidenceCode = Slot(uri=PHENOPACKETS.evidenceCode, name="evidence__evidenceCode", curie=PHENOPACKETS.curie('evidenceCode'),
                   model_uri=PHENOPACKETS.evidence__evidenceCode, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.evidence__reference = Slot(uri=PHENOPACKETS.reference, name="evidence__reference", curie=PHENOPACKETS.curie('reference'),
                   model_uri=PHENOPACKETS.evidence__reference, domain=None, range=Optional[Union[dict, ExternalReference]])

slots.externalReference__description = Slot(uri=PHENOPACKETS.description, name="externalReference__description", curie=PHENOPACKETS.curie('description'),
                   model_uri=PHENOPACKETS.externalReference__description, domain=None, range=Optional[str])

slots.externalReference__id = Slot(uri=PHENOPACKETS.id, name="externalReference__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.externalReference__id, domain=None, range=Optional[str])

slots.externalReference__reference = Slot(uri=PHENOPACKETS.reference, name="externalReference__reference", curie=PHENOPACKETS.curie('reference'),
                   model_uri=PHENOPACKETS.externalReference__reference, domain=None, range=Optional[str])

slots.file__fileAttributes = Slot(uri=PHENOPACKETS.fileAttributes, name="file__fileAttributes", curie=PHENOPACKETS.curie('fileAttributes'),
                   model_uri=PHENOPACKETS.file__fileAttributes, domain=None, range=Optional[Union[dict, Dictionary]])

slots.file__individualToFileIdentifiers = Slot(uri=PHENOPACKETS.individualToFileIdentifiers, name="file__individualToFileIdentifiers", curie=PHENOPACKETS.curie('individualToFileIdentifiers'),
                   model_uri=PHENOPACKETS.file__individualToFileIdentifiers, domain=None, range=Optional[Union[dict, Dictionary]])

slots.file__uri = Slot(uri=PHENOPACKETS.uri, name="file__uri", curie=PHENOPACKETS.curie('uri'),
                   model_uri=PHENOPACKETS.file__uri, domain=None, range=Optional[str])

slots.gestationalAge__days = Slot(uri=PHENOPACKETS.days, name="gestationalAge__days", curie=PHENOPACKETS.curie('days'),
                   model_uri=PHENOPACKETS.gestationalAge__days, domain=None, range=Optional[int])

slots.gestationalAge__weeks = Slot(uri=PHENOPACKETS.weeks, name="gestationalAge__weeks", curie=PHENOPACKETS.curie('weeks'),
                   model_uri=PHENOPACKETS.gestationalAge__weeks, domain=None, range=Optional[int])

slots.ontologyClass__id = Slot(uri=PHENOPACKETS.id, name="ontologyClass__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.ontologyClass__id, domain=None, range=URIRef)

slots.ontologyClass__label = Slot(uri=PHENOPACKETS.label, name="ontologyClass__label", curie=PHENOPACKETS.curie('label'),
                   model_uri=PHENOPACKETS.ontologyClass__label, domain=None, range=Optional[str])

slots.procedure__bodySite = Slot(uri=PHENOPACKETS.bodySite, name="procedure__bodySite", curie=PHENOPACKETS.curie('bodySite'),
                   model_uri=PHENOPACKETS.procedure__bodySite, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.procedure__code = Slot(uri=PHENOPACKETS.code, name="procedure__code", curie=PHENOPACKETS.curie('code'),
                   model_uri=PHENOPACKETS.procedure__code, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.procedure__performed = Slot(uri=PHENOPACKETS.performed, name="procedure__performed", curie=PHENOPACKETS.curie('performed'),
                   model_uri=PHENOPACKETS.procedure__performed, domain=None, range=Optional[Union[dict, TimeElement]])

slots.timeElement__age = Slot(uri=PHENOPACKETS.age, name="timeElement__age", curie=PHENOPACKETS.curie('age'),
                   model_uri=PHENOPACKETS.timeElement__age, domain=None, range=Optional[Union[dict, Age]])

slots.timeElement__ageRange = Slot(uri=PHENOPACKETS.ageRange, name="timeElement__ageRange", curie=PHENOPACKETS.curie('ageRange'),
                   model_uri=PHENOPACKETS.timeElement__ageRange, domain=None, range=Optional[Union[dict, AgeRange]])

slots.timeElement__gestationalAge = Slot(uri=PHENOPACKETS.gestationalAge, name="timeElement__gestationalAge", curie=PHENOPACKETS.curie('gestationalAge'),
                   model_uri=PHENOPACKETS.timeElement__gestationalAge, domain=None, range=Optional[Union[dict, GestationalAge]])

slots.timeElement__interval = Slot(uri=PHENOPACKETS.interval, name="timeElement__interval", curie=PHENOPACKETS.curie('interval'),
                   model_uri=PHENOPACKETS.timeElement__interval, domain=None, range=Optional[Union[dict, TimeInterval]])

slots.timeElement__ontologyClass = Slot(uri=PHENOPACKETS.ontologyClass, name="timeElement__ontologyClass", curie=PHENOPACKETS.curie('ontologyClass'),
                   model_uri=PHENOPACKETS.timeElement__ontologyClass, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.timeElement__timestamp = Slot(uri=PHENOPACKETS.timestamp, name="timeElement__timestamp", curie=PHENOPACKETS.curie('timestamp'),
                   model_uri=PHENOPACKETS.timeElement__timestamp, domain=None, range=Optional[str])

slots.timeInterval__end = Slot(uri=PHENOPACKETS.end, name="timeInterval__end", curie=PHENOPACKETS.curie('end'),
                   model_uri=PHENOPACKETS.timeInterval__end, domain=None, range=Optional[str])

slots.timeInterval__start = Slot(uri=PHENOPACKETS.start, name="timeInterval__start", curie=PHENOPACKETS.curie('start'),
                   model_uri=PHENOPACKETS.timeInterval__start, domain=None, range=Optional[str])

slots.biosample__derivedFromId = Slot(uri=PHENOPACKETS.derivedFromId, name="biosample__derivedFromId", curie=PHENOPACKETS.curie('derivedFromId'),
                   model_uri=PHENOPACKETS.biosample__derivedFromId, domain=None, range=Optional[str])

slots.biosample__description = Slot(uri=PHENOPACKETS.description, name="biosample__description", curie=PHENOPACKETS.curie('description'),
                   model_uri=PHENOPACKETS.biosample__description, domain=None, range=Optional[str])

slots.biosample__diagnosticMarkers = Slot(uri=PHENOPACKETS.diagnosticMarkers, name="biosample__diagnosticMarkers", curie=PHENOPACKETS.curie('diagnosticMarkers'),
                   model_uri=PHENOPACKETS.biosample__diagnosticMarkers, domain=None, range=Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]])

slots.biosample__files = Slot(uri=PHENOPACKETS.files, name="biosample__files", curie=PHENOPACKETS.curie('files'),
                   model_uri=PHENOPACKETS.biosample__files, domain=None, range=Optional[Union[Union[dict, File], list[Union[dict, File]]]])

slots.biosample__histologicalDiagnosis = Slot(uri=PHENOPACKETS.histologicalDiagnosis, name="biosample__histologicalDiagnosis", curie=PHENOPACKETS.curie('histologicalDiagnosis'),
                   model_uri=PHENOPACKETS.biosample__histologicalDiagnosis, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__id = Slot(uri=PHENOPACKETS.id, name="biosample__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.biosample__id, domain=None, range=Optional[str])

slots.biosample__individualId = Slot(uri=PHENOPACKETS.individualId, name="biosample__individualId", curie=PHENOPACKETS.curie('individualId'),
                   model_uri=PHENOPACKETS.biosample__individualId, domain=None, range=Optional[str])

slots.biosample__materialSample = Slot(uri=PHENOPACKETS.materialSample, name="biosample__materialSample", curie=PHENOPACKETS.curie('materialSample'),
                   model_uri=PHENOPACKETS.biosample__materialSample, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__measurements = Slot(uri=PHENOPACKETS.measurements, name="biosample__measurements", curie=PHENOPACKETS.curie('measurements'),
                   model_uri=PHENOPACKETS.biosample__measurements, domain=None, range=Optional[Union[Union[dict, Measurement], list[Union[dict, Measurement]]]])

slots.biosample__pathologicalStage = Slot(uri=PHENOPACKETS.pathologicalStage, name="biosample__pathologicalStage", curie=PHENOPACKETS.curie('pathologicalStage'),
                   model_uri=PHENOPACKETS.biosample__pathologicalStage, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__pathologicalTnmFinding = Slot(uri=PHENOPACKETS.pathologicalTnmFinding, name="biosample__pathologicalTnmFinding", curie=PHENOPACKETS.curie('pathologicalTnmFinding'),
                   model_uri=PHENOPACKETS.biosample__pathologicalTnmFinding, domain=None, range=Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]])

slots.biosample__phenotypicFeatures = Slot(uri=PHENOPACKETS.phenotypicFeatures, name="biosample__phenotypicFeatures", curie=PHENOPACKETS.curie('phenotypicFeatures'),
                   model_uri=PHENOPACKETS.biosample__phenotypicFeatures, domain=None, range=Optional[Union[Union[dict, PhenotypicFeature], list[Union[dict, PhenotypicFeature]]]])

slots.biosample__procedure = Slot(uri=PHENOPACKETS.procedure, name="biosample__procedure", curie=PHENOPACKETS.curie('procedure'),
                   model_uri=PHENOPACKETS.biosample__procedure, domain=None, range=Optional[Union[dict, Procedure]])

slots.biosample__sampleProcessing = Slot(uri=PHENOPACKETS.sampleProcessing, name="biosample__sampleProcessing", curie=PHENOPACKETS.curie('sampleProcessing'),
                   model_uri=PHENOPACKETS.biosample__sampleProcessing, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__sampleStorage = Slot(uri=PHENOPACKETS.sampleStorage, name="biosample__sampleStorage", curie=PHENOPACKETS.curie('sampleStorage'),
                   model_uri=PHENOPACKETS.biosample__sampleStorage, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__sampleType = Slot(uri=PHENOPACKETS.sampleType, name="biosample__sampleType", curie=PHENOPACKETS.curie('sampleType'),
                   model_uri=PHENOPACKETS.biosample__sampleType, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__sampledTissue = Slot(uri=PHENOPACKETS.sampledTissue, name="biosample__sampledTissue", curie=PHENOPACKETS.curie('sampledTissue'),
                   model_uri=PHENOPACKETS.biosample__sampledTissue, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__taxonomy = Slot(uri=PHENOPACKETS.taxonomy, name="biosample__taxonomy", curie=PHENOPACKETS.curie('taxonomy'),
                   model_uri=PHENOPACKETS.biosample__taxonomy, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__timeOfCollection = Slot(uri=PHENOPACKETS.timeOfCollection, name="biosample__timeOfCollection", curie=PHENOPACKETS.curie('timeOfCollection'),
                   model_uri=PHENOPACKETS.biosample__timeOfCollection, domain=None, range=Optional[Union[dict, TimeElement]])

slots.biosample__tumorGrade = Slot(uri=PHENOPACKETS.tumorGrade, name="biosample__tumorGrade", curie=PHENOPACKETS.curie('tumorGrade'),
                   model_uri=PHENOPACKETS.biosample__tumorGrade, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.biosample__tumorProgression = Slot(uri=PHENOPACKETS.tumorProgression, name="biosample__tumorProgression", curie=PHENOPACKETS.curie('tumorProgression'),
                   model_uri=PHENOPACKETS.biosample__tumorProgression, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.disease__clinicalTnmFinding = Slot(uri=PHENOPACKETS.clinicalTnmFinding, name="disease__clinicalTnmFinding", curie=PHENOPACKETS.curie('clinicalTnmFinding'),
                   model_uri=PHENOPACKETS.disease__clinicalTnmFinding, domain=None, range=Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]])

slots.disease__diseaseStage = Slot(uri=PHENOPACKETS.diseaseStage, name="disease__diseaseStage", curie=PHENOPACKETS.curie('diseaseStage'),
                   model_uri=PHENOPACKETS.disease__diseaseStage, domain=None, range=Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]])

slots.disease__excluded = Slot(uri=PHENOPACKETS.excluded, name="disease__excluded", curie=PHENOPACKETS.curie('excluded'),
                   model_uri=PHENOPACKETS.disease__excluded, domain=None, range=Optional[Union[bool, Bool]])

slots.disease__laterality = Slot(uri=PHENOPACKETS.laterality, name="disease__laterality", curie=PHENOPACKETS.curie('laterality'),
                   model_uri=PHENOPACKETS.disease__laterality, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.disease__onset = Slot(uri=PHENOPACKETS.onset, name="disease__onset", curie=PHENOPACKETS.curie('onset'),
                   model_uri=PHENOPACKETS.disease__onset, domain=None, range=Optional[Union[dict, TimeElement]])

slots.disease__primarySite = Slot(uri=PHENOPACKETS.primarySite, name="disease__primarySite", curie=PHENOPACKETS.curie('primarySite'),
                   model_uri=PHENOPACKETS.disease__primarySite, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.disease__resolution = Slot(uri=PHENOPACKETS.resolution, name="disease__resolution", curie=PHENOPACKETS.curie('resolution'),
                   model_uri=PHENOPACKETS.disease__resolution, domain=None, range=Optional[Union[dict, TimeElement]])

slots.disease__term = Slot(uri=PHENOPACKETS.term, name="disease__term", curie=PHENOPACKETS.curie('term'),
                   model_uri=PHENOPACKETS.disease__term, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.diagnosis__disease = Slot(uri=PHENOPACKETS.disease, name="diagnosis__disease", curie=PHENOPACKETS.curie('disease'),
                   model_uri=PHENOPACKETS.diagnosis__disease, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.diagnosis__genomicInterpretations = Slot(uri=PHENOPACKETS.genomicInterpretations, name="diagnosis__genomicInterpretations", curie=PHENOPACKETS.curie('genomicInterpretations'),
                   model_uri=PHENOPACKETS.diagnosis__genomicInterpretations, domain=None, range=Optional[Union[Union[dict, GenomicInterpretation], list[Union[dict, GenomicInterpretation]]]])

slots.genomicInterpretation__gene = Slot(uri=PHENOPACKETS.gene, name="genomicInterpretation__gene", curie=PHENOPACKETS.curie('gene'),
                   model_uri=PHENOPACKETS.genomicInterpretation__gene, domain=None, range=Optional[Union[dict, GeneDescriptor]])

slots.genomicInterpretation__interpretationStatus = Slot(uri=PHENOPACKETS.interpretationStatus, name="genomicInterpretation__interpretationStatus", curie=PHENOPACKETS.curie('interpretationStatus'),
                   model_uri=PHENOPACKETS.genomicInterpretation__interpretationStatus, domain=None, range=Optional[Union[str, "InterpretationStatus"]])

slots.genomicInterpretation__subjectOrBiosampleId = Slot(uri=PHENOPACKETS.subjectOrBiosampleId, name="genomicInterpretation__subjectOrBiosampleId", curie=PHENOPACKETS.curie('subjectOrBiosampleId'),
                   model_uri=PHENOPACKETS.genomicInterpretation__subjectOrBiosampleId, domain=None, range=Optional[str])

slots.genomicInterpretation__variantInterpretation = Slot(uri=PHENOPACKETS.variantInterpretation, name="genomicInterpretation__variantInterpretation", curie=PHENOPACKETS.curie('variantInterpretation'),
                   model_uri=PHENOPACKETS.genomicInterpretation__variantInterpretation, domain=None, range=Optional[Union[dict, VariantInterpretation]])

slots.interpretation__diagnosis = Slot(uri=PHENOPACKETS.diagnosis, name="interpretation__diagnosis", curie=PHENOPACKETS.curie('diagnosis'),
                   model_uri=PHENOPACKETS.interpretation__diagnosis, domain=None, range=Optional[Union[dict, Diagnosis]])

slots.interpretation__id = Slot(uri=PHENOPACKETS.id, name="interpretation__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.interpretation__id, domain=None, range=Optional[str])

slots.interpretation__progressStatus = Slot(uri=PHENOPACKETS.progressStatus, name="interpretation__progressStatus", curie=PHENOPACKETS.curie('progressStatus'),
                   model_uri=PHENOPACKETS.interpretation__progressStatus, domain=None, range=Optional[Union[str, "ProgressStatus"]])

slots.interpretation__summary = Slot(uri=PHENOPACKETS.summary, name="interpretation__summary", curie=PHENOPACKETS.curie('summary'),
                   model_uri=PHENOPACKETS.interpretation__summary, domain=None, range=Optional[str])

slots.variantInterpretation__acmgPathogenicityClassification = Slot(uri=PHENOPACKETS.acmgPathogenicityClassification, name="variantInterpretation__acmgPathogenicityClassification", curie=PHENOPACKETS.curie('acmgPathogenicityClassification'),
                   model_uri=PHENOPACKETS.variantInterpretation__acmgPathogenicityClassification, domain=None, range=Optional[Union[str, "AcmgPathogenicityClassification"]])

slots.variantInterpretation__therapeuticActionability = Slot(uri=PHENOPACKETS.therapeuticActionability, name="variantInterpretation__therapeuticActionability", curie=PHENOPACKETS.curie('therapeuticActionability'),
                   model_uri=PHENOPACKETS.variantInterpretation__therapeuticActionability, domain=None, range=Optional[Union[str, "TherapeuticActionability"]])

slots.variantInterpretation__variationDescriptor = Slot(uri=PHENOPACKETS.variationDescriptor, name="variantInterpretation__variationDescriptor", curie=PHENOPACKETS.curie('variationDescriptor'),
                   model_uri=PHENOPACKETS.variantInterpretation__variationDescriptor, domain=None, range=Optional[Union[dict, VariationDescriptor]])

slots.individual__alternateIds = Slot(uri=PHENOPACKETS.alternateIds, name="individual__alternateIds", curie=PHENOPACKETS.curie('alternateIds'),
                   model_uri=PHENOPACKETS.individual__alternateIds, domain=None, range=Optional[Union[str, list[str]]])

slots.individual__dateOfBirth = Slot(uri=PHENOPACKETS.dateOfBirth, name="individual__dateOfBirth", curie=PHENOPACKETS.curie('dateOfBirth'),
                   model_uri=PHENOPACKETS.individual__dateOfBirth, domain=None, range=Optional[str])

slots.individual__gender = Slot(uri=PHENOPACKETS.gender, name="individual__gender", curie=PHENOPACKETS.curie('gender'),
                   model_uri=PHENOPACKETS.individual__gender, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.individual__id = Slot(uri=PHENOPACKETS.id, name="individual__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.individual__id, domain=None, range=Optional[str])

slots.individual__karyotypicSex = Slot(uri=PHENOPACKETS.karyotypicSex, name="individual__karyotypicSex", curie=PHENOPACKETS.curie('karyotypicSex'),
                   model_uri=PHENOPACKETS.individual__karyotypicSex, domain=None, range=Optional[Union[str, "KaryotypicSex"]])

slots.individual__sex = Slot(uri=PHENOPACKETS.sex, name="individual__sex", curie=PHENOPACKETS.curie('sex'),
                   model_uri=PHENOPACKETS.individual__sex, domain=None, range=Optional[Union[str, "Sex"]])

slots.individual__taxonomy = Slot(uri=PHENOPACKETS.taxonomy, name="individual__taxonomy", curie=PHENOPACKETS.curie('taxonomy'),
                   model_uri=PHENOPACKETS.individual__taxonomy, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.individual__timeAtLastEncounter = Slot(uri=PHENOPACKETS.timeAtLastEncounter, name="individual__timeAtLastEncounter", curie=PHENOPACKETS.curie('timeAtLastEncounter'),
                   model_uri=PHENOPACKETS.individual__timeAtLastEncounter, domain=None, range=Optional[Union[dict, TimeElement]])

slots.individual__vitalStatus = Slot(uri=PHENOPACKETS.vitalStatus, name="individual__vitalStatus", curie=PHENOPACKETS.curie('vitalStatus'),
                   model_uri=PHENOPACKETS.individual__vitalStatus, domain=None, range=Optional[Union[dict, VitalStatus]])

slots.vitalStatus__causeOfDeath = Slot(uri=PHENOPACKETS.causeOfDeath, name="vitalStatus__causeOfDeath", curie=PHENOPACKETS.curie('causeOfDeath'),
                   model_uri=PHENOPACKETS.vitalStatus__causeOfDeath, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.vitalStatus__status = Slot(uri=PHENOPACKETS.status, name="vitalStatus__status", curie=PHENOPACKETS.curie('status'),
                   model_uri=PHENOPACKETS.vitalStatus__status, domain=None, range=Optional[Union[str, "Status"]])

slots.vitalStatus__survivalTimeInDays = Slot(uri=PHENOPACKETS.survivalTimeInDays, name="vitalStatus__survivalTimeInDays", curie=PHENOPACKETS.curie('survivalTimeInDays'),
                   model_uri=PHENOPACKETS.vitalStatus__survivalTimeInDays, domain=None, range=Optional[int])

slots.vitalStatus__timeOfDeath = Slot(uri=PHENOPACKETS.timeOfDeath, name="vitalStatus__timeOfDeath", curie=PHENOPACKETS.curie('timeOfDeath'),
                   model_uri=PHENOPACKETS.vitalStatus__timeOfDeath, domain=None, range=Optional[Union[dict, TimeElement]])

slots.complexValue__typedQuantities = Slot(uri=PHENOPACKETS.typedQuantities, name="complexValue__typedQuantities", curie=PHENOPACKETS.curie('typedQuantities'),
                   model_uri=PHENOPACKETS.complexValue__typedQuantities, domain=None, range=Optional[Union[Union[dict, TypedQuantity], list[Union[dict, TypedQuantity]]]])

slots.measurement__assay = Slot(uri=PHENOPACKETS.assay, name="measurement__assay", curie=PHENOPACKETS.curie('assay'),
                   model_uri=PHENOPACKETS.measurement__assay, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.measurement__complexValue = Slot(uri=PHENOPACKETS.complexValue, name="measurement__complexValue", curie=PHENOPACKETS.curie('complexValue'),
                   model_uri=PHENOPACKETS.measurement__complexValue, domain=None, range=Optional[Union[dict, ComplexValue]])

slots.measurement__description = Slot(uri=PHENOPACKETS.description, name="measurement__description", curie=PHENOPACKETS.curie('description'),
                   model_uri=PHENOPACKETS.measurement__description, domain=None, range=Optional[str])

slots.measurement__procedure = Slot(uri=PHENOPACKETS.procedure, name="measurement__procedure", curie=PHENOPACKETS.curie('procedure'),
                   model_uri=PHENOPACKETS.measurement__procedure, domain=None, range=Optional[Union[dict, Procedure]])

slots.measurement__timeObserved = Slot(uri=PHENOPACKETS.timeObserved, name="measurement__timeObserved", curie=PHENOPACKETS.curie('timeObserved'),
                   model_uri=PHENOPACKETS.measurement__timeObserved, domain=None, range=Optional[Union[dict, TimeElement]])

slots.measurement__value = Slot(uri=PHENOPACKETS.value, name="measurement__value", curie=PHENOPACKETS.curie('value'),
                   model_uri=PHENOPACKETS.measurement__value, domain=None, range=Optional[Union[dict, Value]])

slots.quantity__referenceRange = Slot(uri=PHENOPACKETS.referenceRange, name="quantity__referenceRange", curie=PHENOPACKETS.curie('referenceRange'),
                   model_uri=PHENOPACKETS.quantity__referenceRange, domain=None, range=Optional[Union[dict, ReferenceRange]])

slots.quantity__unit = Slot(uri=PHENOPACKETS.unit, name="quantity__unit", curie=PHENOPACKETS.curie('unit'),
                   model_uri=PHENOPACKETS.quantity__unit, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.quantity__value = Slot(uri=PHENOPACKETS.value, name="quantity__value", curie=PHENOPACKETS.curie('value'),
                   model_uri=PHENOPACKETS.quantity__value, domain=None, range=Optional[float])

slots.referenceRange__high = Slot(uri=PHENOPACKETS.high, name="referenceRange__high", curie=PHENOPACKETS.curie('high'),
                   model_uri=PHENOPACKETS.referenceRange__high, domain=None, range=Optional[float])

slots.referenceRange__low = Slot(uri=PHENOPACKETS.low, name="referenceRange__low", curie=PHENOPACKETS.curie('low'),
                   model_uri=PHENOPACKETS.referenceRange__low, domain=None, range=Optional[float])

slots.referenceRange__unit = Slot(uri=PHENOPACKETS.unit, name="referenceRange__unit", curie=PHENOPACKETS.curie('unit'),
                   model_uri=PHENOPACKETS.referenceRange__unit, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.typedQuantity__quantity = Slot(uri=PHENOPACKETS.quantity, name="typedQuantity__quantity", curie=PHENOPACKETS.curie('quantity'),
                   model_uri=PHENOPACKETS.typedQuantity__quantity, domain=None, range=Optional[Union[dict, Quantity]])

slots.typedQuantity__type = Slot(uri=PHENOPACKETS.type, name="typedQuantity__type", curie=PHENOPACKETS.curie('type'),
                   model_uri=PHENOPACKETS.typedQuantity__type, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.value__ontologyClass = Slot(uri=PHENOPACKETS.ontologyClass, name="value__ontologyClass", curie=PHENOPACKETS.curie('ontologyClass'),
                   model_uri=PHENOPACKETS.value__ontologyClass, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.value__quantity = Slot(uri=PHENOPACKETS.quantity, name="value__quantity", curie=PHENOPACKETS.curie('quantity'),
                   model_uri=PHENOPACKETS.value__quantity, domain=None, range=Optional[Union[dict, Quantity]])

slots.doseInterval__interval = Slot(uri=PHENOPACKETS.interval, name="doseInterval__interval", curie=PHENOPACKETS.curie('interval'),
                   model_uri=PHENOPACKETS.doseInterval__interval, domain=None, range=Optional[Union[dict, TimeInterval]])

slots.doseInterval__quantity = Slot(uri=PHENOPACKETS.quantity, name="doseInterval__quantity", curie=PHENOPACKETS.curie('quantity'),
                   model_uri=PHENOPACKETS.doseInterval__quantity, domain=None, range=Optional[Union[dict, Quantity]])

slots.doseInterval__scheduleFrequency = Slot(uri=PHENOPACKETS.scheduleFrequency, name="doseInterval__scheduleFrequency", curie=PHENOPACKETS.curie('scheduleFrequency'),
                   model_uri=PHENOPACKETS.doseInterval__scheduleFrequency, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.medicalAction__adverseEvents = Slot(uri=PHENOPACKETS.adverseEvents, name="medicalAction__adverseEvents", curie=PHENOPACKETS.curie('adverseEvents'),
                   model_uri=PHENOPACKETS.medicalAction__adverseEvents, domain=None, range=Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]])

slots.medicalAction__procedure = Slot(uri=PHENOPACKETS.procedure, name="medicalAction__procedure", curie=PHENOPACKETS.curie('procedure'),
                   model_uri=PHENOPACKETS.medicalAction__procedure, domain=None, range=Optional[Union[dict, Procedure]])

slots.medicalAction__radiationTherapy = Slot(uri=PHENOPACKETS.radiationTherapy, name="medicalAction__radiationTherapy", curie=PHENOPACKETS.curie('radiationTherapy'),
                   model_uri=PHENOPACKETS.medicalAction__radiationTherapy, domain=None, range=Optional[Union[dict, RadiationTherapy]])

slots.medicalAction__responseToTreatment = Slot(uri=PHENOPACKETS.responseToTreatment, name="medicalAction__responseToTreatment", curie=PHENOPACKETS.curie('responseToTreatment'),
                   model_uri=PHENOPACKETS.medicalAction__responseToTreatment, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.medicalAction__therapeuticRegimen = Slot(uri=PHENOPACKETS.therapeuticRegimen, name="medicalAction__therapeuticRegimen", curie=PHENOPACKETS.curie('therapeuticRegimen'),
                   model_uri=PHENOPACKETS.medicalAction__therapeuticRegimen, domain=None, range=Optional[Union[dict, TherapeuticRegimen]])

slots.medicalAction__treatment = Slot(uri=PHENOPACKETS.treatment, name="medicalAction__treatment", curie=PHENOPACKETS.curie('treatment'),
                   model_uri=PHENOPACKETS.medicalAction__treatment, domain=None, range=Optional[Union[dict, Treatment]])

slots.medicalAction__treatmentIntent = Slot(uri=PHENOPACKETS.treatmentIntent, name="medicalAction__treatmentIntent", curie=PHENOPACKETS.curie('treatmentIntent'),
                   model_uri=PHENOPACKETS.medicalAction__treatmentIntent, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.medicalAction__treatmentTarget = Slot(uri=PHENOPACKETS.treatmentTarget, name="medicalAction__treatmentTarget", curie=PHENOPACKETS.curie('treatmentTarget'),
                   model_uri=PHENOPACKETS.medicalAction__treatmentTarget, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.medicalAction__treatmentTerminationReason = Slot(uri=PHENOPACKETS.treatmentTerminationReason, name="medicalAction__treatmentTerminationReason", curie=PHENOPACKETS.curie('treatmentTerminationReason'),
                   model_uri=PHENOPACKETS.medicalAction__treatmentTerminationReason, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.radiationTherapy__bodySite = Slot(uri=PHENOPACKETS.bodySite, name="radiationTherapy__bodySite", curie=PHENOPACKETS.curie('bodySite'),
                   model_uri=PHENOPACKETS.radiationTherapy__bodySite, domain=None, range=Union[dict, OntologyClass])

slots.radiationTherapy__dosage = Slot(uri=PHENOPACKETS.dosage, name="radiationTherapy__dosage", curie=PHENOPACKETS.curie('dosage'),
                   model_uri=PHENOPACKETS.radiationTherapy__dosage, domain=None, range=int)

slots.radiationTherapy__fractions = Slot(uri=PHENOPACKETS.fractions, name="radiationTherapy__fractions", curie=PHENOPACKETS.curie('fractions'),
                   model_uri=PHENOPACKETS.radiationTherapy__fractions, domain=None, range=int)

slots.radiationTherapy__modality = Slot(uri=PHENOPACKETS.modality, name="radiationTherapy__modality", curie=PHENOPACKETS.curie('modality'),
                   model_uri=PHENOPACKETS.radiationTherapy__modality, domain=None, range=Union[dict, OntologyClass])

slots.therapeuticRegimen__endTime = Slot(uri=PHENOPACKETS.endTime, name="therapeuticRegimen__endTime", curie=PHENOPACKETS.curie('endTime'),
                   model_uri=PHENOPACKETS.therapeuticRegimen__endTime, domain=None, range=Optional[Union[dict, TimeElement]])

slots.therapeuticRegimen__externalReference = Slot(uri=PHENOPACKETS.externalReference, name="therapeuticRegimen__externalReference", curie=PHENOPACKETS.curie('externalReference'),
                   model_uri=PHENOPACKETS.therapeuticRegimen__externalReference, domain=None, range=Optional[Union[dict, ExternalReference]])

slots.therapeuticRegimen__ontologyClass = Slot(uri=PHENOPACKETS.ontologyClass, name="therapeuticRegimen__ontologyClass", curie=PHENOPACKETS.curie('ontologyClass'),
                   model_uri=PHENOPACKETS.therapeuticRegimen__ontologyClass, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.therapeuticRegimen__regimenStatus = Slot(uri=PHENOPACKETS.regimenStatus, name="therapeuticRegimen__regimenStatus", curie=PHENOPACKETS.curie('regimenStatus'),
                   model_uri=PHENOPACKETS.therapeuticRegimen__regimenStatus, domain=None, range=Optional[Union[str, "RegimenStatus"]])

slots.therapeuticRegimen__startTime = Slot(uri=PHENOPACKETS.startTime, name="therapeuticRegimen__startTime", curie=PHENOPACKETS.curie('startTime'),
                   model_uri=PHENOPACKETS.therapeuticRegimen__startTime, domain=None, range=Optional[Union[dict, TimeElement]])

slots.treatment__agent = Slot(uri=PHENOPACKETS.agent, name="treatment__agent", curie=PHENOPACKETS.curie('agent'),
                   model_uri=PHENOPACKETS.treatment__agent, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.treatment__cumulativeDose = Slot(uri=PHENOPACKETS.cumulativeDose, name="treatment__cumulativeDose", curie=PHENOPACKETS.curie('cumulativeDose'),
                   model_uri=PHENOPACKETS.treatment__cumulativeDose, domain=None, range=Optional[Union[dict, Quantity]])

slots.treatment__doseIntervals = Slot(uri=PHENOPACKETS.doseIntervals, name="treatment__doseIntervals", curie=PHENOPACKETS.curie('doseIntervals'),
                   model_uri=PHENOPACKETS.treatment__doseIntervals, domain=None, range=Optional[Union[Union[dict, DoseInterval], list[Union[dict, DoseInterval]]]])

slots.treatment__drugType = Slot(uri=PHENOPACKETS.drugType, name="treatment__drugType", curie=PHENOPACKETS.curie('drugType'),
                   model_uri=PHENOPACKETS.treatment__drugType, domain=None, range=Optional[Union[str, "DrugType"]])

slots.treatment__routeOfAdministration = Slot(uri=PHENOPACKETS.routeOfAdministration, name="treatment__routeOfAdministration", curie=PHENOPACKETS.curie('routeOfAdministration'),
                   model_uri=PHENOPACKETS.treatment__routeOfAdministration, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.metaData__created = Slot(uri=PHENOPACKETS.created, name="metaData__created", curie=PHENOPACKETS.curie('created'),
                   model_uri=PHENOPACKETS.metaData__created, domain=None, range=Optional[str])

slots.metaData__createdBy = Slot(uri=PHENOPACKETS.createdBy, name="metaData__createdBy", curie=PHENOPACKETS.curie('createdBy'),
                   model_uri=PHENOPACKETS.metaData__createdBy, domain=None, range=Optional[str])

slots.metaData__externalReferences = Slot(uri=PHENOPACKETS.externalReferences, name="metaData__externalReferences", curie=PHENOPACKETS.curie('externalReferences'),
                   model_uri=PHENOPACKETS.metaData__externalReferences, domain=None, range=Optional[Union[Union[dict, ExternalReference], list[Union[dict, ExternalReference]]]])

slots.metaData__phenopacketSchemaVersion = Slot(uri=PHENOPACKETS.phenopacketSchemaVersion, name="metaData__phenopacketSchemaVersion", curie=PHENOPACKETS.curie('phenopacketSchemaVersion'),
                   model_uri=PHENOPACKETS.metaData__phenopacketSchemaVersion, domain=None, range=Optional[str])

slots.metaData__resources = Slot(uri=PHENOPACKETS.resources, name="metaData__resources", curie=PHENOPACKETS.curie('resources'),
                   model_uri=PHENOPACKETS.metaData__resources, domain=None, range=Optional[Union[Union[dict, Resource], list[Union[dict, Resource]]]])

slots.metaData__submittedBy = Slot(uri=PHENOPACKETS.submittedBy, name="metaData__submittedBy", curie=PHENOPACKETS.curie('submittedBy'),
                   model_uri=PHENOPACKETS.metaData__submittedBy, domain=None, range=Optional[str])

slots.metaData__updates = Slot(uri=PHENOPACKETS.updates, name="metaData__updates", curie=PHENOPACKETS.curie('updates'),
                   model_uri=PHENOPACKETS.metaData__updates, domain=None, range=Optional[Union[Union[dict, Update], list[Union[dict, Update]]]])

slots.resource__id = Slot(uri=PHENOPACKETS.id, name="resource__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.resource__id, domain=None, range=Optional[str])

slots.resource__iriPrefix = Slot(uri=PHENOPACKETS.iriPrefix, name="resource__iriPrefix", curie=PHENOPACKETS.curie('iriPrefix'),
                   model_uri=PHENOPACKETS.resource__iriPrefix, domain=None, range=Optional[str])

slots.resource__name = Slot(uri=PHENOPACKETS.name, name="resource__name", curie=PHENOPACKETS.curie('name'),
                   model_uri=PHENOPACKETS.resource__name, domain=None, range=Optional[str])

slots.resource__namespacePrefix = Slot(uri=PHENOPACKETS.namespacePrefix, name="resource__namespacePrefix", curie=PHENOPACKETS.curie('namespacePrefix'),
                   model_uri=PHENOPACKETS.resource__namespacePrefix, domain=None, range=Optional[str])

slots.resource__url = Slot(uri=PHENOPACKETS.url, name="resource__url", curie=PHENOPACKETS.curie('url'),
                   model_uri=PHENOPACKETS.resource__url, domain=None, range=Optional[str])

slots.resource__version = Slot(uri=PHENOPACKETS.version, name="resource__version", curie=PHENOPACKETS.curie('version'),
                   model_uri=PHENOPACKETS.resource__version, domain=None, range=Optional[str])

slots.update__comment = Slot(uri=PHENOPACKETS.comment, name="update__comment", curie=PHENOPACKETS.curie('comment'),
                   model_uri=PHENOPACKETS.update__comment, domain=None, range=Optional[str])

slots.update__timestamp = Slot(uri=PHENOPACKETS.timestamp, name="update__timestamp", curie=PHENOPACKETS.curie('timestamp'),
                   model_uri=PHENOPACKETS.update__timestamp, domain=None, range=str)

slots.update__updatedBy = Slot(uri=PHENOPACKETS.updatedBy, name="update__updatedBy", curie=PHENOPACKETS.curie('updatedBy'),
                   model_uri=PHENOPACKETS.update__updatedBy, domain=None, range=Optional[str])

slots.pedigree__persons = Slot(uri=PHENOPACKETS.persons, name="pedigree__persons", curie=PHENOPACKETS.curie('persons'),
                   model_uri=PHENOPACKETS.pedigree__persons, domain=None, range=Optional[Union[Union[dict, Person], list[Union[dict, Person]]]])

slots.person__affectedStatus = Slot(uri=PHENOPACKETS.affectedStatus, name="person__affectedStatus", curie=PHENOPACKETS.curie('affectedStatus'),
                   model_uri=PHENOPACKETS.person__affectedStatus, domain=None, range=Optional[Union[str, "AffectedStatus"]])

slots.person__familyId = Slot(uri=PHENOPACKETS.familyId, name="person__familyId", curie=PHENOPACKETS.curie('familyId'),
                   model_uri=PHENOPACKETS.person__familyId, domain=None, range=Optional[str])

slots.person__individualId = Slot(uri=PHENOPACKETS.individualId, name="person__individualId", curie=PHENOPACKETS.curie('individualId'),
                   model_uri=PHENOPACKETS.person__individualId, domain=None, range=Optional[str])

slots.person__maternalId = Slot(uri=PHENOPACKETS.maternalId, name="person__maternalId", curie=PHENOPACKETS.curie('maternalId'),
                   model_uri=PHENOPACKETS.person__maternalId, domain=None, range=Optional[str])

slots.person__paternalId = Slot(uri=PHENOPACKETS.paternalId, name="person__paternalId", curie=PHENOPACKETS.curie('paternalId'),
                   model_uri=PHENOPACKETS.person__paternalId, domain=None, range=Optional[str])

slots.person__sex = Slot(uri=PHENOPACKETS.sex, name="person__sex", curie=PHENOPACKETS.curie('sex'),
                   model_uri=PHENOPACKETS.person__sex, domain=None, range=Optional[Union[str, "Sex"]])

slots.phenotypicFeature__description = Slot(uri=PHENOPACKETS.description, name="phenotypicFeature__description", curie=PHENOPACKETS.curie('description'),
                   model_uri=PHENOPACKETS.phenotypicFeature__description, domain=None, range=Optional[str])

slots.phenotypicFeature__evidence = Slot(uri=PHENOPACKETS.evidence, name="phenotypicFeature__evidence", curie=PHENOPACKETS.curie('evidence'),
                   model_uri=PHENOPACKETS.phenotypicFeature__evidence, domain=None, range=Optional[Union[Union[dict, Evidence], list[Union[dict, Evidence]]]])

slots.phenotypicFeature__excluded = Slot(uri=PHENOPACKETS.excluded, name="phenotypicFeature__excluded", curie=PHENOPACKETS.curie('excluded'),
                   model_uri=PHENOPACKETS.phenotypicFeature__excluded, domain=None, range=Optional[Union[bool, Bool]])

slots.phenotypicFeature__modifiers = Slot(uri=PHENOPACKETS.modifiers, name="phenotypicFeature__modifiers", curie=PHENOPACKETS.curie('modifiers'),
                   model_uri=PHENOPACKETS.phenotypicFeature__modifiers, domain=None, range=Optional[Union[dict[Union[str, OntologyClassId], Union[dict, OntologyClass]], list[Union[dict, OntologyClass]]]])

slots.phenotypicFeature__onset = Slot(uri=PHENOPACKETS.onset, name="phenotypicFeature__onset", curie=PHENOPACKETS.curie('onset'),
                   model_uri=PHENOPACKETS.phenotypicFeature__onset, domain=None, range=Optional[Union[dict, TimeElement]])

slots.phenotypicFeature__resolution = Slot(uri=PHENOPACKETS.resolution, name="phenotypicFeature__resolution", curie=PHENOPACKETS.curie('resolution'),
                   model_uri=PHENOPACKETS.phenotypicFeature__resolution, domain=None, range=Optional[Union[dict, TimeElement]])

slots.phenotypicFeature__severity = Slot(uri=PHENOPACKETS.severity, name="phenotypicFeature__severity", curie=PHENOPACKETS.curie('severity'),
                   model_uri=PHENOPACKETS.phenotypicFeature__severity, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.phenotypicFeature__type = Slot(uri=PHENOPACKETS.type, name="phenotypicFeature__type", curie=PHENOPACKETS.curie('type'),
                   model_uri=PHENOPACKETS.phenotypicFeature__type, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.timestamp__nanos = Slot(uri=PHENOPACKETS.nanos, name="timestamp__nanos", curie=PHENOPACKETS.curie('nanos'),
                   model_uri=PHENOPACKETS.timestamp__nanos, domain=None, range=Optional[int])

slots.timestamp__seconds = Slot(uri=PHENOPACKETS.seconds, name="timestamp__seconds", curie=PHENOPACKETS.curie('seconds'),
                   model_uri=PHENOPACKETS.timestamp__seconds, domain=None, range=Optional[int])

slots.expression__syntax = Slot(uri=PHENOPACKETS.syntax, name="expression__syntax", curie=PHENOPACKETS.curie('syntax'),
                   model_uri=PHENOPACKETS.expression__syntax, domain=None, range=Optional[str])

slots.expression__value = Slot(uri=PHENOPACKETS.value, name="expression__value", curie=PHENOPACKETS.curie('value'),
                   model_uri=PHENOPACKETS.expression__value, domain=None, range=Optional[str])

slots.expression__version = Slot(uri=PHENOPACKETS.version, name="expression__version", curie=PHENOPACKETS.curie('version'),
                   model_uri=PHENOPACKETS.expression__version, domain=None, range=Optional[str])

slots.extension__name = Slot(uri=PHENOPACKETS.name, name="extension__name", curie=PHENOPACKETS.curie('name'),
                   model_uri=PHENOPACKETS.extension__name, domain=None, range=Optional[str])

slots.extension__value = Slot(uri=PHENOPACKETS.value, name="extension__value", curie=PHENOPACKETS.curie('value'),
                   model_uri=PHENOPACKETS.extension__value, domain=None, range=Optional[Union[Union[dict, Any], list[Union[dict, Any]]]])

slots.geneDescriptor__alternateIds = Slot(uri=PHENOPACKETS.alternateIds, name="geneDescriptor__alternateIds", curie=PHENOPACKETS.curie('alternateIds'),
                   model_uri=PHENOPACKETS.geneDescriptor__alternateIds, domain=None, range=Optional[Union[str, list[str]]])

slots.geneDescriptor__alternateSymbols = Slot(uri=PHENOPACKETS.alternateSymbols, name="geneDescriptor__alternateSymbols", curie=PHENOPACKETS.curie('alternateSymbols'),
                   model_uri=PHENOPACKETS.geneDescriptor__alternateSymbols, domain=None, range=Optional[Union[str, list[str]]])

slots.geneDescriptor__description = Slot(uri=PHENOPACKETS.description, name="geneDescriptor__description", curie=PHENOPACKETS.curie('description'),
                   model_uri=PHENOPACKETS.geneDescriptor__description, domain=None, range=Optional[str])

slots.geneDescriptor__symbol = Slot(uri=PHENOPACKETS.symbol, name="geneDescriptor__symbol", curie=PHENOPACKETS.curie('symbol'),
                   model_uri=PHENOPACKETS.geneDescriptor__symbol, domain=None, range=Optional[str])

slots.geneDescriptor__valueId = Slot(uri=PHENOPACKETS.valueId, name="geneDescriptor__valueId", curie=PHENOPACKETS.curie('valueId'),
                   model_uri=PHENOPACKETS.geneDescriptor__valueId, domain=None, range=Optional[str])

slots.geneDescriptor__xrefs = Slot(uri=PHENOPACKETS.xrefs, name="geneDescriptor__xrefs", curie=PHENOPACKETS.curie('xrefs'),
                   model_uri=PHENOPACKETS.geneDescriptor__xrefs, domain=None, range=Optional[Union[str, list[str]]])

slots.variationDescriptor__allelicState = Slot(uri=PHENOPACKETS.allelicState, name="variationDescriptor__allelicState", curie=PHENOPACKETS.curie('allelicState'),
                   model_uri=PHENOPACKETS.variationDescriptor__allelicState, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.variationDescriptor__alternateLabels = Slot(uri=PHENOPACKETS.alternateLabels, name="variationDescriptor__alternateLabels", curie=PHENOPACKETS.curie('alternateLabels'),
                   model_uri=PHENOPACKETS.variationDescriptor__alternateLabels, domain=None, range=Optional[Union[str, list[str]]])

slots.variationDescriptor__description = Slot(uri=PHENOPACKETS.description, name="variationDescriptor__description", curie=PHENOPACKETS.curie('description'),
                   model_uri=PHENOPACKETS.variationDescriptor__description, domain=None, range=Optional[str])

slots.variationDescriptor__expressions = Slot(uri=PHENOPACKETS.expressions, name="variationDescriptor__expressions", curie=PHENOPACKETS.curie('expressions'),
                   model_uri=PHENOPACKETS.variationDescriptor__expressions, domain=None, range=Optional[Union[Union[dict, Expression], list[Union[dict, Expression]]]])

slots.variationDescriptor__extensions = Slot(uri=PHENOPACKETS.extensions, name="variationDescriptor__extensions", curie=PHENOPACKETS.curie('extensions'),
                   model_uri=PHENOPACKETS.variationDescriptor__extensions, domain=None, range=Optional[Union[Union[dict, Extension], list[Union[dict, Extension]]]])

slots.variationDescriptor__geneContext = Slot(uri=PHENOPACKETS.geneContext, name="variationDescriptor__geneContext", curie=PHENOPACKETS.curie('geneContext'),
                   model_uri=PHENOPACKETS.variationDescriptor__geneContext, domain=None, range=Optional[Union[dict, GeneDescriptor]])

slots.variationDescriptor__id = Slot(uri=PHENOPACKETS.id, name="variationDescriptor__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.variationDescriptor__id, domain=None, range=Optional[str])

slots.variationDescriptor__label = Slot(uri=PHENOPACKETS.label, name="variationDescriptor__label", curie=PHENOPACKETS.curie('label'),
                   model_uri=PHENOPACKETS.variationDescriptor__label, domain=None, range=Optional[str])

slots.variationDescriptor__moleculeContext = Slot(uri=PHENOPACKETS.moleculeContext, name="variationDescriptor__moleculeContext", curie=PHENOPACKETS.curie('moleculeContext'),
                   model_uri=PHENOPACKETS.variationDescriptor__moleculeContext, domain=None, range=Optional[Union[str, "MoleculeContext"]])

slots.variationDescriptor__structuralType = Slot(uri=PHENOPACKETS.structuralType, name="variationDescriptor__structuralType", curie=PHENOPACKETS.curie('structuralType'),
                   model_uri=PHENOPACKETS.variationDescriptor__structuralType, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.variationDescriptor__variation = Slot(uri=PHENOPACKETS.variation, name="variationDescriptor__variation", curie=PHENOPACKETS.curie('variation'),
                   model_uri=PHENOPACKETS.variationDescriptor__variation, domain=None, range=Optional[Union[dict, Variation]])

slots.variationDescriptor__vcfRecord = Slot(uri=PHENOPACKETS.vcfRecord, name="variationDescriptor__vcfRecord", curie=PHENOPACKETS.curie('vcfRecord'),
                   model_uri=PHENOPACKETS.variationDescriptor__vcfRecord, domain=None, range=Optional[Union[dict, VcfRecord]])

slots.variationDescriptor__vrsRefAlleleSeq = Slot(uri=PHENOPACKETS.vrsRefAlleleSeq, name="variationDescriptor__vrsRefAlleleSeq", curie=PHENOPACKETS.curie('vrsRefAlleleSeq'),
                   model_uri=PHENOPACKETS.variationDescriptor__vrsRefAlleleSeq, domain=None, range=Optional[str])

slots.variationDescriptor__xrefs = Slot(uri=PHENOPACKETS.xrefs, name="variationDescriptor__xrefs", curie=PHENOPACKETS.curie('xrefs'),
                   model_uri=PHENOPACKETS.variationDescriptor__xrefs, domain=None, range=Optional[Union[str, list[str]]])

slots.vcfRecord__alt = Slot(uri=PHENOPACKETS.alt, name="vcfRecord__alt", curie=PHENOPACKETS.curie('alt'),
                   model_uri=PHENOPACKETS.vcfRecord__alt, domain=None, range=Optional[str])

slots.vcfRecord__chrom = Slot(uri=PHENOPACKETS.chrom, name="vcfRecord__chrom", curie=PHENOPACKETS.curie('chrom'),
                   model_uri=PHENOPACKETS.vcfRecord__chrom, domain=None, range=Optional[str])

slots.vcfRecord__filter = Slot(uri=PHENOPACKETS.filter, name="vcfRecord__filter", curie=PHENOPACKETS.curie('filter'),
                   model_uri=PHENOPACKETS.vcfRecord__filter, domain=None, range=Optional[str])

slots.vcfRecord__genomeAssembly = Slot(uri=PHENOPACKETS.genomeAssembly, name="vcfRecord__genomeAssembly", curie=PHENOPACKETS.curie('genomeAssembly'),
                   model_uri=PHENOPACKETS.vcfRecord__genomeAssembly, domain=None, range=Optional[str])

slots.vcfRecord__id = Slot(uri=PHENOPACKETS.id, name="vcfRecord__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.vcfRecord__id, domain=None, range=Optional[str])

slots.vcfRecord__info = Slot(uri=PHENOPACKETS.info, name="vcfRecord__info", curie=PHENOPACKETS.curie('info'),
                   model_uri=PHENOPACKETS.vcfRecord__info, domain=None, range=Optional[str])

slots.vcfRecord__pos = Slot(uri=PHENOPACKETS.pos, name="vcfRecord__pos", curie=PHENOPACKETS.curie('pos'),
                   model_uri=PHENOPACKETS.vcfRecord__pos, domain=None, range=Optional[int])

slots.vcfRecord__qual = Slot(uri=PHENOPACKETS.qual, name="vcfRecord__qual", curie=PHENOPACKETS.curie('qual'),
                   model_uri=PHENOPACKETS.vcfRecord__qual, domain=None, range=Optional[str])

slots.vcfRecord__ref = Slot(uri=PHENOPACKETS.ref, name="vcfRecord__ref", curie=PHENOPACKETS.curie('ref'),
                   model_uri=PHENOPACKETS.vcfRecord__ref, domain=None, range=Optional[str])

slots.any__typeUrl = Slot(uri=PHENOPACKETS.typeUrl, name="any__typeUrl", curie=PHENOPACKETS.curie('typeUrl'),
                   model_uri=PHENOPACKETS.any__typeUrl, domain=None, range=Optional[str])

slots.any__value = Slot(uri=PHENOPACKETS.value, name="any__value", curie=PHENOPACKETS.curie('value'),
                   model_uri=PHENOPACKETS.any__value, domain=None, range=Optional[str])

slots.abundance__copyNumber = Slot(uri=PHENOPACKETS.copyNumber, name="abundance__copyNumber", curie=PHENOPACKETS.curie('copyNumber'),
                   model_uri=PHENOPACKETS.abundance__copyNumber, domain=None, range=Optional[Union[dict, CopyNumber]])

slots.allele__chromosomeLocation = Slot(uri=PHENOPACKETS.chromosomeLocation, name="allele__chromosomeLocation", curie=PHENOPACKETS.curie('chromosomeLocation'),
                   model_uri=PHENOPACKETS.allele__chromosomeLocation, domain=None, range=Optional[Union[dict, ChromosomeLocation]])

slots.allele__curie = Slot(uri=PHENOPACKETS.curie, name="allele__curie", curie=PHENOPACKETS.curie('curie'),
                   model_uri=PHENOPACKETS.allele__curie, domain=None, range=Optional[str])

slots.allele__derivedSequenceExpression = Slot(uri=PHENOPACKETS.derivedSequenceExpression, name="allele__derivedSequenceExpression", curie=PHENOPACKETS.curie('derivedSequenceExpression'),
                   model_uri=PHENOPACKETS.allele__derivedSequenceExpression, domain=None, range=Optional[Union[dict, DerivedSequenceExpression]])

slots.allele__id = Slot(uri=PHENOPACKETS.id, name="allele__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.allele__id, domain=None, range=Optional[str])

slots.allele__literalSequenceExpression = Slot(uri=PHENOPACKETS.literalSequenceExpression, name="allele__literalSequenceExpression", curie=PHENOPACKETS.curie('literalSequenceExpression'),
                   model_uri=PHENOPACKETS.allele__literalSequenceExpression, domain=None, range=Optional[Union[dict, LiteralSequenceExpression]])

slots.allele__repeatedSequenceExpression = Slot(uri=PHENOPACKETS.repeatedSequenceExpression, name="allele__repeatedSequenceExpression", curie=PHENOPACKETS.curie('repeatedSequenceExpression'),
                   model_uri=PHENOPACKETS.allele__repeatedSequenceExpression, domain=None, range=Optional[Union[dict, RepeatedSequenceExpression]])

slots.allele__sequenceLocation = Slot(uri=PHENOPACKETS.sequenceLocation, name="allele__sequenceLocation", curie=PHENOPACKETS.curie('sequenceLocation'),
                   model_uri=PHENOPACKETS.allele__sequenceLocation, domain=None, range=Optional[Union[dict, SequenceLocation]])

slots.chromosomeLocation__chr = Slot(uri=PHENOPACKETS.chr, name="chromosomeLocation__chr", curie=PHENOPACKETS.curie('chr'),
                   model_uri=PHENOPACKETS.chromosomeLocation__chr, domain=None, range=Optional[str])

slots.chromosomeLocation__id = Slot(uri=PHENOPACKETS.id, name="chromosomeLocation__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.chromosomeLocation__id, domain=None, range=Optional[str])

slots.chromosomeLocation__interval = Slot(uri=PHENOPACKETS.interval, name="chromosomeLocation__interval", curie=PHENOPACKETS.curie('interval'),
                   model_uri=PHENOPACKETS.chromosomeLocation__interval, domain=None, range=Optional[Union[dict, CytobandInterval]])

slots.chromosomeLocation__speciesId = Slot(uri=PHENOPACKETS.speciesId, name="chromosomeLocation__speciesId", curie=PHENOPACKETS.curie('speciesId'),
                   model_uri=PHENOPACKETS.chromosomeLocation__speciesId, domain=None, range=Optional[str])

slots.copyNumber__allele = Slot(uri=PHENOPACKETS.allele, name="copyNumber__allele", curie=PHENOPACKETS.curie('allele'),
                   model_uri=PHENOPACKETS.copyNumber__allele, domain=None, range=Optional[Union[dict, Allele]])

slots.copyNumber__curie = Slot(uri=PHENOPACKETS.curie, name="copyNumber__curie", curie=PHENOPACKETS.curie('curie'),
                   model_uri=PHENOPACKETS.copyNumber__curie, domain=None, range=Optional[str])

slots.copyNumber__definiteRange = Slot(uri=PHENOPACKETS.definiteRange, name="copyNumber__definiteRange", curie=PHENOPACKETS.curie('definiteRange'),
                   model_uri=PHENOPACKETS.copyNumber__definiteRange, domain=None, range=Optional[Union[dict, DefiniteRange]])

slots.copyNumber__derivedSequenceExpression = Slot(uri=PHENOPACKETS.derivedSequenceExpression, name="copyNumber__derivedSequenceExpression", curie=PHENOPACKETS.curie('derivedSequenceExpression'),
                   model_uri=PHENOPACKETS.copyNumber__derivedSequenceExpression, domain=None, range=Optional[Union[dict, DerivedSequenceExpression]])

slots.copyNumber__gene = Slot(uri=PHENOPACKETS.gene, name="copyNumber__gene", curie=PHENOPACKETS.curie('gene'),
                   model_uri=PHENOPACKETS.copyNumber__gene, domain=None, range=Optional[Union[dict, Gene]])

slots.copyNumber__haplotype = Slot(uri=PHENOPACKETS.haplotype, name="copyNumber__haplotype", curie=PHENOPACKETS.curie('haplotype'),
                   model_uri=PHENOPACKETS.copyNumber__haplotype, domain=None, range=Optional[Union[dict, Haplotype]])

slots.copyNumber__id = Slot(uri=PHENOPACKETS.id, name="copyNumber__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.copyNumber__id, domain=None, range=Optional[str])

slots.copyNumber__indefiniteRange = Slot(uri=PHENOPACKETS.indefiniteRange, name="copyNumber__indefiniteRange", curie=PHENOPACKETS.curie('indefiniteRange'),
                   model_uri=PHENOPACKETS.copyNumber__indefiniteRange, domain=None, range=Optional[Union[dict, IndefiniteRange]])

slots.copyNumber__literalSequenceExpression = Slot(uri=PHENOPACKETS.literalSequenceExpression, name="copyNumber__literalSequenceExpression", curie=PHENOPACKETS.curie('literalSequenceExpression'),
                   model_uri=PHENOPACKETS.copyNumber__literalSequenceExpression, domain=None, range=Optional[Union[dict, LiteralSequenceExpression]])

slots.copyNumber__number = Slot(uri=PHENOPACKETS.number, name="copyNumber__number", curie=PHENOPACKETS.curie('number'),
                   model_uri=PHENOPACKETS.copyNumber__number, domain=None, range=Optional[Union[dict, Number]])

slots.copyNumber__repeatedSequenceExpression = Slot(uri=PHENOPACKETS.repeatedSequenceExpression, name="copyNumber__repeatedSequenceExpression", curie=PHENOPACKETS.curie('repeatedSequenceExpression'),
                   model_uri=PHENOPACKETS.copyNumber__repeatedSequenceExpression, domain=None, range=Optional[Union[dict, RepeatedSequenceExpression]])

slots.cytobandInterval__end = Slot(uri=PHENOPACKETS.end, name="cytobandInterval__end", curie=PHENOPACKETS.curie('end'),
                   model_uri=PHENOPACKETS.cytobandInterval__end, domain=None, range=Optional[str])

slots.cytobandInterval__start = Slot(uri=PHENOPACKETS.start, name="cytobandInterval__start", curie=PHENOPACKETS.curie('start'),
                   model_uri=PHENOPACKETS.cytobandInterval__start, domain=None, range=Optional[str])

slots.definiteRange__max = Slot(uri=PHENOPACKETS.max, name="definiteRange__max", curie=PHENOPACKETS.curie('max'),
                   model_uri=PHENOPACKETS.definiteRange__max, domain=None, range=Optional[int])

slots.definiteRange__min = Slot(uri=PHENOPACKETS.min, name="definiteRange__min", curie=PHENOPACKETS.curie('min'),
                   model_uri=PHENOPACKETS.definiteRange__min, domain=None, range=Optional[int])

slots.derivedSequenceExpression__location = Slot(uri=PHENOPACKETS.location, name="derivedSequenceExpression__location", curie=PHENOPACKETS.curie('location'),
                   model_uri=PHENOPACKETS.derivedSequenceExpression__location, domain=None, range=Optional[Union[dict, SequenceLocation]])

slots.derivedSequenceExpression__reverseComplement = Slot(uri=PHENOPACKETS.reverseComplement, name="derivedSequenceExpression__reverseComplement", curie=PHENOPACKETS.curie('reverseComplement'),
                   model_uri=PHENOPACKETS.derivedSequenceExpression__reverseComplement, domain=None, range=Optional[Union[bool, Bool]])

slots.feature__gene = Slot(uri=PHENOPACKETS.gene, name="feature__gene", curie=PHENOPACKETS.curie('gene'),
                   model_uri=PHENOPACKETS.feature__gene, domain=None, range=Optional[Union[dict, Gene]])

slots.gene__geneId = Slot(uri=PHENOPACKETS.geneId, name="gene__geneId", curie=PHENOPACKETS.curie('geneId'),
                   model_uri=PHENOPACKETS.gene__geneId, domain=None, range=Optional[str])

slots.indefiniteRange__comparator = Slot(uri=PHENOPACKETS.comparator, name="indefiniteRange__comparator", curie=PHENOPACKETS.curie('comparator'),
                   model_uri=PHENOPACKETS.indefiniteRange__comparator, domain=None, range=Optional[str])

slots.indefiniteRange__value = Slot(uri=PHENOPACKETS.value, name="indefiniteRange__value", curie=PHENOPACKETS.curie('value'),
                   model_uri=PHENOPACKETS.indefiniteRange__value, domain=None, range=Optional[int])

slots.literalSequenceExpression__sequence = Slot(uri=PHENOPACKETS.sequence, name="literalSequenceExpression__sequence", curie=PHENOPACKETS.curie('sequence'),
                   model_uri=PHENOPACKETS.literalSequenceExpression__sequence, domain=None, range=Optional[str])

slots.location__chromosomeLocation = Slot(uri=PHENOPACKETS.chromosomeLocation, name="location__chromosomeLocation", curie=PHENOPACKETS.curie('chromosomeLocation'),
                   model_uri=PHENOPACKETS.location__chromosomeLocation, domain=None, range=Optional[Union[dict, ChromosomeLocation]])

slots.location__sequenceLocation = Slot(uri=PHENOPACKETS.sequenceLocation, name="location__sequenceLocation", curie=PHENOPACKETS.curie('sequenceLocation'),
                   model_uri=PHENOPACKETS.location__sequenceLocation, domain=None, range=Optional[Union[dict, SequenceLocation]])

slots.member__allele = Slot(uri=PHENOPACKETS.allele, name="member__allele", curie=PHENOPACKETS.curie('allele'),
                   model_uri=PHENOPACKETS.member__allele, domain=None, range=Optional[Union[dict, Allele]])

slots.member__copyNumber = Slot(uri=PHENOPACKETS.copyNumber, name="member__copyNumber", curie=PHENOPACKETS.curie('copyNumber'),
                   model_uri=PHENOPACKETS.member__copyNumber, domain=None, range=Optional[Union[dict, CopyNumber]])

slots.member__curie = Slot(uri=PHENOPACKETS.curie, name="member__curie", curie=PHENOPACKETS.curie('curie'),
                   model_uri=PHENOPACKETS.member__curie, domain=None, range=Optional[str])

slots.member__haplotype = Slot(uri=PHENOPACKETS.haplotype, name="member__haplotype", curie=PHENOPACKETS.curie('haplotype'),
                   model_uri=PHENOPACKETS.member__haplotype, domain=None, range=Optional[Union[dict, Haplotype]])

slots.member__id = Slot(uri=PHENOPACKETS.id, name="member__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.member__id, domain=None, range=Optional[str])

slots.member__members = Slot(uri=PHENOPACKETS.members, name="member__members", curie=PHENOPACKETS.curie('members'),
                   model_uri=PHENOPACKETS.member__members, domain=None, range=Optional[Union[Union[dict, Member], list[Union[dict, Member]]]])

slots.member__text = Slot(uri=PHENOPACKETS.text, name="member__text", curie=PHENOPACKETS.curie('text'),
                   model_uri=PHENOPACKETS.member__text, domain=None, range=Optional[Union[dict, Text]])

slots.member__variationSet = Slot(uri=PHENOPACKETS.variationSet, name="member__variationSet", curie=PHENOPACKETS.curie('variationSet'),
                   model_uri=PHENOPACKETS.member__variationSet, domain=None, range=Optional[Union[dict, VariationSet]])

slots.molecularVariation__allele = Slot(uri=PHENOPACKETS.allele, name="molecularVariation__allele", curie=PHENOPACKETS.curie('allele'),
                   model_uri=PHENOPACKETS.molecularVariation__allele, domain=None, range=Optional[Union[dict, Allele]])

slots.molecularVariation__haplotype = Slot(uri=PHENOPACKETS.haplotype, name="molecularVariation__haplotype", curie=PHENOPACKETS.curie('haplotype'),
                   model_uri=PHENOPACKETS.molecularVariation__haplotype, domain=None, range=Optional[Union[dict, Haplotype]])

slots.number__value = Slot(uri=PHENOPACKETS.value, name="number__value", curie=PHENOPACKETS.curie('value'),
                   model_uri=PHENOPACKETS.number__value, domain=None, range=Optional[int])

slots.repeatedSequenceExpression__definiteRange = Slot(uri=PHENOPACKETS.definiteRange, name="repeatedSequenceExpression__definiteRange", curie=PHENOPACKETS.curie('definiteRange'),
                   model_uri=PHENOPACKETS.repeatedSequenceExpression__definiteRange, domain=None, range=Optional[Union[dict, DefiniteRange]])

slots.repeatedSequenceExpression__derivedSequenceExpression = Slot(uri=PHENOPACKETS.derivedSequenceExpression, name="repeatedSequenceExpression__derivedSequenceExpression", curie=PHENOPACKETS.curie('derivedSequenceExpression'),
                   model_uri=PHENOPACKETS.repeatedSequenceExpression__derivedSequenceExpression, domain=None, range=Optional[Union[dict, DerivedSequenceExpression]])

slots.repeatedSequenceExpression__indefiniteRange = Slot(uri=PHENOPACKETS.indefiniteRange, name="repeatedSequenceExpression__indefiniteRange", curie=PHENOPACKETS.curie('indefiniteRange'),
                   model_uri=PHENOPACKETS.repeatedSequenceExpression__indefiniteRange, domain=None, range=Optional[Union[dict, IndefiniteRange]])

slots.repeatedSequenceExpression__literalSequenceExpression = Slot(uri=PHENOPACKETS.literalSequenceExpression, name="repeatedSequenceExpression__literalSequenceExpression", curie=PHENOPACKETS.curie('literalSequenceExpression'),
                   model_uri=PHENOPACKETS.repeatedSequenceExpression__literalSequenceExpression, domain=None, range=Optional[Union[dict, LiteralSequenceExpression]])

slots.repeatedSequenceExpression__number = Slot(uri=PHENOPACKETS.number, name="repeatedSequenceExpression__number", curie=PHENOPACKETS.curie('number'),
                   model_uri=PHENOPACKETS.repeatedSequenceExpression__number, domain=None, range=Optional[Union[dict, Number]])

slots.sequenceExpression__derivedSequenceExpression = Slot(uri=PHENOPACKETS.derivedSequenceExpression, name="sequenceExpression__derivedSequenceExpression", curie=PHENOPACKETS.curie('derivedSequenceExpression'),
                   model_uri=PHENOPACKETS.sequenceExpression__derivedSequenceExpression, domain=None, range=Optional[Union[dict, DerivedSequenceExpression]])

slots.sequenceExpression__literalSequenceExpression = Slot(uri=PHENOPACKETS.literalSequenceExpression, name="sequenceExpression__literalSequenceExpression", curie=PHENOPACKETS.curie('literalSequenceExpression'),
                   model_uri=PHENOPACKETS.sequenceExpression__literalSequenceExpression, domain=None, range=Optional[Union[dict, LiteralSequenceExpression]])

slots.sequenceExpression__repeatedSequenceExpression = Slot(uri=PHENOPACKETS.repeatedSequenceExpression, name="sequenceExpression__repeatedSequenceExpression", curie=PHENOPACKETS.curie('repeatedSequenceExpression'),
                   model_uri=PHENOPACKETS.sequenceExpression__repeatedSequenceExpression, domain=None, range=Optional[Union[dict, RepeatedSequenceExpression]])

slots.sequenceInterval__endDefiniteRange = Slot(uri=PHENOPACKETS.endDefiniteRange, name="sequenceInterval__endDefiniteRange", curie=PHENOPACKETS.curie('endDefiniteRange'),
                   model_uri=PHENOPACKETS.sequenceInterval__endDefiniteRange, domain=None, range=Optional[Union[dict, DefiniteRange]])

slots.sequenceInterval__endIndefiniteRange = Slot(uri=PHENOPACKETS.endIndefiniteRange, name="sequenceInterval__endIndefiniteRange", curie=PHENOPACKETS.curie('endIndefiniteRange'),
                   model_uri=PHENOPACKETS.sequenceInterval__endIndefiniteRange, domain=None, range=Optional[Union[dict, IndefiniteRange]])

slots.sequenceInterval__endNumber = Slot(uri=PHENOPACKETS.endNumber, name="sequenceInterval__endNumber", curie=PHENOPACKETS.curie('endNumber'),
                   model_uri=PHENOPACKETS.sequenceInterval__endNumber, domain=None, range=Optional[Union[dict, Number]])

slots.sequenceInterval__startDefiniteRange = Slot(uri=PHENOPACKETS.startDefiniteRange, name="sequenceInterval__startDefiniteRange", curie=PHENOPACKETS.curie('startDefiniteRange'),
                   model_uri=PHENOPACKETS.sequenceInterval__startDefiniteRange, domain=None, range=Optional[Union[dict, DefiniteRange]])

slots.sequenceInterval__startIndefiniteRange = Slot(uri=PHENOPACKETS.startIndefiniteRange, name="sequenceInterval__startIndefiniteRange", curie=PHENOPACKETS.curie('startIndefiniteRange'),
                   model_uri=PHENOPACKETS.sequenceInterval__startIndefiniteRange, domain=None, range=Optional[Union[dict, IndefiniteRange]])

slots.sequenceInterval__startNumber = Slot(uri=PHENOPACKETS.startNumber, name="sequenceInterval__startNumber", curie=PHENOPACKETS.curie('startNumber'),
                   model_uri=PHENOPACKETS.sequenceInterval__startNumber, domain=None, range=Optional[Union[dict, Number]])

slots.sequenceLocation__id = Slot(uri=PHENOPACKETS.id, name="sequenceLocation__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.sequenceLocation__id, domain=None, range=Optional[str])

slots.sequenceLocation__sequenceId = Slot(uri=PHENOPACKETS.sequenceId, name="sequenceLocation__sequenceId", curie=PHENOPACKETS.curie('sequenceId'),
                   model_uri=PHENOPACKETS.sequenceLocation__sequenceId, domain=None, range=Optional[str])

slots.sequenceLocation__sequenceInterval = Slot(uri=PHENOPACKETS.sequenceInterval, name="sequenceLocation__sequenceInterval", curie=PHENOPACKETS.curie('sequenceInterval'),
                   model_uri=PHENOPACKETS.sequenceLocation__sequenceInterval, domain=None, range=Optional[Union[dict, SequenceInterval]])

slots.sequenceState__sequence = Slot(uri=PHENOPACKETS.sequence, name="sequenceState__sequence", curie=PHENOPACKETS.curie('sequence'),
                   model_uri=PHENOPACKETS.sequenceState__sequence, domain=None, range=Optional[str])

slots.simpleInterval__end = Slot(uri=PHENOPACKETS.end, name="simpleInterval__end", curie=PHENOPACKETS.curie('end'),
                   model_uri=PHENOPACKETS.simpleInterval__end, domain=None, range=Optional[int])

slots.simpleInterval__start = Slot(uri=PHENOPACKETS.start, name="simpleInterval__start", curie=PHENOPACKETS.curie('start'),
                   model_uri=PHENOPACKETS.simpleInterval__start, domain=None, range=Optional[int])

slots.systemicVariation__copyNumber = Slot(uri=PHENOPACKETS.copyNumber, name="systemicVariation__copyNumber", curie=PHENOPACKETS.curie('copyNumber'),
                   model_uri=PHENOPACKETS.systemicVariation__copyNumber, domain=None, range=Optional[Union[dict, CopyNumber]])

slots.text__definition = Slot(uri=PHENOPACKETS.definition, name="text__definition", curie=PHENOPACKETS.curie('definition'),
                   model_uri=PHENOPACKETS.text__definition, domain=None, range=Optional[str])

slots.text__id = Slot(uri=PHENOPACKETS.id, name="text__id", curie=PHENOPACKETS.curie('id'),
                   model_uri=PHENOPACKETS.text__id, domain=None, range=Optional[str])

slots.utilityVariation__text = Slot(uri=PHENOPACKETS.text, name="utilityVariation__text", curie=PHENOPACKETS.curie('text'),
                   model_uri=PHENOPACKETS.utilityVariation__text, domain=None, range=Optional[Union[dict, Text]])

slots.utilityVariation__variationSet = Slot(uri=PHENOPACKETS.variationSet, name="utilityVariation__variationSet", curie=PHENOPACKETS.curie('variationSet'),
                   model_uri=PHENOPACKETS.utilityVariation__variationSet, domain=None, range=Optional[Union[dict, VariationSet]])

slots.variation__allele = Slot(uri=PHENOPACKETS.allele, name="variation__allele", curie=PHENOPACKETS.curie('allele'),
                   model_uri=PHENOPACKETS.variation__allele, domain=None, range=Optional[Union[dict, Allele]])

slots.variation__copyNumber = Slot(uri=PHENOPACKETS.copyNumber, name="variation__copyNumber", curie=PHENOPACKETS.curie('copyNumber'),
                   model_uri=PHENOPACKETS.variation__copyNumber, domain=None, range=Optional[Union[dict, CopyNumber]])

slots.variation__haplotype = Slot(uri=PHENOPACKETS.haplotype, name="variation__haplotype", curie=PHENOPACKETS.curie('haplotype'),
                   model_uri=PHENOPACKETS.variation__haplotype, domain=None, range=Optional[Union[dict, Haplotype]])

slots.variation__text = Slot(uri=PHENOPACKETS.text, name="variation__text", curie=PHENOPACKETS.curie('text'),
                   model_uri=PHENOPACKETS.variation__text, domain=None, range=Optional[Union[dict, Text]])

slots.variation__variationSet = Slot(uri=PHENOPACKETS.variationSet, name="variation__variationSet", curie=PHENOPACKETS.curie('variationSet'),
                   model_uri=PHENOPACKETS.variation__variationSet, domain=None, range=Optional[Union[dict, VariationSet]])
