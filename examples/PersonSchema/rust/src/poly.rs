#![allow(non_camel_case_types)]

use crate::*;
use crate::poly_containers::*;


pub trait NamedThing   {

    fn id<'a>(&'a self) -> &'a crate::uriorcurie;
    // fn id_mut(&mut self) -> &mut &'a crate::uriorcurie;
    // fn set_id(&mut self, value: uriorcurie);

    fn name<'a>(&'a self) -> &'a str;
    // fn name_mut(&mut self) -> &mut &'a str;
    // fn set_name(&mut self, value: String);

    fn description<'a>(&'a self) -> Option<&'a str>;
    // fn description_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_description(&mut self, value: Option<&'a str>);

    fn depicted_by<'a>(&'a self) -> Option<&'a str>;
    // fn depicted_by_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_depicted_by(&mut self, value: Option<&'a str>);


}

impl NamedThing for crate::NamedThing {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}
impl NamedThing for crate::Person {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}
impl NamedThing for crate::Organization {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}
impl NamedThing for crate::Concept {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}
impl NamedThing for crate::DiagnosisConcept {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}
impl NamedThing for crate::ProcedureConcept {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}
impl NamedThing for crate::OperationProcedureConcept {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}
impl NamedThing for crate::ImagingProcedureConcept {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        return self.description.as_deref();
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}

impl NamedThing for crate::NamedThingOrSubtype {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        match self {
                NamedThingOrSubtype::Person(val) => val.id(),
                NamedThingOrSubtype::Organization(val) => val.id(),
                NamedThingOrSubtype::Concept(val) => val.id(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.id(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.id(),
                NamedThingOrSubtype::OperationProcedureConcept(val) => val.id(),
                NamedThingOrSubtype::ImagingProcedureConcept(val) => val.id(),

        }
    }
        fn name<'a>(&'a self) -> &'a str {
        match self {
                NamedThingOrSubtype::Person(val) => val.name(),
                NamedThingOrSubtype::Organization(val) => val.name(),
                NamedThingOrSubtype::Concept(val) => val.name(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.name(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.name(),
                NamedThingOrSubtype::OperationProcedureConcept(val) => val.name(),
                NamedThingOrSubtype::ImagingProcedureConcept(val) => val.name(),

        }
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        match self {
                NamedThingOrSubtype::Person(val) => val.description(),
                NamedThingOrSubtype::Organization(val) => val.description(),
                NamedThingOrSubtype::Concept(val) => val.description(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.description(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.description(),
                NamedThingOrSubtype::OperationProcedureConcept(val) => val.description(),
                NamedThingOrSubtype::ImagingProcedureConcept(val) => val.description(),

        }
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        match self {
                NamedThingOrSubtype::Person(val) => val.depicted_by(),
                NamedThingOrSubtype::Organization(val) => val.depicted_by(),
                NamedThingOrSubtype::Concept(val) => val.depicted_by(),
                NamedThingOrSubtype::DiagnosisConcept(val) => val.depicted_by(),
                NamedThingOrSubtype::ProcedureConcept(val) => val.depicted_by(),
                NamedThingOrSubtype::OperationProcedureConcept(val) => val.depicted_by(),
                NamedThingOrSubtype::ImagingProcedureConcept(val) => val.depicted_by(),

        }
    }
}
impl NamedThing for crate::ConceptOrSubtype {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        match self {
                ConceptOrSubtype::DiagnosisConcept(val) => val.id(),
                ConceptOrSubtype::ProcedureConcept(val) => val.id(),
                ConceptOrSubtype::OperationProcedureConcept(val) => val.id(),
                ConceptOrSubtype::ImagingProcedureConcept(val) => val.id(),

        }
    }
        fn name<'a>(&'a self) -> &'a str {
        match self {
                ConceptOrSubtype::DiagnosisConcept(val) => val.name(),
                ConceptOrSubtype::ProcedureConcept(val) => val.name(),
                ConceptOrSubtype::OperationProcedureConcept(val) => val.name(),
                ConceptOrSubtype::ImagingProcedureConcept(val) => val.name(),

        }
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        match self {
                ConceptOrSubtype::DiagnosisConcept(val) => val.description(),
                ConceptOrSubtype::ProcedureConcept(val) => val.description(),
                ConceptOrSubtype::OperationProcedureConcept(val) => val.description(),
                ConceptOrSubtype::ImagingProcedureConcept(val) => val.description(),

        }
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        match self {
                ConceptOrSubtype::DiagnosisConcept(val) => val.depicted_by(),
                ConceptOrSubtype::ProcedureConcept(val) => val.depicted_by(),
                ConceptOrSubtype::OperationProcedureConcept(val) => val.depicted_by(),
                ConceptOrSubtype::ImagingProcedureConcept(val) => val.depicted_by(),

        }
    }
}
impl NamedThing for crate::ProcedureConceptOrSubtype {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        match self {
                ProcedureConceptOrSubtype::OperationProcedureConcept(val) => val.id(),
                ProcedureConceptOrSubtype::ImagingProcedureConcept(val) => val.id(),

        }
    }
        fn name<'a>(&'a self) -> &'a str {
        match self {
                ProcedureConceptOrSubtype::OperationProcedureConcept(val) => val.name(),
                ProcedureConceptOrSubtype::ImagingProcedureConcept(val) => val.name(),

        }
    }
        fn description<'a>(&'a self) -> Option<&'a str> {
        match self {
                ProcedureConceptOrSubtype::OperationProcedureConcept(val) => val.description(),
                ProcedureConceptOrSubtype::ImagingProcedureConcept(val) => val.description(),

        }
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        match self {
                ProcedureConceptOrSubtype::OperationProcedureConcept(val) => val.depicted_by(),
                ProcedureConceptOrSubtype::ImagingProcedureConcept(val) => val.depicted_by(),

        }
    }
}

pub trait Person : NamedThing  +  HasAliases  +  HasNewsEvents   {

    fn primary_email<'a>(&'a self) -> Option<&'a str>;
    // fn primary_email_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_primary_email(&mut self, value: Option<&'a str>);

    fn birth_date<'a>(&'a self) -> Option<&'a str>;
    // fn birth_date_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_birth_date(&mut self, value: Option<&'a str>);

    fn age_in_years(&self) -> Option<isize>;
    // fn age_in_years_mut(&mut self) -> &mut Option<isize>;
    // fn set_age_in_years(&mut self, value: Option<isize>);

    fn gender<'a>(&'a self) -> Option<&'a crate::GenderType>;
    // fn gender_mut(&mut self) -> &mut Option<&'a crate::GenderType>;
    // fn set_gender(&mut self, value: Option<&'a GenderType>);

    fn current_address<'a>(&'a self) -> Option<&'a crate::Address>;
    // fn current_address_mut(&mut self) -> &mut Option<&'a crate::Address>;
    // fn set_current_address<E>(&mut self, value: Option<E>) where E: Into<Address>;

    fn telephone<'a>(&'a self) -> Option<&'a str>;
    // fn telephone_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_telephone(&mut self, value: Option<&'a str>);

    fn has_employment_history<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::EmploymentEvent>>;
    // fn has_employment_history_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::EmploymentEvent>>;
    // fn set_has_employment_history<E>(&mut self, value: Option<&Vec<E>>) where E: Into<EmploymentEvent>;

    fn has_familial_relationships<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::FamilialRelationship>>;
    // fn has_familial_relationships_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::FamilialRelationship>>;
    // fn set_has_familial_relationships<E>(&mut self, value: Option<&Vec<E>>) where E: Into<FamilialRelationship>;

    fn has_interpersonal_relationships<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::InterPersonalRelationship>>;
    // fn has_interpersonal_relationships_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::InterPersonalRelationship>>;
    // fn set_has_interpersonal_relationships<E>(&mut self, value: Option<&Vec<E>>) where E: Into<InterPersonalRelationship>;

    fn has_medical_history<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::MedicalEvent>>;
    // fn has_medical_history_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::MedicalEvent>>;
    // fn set_has_medical_history<E>(&mut self, value: Option<&Vec<E>>) where E: Into<MedicalEvent>;


}

impl Person for crate::Person {
        fn primary_email<'a>(&'a self) -> Option<&'a str> {
        return self.primary_email.as_deref();
    }
        fn birth_date<'a>(&'a self) -> Option<&'a str> {
        return self.birth_date.as_deref();
    }
        fn age_in_years(&self) -> Option<isize> {
        return self.age_in_years;
    }
        fn gender<'a>(&'a self) -> Option<&'a crate::GenderType> {
        return self.gender.as_ref();
    }
        fn current_address<'a>(&'a self) -> Option<&'a crate::Address> {
        return self.current_address.as_ref();
    }
        fn telephone<'a>(&'a self) -> Option<&'a str> {
        return self.telephone.as_deref();
    }
        fn has_employment_history<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::EmploymentEvent>> {
        return self.has_employment_history.as_ref();
    }
        fn has_familial_relationships<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::FamilialRelationship>> {
        return self.has_familial_relationships.as_ref().map(|x| poly_containers::ListView::new(x));
    }
        fn has_interpersonal_relationships<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::InterPersonalRelationship>> {
        return self.has_interpersonal_relationships.as_ref().map(|x| poly_containers::ListView::new(x));
    }
        fn has_medical_history<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::MedicalEvent>> {
        return self.has_medical_history.as_ref();
    }
}


pub trait HasAliases   {

    fn aliases<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>>;
    // fn aliases_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, String>>;
    // fn set_aliases(&mut self, value: Option<&Vec<String>>);


}

impl HasAliases for crate::HasAliases {
        fn aliases<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.aliases.as_ref();
    }
}
impl HasAliases for crate::Person {
        fn aliases<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.aliases.as_ref();
    }
}
impl HasAliases for crate::Organization {
        fn aliases<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.aliases.as_ref();
    }
}
impl HasAliases for crate::Place {
        fn aliases<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.aliases.as_ref();
    }
}

impl HasAliases for crate::HasAliasesOrSubtype {
        fn aliases<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        match self {
                HasAliasesOrSubtype::Person(val) => val.aliases().map(|x| x.to_any()),
                HasAliasesOrSubtype::Organization(val) => val.aliases().map(|x| x.to_any()),
                HasAliasesOrSubtype::Place(val) => val.aliases().map(|x| x.to_any()),

        }
    }
}

pub trait HasNewsEvents   {

    fn has_news_events<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::NewsEvent>>;
    // fn has_news_events_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::NewsEvent>>;
    // fn set_has_news_events<E>(&mut self, value: Option<&Vec<E>>) where E: Into<NewsEvent>;


}

impl HasNewsEvents for crate::HasNewsEvents {
        fn has_news_events<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::NewsEvent>> {
        return self.has_news_events.as_ref();
    }
}
impl HasNewsEvents for crate::Person {
        fn has_news_events<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::NewsEvent>> {
        return self.has_news_events.as_ref();
    }
}
impl HasNewsEvents for crate::Organization {
        fn has_news_events<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::NewsEvent>> {
        return self.has_news_events.as_ref();
    }
}

impl HasNewsEvents for crate::HasNewsEventsOrSubtype {
        fn has_news_events<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::NewsEvent>> {
        match self {
                HasNewsEventsOrSubtype::Person(val) => val.has_news_events().map(|x| x.to_any()),
                HasNewsEventsOrSubtype::Organization(val) => val.has_news_events().map(|x| x.to_any()),

        }
    }
}

pub trait Organization : NamedThing  +  HasAliases  +  HasNewsEvents   {

    fn mission_statement<'a>(&'a self) -> Option<&'a str>;
    // fn mission_statement_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_mission_statement(&mut self, value: Option<&'a str>);

    fn founding_date<'a>(&'a self) -> Option<&'a str>;
    // fn founding_date_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_founding_date(&mut self, value: Option<&'a str>);

    fn founding_location<'a>(&'a self) -> Option<&'a str>;
    // fn founding_location_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_founding_location<E>(&mut self, value: Option<&'a str>) where E: Into<String>;

    fn categories<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::OrganizationType>>;
    // fn categories_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::OrganizationType>>;
    // fn set_categories(&mut self, value: Option<&Vec<OrganizationType>>);

    fn score(&self) -> Option<f64>;
    // fn score_mut(&mut self) -> &mut Option<f64>;
    // fn set_score(&mut self, value: Option<f64>);

    fn min_salary(&self) -> Option<f64>;
    // fn min_salary_mut(&mut self) -> &mut Option<f64>;
    // fn set_min_salary(&mut self, value: Option<f64>);


}

impl Organization for crate::Organization {
        fn mission_statement<'a>(&'a self) -> Option<&'a str> {
        return self.mission_statement.as_deref();
    }
        fn founding_date<'a>(&'a self) -> Option<&'a str> {
        return self.founding_date.as_deref();
    }
        fn founding_location<'a>(&'a self) -> Option<&'a str> {
        return self.founding_location.as_deref();
    }
        fn categories<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::OrganizationType>> {
        return self.categories.as_ref();
    }
        fn score(&self) -> Option<f64> {
        return self.score;
    }
        fn min_salary(&self) -> Option<f64> {
        return self.min_salary;
    }
}


pub trait Place : HasAliases   {

    fn id<'a>(&'a self) -> &'a crate::uriorcurie;
    // fn id_mut(&mut self) -> &mut &'a crate::uriorcurie;
    // fn set_id(&mut self, value: uriorcurie);

    fn name<'a>(&'a self) -> &'a str;
    // fn name_mut(&mut self) -> &mut &'a str;
    // fn set_name(&mut self, value: String);

    fn depicted_by<'a>(&'a self) -> Option<&'a str>;
    // fn depicted_by_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_depicted_by(&mut self, value: Option<&'a str>);


}

impl Place for crate::Place {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
        fn depicted_by<'a>(&'a self) -> Option<&'a str> {
        return self.depicted_by.as_deref();
    }
}


pub trait Address   {

    fn street<'a>(&'a self) -> Option<&'a str>;
    // fn street_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_street(&mut self, value: Option<&'a str>);

    fn city<'a>(&'a self) -> Option<&'a str>;
    // fn city_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_city(&mut self, value: Option<&'a str>);

    fn postal_code<'a>(&'a self) -> Option<&'a str>;
    // fn postal_code_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_postal_code(&mut self, value: Option<&'a str>);


}

impl Address for crate::Address {
        fn street<'a>(&'a self) -> Option<&'a str> {
        return self.street.as_deref();
    }
        fn city<'a>(&'a self) -> Option<&'a str> {
        return self.city.as_deref();
    }
        fn postal_code<'a>(&'a self) -> Option<&'a str> {
        return self.postal_code.as_deref();
    }
}


pub trait Event   {

    fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate>;
    // fn started_at_time_mut(&mut self) -> &mut Option<&'a crate::NaiveDate>;
    // fn set_started_at_time(&mut self, value: Option<&'a NaiveDate>);

    fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate>;
    // fn ended_at_time_mut(&mut self) -> &mut Option<&'a crate::NaiveDate>;
    // fn set_ended_at_time(&mut self, value: Option<&'a NaiveDate>);

    fn duration(&self) -> Option<f64>;
    // fn duration_mut(&mut self) -> &mut Option<f64>;
    // fn set_duration(&mut self, value: Option<f64>);

    fn is_current(&self) -> Option<bool>;
    // fn is_current_mut(&mut self) -> &mut Option<bool>;
    // fn set_is_current(&mut self, value: Option<bool>);


}

impl Event for crate::Event {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn duration(&self) -> Option<f64> {
        return self.duration;
    }
        fn is_current(&self) -> Option<bool> {
        return self.is_current;
    }
}
impl Event for crate::NewsEvent {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn duration(&self) -> Option<f64> {
        return self.duration;
    }
        fn is_current(&self) -> Option<bool> {
        return self.is_current;
    }
}
impl Event for crate::EmploymentEvent {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn duration(&self) -> Option<f64> {
        return self.duration;
    }
        fn is_current(&self) -> Option<bool> {
        return self.is_current;
    }
}
impl Event for crate::MedicalEvent {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn duration(&self) -> Option<f64> {
        return self.duration;
    }
        fn is_current(&self) -> Option<bool> {
        return self.is_current;
    }
}

impl Event for crate::EventOrSubtype {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        match self {
                EventOrSubtype::NewsEvent(val) => val.started_at_time(),
                EventOrSubtype::EmploymentEvent(val) => val.started_at_time(),
                EventOrSubtype::MedicalEvent(val) => val.started_at_time(),

        }
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        match self {
                EventOrSubtype::NewsEvent(val) => val.ended_at_time(),
                EventOrSubtype::EmploymentEvent(val) => val.ended_at_time(),
                EventOrSubtype::MedicalEvent(val) => val.ended_at_time(),

        }
    }
        fn duration(&self) -> Option<f64> {
        match self {
                EventOrSubtype::NewsEvent(val) => val.duration(),
                EventOrSubtype::EmploymentEvent(val) => val.duration(),
                EventOrSubtype::MedicalEvent(val) => val.duration(),

        }
    }
        fn is_current(&self) -> Option<bool> {
        match self {
                EventOrSubtype::NewsEvent(val) => val.is_current(),
                EventOrSubtype::EmploymentEvent(val) => val.is_current(),
                EventOrSubtype::MedicalEvent(val) => val.is_current(),

        }
    }
}

pub trait NewsEvent : Event   {

    fn headline<'a>(&'a self) -> Option<&'a str>;
    // fn headline_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_headline(&mut self, value: Option<&'a str>);


}

impl NewsEvent for crate::NewsEvent {
        fn headline<'a>(&'a self) -> Option<&'a str> {
        return self.headline.as_deref();
    }
}


pub trait Concept : NamedThing   {

    fn code_system<'a>(&'a self) -> Option<&'a str>;
    // fn code_system_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_code_system<E>(&mut self, value: Option<&'a str>) where E: Into<String>;

    fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>>;
    // fn mappings_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, String>>;
    // fn set_mappings(&mut self, value: Option<&Vec<String>>);


}

impl Concept for crate::Concept {
        fn code_system<'a>(&'a self) -> Option<&'a str> {
        return self.code_system.as_deref();
    }
        fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.mappings.as_ref();
    }
}
impl Concept for crate::DiagnosisConcept {
        fn code_system<'a>(&'a self) -> Option<&'a str> {
        return self.code_system.as_deref();
    }
        fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.mappings.as_ref();
    }
}
impl Concept for crate::ProcedureConcept {
        fn code_system<'a>(&'a self) -> Option<&'a str> {
        return self.code_system.as_deref();
    }
        fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.mappings.as_ref();
    }
}
impl Concept for crate::OperationProcedureConcept {
        fn code_system<'a>(&'a self) -> Option<&'a str> {
        return self.code_system.as_deref();
    }
        fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.mappings.as_ref();
    }
}
impl Concept for crate::ImagingProcedureConcept {
        fn code_system<'a>(&'a self) -> Option<&'a str> {
        return self.code_system.as_deref();
    }
        fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        return self.mappings.as_ref();
    }
}

impl Concept for crate::ConceptOrSubtype {
        fn code_system<'a>(&'a self) -> Option<&'a str> {
        match self {
                ConceptOrSubtype::DiagnosisConcept(val) => val.code_system(),
                ConceptOrSubtype::ProcedureConcept(val) => val.code_system(),
                ConceptOrSubtype::OperationProcedureConcept(val) => val.code_system(),
                ConceptOrSubtype::ImagingProcedureConcept(val) => val.code_system(),

        }
    }
        fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        match self {
                ConceptOrSubtype::DiagnosisConcept(val) => val.mappings().map(|x| x.to_any()),
                ConceptOrSubtype::ProcedureConcept(val) => val.mappings().map(|x| x.to_any()),
                ConceptOrSubtype::OperationProcedureConcept(val) => val.mappings().map(|x| x.to_any()),
                ConceptOrSubtype::ImagingProcedureConcept(val) => val.mappings().map(|x| x.to_any()),

        }
    }
}
impl Concept for crate::ProcedureConceptOrSubtype {
        fn code_system<'a>(&'a self) -> Option<&'a str> {
        match self {
                ProcedureConceptOrSubtype::OperationProcedureConcept(val) => val.code_system(),
                ProcedureConceptOrSubtype::ImagingProcedureConcept(val) => val.code_system(),

        }
    }
        fn mappings<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, String>> {
        match self {
                ProcedureConceptOrSubtype::OperationProcedureConcept(val) => val.mappings().map(|x| x.to_any()),
                ProcedureConceptOrSubtype::ImagingProcedureConcept(val) => val.mappings().map(|x| x.to_any()),

        }
    }
}

pub trait DiagnosisConcept : Concept   {


}

impl DiagnosisConcept for crate::DiagnosisConcept {
}


pub trait ProcedureConcept : Concept   {


}

impl ProcedureConcept for crate::ProcedureConcept {
}
impl ProcedureConcept for crate::OperationProcedureConcept {
}
impl ProcedureConcept for crate::ImagingProcedureConcept {
}

impl ProcedureConcept for crate::ProcedureConceptOrSubtype {
}

pub trait IntegerPrimaryKeyObject   {

    fn int_id(&self) -> isize;
    // fn int_id_mut(&mut self) -> &mut isize;
    // fn set_int_id(&mut self, value: isize);


}

impl IntegerPrimaryKeyObject for crate::IntegerPrimaryKeyObject {
        fn int_id(&self) -> isize {
        return self.int_id;
    }
}


pub trait OperationProcedureConcept : ProcedureConcept   {


}

impl OperationProcedureConcept for crate::OperationProcedureConcept {
}


pub trait ImagingProcedureConcept : ProcedureConcept   {


}

impl ImagingProcedureConcept for crate::ImagingProcedureConcept {
}


pub trait CodeSystem   {

    fn id<'a>(&'a self) -> &'a crate::uriorcurie;
    // fn id_mut(&mut self) -> &mut &'a crate::uriorcurie;
    // fn set_id(&mut self, value: uriorcurie);

    fn name<'a>(&'a self) -> &'a str;
    // fn name_mut(&mut self) -> &mut &'a str;
    // fn set_name(&mut self, value: String);


}

impl CodeSystem for crate::CodeSystem {
        fn id<'a>(&'a self) -> &'a crate::uriorcurie {
        return &self.id;
    }
        fn name<'a>(&'a self) -> &'a str {
        return &self.name[..];
    }
}


pub trait Relationship   {

    fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate>;
    // fn started_at_time_mut(&mut self) -> &mut Option<&'a crate::NaiveDate>;
    // fn set_started_at_time(&mut self, value: Option<&'a NaiveDate>);

    fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate>;
    // fn ended_at_time_mut(&mut self) -> &mut Option<&'a crate::NaiveDate>;
    // fn set_ended_at_time(&mut self, value: Option<&'a NaiveDate>);

    fn related_to<'a>(&'a self) -> Option<&'a str>;
    // fn related_to_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_related_to<E>(&mut self, value: Option<&'a str>) where E: Into<String>;

    fn type_(&self) -> Option<relationship_utl::type__range>;
    // fn type__mut(&mut self) -> &mut Option<relationship_utl::type__range>;
    // fn set_type_(&mut self, value: Option<&'a str>);


}

impl Relationship for crate::Relationship {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn related_to<'a>(&'a self) -> Option<&'a str> {
        return self.related_to.as_deref();
    }
        fn type_(&self) -> Option<relationship_utl::type__range> {
                self.type_.as_ref().map(|v| relationship_utl::type__range::String(v.clone()))
    }
}
impl Relationship for crate::FamilialRelationship {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn related_to<'a>(&'a self) -> Option<&'a str> {
        return self.related_to.as_deref();
    }
        fn type_(&self) -> Option<relationship_utl::type__range> {
                Some(relationship_utl::type__range::FamilialRelationshipType(self.type_.clone()))
    }
}
impl Relationship for crate::InterPersonalRelationship {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.started_at_time.as_ref();
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        return self.ended_at_time.as_ref();
    }
        fn related_to<'a>(&'a self) -> Option<&'a str> {
        return self.related_to.as_deref();
    }
        fn type_(&self) -> Option<relationship_utl::type__range> {
                Some(match &self.type_ {
                    inter_personal_relationship_utl::type__range::String(x) => relationship_utl::type__range::String(x.clone()),
                    inter_personal_relationship_utl::type__range::FamilialRelationshipType(x) => relationship_utl::type__range::FamilialRelationshipType(x.clone()),
                    inter_personal_relationship_utl::type__range::NonFamilialRelationshipType(x) => relationship_utl::type__range::NonFamilialRelationshipType(x.clone()),
                })
    }
}

impl Relationship for crate::RelationshipOrSubtype {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        match self {
                RelationshipOrSubtype::FamilialRelationship(val) => val.started_at_time(),
                RelationshipOrSubtype::InterPersonalRelationship(val) => val.started_at_time(),

        }
    }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
        match self {
                RelationshipOrSubtype::FamilialRelationship(val) => val.ended_at_time(),
                RelationshipOrSubtype::InterPersonalRelationship(val) => val.ended_at_time(),

        }
    }
        fn related_to<'a>(&'a self) -> Option<&'a str> {
        match self {
                RelationshipOrSubtype::FamilialRelationship(val) => val.related_to(),
                RelationshipOrSubtype::InterPersonalRelationship(val) => val.related_to(),

        }
    }
        fn type_(&self) -> Option<relationship_utl::type__range> {
        match self {
                RelationshipOrSubtype::FamilialRelationship(val) => val.type_(),
                RelationshipOrSubtype::InterPersonalRelationship(val) => val.type_(),

        }
    }
}

pub trait FamilialRelationship : Relationship   {


}

impl FamilialRelationship for crate::FamilialRelationship {
}


pub trait InterPersonalRelationship : Relationship   {


}

impl InterPersonalRelationship for crate::InterPersonalRelationship {
}


pub trait EmploymentEvent : Event   {

    fn employed_at<'a>(&'a self) -> Option<&'a str>;
    // fn employed_at_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_employed_at<E>(&mut self, value: Option<&'a str>) where E: Into<String>;

    fn salary(&self) -> Option<f64>;
    // fn salary_mut(&mut self) -> &mut Option<f64>;
    // fn set_salary(&mut self, value: Option<f64>);


}

impl EmploymentEvent for crate::EmploymentEvent {
        fn employed_at<'a>(&'a self) -> Option<&'a str> {
        return self.employed_at.as_deref();
    }
        fn salary(&self) -> Option<f64> {
        return self.salary;
    }
}


pub trait MedicalEvent : Event  +  WithLocation   {

    fn diagnosis<'a>(&'a self) -> Option<&'a crate::DiagnosisConcept>;
    // fn diagnosis_mut(&mut self) -> &mut Option<&'a crate::DiagnosisConcept>;
    // fn set_diagnosis<E>(&mut self, value: Option<E>) where E: Into<DiagnosisConcept>;

    fn procedure<'a>(&'a self) -> Option<&'a ProcedureConceptOrSubtype>;
    // fn procedure_mut(&mut self) -> &mut Option<&'a ProcedureConceptOrSubtype>;
    // fn set_procedure<E>(&mut self, value: Option<E>) where E: Into<ProcedureConcept>;


}

impl MedicalEvent for crate::MedicalEvent {
        fn diagnosis<'a>(&'a self) -> Option<&'a crate::DiagnosisConcept> {
        return self.diagnosis.as_ref();
    }
        fn procedure<'a>(&'a self) -> Option<&'a ProcedureConceptOrSubtype> {
        return self.procedure.as_ref();
    }
}


pub trait WithLocation   {

    fn in_location<'a>(&'a self) -> Option<&'a str>;
    // fn in_location_mut(&mut self) -> &mut Option<&'a str>;
    // fn set_in_location<E>(&mut self, value: Option<&'a str>) where E: Into<String>;


}

impl WithLocation for crate::WithLocation {
        fn in_location<'a>(&'a self) -> Option<&'a str> {
        return self.in_location.as_deref();
    }
}
impl WithLocation for crate::MedicalEvent {
        fn in_location<'a>(&'a self) -> Option<&'a str> {
        return self.in_location.as_deref();
    }
}

impl WithLocation for crate::WithLocationOrSubtype {
        fn in_location<'a>(&'a self) -> Option<&'a str> {
        match self {
                WithLocationOrSubtype::MedicalEvent(val) => val.in_location(),

        }
    }
}

pub trait Container   {

    fn persons<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::Person>>;
    // fn persons_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::Person>>;
    // fn set_persons<E>(&mut self, value: Option<&Vec<E>>) where E: Into<Person>;

    fn organizations<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::Organization>>;
    // fn organizations_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::Organization>>;
    // fn set_organizations<E>(&mut self, value: Option<&Vec<E>>) where E: Into<Organization>;

    fn places<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::Place>>;
    // fn places_mut(&mut self) -> &mut Option<impl poly_containers::SeqRef<'a, crate::Place>>;
    // fn set_places<E>(&mut self, value: Option<&Vec<E>>) where E: Into<Place>;


}

impl Container for crate::Container {
        fn persons<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::Person>> {
        return self.persons.as_ref();
    }
        fn organizations<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::Organization>> {
        return self.organizations.as_ref();
    }
        fn places<'a>(&'a self) -> Option<impl poly_containers::SeqRef<'a, crate::Place>> {
        return self.places.as_ref();
    }
}
