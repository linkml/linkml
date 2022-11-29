# Auto generated from omop.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-11-28T13:31:22
# Schema: omop_vocabulary
#
# id: https://w3id.org/omop_vocabulary
# description: omop_vocabulary
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
from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OMOP_VOCABULARY = CurieNamespace('omop_vocabulary', 'https://w3id.org/omop_vocabulary')
DEFAULT_ = OMOP_VOCABULARY


# Types

# Class references



@dataclass
class CONCEPTRELATIONSHIP(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTRELATIONSHIP
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTRELATIONSHIP"
    class_name: ClassVar[str] = "CONCEPT_RELATIONSHIP"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTRELATIONSHIP

    concept_id_1: Optional[int] = None
    concept_id_2: Optional[int] = None
    relationship_id: Optional[str] = None
    valid_start_date: Optional[int] = None
    valid_end_date: Optional[int] = None
    invalid_reason: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.concept_id_1 is not None and not isinstance(self.concept_id_1, int):
            self.concept_id_1 = int(self.concept_id_1)

        if self.concept_id_2 is not None and not isinstance(self.concept_id_2, int):
            self.concept_id_2 = int(self.concept_id_2)

        if self.relationship_id is not None and not isinstance(self.relationship_id, str):
            self.relationship_id = str(self.relationship_id)

        if self.valid_start_date is not None and not isinstance(self.valid_start_date, int):
            self.valid_start_date = int(self.valid_start_date)

        if self.valid_end_date is not None and not isinstance(self.valid_end_date, int):
            self.valid_end_date = int(self.valid_end_date)

        if self.invalid_reason is not None and not isinstance(self.invalid_reason, str):
            self.invalid_reason = str(self.invalid_reason)

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTRELATIONSHIPCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTRELATIONSHIPCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTRELATIONSHIPCONTAINER"
    class_name: ClassVar[str] = "CONCEPT_RELATIONSHIP_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTRELATIONSHIPCONTAINER

    concept_relationship_list: Optional[Union[Union[dict, CONCEPTRELATIONSHIP], List[Union[dict, CONCEPTRELATIONSHIP]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.concept_relationship_list, list):
            self.concept_relationship_list = [self.concept_relationship_list] if self.concept_relationship_list is not None else []
        self.concept_relationship_list = [v if isinstance(v, CONCEPTRELATIONSHIP) else CONCEPTRELATIONSHIP(**as_dict(v)) for v in self.concept_relationship_list]

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTANCESTOR(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTANCESTOR
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTANCESTOR"
    class_name: ClassVar[str] = "CONCEPT_ANCESTOR"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTANCESTOR

    ancestor_concept_id: Optional[int] = None
    descendant_concept_id: Optional[int] = None
    min_levels_of_separation: Optional[int] = None
    max_levels_of_separation: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.ancestor_concept_id is not None and not isinstance(self.ancestor_concept_id, int):
            self.ancestor_concept_id = int(self.ancestor_concept_id)

        if self.descendant_concept_id is not None and not isinstance(self.descendant_concept_id, int):
            self.descendant_concept_id = int(self.descendant_concept_id)

        if self.min_levels_of_separation is not None and not isinstance(self.min_levels_of_separation, int):
            self.min_levels_of_separation = int(self.min_levels_of_separation)

        if self.max_levels_of_separation is not None and not isinstance(self.max_levels_of_separation, int):
            self.max_levels_of_separation = int(self.max_levels_of_separation)

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTANCESTORCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTANCESTORCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTANCESTORCONTAINER"
    class_name: ClassVar[str] = "CONCEPT_ANCESTOR_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTANCESTORCONTAINER

    concept_ancestor_list: Optional[Union[Union[dict, CONCEPTANCESTOR], List[Union[dict, CONCEPTANCESTOR]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.concept_ancestor_list, list):
            self.concept_ancestor_list = [self.concept_ancestor_list] if self.concept_ancestor_list is not None else []
        self.concept_ancestor_list = [v if isinstance(v, CONCEPTANCESTOR) else CONCEPTANCESTOR(**as_dict(v)) for v in self.concept_ancestor_list]

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTCLASS(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTCLASS
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTCLASS"
    class_name: ClassVar[str] = "CONCEPT_CLASS"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTCLASS

    concept_class_id: Optional[str] = None
    concept_class_name: Optional[str] = None
    concept_class_concept_id: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.concept_class_id is not None and not isinstance(self.concept_class_id, str):
            self.concept_class_id = str(self.concept_class_id)

        if self.concept_class_name is not None and not isinstance(self.concept_class_name, str):
            self.concept_class_name = str(self.concept_class_name)

        if self.concept_class_concept_id is not None and not isinstance(self.concept_class_concept_id, int):
            self.concept_class_concept_id = int(self.concept_class_concept_id)

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTCLASSCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTCLASSCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTCLASSCONTAINER"
    class_name: ClassVar[str] = "CONCEPT_CLASS_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTCLASSCONTAINER

    concept_class_list: Optional[Union[Union[dict, CONCEPTCLASS], List[Union[dict, CONCEPTCLASS]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.concept_class_list, list):
            self.concept_class_list = [self.concept_class_list] if self.concept_class_list is not None else []
        self.concept_class_list = [v if isinstance(v, CONCEPTCLASS) else CONCEPTCLASS(**as_dict(v)) for v in self.concept_class_list]

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTSYNONYM(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTSYNONYM
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTSYNONYM"
    class_name: ClassVar[str] = "CONCEPT_SYNONYM"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTSYNONYM

    concept_id: Optional[int] = None
    concept_synonym_name: Optional[str] = None
    language_concept_id: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.concept_id is not None and not isinstance(self.concept_id, int):
            self.concept_id = int(self.concept_id)

        if self.concept_synonym_name is not None and not isinstance(self.concept_synonym_name, str):
            self.concept_synonym_name = str(self.concept_synonym_name)

        if self.language_concept_id is not None and not isinstance(self.language_concept_id, int):
            self.language_concept_id = int(self.language_concept_id)

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTSYNONYMCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTSYNONYMCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTSYNONYMCONTAINER"
    class_name: ClassVar[str] = "CONCEPT_SYNONYM_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTSYNONYMCONTAINER

    concept_synonym_list: Optional[Union[Union[dict, CONCEPTSYNONYM], List[Union[dict, CONCEPTSYNONYM]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.concept_synonym_list, list):
            self.concept_synonym_list = [self.concept_synonym_list] if self.concept_synonym_list is not None else []
        self.concept_synonym_list = [v if isinstance(v, CONCEPTSYNONYM) else CONCEPTSYNONYM(**as_dict(v)) for v in self.concept_synonym_list]

        super().__post_init__(**kwargs)


@dataclass
class CONCEPT(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPT
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPT"
    class_name: ClassVar[str] = "CONCEPT"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPT

    concept_id: Optional[int] = None
    concept_name: Optional[str] = None
    domain_id: Optional[Union[str, "DomainIdEnum"]] = None
    vocabulary_id: Optional[Union[str, "VocabularyIdEnum"]] = None
    concept_class_id: Optional[str] = None
    standard_concept: Optional[Union[str, "StandardConceptEnum"]] = None
    concept_code: Optional[str] = None
    valid_start_date: Optional[int] = None
    valid_end_date: Optional[int] = None
    invalid_reason: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.concept_id is not None and not isinstance(self.concept_id, int):
            self.concept_id = int(self.concept_id)

        if self.concept_name is not None and not isinstance(self.concept_name, str):
            self.concept_name = str(self.concept_name)

        if self.domain_id is not None and not isinstance(self.domain_id, DomainIdEnum):
            self.domain_id = DomainIdEnum(self.domain_id)

        if self.vocabulary_id is not None and not isinstance(self.vocabulary_id, VocabularyIdEnum):
            self.vocabulary_id = VocabularyIdEnum(self.vocabulary_id)

        if self.concept_class_id is not None and not isinstance(self.concept_class_id, str):
            self.concept_class_id = str(self.concept_class_id)

        if self.standard_concept is not None and not isinstance(self.standard_concept, StandardConceptEnum):
            self.standard_concept = StandardConceptEnum(self.standard_concept)

        if self.concept_code is not None and not isinstance(self.concept_code, str):
            self.concept_code = str(self.concept_code)

        if self.valid_start_date is not None and not isinstance(self.valid_start_date, int):
            self.valid_start_date = int(self.valid_start_date)

        if self.valid_end_date is not None and not isinstance(self.valid_end_date, int):
            self.valid_end_date = int(self.valid_end_date)

        if self.invalid_reason is not None and not isinstance(self.invalid_reason, str):
            self.invalid_reason = str(self.invalid_reason)

        super().__post_init__(**kwargs)


@dataclass
class CONCEPTCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:CONCEPTCONTAINER"
    class_name: ClassVar[str] = "CONCEPT_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.CONCEPTCONTAINER

    concept_list: Optional[Union[Union[dict, CONCEPT], List[Union[dict, CONCEPT]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.concept_list, list):
            self.concept_list = [self.concept_list] if self.concept_list is not None else []
        self.concept_list = [v if isinstance(v, CONCEPT) else CONCEPT(**as_dict(v)) for v in self.concept_list]

        super().__post_init__(**kwargs)


@dataclass
class DOMAIN(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.DOMAIN
    class_class_curie: ClassVar[str] = "omop_vocabulary:DOMAIN"
    class_name: ClassVar[str] = "DOMAIN"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.DOMAIN

    domain_id: Optional[Union[str, "DomainIdEnum"]] = None
    domain_name: Optional[str] = None
    domain_concept_id: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.domain_id is not None and not isinstance(self.domain_id, DomainIdEnum):
            self.domain_id = DomainIdEnum(self.domain_id)

        if self.domain_name is not None and not isinstance(self.domain_name, str):
            self.domain_name = str(self.domain_name)

        if self.domain_concept_id is not None and not isinstance(self.domain_concept_id, int):
            self.domain_concept_id = int(self.domain_concept_id)

        super().__post_init__(**kwargs)


@dataclass
class DOMAINCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.DOMAINCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:DOMAINCONTAINER"
    class_name: ClassVar[str] = "DOMAIN_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.DOMAINCONTAINER

    domain_list: Optional[Union[Union[dict, DOMAIN], List[Union[dict, DOMAIN]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.domain_list, list):
            self.domain_list = [self.domain_list] if self.domain_list is not None else []
        self.domain_list = [v if isinstance(v, DOMAIN) else DOMAIN(**as_dict(v)) for v in self.domain_list]

        super().__post_init__(**kwargs)


@dataclass
class RELATIONSHIP(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.RELATIONSHIP
    class_class_curie: ClassVar[str] = "omop_vocabulary:RELATIONSHIP"
    class_name: ClassVar[str] = "RELATIONSHIP"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.RELATIONSHIP

    relationship_id: Optional[str] = None
    relationship_name: Optional[str] = None
    is_hierarchical: Optional[int] = None
    defines_ancestry: Optional[int] = None
    reverse_relationship_id: Optional[str] = None
    relationship_concept_id: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.relationship_id is not None and not isinstance(self.relationship_id, str):
            self.relationship_id = str(self.relationship_id)

        if self.relationship_name is not None and not isinstance(self.relationship_name, str):
            self.relationship_name = str(self.relationship_name)

        if self.is_hierarchical is not None and not isinstance(self.is_hierarchical, int):
            self.is_hierarchical = int(self.is_hierarchical)

        if self.defines_ancestry is not None and not isinstance(self.defines_ancestry, int):
            self.defines_ancestry = int(self.defines_ancestry)

        if self.reverse_relationship_id is not None and not isinstance(self.reverse_relationship_id, str):
            self.reverse_relationship_id = str(self.reverse_relationship_id)

        if self.relationship_concept_id is not None and not isinstance(self.relationship_concept_id, int):
            self.relationship_concept_id = int(self.relationship_concept_id)

        super().__post_init__(**kwargs)


@dataclass
class RELATIONSHIPCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.RELATIONSHIPCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:RELATIONSHIPCONTAINER"
    class_name: ClassVar[str] = "RELATIONSHIP_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.RELATIONSHIPCONTAINER

    relationship_list: Optional[Union[Union[dict, RELATIONSHIP], List[Union[dict, RELATIONSHIP]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.relationship_list, list):
            self.relationship_list = [self.relationship_list] if self.relationship_list is not None else []
        self.relationship_list = [v if isinstance(v, RELATIONSHIP) else RELATIONSHIP(**as_dict(v)) for v in self.relationship_list]

        super().__post_init__(**kwargs)


@dataclass
class VOCABULARY(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.VOCABULARY
    class_class_curie: ClassVar[str] = "omop_vocabulary:VOCABULARY"
    class_name: ClassVar[str] = "VOCABULARY"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.VOCABULARY

    vocabulary_id: Optional[Union[str, "VocabularyIdEnum"]] = None
    vocabulary_name: Optional[str] = None
    vocabulary_reference: Optional[str] = None
    vocabulary_version: Optional[str] = None
    vocabulary_concept_id: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.vocabulary_id is not None and not isinstance(self.vocabulary_id, VocabularyIdEnum):
            self.vocabulary_id = VocabularyIdEnum(self.vocabulary_id)

        if self.vocabulary_name is not None and not isinstance(self.vocabulary_name, str):
            self.vocabulary_name = str(self.vocabulary_name)

        if self.vocabulary_reference is not None and not isinstance(self.vocabulary_reference, str):
            self.vocabulary_reference = str(self.vocabulary_reference)

        if self.vocabulary_version is not None and not isinstance(self.vocabulary_version, str):
            self.vocabulary_version = str(self.vocabulary_version)

        if self.vocabulary_concept_id is not None and not isinstance(self.vocabulary_concept_id, int):
            self.vocabulary_concept_id = int(self.vocabulary_concept_id)

        super().__post_init__(**kwargs)


@dataclass
class VOCABULARYCONTAINER(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOP_VOCABULARY.VOCABULARYCONTAINER
    class_class_curie: ClassVar[str] = "omop_vocabulary:VOCABULARYCONTAINER"
    class_name: ClassVar[str] = "VOCABULARY_CONTAINER"
    class_model_uri: ClassVar[URIRef] = OMOP_VOCABULARY.VOCABULARYCONTAINER

    vocabulary_list: Optional[Union[Union[dict, VOCABULARY], List[Union[dict, VOCABULARY]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.vocabulary_list, list):
            self.vocabulary_list = [self.vocabulary_list] if self.vocabulary_list is not None else []
        self.vocabulary_list = [v if isinstance(v, VOCABULARY) else VOCABULARY(**as_dict(v)) for v in self.vocabulary_list]

        super().__post_init__(**kwargs)


# Enumerations
class DomainIdEnum(EnumDefinitionImpl):

    Metadata = PermissibleValue(text="Metadata",
                                       description="Metadata")

    _defn = EnumDefinition(
        name="DomainIdEnum",
    )

class VocabularyIdEnum(EnumDefinitionImpl):

    CDM = PermissibleValue(text="CDM",
                             description="CDM")

    _defn = EnumDefinition(
        name="VocabularyIdEnum",
    )

class ConceptClassIdEnum(EnumDefinitionImpl):

    Field = PermissibleValue(text="Field",
                                 description="Field")

    _defn = EnumDefinition(
        name="ConceptClassIdEnum",
    )

class StandardConceptEnum(EnumDefinitionImpl):

    S = PermissibleValue(text="S",
                         description="S")

    _defn = EnumDefinition(
        name="StandardConceptEnum",
    )

# Slots
class slots:
    pass

slots.concept_id_1 = Slot(uri=OMOP_VOCABULARY.concept_id_1, name="concept_id_1", curie=OMOP_VOCABULARY.curie('concept_id_1'),
                   model_uri=OMOP_VOCABULARY.concept_id_1, domain=None, range=Optional[int])

slots.concept_id_2 = Slot(uri=OMOP_VOCABULARY.concept_id_2, name="concept_id_2", curie=OMOP_VOCABULARY.curie('concept_id_2'),
                   model_uri=OMOP_VOCABULARY.concept_id_2, domain=None, range=Optional[int])

slots.relationship_id = Slot(uri=OMOP_VOCABULARY.relationship_id, name="relationship_id", curie=OMOP_VOCABULARY.curie('relationship_id'),
                   model_uri=OMOP_VOCABULARY.relationship_id, domain=None, range=Optional[str])

slots.valid_start_date = Slot(uri=OMOP_VOCABULARY.valid_start_date, name="valid_start_date", curie=OMOP_VOCABULARY.curie('valid_start_date'),
                   model_uri=OMOP_VOCABULARY.valid_start_date, domain=None, range=Optional[int])

slots.valid_end_date = Slot(uri=OMOP_VOCABULARY.valid_end_date, name="valid_end_date", curie=OMOP_VOCABULARY.curie('valid_end_date'),
                   model_uri=OMOP_VOCABULARY.valid_end_date, domain=None, range=Optional[int])

slots.invalid_reason = Slot(uri=OMOP_VOCABULARY.invalid_reason, name="invalid_reason", curie=OMOP_VOCABULARY.curie('invalid_reason'),
                   model_uri=OMOP_VOCABULARY.invalid_reason, domain=None, range=Optional[str])

slots.concept_relationship_list = Slot(uri=OMOP_VOCABULARY.concept_relationship_list, name="concept_relationship_list", curie=OMOP_VOCABULARY.curie('concept_relationship_list'),
                   model_uri=OMOP_VOCABULARY.concept_relationship_list, domain=None, range=Optional[Union[Union[dict, CONCEPTRELATIONSHIP], List[Union[dict, CONCEPTRELATIONSHIP]]]])

slots.ancestor_concept_id = Slot(uri=OMOP_VOCABULARY.ancestor_concept_id, name="ancestor_concept_id", curie=OMOP_VOCABULARY.curie('ancestor_concept_id'),
                   model_uri=OMOP_VOCABULARY.ancestor_concept_id, domain=None, range=Optional[int])

slots.descendant_concept_id = Slot(uri=OMOP_VOCABULARY.descendant_concept_id, name="descendant_concept_id", curie=OMOP_VOCABULARY.curie('descendant_concept_id'),
                   model_uri=OMOP_VOCABULARY.descendant_concept_id, domain=None, range=Optional[int])

slots.min_levels_of_separation = Slot(uri=OMOP_VOCABULARY.min_levels_of_separation, name="min_levels_of_separation", curie=OMOP_VOCABULARY.curie('min_levels_of_separation'),
                   model_uri=OMOP_VOCABULARY.min_levels_of_separation, domain=None, range=Optional[int])

slots.max_levels_of_separation = Slot(uri=OMOP_VOCABULARY.max_levels_of_separation, name="max_levels_of_separation", curie=OMOP_VOCABULARY.curie('max_levels_of_separation'),
                   model_uri=OMOP_VOCABULARY.max_levels_of_separation, domain=None, range=Optional[int])

slots.concept_ancestor_list = Slot(uri=OMOP_VOCABULARY.concept_ancestor_list, name="concept_ancestor_list", curie=OMOP_VOCABULARY.curie('concept_ancestor_list'),
                   model_uri=OMOP_VOCABULARY.concept_ancestor_list, domain=None, range=Optional[Union[Union[dict, CONCEPTANCESTOR], List[Union[dict, CONCEPTANCESTOR]]]])

slots.concept_class_id = Slot(uri=OMOP_VOCABULARY.concept_class_id, name="concept_class_id", curie=OMOP_VOCABULARY.curie('concept_class_id'),
                   model_uri=OMOP_VOCABULARY.concept_class_id, domain=None, range=Optional[str])

slots.concept_class_name = Slot(uri=OMOP_VOCABULARY.concept_class_name, name="concept_class_name", curie=OMOP_VOCABULARY.curie('concept_class_name'),
                   model_uri=OMOP_VOCABULARY.concept_class_name, domain=None, range=Optional[str])

slots.concept_class_concept_id = Slot(uri=OMOP_VOCABULARY.concept_class_concept_id, name="concept_class_concept_id", curie=OMOP_VOCABULARY.curie('concept_class_concept_id'),
                   model_uri=OMOP_VOCABULARY.concept_class_concept_id, domain=None, range=Optional[int])

slots.concept_class_list = Slot(uri=OMOP_VOCABULARY.concept_class_list, name="concept_class_list", curie=OMOP_VOCABULARY.curie('concept_class_list'),
                   model_uri=OMOP_VOCABULARY.concept_class_list, domain=None, range=Optional[Union[Union[dict, CONCEPTCLASS], List[Union[dict, CONCEPTCLASS]]]])

slots.concept_id = Slot(uri=OMOP_VOCABULARY.concept_id, name="concept_id", curie=OMOP_VOCABULARY.curie('concept_id'),
                   model_uri=OMOP_VOCABULARY.concept_id, domain=None, range=Optional[int])

slots.concept_synonym_name = Slot(uri=OMOP_VOCABULARY.concept_synonym_name, name="concept_synonym_name", curie=OMOP_VOCABULARY.curie('concept_synonym_name'),
                   model_uri=OMOP_VOCABULARY.concept_synonym_name, domain=None, range=Optional[str])

slots.language_concept_id = Slot(uri=OMOP_VOCABULARY.language_concept_id, name="language_concept_id", curie=OMOP_VOCABULARY.curie('language_concept_id'),
                   model_uri=OMOP_VOCABULARY.language_concept_id, domain=None, range=Optional[int])

slots.concept_synonym_list = Slot(uri=OMOP_VOCABULARY.concept_synonym_list, name="concept_synonym_list", curie=OMOP_VOCABULARY.curie('concept_synonym_list'),
                   model_uri=OMOP_VOCABULARY.concept_synonym_list, domain=None, range=Optional[Union[Union[dict, CONCEPTSYNONYM], List[Union[dict, CONCEPTSYNONYM]]]])

slots.concept_name = Slot(uri=OMOP_VOCABULARY.concept_name, name="concept_name", curie=OMOP_VOCABULARY.curie('concept_name'),
                   model_uri=OMOP_VOCABULARY.concept_name, domain=None, range=Optional[str])

slots.domain_id = Slot(uri=OMOP_VOCABULARY.domain_id, name="domain_id", curie=OMOP_VOCABULARY.curie('domain_id'),
                   model_uri=OMOP_VOCABULARY.domain_id, domain=None, range=Optional[Union[str, "DomainIdEnum"]])

slots.vocabulary_id = Slot(uri=OMOP_VOCABULARY.vocabulary_id, name="vocabulary_id", curie=OMOP_VOCABULARY.curie('vocabulary_id'),
                   model_uri=OMOP_VOCABULARY.vocabulary_id, domain=None, range=Optional[Union[str, "VocabularyIdEnum"]])

slots.standard_concept = Slot(uri=OMOP_VOCABULARY.standard_concept, name="standard_concept", curie=OMOP_VOCABULARY.curie('standard_concept'),
                   model_uri=OMOP_VOCABULARY.standard_concept, domain=None, range=Optional[Union[str, "StandardConceptEnum"]])

slots.concept_code = Slot(uri=OMOP_VOCABULARY.concept_code, name="concept_code", curie=OMOP_VOCABULARY.curie('concept_code'),
                   model_uri=OMOP_VOCABULARY.concept_code, domain=None, range=Optional[str])

slots.concept_list = Slot(uri=OMOP_VOCABULARY.concept_list, name="concept_list", curie=OMOP_VOCABULARY.curie('concept_list'),
                   model_uri=OMOP_VOCABULARY.concept_list, domain=None, range=Optional[Union[Union[dict, CONCEPT], List[Union[dict, CONCEPT]]]])

slots.domain_name = Slot(uri=OMOP_VOCABULARY.domain_name, name="domain_name", curie=OMOP_VOCABULARY.curie('domain_name'),
                   model_uri=OMOP_VOCABULARY.domain_name, domain=None, range=Optional[str])

slots.domain_concept_id = Slot(uri=OMOP_VOCABULARY.domain_concept_id, name="domain_concept_id", curie=OMOP_VOCABULARY.curie('domain_concept_id'),
                   model_uri=OMOP_VOCABULARY.domain_concept_id, domain=None, range=Optional[int])

slots.domain_list = Slot(uri=OMOP_VOCABULARY.domain_list, name="domain_list", curie=OMOP_VOCABULARY.curie('domain_list'),
                   model_uri=OMOP_VOCABULARY.domain_list, domain=None, range=Optional[Union[Union[dict, DOMAIN], List[Union[dict, DOMAIN]]]])

slots.relationship_name = Slot(uri=OMOP_VOCABULARY.relationship_name, name="relationship_name", curie=OMOP_VOCABULARY.curie('relationship_name'),
                   model_uri=OMOP_VOCABULARY.relationship_name, domain=None, range=Optional[str])

slots.is_hierarchical = Slot(uri=OMOP_VOCABULARY.is_hierarchical, name="is_hierarchical", curie=OMOP_VOCABULARY.curie('is_hierarchical'),
                   model_uri=OMOP_VOCABULARY.is_hierarchical, domain=None, range=Optional[int])

slots.defines_ancestry = Slot(uri=OMOP_VOCABULARY.defines_ancestry, name="defines_ancestry", curie=OMOP_VOCABULARY.curie('defines_ancestry'),
                   model_uri=OMOP_VOCABULARY.defines_ancestry, domain=None, range=Optional[int])

slots.reverse_relationship_id = Slot(uri=OMOP_VOCABULARY.reverse_relationship_id, name="reverse_relationship_id", curie=OMOP_VOCABULARY.curie('reverse_relationship_id'),
                   model_uri=OMOP_VOCABULARY.reverse_relationship_id, domain=None, range=Optional[str])

slots.relationship_concept_id = Slot(uri=OMOP_VOCABULARY.relationship_concept_id, name="relationship_concept_id", curie=OMOP_VOCABULARY.curie('relationship_concept_id'),
                   model_uri=OMOP_VOCABULARY.relationship_concept_id, domain=None, range=Optional[int])

slots.relationship_list = Slot(uri=OMOP_VOCABULARY.relationship_list, name="relationship_list", curie=OMOP_VOCABULARY.curie('relationship_list'),
                   model_uri=OMOP_VOCABULARY.relationship_list, domain=None, range=Optional[Union[Union[dict, RELATIONSHIP], List[Union[dict, RELATIONSHIP]]]])

slots.vocabulary_name = Slot(uri=OMOP_VOCABULARY.vocabulary_name, name="vocabulary_name", curie=OMOP_VOCABULARY.curie('vocabulary_name'),
                   model_uri=OMOP_VOCABULARY.vocabulary_name, domain=None, range=Optional[str])

slots.vocabulary_reference = Slot(uri=OMOP_VOCABULARY.vocabulary_reference, name="vocabulary_reference", curie=OMOP_VOCABULARY.curie('vocabulary_reference'),
                   model_uri=OMOP_VOCABULARY.vocabulary_reference, domain=None, range=Optional[str])

slots.vocabulary_version = Slot(uri=OMOP_VOCABULARY.vocabulary_version, name="vocabulary_version", curie=OMOP_VOCABULARY.curie('vocabulary_version'),
                   model_uri=OMOP_VOCABULARY.vocabulary_version, domain=None, range=Optional[str])

slots.vocabulary_concept_id = Slot(uri=OMOP_VOCABULARY.vocabulary_concept_id, name="vocabulary_concept_id", curie=OMOP_VOCABULARY.curie('vocabulary_concept_id'),
                   model_uri=OMOP_VOCABULARY.vocabulary_concept_id, domain=None, range=Optional[int])

slots.vocabulary_list = Slot(uri=OMOP_VOCABULARY.vocabulary_list, name="vocabulary_list", curie=OMOP_VOCABULARY.curie('vocabulary_list'),
                   model_uri=OMOP_VOCABULARY.vocabulary_list, domain=None, range=Optional[Union[Union[dict, VOCABULARY], List[Union[dict, VOCABULARY]]]])