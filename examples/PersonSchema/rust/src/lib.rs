#![allow(non_camel_case_types)]

#[cfg(feature = "serde")]
mod serde_utils;
pub mod poly;
pub mod poly_containers;

#[cfg(feature = "serde")]
use serde_yml as _ ;
use chrono::NaiveDate;
#[cfg(feature = "pyo3")]
use pyo3::{FromPyObject,prelude::*};
#[cfg(feature = "serde")]
use serde::{Deserialize,Serialize,de::IntoDeserializer};
use serde_value::Value;
#[cfg(feature = "serde")]
use serde_path_to_error;
use std::collections::HashMap;
use std::collections::BTreeMap;

// Types

pub type string = String;
pub type integer = String;
pub type boolean = String;
pub type float = f64;
pub type double = f64;
pub type decimal = String;
pub type time = String;
pub type date = String;
pub type datetime = String;
pub type date_or_datetime = String;
pub type uriorcurie = String;
pub type curie = String;
pub type uri = String;
pub type ncname = String;
pub type objectidentifier = String;
pub type nodeidentifier = String;
pub type jsonpointer = String;
pub type jsonpath = String;
pub type sparqlpath = String;

// Slots

pub type id = String;
pub type name = String;
pub type description = String;
pub type image = String;
pub type gender = String;
pub type primary_email = String;
pub type birth_date = String;
pub type employed_at = Organization;
pub type is_current = bool;
pub type has_employment_history = Vec<EmploymentEvent>;
pub type has_medical_history = Vec<MedicalEvent>;
pub type has_familial_relationships = Vec<FamilialRelationship>;
pub type in_location = Place;
pub type current_address = Address;
pub type age_in_years = isize;
pub type related_to = String;
pub type type_ = String;
pub type street = String;
pub type city = String;
pub type mission_statement = String;
pub type founding_date = String;
pub type founding_location = Place;
pub type postal_code = String;
pub type started_at_time = NaiveDate;
pub type duration = f64;
pub type diagnosis = DiagnosisConcept;
pub type procedure = ProcedureConcept;
pub type ended_at_time = NaiveDate;
pub type persons = Vec<Person>;
pub type organizations = Vec<Organization>;
pub type aliases = Vec<String>;

// Enums

#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum FamilialRelationshipType {
    SIBLINGOF,
    PARENTOF,
    CHILDOF,
}
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum GenderType {
    NonbinaryMan,
    NonbinaryWoman,
    TransgenderWoman,
    TransgenderMan,
    CisgenderMan,
    CisgenderWoman,
}
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum DiagnosisType {
}

// Classes

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct NamedThing {
    pub id: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub name: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub image: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl NamedThing {
    #[new]
    pub fn new(id: String, name: Option<String>, description: Option<String>, image: Option<String>) -> Self {
        NamedThing{id, name, description, image}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<NamedThing>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<NamedThing> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<NamedThing>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid NamedThing",
        ))
    }
}
#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for NamedThing {
    type Key   = String;
        
    type Value = String;
    type Error = String;

    fn extract_key(&self) -> &Self::Key {
        return &self.id;
    }

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map = match v {
            Value::Map(m) => m,
            _ => return Err("ClassDefinition must be a mapping".into()),
        };
        map.insert(Value::String("id".into()), Value::String(k));
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }
    }


        
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map:  BTreeMap<Value, Value> = BTreeMap::new();
        map.insert(Value::String("id".into()), Value::String(k));
        map.insert(Value::String("name".into()), v);
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }        

    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature="serde", serde(untagged))]
pub enum NamedThingOrSubtype {    NamedThing(NamedThing),     Person(Person),     Organization(Organization),     Concept(Concept),     DiagnosisConcept(DiagnosisConcept),     ProcedureConcept(ProcedureConcept)}

impl From<NamedThing>   for NamedThingOrSubtype { fn from(x: NamedThing)   -> Self { Self::NamedThing(x) } }
impl From<Person>   for NamedThingOrSubtype { fn from(x: Person)   -> Self { Self::Person(x) } }
impl From<Organization>   for NamedThingOrSubtype { fn from(x: Organization)   -> Self { Self::Organization(x) } }
impl From<Concept>   for NamedThingOrSubtype { fn from(x: Concept)   -> Self { Self::Concept(x) } }
impl From<DiagnosisConcept>   for NamedThingOrSubtype { fn from(x: DiagnosisConcept)   -> Self { Self::DiagnosisConcept(x) } }
impl From<ProcedureConcept>   for NamedThingOrSubtype { fn from(x: ProcedureConcept)   -> Self { Self::ProcedureConcept(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for NamedThingOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<NamedThing>() {
            return Ok(NamedThingOrSubtype::NamedThing(val));
        }        if let Ok(val) = ob.extract::<Person>() {
            return Ok(NamedThingOrSubtype::Person(val));
        }        if let Ok(val) = ob.extract::<Organization>() {
            return Ok(NamedThingOrSubtype::Organization(val));
        }        if let Ok(val) = ob.extract::<Concept>() {
            return Ok(NamedThingOrSubtype::Concept(val));
        }        if let Ok(val) = ob.extract::<DiagnosisConcept>() {
            return Ok(NamedThingOrSubtype::DiagnosisConcept(val));
        }        if let Ok(val) = ob.extract::<ProcedureConcept>() {
            return Ok(NamedThingOrSubtype::ProcedureConcept(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid NamedThingOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for NamedThingOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            NamedThingOrSubtype::NamedThing(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::Person(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::Organization(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::Concept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::DiagnosisConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::ProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<NamedThingOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<NamedThingOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<NamedThingOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid NamedThingOrSubtype",
        ))
    }
}

#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for NamedThingOrSubtype {
    type Key       = String;
    type Value     = serde_value::Value;
    type Error     = String;

    fn from_pair_mapping(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
        if let Ok(x) = NamedThing::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::NamedThing(x));
        }
        if let Ok(x) = Person::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::Person(x));
        }
        if let Ok(x) = Organization::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::Organization(x));
        }
        if let Ok(x) = Concept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::Concept(x));
        }
        if let Ok(x) = DiagnosisConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::DiagnosisConcept(x));
        }
        if let Ok(x) = ProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::ProcedureConcept(x));
        }
        Err("none of the variants matched the mapping form".into())
    }

    fn from_pair_simple(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
        if let Ok(x) = NamedThing::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::NamedThing(x));
        }
        if let Ok(x) = Person::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::Person(x));
        }
        if let Ok(x) = Organization::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::Organization(x));
        }
        if let Ok(x) = Concept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::Concept(x));
        }
        if let Ok(x) = DiagnosisConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::DiagnosisConcept(x));
        }
        if let Ok(x) = ProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::ProcedureConcept(x));
        }
        Err("none of the variants support the primitive form".into())
    }

    fn extract_key(&self) -> &Self::Key {
        match self {
            NamedThingOrSubtype::NamedThing(inner) => inner.extract_key(),
            NamedThingOrSubtype::Person(inner) => inner.extract_key(),
            NamedThingOrSubtype::Organization(inner) => inner.extract_key(),
            NamedThingOrSubtype::Concept(inner) => inner.extract_key(),
            NamedThingOrSubtype::DiagnosisConcept(inner) => inner.extract_key(),
            NamedThingOrSubtype::ProcedureConcept(inner) => inner.extract_key(),
        }
    }
}


#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Person {
    #[cfg_attr(feature = "serde", serde(default))]
    pub primary_email: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub birth_date: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub age_in_years: Option<isize>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub gender: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub current_address: Option<Address>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_employment_history: Vec<EmploymentEvent>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_familial_relationships: Vec<Box<FamilialRelationship>>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_medical_history: Vec<MedicalEvent>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value"))]#[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Vec<String>,
    pub id: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub name: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub image: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Person {
    #[new]
    pub fn new(primary_email: Option<String>, birth_date: Option<String>, age_in_years: Option<isize>, gender: Option<String>, current_address: Option<Address>, has_employment_history: Vec<EmploymentEvent>, has_familial_relationships: Vec<Box<FamilialRelationship>>, has_medical_history: Vec<MedicalEvent>, aliases: Vec<String>, id: String, name: Option<String>, description: Option<String>, image: Option<String>) -> Self {
        Person{primary_email, birth_date, age_in_years, gender, current_address, has_employment_history, has_familial_relationships, has_medical_history, aliases, id, name, description, image}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Person>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Person> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Person>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Person",
        ))
    }
}
#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for Person {
    type Key   = String;
        
    type Value = String;
    type Error = String;

    fn extract_key(&self) -> &Self::Key {
        return &self.id;
    }

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map = match v {
            Value::Map(m) => m,
            _ => return Err("ClassDefinition must be a mapping".into()),
        };
        map.insert(Value::String("id".into()), Value::String(k));
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }
    }


        
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map:  BTreeMap<Value, Value> = BTreeMap::new();
        map.insert(Value::String("id".into()), Value::String(k));
        map.insert(Value::String("primary_email".into()), v);
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }        

    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct HasAliases {
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value"))]#[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Vec<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl HasAliases {
    #[new]
    pub fn new(aliases: Vec<String>) -> Self {
        HasAliases{aliases}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<HasAliases>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<HasAliases> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<HasAliases>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid HasAliases",
        ))
    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature="serde", serde(untagged))]
pub enum HasAliasesOrSubtype {    HasAliases(HasAliases),     Person(Person),     Organization(Organization),     Place(Place)}

impl From<HasAliases>   for HasAliasesOrSubtype { fn from(x: HasAliases)   -> Self { Self::HasAliases(x) } }
impl From<Person>   for HasAliasesOrSubtype { fn from(x: Person)   -> Self { Self::Person(x) } }
impl From<Organization>   for HasAliasesOrSubtype { fn from(x: Organization)   -> Self { Self::Organization(x) } }
impl From<Place>   for HasAliasesOrSubtype { fn from(x: Place)   -> Self { Self::Place(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for HasAliasesOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<HasAliases>() {
            return Ok(HasAliasesOrSubtype::HasAliases(val));
        }        if let Ok(val) = ob.extract::<Person>() {
            return Ok(HasAliasesOrSubtype::Person(val));
        }        if let Ok(val) = ob.extract::<Organization>() {
            return Ok(HasAliasesOrSubtype::Organization(val));
        }        if let Ok(val) = ob.extract::<Place>() {
            return Ok(HasAliasesOrSubtype::Place(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid HasAliasesOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for HasAliasesOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            HasAliasesOrSubtype::HasAliases(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            HasAliasesOrSubtype::Person(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            HasAliasesOrSubtype::Organization(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            HasAliasesOrSubtype::Place(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<HasAliasesOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<HasAliasesOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<HasAliasesOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid HasAliasesOrSubtype",
        ))
    }
}



#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Organization {
    #[cfg_attr(feature = "serde", serde(default))]
    pub mission_statement: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub founding_date: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub founding_location: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value"))]#[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Vec<String>,
    pub id: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub name: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub image: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Organization {
    #[new]
    pub fn new(mission_statement: Option<String>, founding_date: Option<String>, founding_location: Option<String>, aliases: Vec<String>, id: String, name: Option<String>, description: Option<String>, image: Option<String>) -> Self {
        Organization{mission_statement, founding_date, founding_location, aliases, id, name, description, image}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Organization>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Organization> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Organization>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Organization",
        ))
    }
}
#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for Organization {
    type Key   = String;
        
    type Value = String;
    type Error = String;

    fn extract_key(&self) -> &Self::Key {
        return &self.id;
    }

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map = match v {
            Value::Map(m) => m,
            _ => return Err("ClassDefinition must be a mapping".into()),
        };
        map.insert(Value::String("id".into()), Value::String(k));
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }
    }


        
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map:  BTreeMap<Value, Value> = BTreeMap::new();
        map.insert(Value::String("id".into()), Value::String(k));
        map.insert(Value::String("mission_statement".into()), v);
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }        

    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Place {
    pub id: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub name: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value"))]#[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Vec<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Place {
    #[new]
    pub fn new(id: String, name: Option<String>, aliases: Vec<String>) -> Self {
        Place{id, name, aliases}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Place>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Place> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Place>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Place",
        ))
    }
}
#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for Place {
    type Key   = String;
        
    type Value = String;
    type Error = String;

    fn extract_key(&self) -> &Self::Key {
        return &self.id;
    }

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map = match v {
            Value::Map(m) => m,
            _ => return Err("ClassDefinition must be a mapping".into()),
        };
        map.insert(Value::String("id".into()), Value::String(k));
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }
    }


        
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map:  BTreeMap<Value, Value> = BTreeMap::new();
        map.insert(Value::String("id".into()), Value::String(k));
        map.insert(Value::String("name".into()), v);
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }        

    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Address {
    #[cfg_attr(feature = "serde", serde(default))]
    pub street: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub city: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub postal_code: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Address {
    #[new]
    pub fn new(street: Option<String>, city: Option<String>, postal_code: Option<String>) -> Self {
        Address{street, city, postal_code}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Address>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Address> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Address>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Address",
        ))
    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Event {
    #[cfg_attr(feature = "serde", serde(default))]
    pub started_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub ended_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub duration: Option<f64>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub is_current: Option<bool>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Event {
    #[new]
    pub fn new(started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, duration: Option<f64>, is_current: Option<bool>) -> Self {
        Event{started_at_time, ended_at_time, duration, is_current}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Event>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Event> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Event>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Event",
        ))
    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature="serde", serde(untagged))]
pub enum EventOrSubtype {    Event(Event),     EmploymentEvent(EmploymentEvent),     MedicalEvent(MedicalEvent)}

impl From<Event>   for EventOrSubtype { fn from(x: Event)   -> Self { Self::Event(x) } }
impl From<EmploymentEvent>   for EventOrSubtype { fn from(x: EmploymentEvent)   -> Self { Self::EmploymentEvent(x) } }
impl From<MedicalEvent>   for EventOrSubtype { fn from(x: MedicalEvent)   -> Self { Self::MedicalEvent(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for EventOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Event>() {
            return Ok(EventOrSubtype::Event(val));
        }        if let Ok(val) = ob.extract::<EmploymentEvent>() {
            return Ok(EventOrSubtype::EmploymentEvent(val));
        }        if let Ok(val) = ob.extract::<MedicalEvent>() {
            return Ok(EventOrSubtype::MedicalEvent(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid EventOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for EventOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            EventOrSubtype::Event(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            EventOrSubtype::EmploymentEvent(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            EventOrSubtype::MedicalEvent(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<EventOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<EventOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<EventOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid EventOrSubtype",
        ))
    }
}



#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Concept {
    pub id: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub name: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub image: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Concept {
    #[new]
    pub fn new(id: String, name: Option<String>, description: Option<String>, image: Option<String>) -> Self {
        Concept{id, name, description, image}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Concept>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Concept> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Concept>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Concept",
        ))
    }
}
#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for Concept {
    type Key   = String;
        
    type Value = String;
    type Error = String;

    fn extract_key(&self) -> &Self::Key {
        return &self.id;
    }

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map = match v {
            Value::Map(m) => m,
            _ => return Err("ClassDefinition must be a mapping".into()),
        };
        map.insert(Value::String("id".into()), Value::String(k));
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }
    }


        
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map:  BTreeMap<Value, Value> = BTreeMap::new();
        map.insert(Value::String("id".into()), Value::String(k));
        map.insert(Value::String("name".into()), v);
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }        

    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature="serde", serde(untagged))]
pub enum ConceptOrSubtype {    Concept(Concept),     DiagnosisConcept(DiagnosisConcept),     ProcedureConcept(ProcedureConcept)}

impl From<Concept>   for ConceptOrSubtype { fn from(x: Concept)   -> Self { Self::Concept(x) } }
impl From<DiagnosisConcept>   for ConceptOrSubtype { fn from(x: DiagnosisConcept)   -> Self { Self::DiagnosisConcept(x) } }
impl From<ProcedureConcept>   for ConceptOrSubtype { fn from(x: ProcedureConcept)   -> Self { Self::ProcedureConcept(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for ConceptOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Concept>() {
            return Ok(ConceptOrSubtype::Concept(val));
        }        if let Ok(val) = ob.extract::<DiagnosisConcept>() {
            return Ok(ConceptOrSubtype::DiagnosisConcept(val));
        }        if let Ok(val) = ob.extract::<ProcedureConcept>() {
            return Ok(ConceptOrSubtype::ProcedureConcept(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid ConceptOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for ConceptOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            ConceptOrSubtype::Concept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            ConceptOrSubtype::DiagnosisConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            ConceptOrSubtype::ProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<ConceptOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<ConceptOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<ConceptOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid ConceptOrSubtype",
        ))
    }
}

#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for ConceptOrSubtype {
    type Key       = String;
    type Value     = serde_value::Value;
    type Error     = String;

    fn from_pair_mapping(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
        if let Ok(x) = Concept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::Concept(x));
        }
        if let Ok(x) = DiagnosisConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::DiagnosisConcept(x));
        }
        if let Ok(x) = ProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::ProcedureConcept(x));
        }
        Err("none of the variants matched the mapping form".into())
    }

    fn from_pair_simple(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
        if let Ok(x) = Concept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::Concept(x));
        }
        if let Ok(x) = DiagnosisConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::DiagnosisConcept(x));
        }
        if let Ok(x) = ProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::ProcedureConcept(x));
        }
        Err("none of the variants support the primitive form".into())
    }

    fn extract_key(&self) -> &Self::Key {
        match self {
            ConceptOrSubtype::Concept(inner) => inner.extract_key(),
            ConceptOrSubtype::DiagnosisConcept(inner) => inner.extract_key(),
            ConceptOrSubtype::ProcedureConcept(inner) => inner.extract_key(),
        }
    }
}


#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct DiagnosisConcept {
    pub id: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub name: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub image: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl DiagnosisConcept {
    #[new]
    pub fn new(id: String, name: Option<String>, description: Option<String>, image: Option<String>) -> Self {
        DiagnosisConcept{id, name, description, image}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<DiagnosisConcept>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<DiagnosisConcept> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<DiagnosisConcept>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid DiagnosisConcept",
        ))
    }
}
#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for DiagnosisConcept {
    type Key   = String;
        
    type Value = String;
    type Error = String;

    fn extract_key(&self) -> &Self::Key {
        return &self.id;
    }

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map = match v {
            Value::Map(m) => m,
            _ => return Err("ClassDefinition must be a mapping".into()),
        };
        map.insert(Value::String("id".into()), Value::String(k));
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }
    }


        
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map:  BTreeMap<Value, Value> = BTreeMap::new();
        map.insert(Value::String("id".into()), Value::String(k));
        map.insert(Value::String("name".into()), v);
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }        

    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct ProcedureConcept {
    pub id: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub name: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub image: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl ProcedureConcept {
    #[new]
    pub fn new(id: String, name: Option<String>, description: Option<String>, image: Option<String>) -> Self {
        ProcedureConcept{id, name, description, image}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<ProcedureConcept>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<ProcedureConcept> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<ProcedureConcept>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid ProcedureConcept",
        ))
    }
}
#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for ProcedureConcept {
    type Key   = String;
        
    type Value = String;
    type Error = String;

    fn extract_key(&self) -> &Self::Key {
        return &self.id;
    }

    fn from_pair_mapping(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map = match v {
            Value::Map(m) => m,
            _ => return Err("ClassDefinition must be a mapping".into()),
        };
        map.insert(Value::String("id".into()), Value::String(k));
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }
    }


        
    fn from_pair_simple(k: Self::Key, v: Value) -> Result<Self,Self::Error> {
        let mut map:  BTreeMap<Value, Value> = BTreeMap::new();
        map.insert(Value::String("id".into()), Value::String(k));
        map.insert(Value::String("name".into()), v);
        let de          = Value::Map(map).into_deserializer();
        match serde_path_to_error::deserialize(de) {
            Ok(ok)  => Ok(ok),
            Err(e)  => Err(format!("at `{}`: {}", e.path(), e.inner())),
        }        

    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Relationship {
    #[cfg_attr(feature = "serde", serde(default))]
    pub started_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub ended_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub related_to: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub type_: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Relationship {
    #[new]
    pub fn new(started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, related_to: Option<String>, type_: Option<String>) -> Self {
        Relationship{started_at_time, ended_at_time, related_to, type_}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Relationship>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Relationship> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Relationship>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Relationship",
        ))
    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature="serde", serde(untagged))]
pub enum RelationshipOrSubtype {    Relationship(Relationship),     FamilialRelationship(FamilialRelationship)}

impl From<Relationship>   for RelationshipOrSubtype { fn from(x: Relationship)   -> Self { Self::Relationship(x) } }
impl From<FamilialRelationship>   for RelationshipOrSubtype { fn from(x: FamilialRelationship)   -> Self { Self::FamilialRelationship(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for RelationshipOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Relationship>() {
            return Ok(RelationshipOrSubtype::Relationship(val));
        }        if let Ok(val) = ob.extract::<FamilialRelationship>() {
            return Ok(RelationshipOrSubtype::FamilialRelationship(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid RelationshipOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for RelationshipOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            RelationshipOrSubtype::Relationship(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            RelationshipOrSubtype::FamilialRelationship(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<RelationshipOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<RelationshipOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<RelationshipOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid RelationshipOrSubtype",
        ))
    }
}



#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct FamilialRelationship {
    #[cfg_attr(feature = "serde", serde(default))]
    pub started_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub ended_at_time: Option<NaiveDate>,
    pub related_to: String,
    pub type_: String
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl FamilialRelationship {
    #[new]
    pub fn new(started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, related_to: String, type_: String) -> Self {
        FamilialRelationship{started_at_time, ended_at_time, related_to, type_}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<FamilialRelationship>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<FamilialRelationship> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<FamilialRelationship>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid FamilialRelationship",
        ))
    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct EmploymentEvent {
    #[cfg_attr(feature = "serde", serde(default))]
    pub employed_at: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub started_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub ended_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub duration: Option<f64>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub is_current: Option<bool>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl EmploymentEvent {
    #[new]
    pub fn new(employed_at: Option<String>, started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, duration: Option<f64>, is_current: Option<bool>) -> Self {
        EmploymentEvent{employed_at, started_at_time, ended_at_time, duration, is_current}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<EmploymentEvent>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<EmploymentEvent> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<EmploymentEvent>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid EmploymentEvent",
        ))
    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct MedicalEvent {
    #[cfg_attr(feature = "serde", serde(default))]
    pub in_location: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub diagnosis: Option<DiagnosisConcept>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub procedure: Option<ProcedureConcept>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub started_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub ended_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub duration: Option<f64>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub is_current: Option<bool>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl MedicalEvent {
    #[new]
    pub fn new(in_location: Option<String>, diagnosis: Option<DiagnosisConcept>, procedure: Option<ProcedureConcept>, started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, duration: Option<f64>, is_current: Option<bool>) -> Self {
        MedicalEvent{in_location, diagnosis, procedure, started_at_time, ended_at_time, duration, is_current}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<MedicalEvent>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<MedicalEvent> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<MedicalEvent>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid MedicalEvent",
        ))
    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct WithLocation {
    #[cfg_attr(feature = "serde", serde(default))]
    pub in_location: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl WithLocation {
    #[new]
    pub fn new(in_location: Option<String>) -> Self {
        WithLocation{in_location}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<WithLocation>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<WithLocation> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<WithLocation>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid WithLocation",
        ))
    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Container {
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_inlined_dict_list"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub persons: Vec<Person>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_inlined_dict_list"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub organizations: Vec<Organization>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Container {
    #[new]
    pub fn new(persons: Vec<Person>, organizations: Vec<Organization>) -> Self {
        Container{persons, organizations}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<Container>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<Container> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Container>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid Container",
        ))
    }
}



