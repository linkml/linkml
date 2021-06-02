# Auto generated from organization.yaml by pythongen.py version: 0.4.0
# Generation date: 2020-12-08 16:49
# Schema: organization
#
# id: http://example.org/sample/organization
# description:
# license:

import dataclasses
import sys
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace


metamodel_version = "1.4.3"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ORGDATA = CurieNamespace('ORGDATA', 'http://example.org/sample/organization/data/')
XSD = CurieNamespace('xsd', 'http://example.org/UNKNOWN/xsd/')
DEFAULT_ = CurieNamespace('', 'http://example.org/sample/organization/')


# Types
class YearCount(int):
    type_class_uri = XSD.int
    type_class_curie = "xsd:int"
    type_name = "yearCount"
    type_model_uri = URIRef("http://example.org/sample/organization/YearCount")


class String(str):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("http://example.org/sample/organization/String")


# Class references
class OrganizationId(extended_str):
    pass


class EmployeeId(extended_str):
    pass


class ManagerId(EmployeeId):
    pass


@dataclass
class Organization(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Organization")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "organization"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Organization")

    id: Union[str, OrganizationId]
    name: Optional[str] = None
    has_boss: Optional[Union[dict, "Manager"]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, OrganizationId):
            self.id = OrganizationId(self.id)
        if self.has_boss is not None and not isinstance(self.has_boss, Manager):
            self.has_boss = Manager(self.has_boss)
        super().__post_init__(**kwargs)


@dataclass
class Employee(YAMLRoot):
    """
    A person
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Employee")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "employee"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Employee")

    id: Union[str, EmployeeId]
    last_name: str
    first_name: Optional[str] = None
    aliases: List[str] = empty_list()
    age_in_years: Optional[int] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, EmployeeId):
            self.id = EmployeeId(self.id)
        if self.last_name is None:
            raise ValueError(f"last_name must be supplied")
        super().__post_init__(**kwargs)


@dataclass
class Manager(Employee):
    """
    An employee who manages others
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Manager")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "manager"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Manager")

    id: Union[str, ManagerId] = None
    last_name: str = None
    has_employees: Dict[Union[str, EmployeeId], Union[dict, Employee]] = empty_dict()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, ManagerId):
            self.id = ManagerId(self.id)
        for k, v in self.has_employees.items():
            if not isinstance(v, Employee):
                self.has_employees[k] = Employee(id=k, **({} if v is None else v))
        super().__post_init__(**kwargs)



# Slots
class slots:
    pass

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                      model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.name = Slot(uri=DEFAULT_.name, name="name", curie=DEFAULT_.curie('name'),
                      model_uri=DEFAULT_.name, domain=None, range=Optional[str])

slots.aliases = Slot(uri=DEFAULT_.aliases, name="aliases", curie=DEFAULT_.curie('aliases'),
                      model_uri=DEFAULT_.aliases, domain=None, range=List[str])

slots.first_name = Slot(uri=DEFAULT_.first_name, name="first name", curie=DEFAULT_.curie('first_name'),
                      model_uri=DEFAULT_.first_name, domain=None, range=Optional[str])

slots.last_name = Slot(uri=DEFAULT_.last_name, name="last name", curie=DEFAULT_.curie('last_name'),
                      model_uri=DEFAULT_.last_name, domain=None, range=Optional[str])

slots.age_in_years = Slot(uri=DEFAULT_.age_in_years, name="age in years", curie=DEFAULT_.curie('age_in_years'),
                      model_uri=DEFAULT_.age_in_years, domain=None, range=Optional[int])

slots.has_employees = Slot(uri=DEFAULT_.has_employees, name="has employees", curie=DEFAULT_.curie('has_employees'),
                      model_uri=DEFAULT_.has_employees, domain=None, range=Dict[Union[str, EmployeeId], Union[dict, Employee]])

slots.has_boss = Slot(uri=DEFAULT_.has_boss, name="has boss", curie=DEFAULT_.curie('has_boss'),
                      model_uri=DEFAULT_.has_boss, domain=None, range=Optional[Union[dict, Manager]])

slots.employee_last_name = Slot(uri=DEFAULT_.last_name, name="employee_last name", curie=DEFAULT_.curie('last_name'),
                      model_uri=DEFAULT_.employee_last_name, domain=Employee, range=str)
