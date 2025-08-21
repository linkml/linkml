#![allow(non_camel_case_types)]

use crate::*;
use crate::poly_containers::*;


pub trait NamedThing   {

    fn id(&self) -> &str;
    // fn id_mut(&mut self) -> &mut &str;
    // fn set_id(&mut self, value: String);

    fn name(&self) -> Option<&str>;
    // fn name_mut(&mut self) -> &mut Option<&str>;
    // fn set_name(&mut self, value: Option<&str>);

    fn description(&self) -> Option<&str>;
    // fn description_mut(&mut self) -> &mut Option<&str>;
    // fn set_description(&mut self, value: Option<&str>);

    fn image(&self) -> Option<&str>;
    // fn image_mut(&mut self) -> &mut Option<&str>;
    // fn set_image(&mut self, value: Option<&str>);


}

impl NamedThing for crate::NamedThing {
        fn id(&self) -> &str {
        return &self.id;
    }
        fn name(&self) -> Option<&str> {
        return self.name.as_deref();
    }
        fn description(&self) -> Option<&str> {
        return self.description.as_deref();
    }
        fn image(&self) -> Option<&str> {
        return self.image.as_deref();
    }
}
impl NamedThing for crate::Person {
        fn id(&self) -> &str {
        return &self.id;
    }
        fn name(&self) -> Option<&str> {
        return self.name.as_deref();
    }
        fn description(&self) -> Option<&str> {
        return self.description.as_deref();
    }
        fn image(&self) -> Option<&str> {
        return self.image.as_deref();
    }
}
impl NamedThing for crate::Organization {
        fn id(&self) -> &str {
        return &self.id;
    }
        fn name(&self) -> Option<&str> {
        return self.name.as_deref();
    }
        fn description(&self) -> Option<&str> {
        return self.description.as_deref();
    }
        fn image(&self) -> Option<&str> {
        return self.image.as_deref();
    }
}
impl NamedThing for crate::Concept {
        fn id(&self) -> &str {
        return &self.id;
    }
        fn name(&self) -> Option<&str> {
        return self.name.as_deref();
    }
        fn description(&self) -> Option<&str> {
        return self.description.as_deref();
    }
        fn image(&self) -> Option<&str> {
        return self.image.as_deref();
    }
}
impl NamedThing for crate::DiagnosisConcept {
        fn id(&self) -> &str {
        return &self.id;
    }
        fn name(&self) -> Option<&str> {
        return self.name.as_deref();
    }
        fn description(&self) -> Option<&str> {
        return self.description.as_deref();
    }
        fn image(&self) -> Option<&str> {
        return self.image.as_deref();
    }
}
impl NamedThing for crate::ProcedureConcept {
        fn id(&self) -> &str {
        return &self.id;
    }
        fn name(&self) -> Option<&str> {
        return self.name.as_deref();
    }
        fn description(&self) -> Option<&str> {
        return self.description.as_deref();
    }
        fn image(&self) -> Option<&str> {
        return self.image.as_deref();
    }
}

impl NamedThing for crate::NamedThingOrSubtype {
        fn id(&self) -> &str {
        match self {
                NamedThingOrSubtype::NamedThing(val) => val.id(),
                NamedThingOrSubtype::Person(val) => val.id(),
                NamedThingOrSubtype::Organization(val) => val.id(),
                NamedThingOrSubtype::Concept(val) => val.id(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.id(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.id(),

        }
    }
        fn name(&self) -> Option<&str> {
        match self {
                NamedThingOrSubtype::NamedThing(val) => val.name(),
                NamedThingOrSubtype::Person(val) => val.name(),
                NamedThingOrSubtype::Organization(val) => val.name(),
                NamedThingOrSubtype::Concept(val) => val.name(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.name(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.name(),

        }
    }
        fn description(&self) -> Option<&str> {
        match self {
                NamedThingOrSubtype::NamedThing(val) => val.description(),
                NamedThingOrSubtype::Person(val) => val.description(),
                NamedThingOrSubtype::Organization(val) => val.description(),
                NamedThingOrSubtype::Concept(val) => val.description(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.description(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.description(),

        }
    }
        fn image(&self) -> Option<&str> {
        match self {
                NamedThingOrSubtype::NamedThing(val) => val.image(),
                NamedThingOrSubtype::Person(val) => val.image(),
                NamedThingOrSubtype::Organization(val) => val.image(),
                NamedThingOrSubtype::Concept(val) => val.image(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.image(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.image(),

        }
    }
}
impl NamedThing for crate::ConceptOrSubtype {
        fn id(&self) -> &str {
        match self {
                ConceptOrSubtype::Concept(val) => val.id(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.id(),
                ConceptOrSubtype::ProcedureConcept(val) => val.id(),

        }
    }
        fn name(&self) -> Option<&str> {
        match self {
                ConceptOrSubtype::Concept(val) => val.name(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.name(),
                ConceptOrSubtype::ProcedureConcept(val) => val.name(),

        }
    }
        fn description(&self) -> Option<&str> {
        match self {
                ConceptOrSubtype::Concept(val) => val.description(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.description(),
                ConceptOrSubtype::ProcedureConcept(val) => val.description(),

        }
    }
        fn image(&self) -> Option<&str> {
        match self {
                ConceptOrSubtype::Concept(val) => val.image(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.image(),
                ConceptOrSubtype::ProcedureConcept(val) => val.image(),

        }
    }
}

pub trait Person : NamedThing  +  HasAliases   {

    fn primary_email(&self) -> Option<&str>;
    // fn primary_email_mut(&mut self) -> &mut Option<&str>;
    // fn set_primary_email(&mut self, value: Option<&str>);

    fn birth_date(&self) -> Option<&str>;
    // fn birth_date_mut(&mut self) -> &mut Option<&str>;
    // fn set_birth_date(&mut self, value: Option<&str>);

    fn age_in_years(&self) -> Option<&isize>;
    // fn age_in_years_mut(&mut self) -> &mut Option<&isize>;
    // fn set_age_in_years(&mut self, value: Option<&isize>);

    fn gender(&self) -> Option<&str>;
    // fn gender_mut(&mut self) -> &mut Option<&str>;
    // fn set_gender(&mut self, value: Option<&str>);

    fn current_address(&self) -> Option<&crate::Address>;
    // fn current_address_mut(&mut self) -> &mut Option<&crate::Address>;
    // fn set_current_address<E>(&mut self, value: Option<E>) where E: Into<Address>;

    fn has_employment_history(&self) -> impl poly_containers::SeqRef<crate::EmploymentEvent>;
    // fn has_employment_history_mut(&mut self) -> &mut impl poly_containers::SeqRef<crate::EmploymentEvent>;
    // fn set_has_employment_history<E>(&mut self, value: &Vec<E>) where E: Into<EmploymentEvent>;

    fn has_familial_relationships(&self) -> impl poly_containers::SeqRef<crate::FamilialRelationship>;
    // fn has_familial_relationships_mut(&mut self) -> &mut impl poly_containers::SeqRef<crate::FamilialRelationship>;
    // fn set_has_familial_relationships<E>(&mut self, value: &Vec<E>) where E: Into<FamilialRelationship>;

    fn has_medical_history(&self) -> impl poly_containers::SeqRef<crate::MedicalEvent>;
    // fn has_medical_history_mut(&mut self) -> &mut impl poly_containers::SeqRef<crate::MedicalEvent>;
    // fn set_has_medical_history<E>(&mut self, value: &Vec<E>) where E: Into<MedicalEvent>;


}

impl Person for crate::Person {
        fn primary_email(&self) -> Option<&str> {
        return self.primary_email.as_deref();
    }
        fn birth_date(&self) -> Option<&str> {
        return self.birth_date.as_deref();
    }
        fn age_in_years(&self) -> Option<&isize> {
        return self.age_in_years.as_ref();
    }
        fn gender(&self) -> Option<&str> {
        return self.gender.as_deref();
    }
        fn current_address(&self) -> Option<&crate::Address> {
        return self.current_address.as_ref();
    }
        fn has_employment_history(&self) -> impl poly_containers::SeqRef<crate::EmploymentEvent> {
        return &self.has_employment_history;
    }
        fn has_familial_relationships(&self) -> impl poly_containers::SeqRef<crate::FamilialRelationship> {
// list
        return poly_containers::ListView::new(&self.has_familial_relationships);
    }
        fn has_medical_history(&self) -> impl poly_containers::SeqRef<crate::MedicalEvent> {
        return &self.has_medical_history;
    }
}


pub trait HasAliases   {

    fn aliases(&self) -> impl poly_containers::SeqRef<String>;
    // fn aliases_mut(&mut self) -> &mut impl poly_containers::SeqRef<String>;
    // fn set_aliases(&mut self, value: &Vec<String>);


}

impl HasAliases for crate::HasAliases {
        fn aliases(&self) -> impl poly_containers::SeqRef<String> {
        return &self.aliases;
    }
}
impl HasAliases for crate::Person {
        fn aliases(&self) -> impl poly_containers::SeqRef<String> {
        return &self.aliases;
    }
}
impl HasAliases for crate::Organization {
        fn aliases(&self) -> impl poly_containers::SeqRef<String> {
        return &self.aliases;
    }
}
impl HasAliases for crate::Place {
        fn aliases(&self) -> impl poly_containers::SeqRef<String> {
        return &self.aliases;
    }
}

impl HasAliases for crate::HasAliasesOrSubtype {
        fn aliases(&self) -> impl poly_containers::SeqRef<String> {
        match self {
                HasAliasesOrSubtype::HasAliases(val) => val.aliases().to_any(),
                HasAliasesOrSubtype::Person(val) => val.aliases().to_any(),
                HasAliasesOrSubtype::Organization(val) => val.aliases().to_any(),
                HasAliasesOrSubtype::Place(val) => val.aliases().to_any(),

        }
    }
}

pub trait Organization : NamedThing  +  HasAliases   {

    fn mission_statement(&self) -> Option<&str>;
    // fn mission_statement_mut(&mut self) -> &mut Option<&str>;
    // fn set_mission_statement(&mut self, value: Option<&str>);

    fn founding_date(&self) -> Option<&str>;
    // fn founding_date_mut(&mut self) -> &mut Option<&str>;
    // fn set_founding_date(&mut self, value: Option<&str>);

    fn founding_location(&self) -> Option<&str>;
    // fn founding_location_mut(&mut self) -> &mut Option<&str>;
    // fn set_founding_location<E>(&mut self, value: Option<&str>) where E: Into<String>;


}

impl Organization for crate::Organization {
        fn mission_statement(&self) -> Option<&str> {
        return self.mission_statement.as_deref();
    }
        fn founding_date(&self) -> Option<&str> {
        return self.founding_date.as_deref();
    }
        fn founding_location(&self) -> Option<&str> {
        return self.founding_location.as_deref();
    }
}


pub trait Place : HasAliases   {

    fn id(&self) -> &str;
    // fn id_mut(&mut self) -> &mut &str;
    // fn set_id(&mut self, value: String);

    fn name(&self) -> Option<&str>;
    // fn name_mut(&mut self) -> &mut Option<&str>;
    // fn set_name(&mut self, value: Option<&str>);


}

impl Place for crate::Place {
        fn id(&self) -> &str {
        return &self.id;
    }
        fn name(&self) -> Option<&str> {
        return self.name.as_deref();
    }
}


pub trait Address   {

    fn street(&self) -> Option<&str>;
    // fn street_mut(&mut self) -> &mut Option<&str>;
    // fn set_street(&mut self, value: Option<&str>);

    fn city(&self) -> Option<&str>;
    // fn city_mut(&mut self) -> &mut Option<&str>;
    // fn set_city(&mut self, value: Option<&str>);

    fn postal_code(&self) -> Option<&str>;
    // fn postal_code_mut(&mut self) -> &mut Option<&str>;
    // fn set_postal_code(&mut self, value: Option<&str>);


}

impl Address for crate::Address {
        fn street(&self) -> Option<&str> {
        return self.street.as_deref();
    }
        fn city(&self) -> Option<&str> {
        return self.city.as_deref();
    }
        fn postal_code(&self) -> Option<&str> {
        return self.postal_code.as_deref();
    }
}


pub trait Event   {

    fn started_at_time(&self) -> Option<&NaiveDate>;
    // fn started_at_time_mut(&mut self) -> &mut Option<&NaiveDate>;
    // fn set_started_at_time(&mut self, value: Option<&NaiveDate>);

    fn ended_at_time(&self) -> Option<&NaiveDate>;
    // fn ended_at_time_mut(&mut self) -> &mut Option<&NaiveDate>;
    // fn set_ended_at_time(&mut self, value: Option<&NaiveDate>);

    fn duration(&self) -> Option<&f64>;
    // fn duration_mut(&mut self) -> &mut Option<&f64>;
    // fn set_duration(&mut self, value: Option<&f64>);

    fn is_current(&self) -> Option<&bool>;
    // fn is_current_mut(&mut self) -> &mut Option<&bool>;
    // fn set_is_current(&mut self, value: Option<&bool>);


}

impl Event for crate::Event {
        fn started_at_time(&self) -> Option<&NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time(&self) -> Option<&NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn duration(&self) -> Option<&f64> {
        return self.duration.as_ref();
    }
        fn is_current(&self) -> Option<&bool> {
        return self.is_current.as_ref();
    }
}
impl Event for crate::EmploymentEvent {
        fn started_at_time(&self) -> Option<&NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time(&self) -> Option<&NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn duration(&self) -> Option<&f64> {
        return self.duration.as_ref();
    }
        fn is_current(&self) -> Option<&bool> {
        return self.is_current.as_ref();
    }
}
impl Event for crate::MedicalEvent {
        fn started_at_time(&self) -> Option<&NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time(&self) -> Option<&NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn duration(&self) -> Option<&f64> {
        return self.duration.as_ref();
    }
        fn is_current(&self) -> Option<&bool> {
        return self.is_current.as_ref();
    }
}

impl Event for crate::EventOrSubtype {
        fn started_at_time(&self) -> Option<&NaiveDate> {
        match self {
                EventOrSubtype::Event(val) => val.started_at_time(),
                EventOrSubtype::EmploymentEvent(val) => val.started_at_time(),
                EventOrSubtype::MedicalEvent(val) => val.started_at_time(),

        }
    }
        fn ended_at_time(&self) -> Option<&NaiveDate> {
        match self {
                EventOrSubtype::Event(val) => val.ended_at_time(),
                EventOrSubtype::EmploymentEvent(val) => val.ended_at_time(),
                EventOrSubtype::MedicalEvent(val) => val.ended_at_time(),

        }
    }
        fn duration(&self) -> Option<&f64> {
        match self {
                EventOrSubtype::Event(val) => val.duration(),
                EventOrSubtype::EmploymentEvent(val) => val.duration(),
                EventOrSubtype::MedicalEvent(val) => val.duration(),

        }
    }
        fn is_current(&self) -> Option<&bool> {
        match self {
                EventOrSubtype::Event(val) => val.is_current(),
                EventOrSubtype::EmploymentEvent(val) => val.is_current(),
                EventOrSubtype::MedicalEvent(val) => val.is_current(),

        }
    }
}

pub trait Concept : NamedThing   {


}

impl Concept for crate::Concept {
}
impl Concept for crate::DiagnosisConcept {
}
impl Concept for crate::ProcedureConcept {
}

impl Concept for crate::ConceptOrSubtype {
}

pub trait DiagnosisConcept : Concept   {


}

impl DiagnosisConcept for crate::DiagnosisConcept {
}


pub trait ProcedureConcept : Concept   {


}

impl ProcedureConcept for crate::ProcedureConcept {
}


pub trait Relationship   {

    fn started_at_time(&self) -> Option<&NaiveDate>;
    // fn started_at_time_mut(&mut self) -> &mut Option<&NaiveDate>;
    // fn set_started_at_time(&mut self, value: Option<&NaiveDate>);

    fn ended_at_time(&self) -> Option<&NaiveDate>;
    // fn ended_at_time_mut(&mut self) -> &mut Option<&NaiveDate>;
    // fn set_ended_at_time(&mut self, value: Option<&NaiveDate>);

    fn related_to(&self) -> Option<&str>;
    // fn related_to_mut(&mut self) -> &mut Option<&str>;
    // fn set_related_to(&mut self, value: Option<&str>);

    fn type_(&self) -> Option<&str>;
    // fn type__mut(&mut self) -> &mut Option<&str>;
    // fn set_type_(&mut self, value: Option<&str>);


}

impl Relationship for crate::Relationship {
        fn started_at_time(&self) -> Option<&NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time(&self) -> Option<&NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn related_to(&self) -> Option<&str> {
        return self.related_to.as_deref();
    }
        fn type_(&self) -> Option<&str> {
        return self.type_.as_deref();
    }
}
impl Relationship for crate::FamilialRelationship {
        fn started_at_time(&self) -> Option<&NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time(&self) -> Option<&NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn related_to(&self) -> Option<&str> {
        return Some(&self.related_to);
    }
        fn type_(&self) -> Option<&str> {
        return Some(&self.type_);
    }
}

impl Relationship for crate::RelationshipOrSubtype {
        fn started_at_time(&self) -> Option<&NaiveDate> {
        match self {
                RelationshipOrSubtype::Relationship(val) => val.started_at_time(),
                RelationshipOrSubtype::FamilialRelationship(val) => val.started_at_time(),

        }
    }
        fn ended_at_time(&self) -> Option<&NaiveDate> {
        match self {
                RelationshipOrSubtype::Relationship(val) => val.ended_at_time(),
                RelationshipOrSubtype::FamilialRelationship(val) => val.ended_at_time(),

        }
    }
        fn related_to(&self) -> Option<&str> {
        match self {
                RelationshipOrSubtype::Relationship(val) => val.related_to(),
                RelationshipOrSubtype::FamilialRelationship(val) => val.related_to(),

        }
    }
        fn type_(&self) -> Option<&str> {
        match self {
                RelationshipOrSubtype::Relationship(val) => val.type_(),
                RelationshipOrSubtype::FamilialRelationship(val) => val.type_(),

        }
    }
}

pub trait FamilialRelationship : Relationship   {


}

impl FamilialRelationship for crate::FamilialRelationship {
}


pub trait EmploymentEvent : Event   {

    fn employed_at(&self) -> Option<&str>;
    // fn employed_at_mut(&mut self) -> &mut Option<&str>;
    // fn set_employed_at<E>(&mut self, value: Option<&str>) where E: Into<String>;


}

impl EmploymentEvent for crate::EmploymentEvent {
        fn employed_at(&self) -> Option<&str> {
        return self.employed_at.as_deref();
    }
}


pub trait MedicalEvent : Event   {

    fn in_location(&self) -> Option<&str>;
    // fn in_location_mut(&mut self) -> &mut Option<&str>;
    // fn set_in_location<E>(&mut self, value: Option<&str>) where E: Into<String>;

    fn diagnosis(&self) -> Option<&crate::DiagnosisConcept>;
    // fn diagnosis_mut(&mut self) -> &mut Option<&crate::DiagnosisConcept>;
    // fn set_diagnosis<E>(&mut self, value: Option<E>) where E: Into<DiagnosisConcept>;

    fn procedure(&self) -> Option<&crate::ProcedureConcept>;
    // fn procedure_mut(&mut self) -> &mut Option<&crate::ProcedureConcept>;
    // fn set_procedure<E>(&mut self, value: Option<E>) where E: Into<ProcedureConcept>;


}

impl MedicalEvent for crate::MedicalEvent {
        fn in_location(&self) -> Option<&str> {
        return self.in_location.as_deref();
    }
        fn diagnosis(&self) -> Option<&crate::DiagnosisConcept> {
        return self.diagnosis.as_ref();
    }
        fn procedure(&self) -> Option<&crate::ProcedureConcept> {
        return self.procedure.as_ref();
    }
}


pub trait WithLocation   {

    fn in_location(&self) -> Option<&str>;
    // fn in_location_mut(&mut self) -> &mut Option<&str>;
    // fn set_in_location<E>(&mut self, value: Option<&str>) where E: Into<String>;


}

impl WithLocation for crate::WithLocation {
        fn in_location(&self) -> Option<&str> {
        return self.in_location.as_deref();
    }
}


pub trait Container   {

    fn persons(&self) -> impl poly_containers::SeqRef<crate::Person>;
    // fn persons_mut(&mut self) -> &mut impl poly_containers::SeqRef<crate::Person>;
    // fn set_persons<E>(&mut self, value: &Vec<E>) where E: Into<Person>;

    fn organizations(&self) -> impl poly_containers::SeqRef<crate::Organization>;
    // fn organizations_mut(&mut self) -> &mut impl poly_containers::SeqRef<crate::Organization>;
    // fn set_organizations<E>(&mut self, value: &Vec<E>) where E: Into<Organization>;


}

impl Container for crate::Container {
        fn persons(&self) -> impl poly_containers::SeqRef<crate::Person> {
        return &self.persons;
    }
        fn organizations(&self) -> impl poly_containers::SeqRef<crate::Organization> {
        return &self.organizations;
    }
}


