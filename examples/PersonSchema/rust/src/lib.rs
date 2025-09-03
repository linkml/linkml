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
pub type CrossReference = String;
pub type ImageURL = String;
pub type SalaryType = String;

// Slots

pub type id = uriorcurie;
pub type int_id = isize;
pub type name = String;
pub type description = String;
pub type image = String;
pub type gender = GenderType;
pub type telephone = String;
pub type primary_email = String;
pub type birth_date = String;
pub type employed_at = Organization;
pub type is_current = bool;
pub type has_employment_history = Vec<EmploymentEvent>;
pub type has_medical_history = Vec<MedicalEvent>;
pub type has_familial_relationships = Vec<FamilialRelationship>;
pub type has_interpersonal_relationships = Vec<InterPersonalRelationship>;
pub type in_location = Place;
pub type current_address = Address;
pub type age_in_years = isize;
pub type score = f64;
pub type related_to = Person;
pub type depicted_by = String;
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
pub type places = Vec<Place>;
pub type categories = Vec<String>;
pub type salary = f64;
pub type min_salary = f64;
pub type aliases = Vec<String>;
pub type headline = String;
pub type has_news_events = Vec<NewsEvent>;
pub type code_system = CodeSystem;
pub type mappings = Vec<String>;

// Enums

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum FamilialRelationshipType {
    SIBLINGOF,
    PARENTOF,
    CHILDOF,
}

impl core::fmt::Display for FamilialRelationshipType {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            FamilialRelationshipType::SIBLINGOF => f.write_str("SIBLINGOF"),
            FamilialRelationshipType::PARENTOF => f.write_str("PARENTOF"),
            FamilialRelationshipType::CHILDOF => f.write_str("CHILDOF"),
        }
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for FamilialRelationshipType {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s: &str = match self {
            FamilialRelationshipType::SIBLINGOF => "SIBLINGOF",
            FamilialRelationshipType::PARENTOF => "PARENTOF",
            FamilialRelationshipType::CHILDOF => "CHILDOF",
        };
        Ok(pyo3::types::PyString::new(py, s).into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for FamilialRelationshipType {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(s) = ob.extract::<&str>() {
            match s {
                "SIBLINGOF" => Ok(FamilialRelationshipType::SIBLINGOF),
                "PARENTOF" => Ok(FamilialRelationshipType::PARENTOF),
                "CHILDOF" => Ok(FamilialRelationshipType::CHILDOF),
                _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("invalid value for FamilialRelationshipType: {}", s),
                )),
            }
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                concat!("expected str for ", stringify!(FamilialRelationshipType)),
            ))
        }
    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum NonFamilialRelationshipType {
    COWORKEROF,
    ROOMMATEOF,
    BESTFRIENDOF,
    MORTALENEMYOF,
}

impl core::fmt::Display for NonFamilialRelationshipType {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            NonFamilialRelationshipType::COWORKEROF => f.write_str("COWORKEROF"),
            NonFamilialRelationshipType::ROOMMATEOF => f.write_str("ROOMMATEOF"),
            NonFamilialRelationshipType::BESTFRIENDOF => f.write_str("BESTFRIENDOF"),
            NonFamilialRelationshipType::MORTALENEMYOF => f.write_str("MORTALENEMYOF"),
        }
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for NonFamilialRelationshipType {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s: &str = match self {
            NonFamilialRelationshipType::COWORKEROF => "COWORKEROF",
            NonFamilialRelationshipType::ROOMMATEOF => "ROOMMATEOF",
            NonFamilialRelationshipType::BESTFRIENDOF => "BESTFRIENDOF",
            NonFamilialRelationshipType::MORTALENEMYOF => "MORTALENEMYOF",
        };
        Ok(pyo3::types::PyString::new(py, s).into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for NonFamilialRelationshipType {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(s) = ob.extract::<&str>() {
            match s {
                "COWORKEROF" => Ok(NonFamilialRelationshipType::COWORKEROF),
                "ROOMMATEOF" => Ok(NonFamilialRelationshipType::ROOMMATEOF),
                "BESTFRIENDOF" => Ok(NonFamilialRelationshipType::BESTFRIENDOF),
                "MORTALENEMYOF" => Ok(NonFamilialRelationshipType::MORTALENEMYOF),
                _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("invalid value for NonFamilialRelationshipType: {}", s),
                )),
            }
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                concat!("expected str for ", stringify!(NonFamilialRelationshipType)),
            ))
        }
    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum GenderType {
    NonbinaryMan,
    NonbinaryWoman,
    TransgenderWoman,
    TransgenderMan,
    CisgenderMan,
    CisgenderWoman,
}

impl core::fmt::Display for GenderType {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            GenderType::NonbinaryMan => f.write_str("NonbinaryMan"),
            GenderType::NonbinaryWoman => f.write_str("NonbinaryWoman"),
            GenderType::TransgenderWoman => f.write_str("TransgenderWoman"),
            GenderType::TransgenderMan => f.write_str("TransgenderMan"),
            GenderType::CisgenderMan => f.write_str("CisgenderMan"),
            GenderType::CisgenderWoman => f.write_str("CisgenderWoman"),
        }
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for GenderType {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s: &str = match self {
            GenderType::NonbinaryMan => "NonbinaryMan",
            GenderType::NonbinaryWoman => "NonbinaryWoman",
            GenderType::TransgenderWoman => "TransgenderWoman",
            GenderType::TransgenderMan => "TransgenderMan",
            GenderType::CisgenderMan => "CisgenderMan",
            GenderType::CisgenderWoman => "CisgenderWoman",
        };
        Ok(pyo3::types::PyString::new(py, s).into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for GenderType {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(s) = ob.extract::<&str>() {
            match s {
                "NonbinaryMan" => Ok(GenderType::NonbinaryMan),
                "NonbinaryWoman" => Ok(GenderType::NonbinaryWoman),
                "TransgenderWoman" => Ok(GenderType::TransgenderWoman),
                "TransgenderMan" => Ok(GenderType::TransgenderMan),
                "CisgenderMan" => Ok(GenderType::CisgenderMan),
                "CisgenderWoman" => Ok(GenderType::CisgenderWoman),
                _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("invalid value for GenderType: {}", s),
                )),
            }
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                concat!("expected str for ", stringify!(GenderType)),
            ))
        }
    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum DiagnosisType {
    Todo,
}

impl core::fmt::Display for DiagnosisType {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            DiagnosisType::Todo => f.write_str("Todo"),
        }
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for DiagnosisType {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s: &str = match self {
            DiagnosisType::Todo => "Todo",
        };
        Ok(pyo3::types::PyString::new(py, s).into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for DiagnosisType {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(s) = ob.extract::<&str>() {
            match s {
                "Todo" => Ok(DiagnosisType::Todo),
                _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("invalid value for DiagnosisType: {}", s),
                )),
            }
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                concat!("expected str for ", stringify!(DiagnosisType)),
            ))
        }
    }
}
#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
pub enum OrganizationType {
    NonProfit,
    ForProfit,
    Offshore,
    Charity,
    ShellCompany,
    LooseOrganization,
}

impl core::fmt::Display for OrganizationType {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            OrganizationType::NonProfit => f.write_str("NonProfit"),
            OrganizationType::ForProfit => f.write_str("ForProfit"),
            OrganizationType::Offshore => f.write_str("Offshore"),
            OrganizationType::Charity => f.write_str("Charity"),
            OrganizationType::ShellCompany => f.write_str("ShellCompany"),
            OrganizationType::LooseOrganization => f.write_str("LooseOrganization"),
        }
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for OrganizationType {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        let s: &str = match self {
            OrganizationType::NonProfit => "NonProfit",
            OrganizationType::ForProfit => "ForProfit",
            OrganizationType::Offshore => "Offshore",
            OrganizationType::Charity => "Charity",
            OrganizationType::ShellCompany => "ShellCompany",
            OrganizationType::LooseOrganization => "LooseOrganization",
        };
        Ok(pyo3::types::PyString::new(py, s).into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for OrganizationType {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(s) = ob.extract::<&str>() {
            match s {
                "NonProfit" => Ok(OrganizationType::NonProfit),
                "ForProfit" => Ok(OrganizationType::ForProfit),
                "Offshore" => Ok(OrganizationType::Offshore),
                "Charity" => Ok(OrganizationType::Charity),
                "ShellCompany" => Ok(OrganizationType::ShellCompany),
                "LooseOrganization" => Ok(OrganizationType::LooseOrganization),
                _ => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("invalid value for OrganizationType: {}", s),
                )),
            }
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                concat!("expected str for ", stringify!(OrganizationType)),
            ))
        }
    }
}

// Classes

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct NamedThing {
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl NamedThing {
    #[new]
    pub fn new(id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        NamedThing{id, name, description, depicted_by}
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
    type Key   = uriorcurie;
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
pub enum NamedThingOrSubtype {    Person(Person),     Organization(Organization),     Concept(Concept),     DiagnosisConcept(DiagnosisConcept),     ProcedureConcept(ProcedureConcept),     OperationProcedureConcept(OperationProcedureConcept),     ImagingProcedureConcept(ImagingProcedureConcept)}

impl From<Person>   for NamedThingOrSubtype { fn from(x: Person)   -> Self { Self::Person(x) } }
impl From<Organization>   for NamedThingOrSubtype { fn from(x: Organization)   -> Self { Self::Organization(x) } }
impl From<Concept>   for NamedThingOrSubtype { fn from(x: Concept)   -> Self { Self::Concept(x) } }
impl From<DiagnosisConcept>   for NamedThingOrSubtype { fn from(x: DiagnosisConcept)   -> Self { Self::DiagnosisConcept(x) } }
impl From<ProcedureConcept>   for NamedThingOrSubtype { fn from(x: ProcedureConcept)   -> Self { Self::ProcedureConcept(x) } }
impl From<OperationProcedureConcept>   for NamedThingOrSubtype { fn from(x: OperationProcedureConcept)   -> Self { Self::OperationProcedureConcept(x) } }
impl From<ImagingProcedureConcept>   for NamedThingOrSubtype { fn from(x: ImagingProcedureConcept)   -> Self { Self::ImagingProcedureConcept(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for NamedThingOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Person>() {
            return Ok(NamedThingOrSubtype::Person(val));
        }        if let Ok(val) = ob.extract::<Organization>() {
            return Ok(NamedThingOrSubtype::Organization(val));
        }        if let Ok(val) = ob.extract::<Concept>() {
            return Ok(NamedThingOrSubtype::Concept(val));
        }        if let Ok(val) = ob.extract::<DiagnosisConcept>() {
            return Ok(NamedThingOrSubtype::DiagnosisConcept(val));
        }        if let Ok(val) = ob.extract::<ProcedureConcept>() {
            return Ok(NamedThingOrSubtype::ProcedureConcept(val));
        }        if let Ok(val) = ob.extract::<OperationProcedureConcept>() {
            return Ok(NamedThingOrSubtype::OperationProcedureConcept(val));
        }        if let Ok(val) = ob.extract::<ImagingProcedureConcept>() {
            return Ok(NamedThingOrSubtype::ImagingProcedureConcept(val));
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
            NamedThingOrSubtype::Person(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::Organization(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::Concept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::DiagnosisConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::ProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::OperationProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            NamedThingOrSubtype::ImagingProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
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
        if let Ok(x) = OperationProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::OperationProcedureConcept(x));
        }
        if let Ok(x) = ImagingProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::ImagingProcedureConcept(x));
        }
        Err("none of the variants matched the mapping form".into())
    }

    fn from_pair_simple(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
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
        if let Ok(x) = OperationProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::OperationProcedureConcept(x));
        }
        if let Ok(x) = ImagingProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(NamedThingOrSubtype::ImagingProcedureConcept(x));
        }
        Err("none of the variants support the primitive form".into())
    }

    fn extract_key(&self) -> &Self::Key {
        match self {
            NamedThingOrSubtype::Person(inner) => inner.extract_key(),
            NamedThingOrSubtype::Organization(inner) => inner.extract_key(),
            NamedThingOrSubtype::Concept(inner) => inner.extract_key(),
            NamedThingOrSubtype::DiagnosisConcept(inner) => inner.extract_key(),
            NamedThingOrSubtype::ProcedureConcept(inner) => inner.extract_key(),
            NamedThingOrSubtype::OperationProcedureConcept(inner) => inner.extract_key(),
            NamedThingOrSubtype::ImagingProcedureConcept(inner) => inner.extract_key(),
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
    #[cfg_attr(feature = "serde", serde(alias = "age"))]
    pub age_in_years: Option<isize>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub gender: Option<GenderType>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub current_address: Option<Address>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub telephone: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_employment_history: Option<Vec<EmploymentEvent>>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_familial_relationships: Option<Vec<Box<FamilialRelationship>>>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_interpersonal_relationships: Option<Vec<Box<InterPersonalRelationship>>>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_medical_history: Option<Vec<MedicalEvent>>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Option<Vec<String>>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_news_events: Option<Vec<NewsEvent>>,
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Person {
    #[new]
    pub fn new(primary_email: Option<String>, birth_date: Option<String>, age_in_years: Option<isize>, gender: Option<GenderType>, current_address: Option<Address>, telephone: Option<String>, has_employment_history: Option<Vec<EmploymentEvent>>, has_familial_relationships: Option<Vec<Box<FamilialRelationship>>>, has_interpersonal_relationships: Option<Vec<Box<InterPersonalRelationship>>>, has_medical_history: Option<Vec<MedicalEvent>>, aliases: Option<Vec<String>>, has_news_events: Option<Vec<NewsEvent>>, id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        Person{primary_email, birth_date, age_in_years, gender, current_address, telephone, has_employment_history, has_familial_relationships, has_interpersonal_relationships, has_medical_history, aliases, has_news_events, id, name, description, depicted_by}
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
    type Key   = uriorcurie;
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
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Option<Vec<String>>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl HasAliases {
    #[new]
    pub fn new(aliases: Option<Vec<String>>) -> Self {
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
pub enum HasAliasesOrSubtype {    Person(Person),     Organization(Organization),     Place(Place)}

impl From<Person>   for HasAliasesOrSubtype { fn from(x: Person)   -> Self { Self::Person(x) } }
impl From<Organization>   for HasAliasesOrSubtype { fn from(x: Organization)   -> Self { Self::Organization(x) } }
impl From<Place>   for HasAliasesOrSubtype { fn from(x: Place)   -> Self { Self::Place(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for HasAliasesOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Person>() {
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
pub struct HasNewsEvents {
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_news_events: Option<Vec<NewsEvent>>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl HasNewsEvents {
    #[new]
    pub fn new(has_news_events: Option<Vec<NewsEvent>>) -> Self {
        HasNewsEvents{has_news_events}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<HasNewsEvents>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<HasNewsEvents> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<HasNewsEvents>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid HasNewsEvents",
        ))
    }
}


#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature="serde", serde(untagged))]
pub enum HasNewsEventsOrSubtype {    Person(Person),     Organization(Organization)}

impl From<Person>   for HasNewsEventsOrSubtype { fn from(x: Person)   -> Self { Self::Person(x) } }
impl From<Organization>   for HasNewsEventsOrSubtype { fn from(x: Organization)   -> Self { Self::Organization(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for HasNewsEventsOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<Person>() {
            return Ok(HasNewsEventsOrSubtype::Person(val));
        }        if let Ok(val) = ob.extract::<Organization>() {
            return Ok(HasNewsEventsOrSubtype::Organization(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid HasNewsEventsOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for HasNewsEventsOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            HasNewsEventsOrSubtype::Person(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            HasNewsEventsOrSubtype::Organization(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<HasNewsEventsOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<HasNewsEventsOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<HasNewsEventsOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid HasNewsEventsOrSubtype",
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
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub categories: Option<Vec<OrganizationType>>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub score: Option<f64>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub min_salary: Option<f64>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Option<Vec<String>>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub has_news_events: Option<Vec<NewsEvent>>,
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Organization {
    #[new]
    pub fn new(mission_statement: Option<String>, founding_date: Option<String>, founding_location: Option<String>, categories: Option<Vec<OrganizationType>>, score: Option<f64>, min_salary: Option<f64>, aliases: Option<Vec<String>>, has_news_events: Option<Vec<NewsEvent>>, id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        Organization{mission_statement, founding_date, founding_location, categories, score, min_salary, aliases, has_news_events, id, name, description, depicted_by}
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
    type Key   = uriorcurie;
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
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub aliases: Option<Vec<String>>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Place {
    #[new]
    pub fn new(id: uriorcurie, name: String, depicted_by: Option<String>, aliases: Option<Vec<String>>) -> Self {
        Place{id, name, depicted_by, aliases}
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
    type Key   = uriorcurie;
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
pub enum EventOrSubtype {    NewsEvent(NewsEvent),     EmploymentEvent(EmploymentEvent),     MedicalEvent(MedicalEvent)}

impl From<NewsEvent>   for EventOrSubtype { fn from(x: NewsEvent)   -> Self { Self::NewsEvent(x) } }
impl From<EmploymentEvent>   for EventOrSubtype { fn from(x: EmploymentEvent)   -> Self { Self::EmploymentEvent(x) } }
impl From<MedicalEvent>   for EventOrSubtype { fn from(x: MedicalEvent)   -> Self { Self::MedicalEvent(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for EventOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<NewsEvent>() {
            return Ok(EventOrSubtype::NewsEvent(val));
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
            EventOrSubtype::NewsEvent(val) => val.into_pyobject(py).map(move |b| b.into_any()),
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
pub struct NewsEvent {
    #[cfg_attr(feature = "serde", serde(default))]
    pub headline: Option<String>,
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
impl NewsEvent {
    #[new]
    pub fn new(headline: Option<String>, started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, duration: Option<f64>, is_current: Option<bool>) -> Self {
        NewsEvent{headline, started_at_time, ended_at_time, duration, is_current}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<NewsEvent>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<NewsEvent> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<NewsEvent>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid NewsEvent",
        ))
    }
}



#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Concept {
    #[cfg_attr(feature = "serde", serde(default))]
    pub code_system: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub mappings: Option<Vec<String>>,
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Concept {
    #[new]
    pub fn new(code_system: Option<String>, mappings: Option<Vec<String>>, id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        Concept{code_system, mappings, id, name, description, depicted_by}
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
    type Key   = uriorcurie;
    type Value = CodeSystem;
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
        map.insert(Value::String("code_system".into()), v);
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
pub enum ConceptOrSubtype {    DiagnosisConcept(DiagnosisConcept),     ProcedureConcept(ProcedureConcept),     OperationProcedureConcept(OperationProcedureConcept),     ImagingProcedureConcept(ImagingProcedureConcept)}

impl From<DiagnosisConcept>   for ConceptOrSubtype { fn from(x: DiagnosisConcept)   -> Self { Self::DiagnosisConcept(x) } }
impl From<ProcedureConcept>   for ConceptOrSubtype { fn from(x: ProcedureConcept)   -> Self { Self::ProcedureConcept(x) } }
impl From<OperationProcedureConcept>   for ConceptOrSubtype { fn from(x: OperationProcedureConcept)   -> Self { Self::OperationProcedureConcept(x) } }
impl From<ImagingProcedureConcept>   for ConceptOrSubtype { fn from(x: ImagingProcedureConcept)   -> Self { Self::ImagingProcedureConcept(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for ConceptOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<DiagnosisConcept>() {
            return Ok(ConceptOrSubtype::DiagnosisConcept(val));
        }        if let Ok(val) = ob.extract::<ProcedureConcept>() {
            return Ok(ConceptOrSubtype::ProcedureConcept(val));
        }        if let Ok(val) = ob.extract::<OperationProcedureConcept>() {
            return Ok(ConceptOrSubtype::OperationProcedureConcept(val));
        }        if let Ok(val) = ob.extract::<ImagingProcedureConcept>() {
            return Ok(ConceptOrSubtype::ImagingProcedureConcept(val));
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
            ConceptOrSubtype::DiagnosisConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            ConceptOrSubtype::ProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            ConceptOrSubtype::OperationProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            ConceptOrSubtype::ImagingProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
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
        if let Ok(x) = DiagnosisConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::DiagnosisConcept(x));
        }
        if let Ok(x) = ProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::ProcedureConcept(x));
        }
        if let Ok(x) = OperationProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::OperationProcedureConcept(x));
        }
        if let Ok(x) = ImagingProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::ImagingProcedureConcept(x));
        }
        Err("none of the variants matched the mapping form".into())
    }

    fn from_pair_simple(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
        if let Ok(x) = DiagnosisConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::DiagnosisConcept(x));
        }
        if let Ok(x) = ProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::ProcedureConcept(x));
        }
        if let Ok(x) = OperationProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::OperationProcedureConcept(x));
        }
        if let Ok(x) = ImagingProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ConceptOrSubtype::ImagingProcedureConcept(x));
        }
        Err("none of the variants support the primitive form".into())
    }

    fn extract_key(&self) -> &Self::Key {
        match self {
            ConceptOrSubtype::DiagnosisConcept(inner) => inner.extract_key(),
            ConceptOrSubtype::ProcedureConcept(inner) => inner.extract_key(),
            ConceptOrSubtype::OperationProcedureConcept(inner) => inner.extract_key(),
            ConceptOrSubtype::ImagingProcedureConcept(inner) => inner.extract_key(),
        }
    }
}


#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct DiagnosisConcept {
    #[cfg_attr(feature = "serde", serde(default))]
    pub code_system: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub mappings: Option<Vec<String>>,
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl DiagnosisConcept {
    #[new]
    pub fn new(code_system: Option<String>, mappings: Option<Vec<String>>, id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        DiagnosisConcept{code_system, mappings, id, name, description, depicted_by}
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
    type Key   = uriorcurie;
    type Value = CodeSystem;
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
        map.insert(Value::String("code_system".into()), v);
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
    #[cfg_attr(feature = "serde", serde(default))]
    pub code_system: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub mappings: Option<Vec<String>>,
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl ProcedureConcept {
    #[new]
    pub fn new(code_system: Option<String>, mappings: Option<Vec<String>>, id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        ProcedureConcept{code_system, mappings, id, name, description, depicted_by}
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
    type Key   = uriorcurie;
    type Value = CodeSystem;
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
        map.insert(Value::String("code_system".into()), v);
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
pub enum ProcedureConceptOrSubtype {    OperationProcedureConcept(OperationProcedureConcept),     ImagingProcedureConcept(ImagingProcedureConcept)}

impl From<OperationProcedureConcept>   for ProcedureConceptOrSubtype { fn from(x: OperationProcedureConcept)   -> Self { Self::OperationProcedureConcept(x) } }
impl From<ImagingProcedureConcept>   for ProcedureConceptOrSubtype { fn from(x: ImagingProcedureConcept)   -> Self { Self::ImagingProcedureConcept(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for ProcedureConceptOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<OperationProcedureConcept>() {
            return Ok(ProcedureConceptOrSubtype::OperationProcedureConcept(val));
        }        if let Ok(val) = ob.extract::<ImagingProcedureConcept>() {
            return Ok(ProcedureConceptOrSubtype::ImagingProcedureConcept(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid ProcedureConceptOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for ProcedureConceptOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            ProcedureConceptOrSubtype::OperationProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            ProcedureConceptOrSubtype::ImagingProcedureConcept(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<ProcedureConceptOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<ProcedureConceptOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<ProcedureConceptOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid ProcedureConceptOrSubtype",
        ))
    }
}

#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for ProcedureConceptOrSubtype {
    type Key       = String;
    type Value     = serde_value::Value;
    type Error     = String;

    fn from_pair_mapping(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
        if let Ok(x) = OperationProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ProcedureConceptOrSubtype::OperationProcedureConcept(x));
        }
        if let Ok(x) = ImagingProcedureConcept::from_pair_mapping(k.clone(), v.clone()) {
            return Ok(ProcedureConceptOrSubtype::ImagingProcedureConcept(x));
        }
        Err("none of the variants matched the mapping form".into())
    }

    fn from_pair_simple(k: Self::Key, v: Self::Value) -> Result<Self, Self::Error> {
        if let Ok(x) = OperationProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ProcedureConceptOrSubtype::OperationProcedureConcept(x));
        }
        if let Ok(x) = ImagingProcedureConcept::from_pair_simple(k.clone(), v.clone()) {
            return Ok(ProcedureConceptOrSubtype::ImagingProcedureConcept(x));
        }
        Err("none of the variants support the primitive form".into())
    }

    fn extract_key(&self) -> &Self::Key {
        match self {
            ProcedureConceptOrSubtype::OperationProcedureConcept(inner) => inner.extract_key(),
            ProcedureConceptOrSubtype::ImagingProcedureConcept(inner) => inner.extract_key(),
        }
    }
}


#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct IntegerPrimaryKeyObject {
    pub int_id: isize
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl IntegerPrimaryKeyObject {
    #[new]
    pub fn new(int_id: isize) -> Self {
        IntegerPrimaryKeyObject{int_id}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<IntegerPrimaryKeyObject>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<IntegerPrimaryKeyObject> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<IntegerPrimaryKeyObject>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid IntegerPrimaryKeyObject",
        ))
    }
}



#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct OperationProcedureConcept {
    #[cfg_attr(feature = "serde", serde(default))]
    pub code_system: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub mappings: Option<Vec<String>>,
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl OperationProcedureConcept {
    #[new]
    pub fn new(code_system: Option<String>, mappings: Option<Vec<String>>, id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        OperationProcedureConcept{code_system, mappings, id, name, description, depicted_by}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<OperationProcedureConcept>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<OperationProcedureConcept> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<OperationProcedureConcept>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid OperationProcedureConcept",
        ))
    }
}


#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for OperationProcedureConcept {
    type Key   = uriorcurie;
    type Value = CodeSystem;
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
        map.insert(Value::String("code_system".into()), v);
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
pub struct ImagingProcedureConcept {
    #[cfg_attr(feature = "serde", serde(default))]
    pub code_system: Option<String>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_primitive_list_or_single_value_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub mappings: Option<Vec<String>>,
    pub id: uriorcurie,
    pub name: String,
    #[cfg_attr(feature = "serde", serde(default))]
    pub description: Option<String>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub depicted_by: Option<String>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl ImagingProcedureConcept {
    #[new]
    pub fn new(code_system: Option<String>, mappings: Option<Vec<String>>, id: uriorcurie, name: String, description: Option<String>, depicted_by: Option<String>) -> Self {
        ImagingProcedureConcept{code_system, mappings, id, name, description, depicted_by}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<ImagingProcedureConcept>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<ImagingProcedureConcept> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<ImagingProcedureConcept>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid ImagingProcedureConcept",
        ))
    }
}


#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for ImagingProcedureConcept {
    type Key   = uriorcurie;
    type Value = CodeSystem;
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
        map.insert(Value::String("code_system".into()), v);
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
pub struct CodeSystem {
    pub id: uriorcurie,
    pub name: String
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl CodeSystem {
    #[new]
    pub fn new(id: uriorcurie, name: String) -> Self {
        CodeSystem{id, name}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<CodeSystem>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<CodeSystem> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<CodeSystem>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid CodeSystem",
        ))
    }
}


#[cfg(feature = "serde")]
impl serde_utils::InlinedPair for CodeSystem {
    type Key   = uriorcurie;
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

pub mod relationship_utl {
    use super::*;
    #[derive(Debug, Clone, PartialEq)]
    #[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
    pub enum type__range {
        String(String),
        FamilialRelationshipType(FamilialRelationshipType),
        NonFamilialRelationshipType(NonFamilialRelationshipType)    }

    #[cfg(feature = "pyo3")]
    impl<'py> FromPyObject<'py> for type__range {
        fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
            if let Ok(val) = ob.extract::<String>() {
                return Ok(type__range::String(val));
            }            if let Ok(val) = ob.extract::<FamilialRelationshipType>() {
                return Ok(type__range::FamilialRelationshipType(val));
            }            if let Ok(val) = ob.extract::<NonFamilialRelationshipType>() {
                return Ok(type__range::NonFamilialRelationshipType(val));
            }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "invalid type_",
            ))
        }
    }

    #[cfg(feature = "pyo3")]
    impl<'py> IntoPyObject<'py> for type__range {
        type Target = PyAny;
        type Output = Bound<'py, Self::Target>;
        type Error = PyErr;

        fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
            match self {
                type__range::String(val) => Ok(val.into_pyobject(py).map(move |b| <pyo3::Bound<'_, _> as Clone>::clone(&b).into_any())?),
                type__range::FamilialRelationshipType(val) => Ok(val.into_pyobject(py).map(move |b| <pyo3::Bound<'_, _> as Clone>::clone(&b).into_any())?),
                type__range::NonFamilialRelationshipType(val) => Ok(val.into_pyobject(py).map(move |b| <pyo3::Bound<'_, _> as Clone>::clone(&b).into_any())?),
            }
        }
    }


    #[cfg(feature = "pyo3")]
    impl<'py> IntoPyObject<'py> for Box<type__range>
    {
        type Target = PyAny;
        type Output = Bound<'py, Self::Target>;
        type Error = PyErr;
        fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
            (*self).into_pyobject(py).map(move |x| x.into_any())
        }
    }

    #[cfg(feature = "pyo3")]
    impl<'py> FromPyObject<'py> for Box<type__range> {
        fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
            if let Ok(val) = ob.extract::<type__range>() {
                return Ok(Box::new(val));
            }
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "invalid type_",
            ))
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
    #[cfg_attr(feature = "serde", serde(alias = "type"))]
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
pub enum RelationshipOrSubtype {    FamilialRelationship(FamilialRelationship),     InterPersonalRelationship(InterPersonalRelationship)}

impl From<FamilialRelationship>   for RelationshipOrSubtype { fn from(x: FamilialRelationship)   -> Self { Self::FamilialRelationship(x) } }
impl From<InterPersonalRelationship>   for RelationshipOrSubtype { fn from(x: InterPersonalRelationship)   -> Self { Self::InterPersonalRelationship(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for RelationshipOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<FamilialRelationship>() {
            return Ok(RelationshipOrSubtype::FamilialRelationship(val));
        }        if let Ok(val) = ob.extract::<InterPersonalRelationship>() {
            return Ok(RelationshipOrSubtype::InterPersonalRelationship(val));
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
            RelationshipOrSubtype::FamilialRelationship(val) => val.into_pyobject(py).map(move |b| b.into_any()),
            RelationshipOrSubtype::InterPersonalRelationship(val) => val.into_pyobject(py).map(move |b| b.into_any()),
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
    #[cfg_attr(feature = "serde", serde(default))]
    pub related_to: Option<String>,
    #[cfg_attr(feature = "serde", serde(alias = "type"))]
    pub type_: FamilialRelationshipType
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl FamilialRelationship {
    #[new]
    pub fn new(started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, related_to: Option<String>, type_: FamilialRelationshipType) -> Self {
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



pub mod inter_personal_relationship_utl {
    use super::*;
    #[derive(Debug, Clone, PartialEq)]
    #[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
    pub enum type__range {
        String(String),
        FamilialRelationshipType(FamilialRelationshipType),
        NonFamilialRelationshipType(NonFamilialRelationshipType)    }

    #[cfg(feature = "pyo3")]
    impl<'py> FromPyObject<'py> for type__range {
        fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
            if let Ok(val) = ob.extract::<String>() {
                return Ok(type__range::String(val));
            }            if let Ok(val) = ob.extract::<FamilialRelationshipType>() {
                return Ok(type__range::FamilialRelationshipType(val));
            }            if let Ok(val) = ob.extract::<NonFamilialRelationshipType>() {
                return Ok(type__range::NonFamilialRelationshipType(val));
            }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "invalid type_",
            ))
        }
    }

    #[cfg(feature = "pyo3")]
    impl<'py> IntoPyObject<'py> for type__range {
        type Target = PyAny;
        type Output = Bound<'py, Self::Target>;
        type Error = PyErr;

        fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
            match self {
                type__range::String(val) => Ok(val.into_pyobject(py).map(move |b| <pyo3::Bound<'_, _> as Clone>::clone(&b).into_any())?),
                type__range::FamilialRelationshipType(val) => Ok(val.into_pyobject(py).map(move |b| <pyo3::Bound<'_, _> as Clone>::clone(&b).into_any())?),
                type__range::NonFamilialRelationshipType(val) => Ok(val.into_pyobject(py).map(move |b| <pyo3::Bound<'_, _> as Clone>::clone(&b).into_any())?),
            }
        }
    }


    #[cfg(feature = "pyo3")]
    impl<'py> IntoPyObject<'py> for Box<type__range>
    {
        type Target = PyAny;
        type Output = Bound<'py, Self::Target>;
        type Error = PyErr;
        fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
            (*self).into_pyobject(py).map(move |x| x.into_any())
        }
    }

    #[cfg(feature = "pyo3")]
    impl<'py> FromPyObject<'py> for Box<type__range> {
        fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
            if let Ok(val) = ob.extract::<type__range>() {
                return Ok(Box::new(val));
            }
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "invalid type_",
            ))
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct InterPersonalRelationship {
    #[cfg_attr(feature = "serde", serde(default))]
    pub started_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub ended_at_time: Option<NaiveDate>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub related_to: Option<String>,
    #[cfg_attr(feature = "serde", serde(alias = "type"))]
    pub type_: inter_personal_relationship_utl::type__range
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl InterPersonalRelationship {
    #[new]
    pub fn new(started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, related_to: Option<String>, type_: inter_personal_relationship_utl::type__range) -> Self {
        InterPersonalRelationship{started_at_time, ended_at_time, related_to, type_}
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<InterPersonalRelationship>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<InterPersonalRelationship> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<InterPersonalRelationship>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid InterPersonalRelationship",
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
    pub salary: Option<f64>,
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
    pub fn new(employed_at: Option<String>, salary: Option<f64>, started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, duration: Option<f64>, is_current: Option<bool>) -> Self {
        EmploymentEvent{employed_at, salary, started_at_time, ended_at_time, duration, is_current}
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
    pub diagnosis: Option<DiagnosisConcept>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub procedure: Option<ProcedureConceptOrSubtype>,
    #[cfg_attr(feature = "serde", serde(default))]
    pub in_location: Option<String>,
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
    pub fn new(diagnosis: Option<DiagnosisConcept>, procedure: Option<ProcedureConceptOrSubtype>, in_location: Option<String>, started_at_time: Option<NaiveDate>, ended_at_time: Option<NaiveDate>, duration: Option<f64>, is_current: Option<bool>) -> Self {
        MedicalEvent{diagnosis, procedure, in_location, started_at_time, ended_at_time, duration, is_current}
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
#[cfg_attr(feature="serde", serde(untagged))]
pub enum WithLocationOrSubtype {    MedicalEvent(MedicalEvent)}

impl From<MedicalEvent>   for WithLocationOrSubtype { fn from(x: MedicalEvent)   -> Self { Self::MedicalEvent(x) } }

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for WithLocationOrSubtype {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<MedicalEvent>() {
            return Ok(WithLocationOrSubtype::MedicalEvent(val));
        }Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid WithLocationOrSubtype",
        ))
    }
}

#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for WithLocationOrSubtype {
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        match self {
            WithLocationOrSubtype::MedicalEvent(val) => val.into_pyobject(py).map(move |b| b.into_any()),
        }
    }
}


#[cfg(feature = "pyo3")]
impl<'py> IntoPyObject<'py> for Box<WithLocationOrSubtype>
{
    type Target = PyAny;
    type Output = Bound<'py, Self::Target>;
    type Error = PyErr;
    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        (*self).into_pyobject(py).map(move |x| x.into_any())
    }
}

#[cfg(feature = "pyo3")]
impl<'py> FromPyObject<'py> for Box<WithLocationOrSubtype> {
    fn extract_bound(ob: &pyo3::Bound<'py, pyo3::types::PyAny>) -> pyo3::PyResult<Self> {
        if let Ok(val) = ob.extract::<WithLocationOrSubtype>() {
            return Ok(Box::new(val));
        }
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "invalid WithLocationOrSubtype",
        ))
    }
}



#[derive(Debug, Clone, PartialEq)]
#[cfg_attr(feature = "serde", derive(Serialize, Deserialize))]
#[cfg_attr(feature = "pyo3", pyclass(subclass, get_all, set_all))]
pub struct Container {
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_inlined_dict_list_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub persons: Option<Vec<Person>>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_inlined_dict_list_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub organizations: Option<Vec<Organization>>,
    #[cfg_attr(feature = "serde", serde(deserialize_with = "serde_utils::deserialize_inlined_dict_list_optional"))]
    #[cfg_attr(feature = "serde", serde(default))]
    pub places: Option<Vec<Place>>
}
#[cfg(feature = "pyo3")]
#[pymethods]
impl Container {
    #[new]
    pub fn new(persons: Option<Vec<Person>>, organizations: Option<Vec<Organization>>, places: Option<Vec<Place>>) -> Self {
        Container{persons, organizations, places}
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
