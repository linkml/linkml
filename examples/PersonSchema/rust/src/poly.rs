#![allow(non_camel_case_types)]

use crate::*;
use crate::poly_containers::*;


pub trait NamedThing   {

    fn id(&self) -> &String;
    // fn id_mut(&mut self) -> &mut &String;
    // fn set_id(&mut self, value: String);

    fn name(&self) -> &Option<String>;
    // fn name_mut(&mut self) -> &mut &Option<String>;
    // fn set_name(&mut self, value: &Option<String>);

    fn description(&self) -> &Option<String>;
    // fn description_mut(&mut self) -> &mut &Option<String>;
    // fn set_description(&mut self, value: &Option<String>);

    fn image(&self) -> &Option<String>;
    // fn image_mut(&mut self) -> &mut &Option<String>;
    // fn set_image(&mut self, value: &Option<String>);


}

impl NamedThing for crate::NamedThing {
        fn id(&self) -> &String {
        return &self.id;
    }
        fn name(&self) -> &Option<String> {
        return &self.name;
    }
        fn description(&self) -> &Option<String> {
        return &self.description;
    }
        fn image(&self) -> &Option<String> {
        return &self.image;
    }
}
impl NamedThing for crate::Person {
        fn id(&self) -> &String {
        return &self.id;
    }
        fn name(&self) -> &Option<String> {
        return &self.name;
    }
        fn description(&self) -> &Option<String> {
        return &self.description;
    }
        fn image(&self) -> &Option<String> {
        return &self.image;
    }
}
impl NamedThing for crate::Organization {
        fn id(&self) -> &String {
        return &self.id;
    }
        fn name(&self) -> &Option<String> {
        return &self.name;
    }
        fn description(&self) -> &Option<String> {
        return &self.description;
    }
        fn image(&self) -> &Option<String> {
        return &self.image;
    }
}
impl NamedThing for crate::Concept {
        fn id(&self) -> &String {
        return &self.id;
    }
        fn name(&self) -> &Option<String> {
        return &self.name;
    }
        fn description(&self) -> &Option<String> {
        return &self.description;
    }
        fn image(&self) -> &Option<String> {
        return &self.image;
    }
}
impl NamedThing for crate::DiagnosisConcept {
        fn id(&self) -> &String {
        return &self.id;
    }
        fn name(&self) -> &Option<String> {
        return &self.name;
    }
        fn description(&self) -> &Option<String> {
        return &self.description;
    }
        fn image(&self) -> &Option<String> {
        return &self.image;
    }
}
impl NamedThing for crate::ProcedureConcept {
        fn id(&self) -> &String {
        return &self.id;
    }
        fn name(&self) -> &Option<String> {
        return &self.name;
    }
        fn description(&self) -> &Option<String> {
        return &self.description;
    }
        fn image(&self) -> &Option<String> {
        return &self.image;
    }
}

impl NamedThing for crate::NamedThingOrSubtype {
        fn id(&self) -> &String {
        match self {
                NamedThingOrSubtype::NamedThing(val) => val.id(),
                NamedThingOrSubtype::Person(val) => val.id(),
                NamedThingOrSubtype::Organization(val) => val.id(),
                NamedThingOrSubtype::Concept(val) => val.id(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.id(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.id(),

        }
    }
        fn name(&self) -> &Option<String> {
        match self {
                NamedThingOrSubtype::NamedThing(val) => val.name(),
                NamedThingOrSubtype::Person(val) => val.name(),
                NamedThingOrSubtype::Organization(val) => val.name(),
                NamedThingOrSubtype::Concept(val) => val.name(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.name(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.name(),

        }
    }
        fn description(&self) -> &Option<String> {
        match self {
                NamedThingOrSubtype::NamedThing(val) => val.description(),
                NamedThingOrSubtype::Person(val) => val.description(),
                NamedThingOrSubtype::Organization(val) => val.description(),
                NamedThingOrSubtype::Concept(val) => val.description(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.description(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.description(),

        }
    }
        fn image(&self) -> &Option<String> {
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
        fn id(&self) -> &String {
        match self {
                ConceptOrSubtype::Concept(val) => val.id(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.id(),
                ConceptOrSubtype::ProcedureConcept(val) => val.id(),

        }
    }
        fn name(&self) -> &Option<String> {
        match self {
                ConceptOrSubtype::Concept(val) => val.name(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.name(),
                ConceptOrSubtype::ProcedureConcept(val) => val.name(),

        }
    }
        fn description(&self) -> &Option<String> {
        match self {
                ConceptOrSubtype::Concept(val) => val.description(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.description(),
                ConceptOrSubtype::ProcedureConcept(val) => val.description(),

        }
    }
        fn image(&self) -> &Option<String> {
        match self {
                ConceptOrSubtype::Concept(val) => val.image(),
                ConceptOrSubtype::DiagnosisConcept(val) => val.image(),
                ConceptOrSubtype::ProcedureConcept(val) => val.image(),

        }
    }
}

pub trait Person : NamedThing  +  HasAliases   {

    fn primary_email(&self) -> &Option<String>;
    // fn primary_email_mut(&mut self) -> &mut &Option<String>;
    // fn set_primary_email(&mut self, value: &Option<String>);

    fn birth_date(&self) -> &Option<String>;
    // fn birth_date_mut(&mut self) -> &mut &Option<String>;
    // fn set_birth_date(&mut self, value: &Option<String>);

    fn age_in_years(&self) -> &Option<isize>;
    // fn age_in_years_mut(&mut self) -> &mut &Option<isize>;
    // fn set_age_in_years(&mut self, value: &Option<isize>);

    fn gender(&self) -> &Option<String>;
    // fn gender_mut(&mut self) -> &mut &Option<String>;
    // fn set_gender(&mut self, value: &Option<String>);

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
        fn primary_email(&self) -> &Option<String> {
        return &self.primary_email;
    }
        fn birth_date(&self) -> &Option<String> {
        return &self.birth_date;
    }
        fn age_in_years(&self) -> &Option<isize> {
        return &self.age_in_years;
    }
        fn gender(&self) -> &Option<String> {
        return &self.gender;
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

    fn mission_statement(&self) -> &Option<String>;
    // fn mission_statement_mut(&mut self) -> &mut &Option<String>;
    // fn set_mission_statement(&mut self, value: &Option<String>);

    fn founding_date(&self) -> &Option<String>;
    // fn founding_date_mut(&mut self) -> &mut &Option<String>;
    // fn set_founding_date(&mut self, value: &Option<String>);

    fn founding_location(&self) -> &Option<String>;
    // fn founding_location_mut(&mut self) -> &mut &Option<String>;
    // fn set_founding_location<E>(&mut self, value: &Option<String>) where E: Into<String>;


}

impl Organization for crate::Organization {
        fn mission_statement(&self) -> &Option<String> {
        return &self.mission_statement;
    }
        fn founding_date(&self) -> &Option<String> {
        return &self.founding_date;
    }
        fn founding_location(&self) -> &Option<String> {
        return &self.founding_location;
    }
}


pub trait Place : HasAliases   {

    fn id(&self) -> &String;
    // fn id_mut(&mut self) -> &mut &String;
    // fn set_id(&mut self, value: String);

    fn name(&self) -> &Option<String>;
    // fn name_mut(&mut self) -> &mut &Option<String>;
    // fn set_name(&mut self, value: &Option<String>);


}

impl Place for crate::Place {
        fn id(&self) -> &String {
        return &self.id;
    }
        fn name(&self) -> &Option<String> {
        return &self.name;
    }
}


pub trait Address   {

    fn street(&self) -> &Option<String>;
    // fn street_mut(&mut self) -> &mut &Option<String>;
    // fn set_street(&mut self, value: &Option<String>);

    fn city(&self) -> &Option<String>;
    // fn city_mut(&mut self) -> &mut &Option<String>;
    // fn set_city(&mut self, value: &Option<String>);

    fn postal_code(&self) -> &Option<String>;
    // fn postal_code_mut(&mut self) -> &mut &Option<String>;
    // fn set_postal_code(&mut self, value: &Option<String>);


}

impl Address for crate::Address {
        fn street(&self) -> &Option<String> {
        return &self.street;
    }
        fn city(&self) -> &Option<String> {
        return &self.city;
    }
        fn postal_code(&self) -> &Option<String> {
        return &self.postal_code;
    }
}


pub trait Event   {

    fn started_at_time(&self) -> &Option<NaiveDate>;
    // fn started_at_time_mut(&mut self) -> &mut &Option<NaiveDate>;
    // fn set_started_at_time(&mut self, value: &Option<NaiveDate>);

    fn ended_at_time(&self) -> &Option<NaiveDate>;
    // fn ended_at_time_mut(&mut self) -> &mut &Option<NaiveDate>;
    // fn set_ended_at_time(&mut self, value: &Option<NaiveDate>);

    fn duration(&self) -> &Option<f64>;
    // fn duration_mut(&mut self) -> &mut &Option<f64>;
    // fn set_duration(&mut self, value: &Option<f64>);

    fn is_current(&self) -> &Option<bool>;
    // fn is_current_mut(&mut self) -> &mut &Option<bool>;
    // fn set_is_current(&mut self, value: &Option<bool>);


}

impl Event for crate::Event {
        fn started_at_time(&self) -> &Option<NaiveDate> {
        return &self.started_at_time;
    }
        fn ended_at_time(&self) -> &Option<NaiveDate> {
        return &self.ended_at_time;
    }
        fn duration(&self) -> &Option<f64> {
        return &self.duration;
    }
        fn is_current(&self) -> &Option<bool> {
        return &self.is_current;
    }
}
impl Event for crate::EmploymentEvent {
        fn started_at_time(&self) -> &Option<NaiveDate> {
        return &self.started_at_time;
    }
        fn ended_at_time(&self) -> &Option<NaiveDate> {
        return &self.ended_at_time;
    }
        fn duration(&self) -> &Option<f64> {
        return &self.duration;
    }
        fn is_current(&self) -> &Option<bool> {
        return &self.is_current;
    }
}
impl Event for crate::MedicalEvent {
        fn started_at_time(&self) -> &Option<NaiveDate> {
        return &self.started_at_time;
    }
        fn ended_at_time(&self) -> &Option<NaiveDate> {
        return &self.ended_at_time;
    }
        fn duration(&self) -> &Option<f64> {
        return &self.duration;
    }
        fn is_current(&self) -> &Option<bool> {
        return &self.is_current;
    }
}

impl Event for crate::EventOrSubtype {
        fn started_at_time(&self) -> &Option<NaiveDate> {
        match self {
                EventOrSubtype::Event(val) => val.started_at_time(),
                EventOrSubtype::EmploymentEvent(val) => val.started_at_time(),
                EventOrSubtype::MedicalEvent(val) => val.started_at_time(),

        }
    }
        fn ended_at_time(&self) -> &Option<NaiveDate> {
        match self {
                EventOrSubtype::Event(val) => val.ended_at_time(),
                EventOrSubtype::EmploymentEvent(val) => val.ended_at_time(),
                EventOrSubtype::MedicalEvent(val) => val.ended_at_time(),

        }
    }
        fn duration(&self) -> &Option<f64> {
        match self {
                EventOrSubtype::Event(val) => val.duration(),
                EventOrSubtype::EmploymentEvent(val) => val.duration(),
                EventOrSubtype::MedicalEvent(val) => val.duration(),

        }
    }
        fn is_current(&self) -> &Option<bool> {
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

    fn started_at_time(&self) -> &Option<NaiveDate>;
    // fn started_at_time_mut(&mut self) -> &mut &Option<NaiveDate>;
    // fn set_started_at_time(&mut self, value: &Option<NaiveDate>);

    fn ended_at_time(&self) -> &Option<NaiveDate>;
    // fn ended_at_time_mut(&mut self) -> &mut &Option<NaiveDate>;
    // fn set_ended_at_time(&mut self, value: &Option<NaiveDate>);

    fn related_to(&self) -> &Option<String>;
    // fn related_to_mut(&mut self) -> &mut &Option<String>;
    // fn set_related_to(&mut self, value: &Option<String>);

    fn type_(&self) -> &Option<String>;
    // fn type__mut(&mut self) -> &mut &Option<String>;
    // fn set_type_(&mut self, value: &Option<String>);


}

impl Relationship for crate::Relationship {
        fn started_at_time(&self) -> &Option<NaiveDate> {
        return &self.started_at_time;
    }
        fn ended_at_time(&self) -> &Option<NaiveDate> {
        return &self.ended_at_time;
    }
        fn related_to(&self) -> &Option<String> {
        return &self.related_to;
    }
        fn type_(&self) -> &Option<String> {
        return &self.type_;
    }
}
impl Relationship for crate::FamilialRelationship {
        fn started_at_time(&self) -> &Option<NaiveDate> {
        return &self.started_at_time;
    }
        fn ended_at_time(&self) -> &Option<NaiveDate> {
        return &self.ended_at_time;
    }
        fn related_to(&self) -> &Option<String> {
        return &self.related_to;
    }
        fn type_(&self) -> &Option<String> {
        return &self.type_;
    }
}

impl Relationship for crate::RelationshipOrSubtype {
        fn started_at_time(&self) -> &Option<NaiveDate> {
        match self {
                RelationshipOrSubtype::Relationship(val) => val.started_at_time(),
                RelationshipOrSubtype::FamilialRelationship(val) => val.started_at_time(),

        }
    }
        fn ended_at_time(&self) -> &Option<NaiveDate> {
        match self {
                RelationshipOrSubtype::Relationship(val) => val.ended_at_time(),
                RelationshipOrSubtype::FamilialRelationship(val) => val.ended_at_time(),

        }
    }
        fn related_to(&self) -> &Option<String> {
        match self {
                RelationshipOrSubtype::Relationship(val) => val.related_to(),
                RelationshipOrSubtype::FamilialRelationship(val) => val.related_to(),

        }
    }
        fn type_(&self) -> &Option<String> {
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

    fn employed_at(&self) -> &Option<String>;
    // fn employed_at_mut(&mut self) -> &mut &Option<String>;
    // fn set_employed_at<E>(&mut self, value: &Option<String>) where E: Into<String>;


}

impl EmploymentEvent for crate::EmploymentEvent {
        fn employed_at(&self) -> &Option<String> {
        return &self.employed_at;
    }
}


pub trait MedicalEvent : Event   {

    fn in_location(&self) -> &Option<String>;
    // fn in_location_mut(&mut self) -> &mut &Option<String>;
    // fn set_in_location<E>(&mut self, value: &Option<String>) where E: Into<String>;

    fn diagnosis(&self) -> Option<&crate::DiagnosisConcept>;
    // fn diagnosis_mut(&mut self) -> &mut Option<&crate::DiagnosisConcept>;
    // fn set_diagnosis<E>(&mut self, value: Option<E>) where E: Into<DiagnosisConcept>;

    fn procedure(&self) -> Option<&crate::ProcedureConcept>;
    // fn procedure_mut(&mut self) -> &mut Option<&crate::ProcedureConcept>;
    // fn set_procedure<E>(&mut self, value: Option<E>) where E: Into<ProcedureConcept>;


}

impl MedicalEvent for crate::MedicalEvent {
        fn in_location(&self) -> &Option<String> {
        return &self.in_location;
    }
        fn diagnosis(&self) -> Option<&crate::DiagnosisConcept> {
        return self.diagnosis.as_ref();
    }
        fn procedure(&self) -> Option<&crate::ProcedureConcept> {
        return self.procedure.as_ref();
    }
}


pub trait WithLocation   {

    fn in_location(&self) -> &Option<String>;
    // fn in_location_mut(&mut self) -> &mut &Option<String>;
    // fn set_in_location<E>(&mut self, value: &Option<String>) where E: Into<String>;


}

impl WithLocation for crate::WithLocation {
        fn in_location(&self) -> &Option<String> {
        return &self.in_location;
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


