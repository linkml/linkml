# Auto generated from inference-example.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-07-01T19:52:59
# Schema: inference
#
# id: https://w3id.org/linkml/examples/inference
# description: This demonstrates the use of inference
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from jsonasobj2 import as_dict
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list
from linkml_runtime.utils.yamlutils import YAMLRoot
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Decimal
from linkml_runtime.utils.metamodelcore import Bool, Decimal

metamodel_version = "1.7.0"

# Namespaces
EX = CurieNamespace('ex', 'https://w3id.org/linkml/examples/inference/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
DEFAULT_ = EX


# Types

# Class references



@dataclass
class Term(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Term
    class_class_curie: ClassVar[str] = "ex:Term"
    class_name: ClassVar[str] = "Term"
    class_model_uri: ClassVar[URIRef] = EX.Term

    id: Optional[str] = None
    name: Optional[str] = None
    synonyms: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.synonyms, list):
            self.synonyms = [self.synonyms] if self.synonyms is not None else []
        self.synonyms = [v if isinstance(v, str) else str(v) for v in self.synonyms]

        super().__post_init__(**kwargs)


@dataclass
class Person(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Person
    class_class_curie: ClassVar[str] = "ex:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = EX.Person

    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    age_in_years: Optional[Decimal] = None
    age_in_months: Optional[Decimal] = None
    primary_address: Optional[Union[dict, "Address"]] = None
    description: Optional[str] = None
    is_juvenile: Optional[Union[bool, Bool]] = None
    age_category: Optional[Union[str, "AgeEnum"]] = None
    slot_with_spaces: Optional[str] = None
    derived_slot_with_spaces: Optional[str] = None
    derived_expression_from_spaces: Optional[str] = None
    summary: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.first_name is not None and not isinstance(self.first_name, str):
            self.first_name = str(self.first_name)

        if self.last_name is not None and not isinstance(self.last_name, str):
            self.last_name = str(self.last_name)

        if self.full_name is not None and not isinstance(self.full_name, str):
            self.full_name = str(self.full_name)

        if self.age_in_years is not None and not isinstance(self.age_in_years, Decimal):
            self.age_in_years = Decimal(self.age_in_years)

        if self.age_in_months is not None and not isinstance(self.age_in_months, Decimal):
            self.age_in_months = Decimal(self.age_in_months)

        if self.primary_address is not None and not isinstance(self.primary_address, Address):
            self.primary_address = Address(**as_dict(self.primary_address))

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.is_juvenile is not None and not isinstance(self.is_juvenile, Bool):
            self.is_juvenile = Bool(self.is_juvenile)

        if self.age_category is not None and not isinstance(self.age_category, AgeEnum):
            self.age_category = AgeEnum(self.age_category)

        if self.slot_with_spaces is not None and not isinstance(self.slot_with_spaces, str):
            self.slot_with_spaces = str(self.slot_with_spaces)

        if self.derived_slot_with_spaces is not None and not isinstance(self.derived_slot_with_spaces, str):
            self.derived_slot_with_spaces = str(self.derived_slot_with_spaces)

        if self.derived_expression_from_spaces is not None and not isinstance(self.derived_expression_from_spaces, str):
            self.derived_expression_from_spaces = str(self.derived_expression_from_spaces)

        if self.summary is not None and not isinstance(self.summary, str):
            self.summary = str(self.summary)

        super().__post_init__(**kwargs)


@dataclass
class Evil(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Evil
    class_class_curie: ClassVar[str] = "ex:Evil"
    class_name: ClassVar[str] = "Evil"
    class_model_uri: ClassVar[URIRef] = EX.Evil

    prohibited: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.prohibited is not None and not isinstance(self.prohibited, str):
            self.prohibited = str(self.prohibited)

        super().__post_init__(**kwargs)


@dataclass
class Relationship(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Relationship
    class_class_curie: ClassVar[str] = "ex:Relationship"
    class_name: ClassVar[str] = "Relationship"
    class_model_uri: ClassVar[URIRef] = EX.Relationship

    person1: Optional[Union[dict, Person]] = None
    person2: Optional[Union[dict, Person]] = None
    type: Optional[str] = None
    description: Optional[str] = None
    description2: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.person1 is not None and not isinstance(self.person1, Person):
            self.person1 = Person(**as_dict(self.person1))

        if self.person2 is not None and not isinstance(self.person2, Person):
            self.person2 = Person(**as_dict(self.person2))

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.description2 is not None and not isinstance(self.description2, str):
            self.description2 = str(self.description2)

        super().__post_init__(**kwargs)


@dataclass
class Address(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Address
    class_class_curie: ClassVar[str] = "ex:Address"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = EX.Address

    street: Optional[str] = None
    city: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.street is not None and not isinstance(self.street, str):
            self.street = str(self.street)

        if self.city is not None and not isinstance(self.city, str):
            self.city = str(self.city)

        super().__post_init__(**kwargs)


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX.Container
    class_class_curie: ClassVar[str] = "ex:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = EX.Container

    persons: Optional[Union[Union[dict, Person], list[Union[dict, Person]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if not isinstance(self.persons, list):
            self.persons = [self.persons] if self.persons is not None else []
        self.persons = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.persons]

        super().__post_init__(**kwargs)


# Enumerations
class AgeEnum(EnumDefinitionImpl):

    infant = PermissibleValue(text="infant")
    juvenile = PermissibleValue(text="juvenile")
    adult = PermissibleValue(text="adult")

    _defn = EnumDefinition(
        name="AgeEnum",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=EX.id, name="id", curie=EX.curie('id'),
                   model_uri=EX.id, domain=None, range=Optional[str])

slots.name = Slot(uri=EX.name, name="name", curie=EX.curie('name'),
                   model_uri=EX.name, domain=None, range=Optional[str])

slots.synonyms = Slot(uri=EX.synonyms, name="synonyms", curie=EX.curie('synonyms'),
                   model_uri=EX.synonyms, domain=None, range=Optional[Union[str, list[str]]])

slots.full_name = Slot(uri=EX.full_name, name="full_name", curie=EX.curie('full_name'),
                   model_uri=EX.full_name, domain=None, range=Optional[str])

slots.first_name = Slot(uri=EX.first_name, name="first_name", curie=EX.curie('first_name'),
                   model_uri=EX.first_name, domain=None, range=Optional[str])

slots.last_name = Slot(uri=EX.last_name, name="last_name", curie=EX.curie('last_name'),
                   model_uri=EX.last_name, domain=None, range=Optional[str])

slots.age_in_years = Slot(uri=EX.age_in_years, name="age_in_years", curie=EX.curie('age_in_years'),
                   model_uri=EX.age_in_years, domain=None, range=Optional[Decimal])

slots.age_in_months = Slot(uri=EX.age_in_months, name="age_in_months", curie=EX.curie('age_in_months'),
                   model_uri=EX.age_in_months, domain=None, range=Optional[Decimal])

slots.is_juvenile = Slot(uri=EX.is_juvenile, name="is_juvenile", curie=EX.curie('is_juvenile'),
                   model_uri=EX.is_juvenile, domain=None, range=Optional[Union[bool, Bool]])

slots.age_category = Slot(uri=EX.age_category, name="age_category", curie=EX.curie('age_category'),
                   model_uri=EX.age_category, domain=None, range=Optional[Union[str, "AgeEnum"]])

slots.prohibited = Slot(uri=EX.prohibited, name="prohibited", curie=EX.curie('prohibited'),
                   model_uri=EX.prohibited, domain=None, range=Optional[str])

slots.street = Slot(uri=EX.street, name="street", curie=EX.curie('street'),
                   model_uri=EX.street, domain=None, range=Optional[str])

slots.city = Slot(uri=EX.city, name="city", curie=EX.curie('city'),
                   model_uri=EX.city, domain=None, range=Optional[str])

slots.verbatim = Slot(uri=EX.verbatim, name="verbatim", curie=EX.curie('verbatim'),
                   model_uri=EX.verbatim, domain=None, range=Optional[str])

slots.primary_address = Slot(uri=EX.primary_address, name="primary_address", curie=EX.curie('primary_address'),
                   model_uri=EX.primary_address, domain=None, range=Optional[Union[dict, Address]])

slots.description = Slot(uri=EX.description, name="description", curie=EX.curie('description'),
                   model_uri=EX.description, domain=None, range=Optional[str])

slots.summary = Slot(uri=EX.summary, name="summary", curie=EX.curie('summary'),
                   model_uri=EX.summary, domain=None, range=Optional[str])

slots.slot_with_spaces = Slot(uri=EX.slot_with_spaces, name="slot with spaces", curie=EX.curie('slot_with_spaces'),
                   model_uri=EX.slot_with_spaces, domain=None, range=Optional[str])

slots.derived_slot_with_spaces = Slot(uri=EX.derived_slot_with_spaces, name="derived slot with spaces", curie=EX.curie('derived_slot_with_spaces'),
                   model_uri=EX.derived_slot_with_spaces, domain=None, range=Optional[str])

slots.derived_expression_from_spaces = Slot(uri=EX.derived_expression_from_spaces, name="derived expression from spaces", curie=EX.curie('derived_expression_from_spaces'),
                   model_uri=EX.derived_expression_from_spaces, domain=None, range=Optional[str])

slots.relationship__person1 = Slot(uri=EX.person1, name="relationship__person1", curie=EX.curie('person1'),
                   model_uri=EX.relationship__person1, domain=None, range=Optional[Union[dict, Person]])

slots.relationship__person2 = Slot(uri=EX.person2, name="relationship__person2", curie=EX.curie('person2'),
                   model_uri=EX.relationship__person2, domain=None, range=Optional[Union[dict, Person]])

slots.relationship__type = Slot(uri=EX.type, name="relationship__type", curie=EX.curie('type'),
                   model_uri=EX.relationship__type, domain=None, range=Optional[str])

slots.relationship__description = Slot(uri=EX.description, name="relationship__description", curie=EX.curie('description'),
                   model_uri=EX.relationship__description, domain=None, range=Optional[str])

slots.relationship__description2 = Slot(uri=EX.description2, name="relationship__description2", curie=EX.curie('description2'),
                   model_uri=EX.relationship__description2, domain=None, range=Optional[str])

slots.container__persons = Slot(uri=EX.persons, name="container__persons", curie=EX.curie('persons'),
                   model_uri=EX.container__persons, domain=None, range=Optional[Union[Union[dict, Person], list[Union[dict, Person]]]])

slots.Person_description = Slot(uri=EX.description, name="Person_description", curie=EX.curie('description'),
                   model_uri=EX.Person_description, domain=Person, range=Optional[str])

slots.Person_summary = Slot(uri=EX.summary, name="Person_summary", curie=EX.curie('summary'),
                   model_uri=EX.Person_summary, domain=Person, range=Optional[str])
