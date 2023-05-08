export type PersonId = string
export type OrganizationId = string
export type PlaceId = string
export type ConceptId = string
export type DiagnosisConceptId = string
export type ProcedureConceptId = string
export type CompanyId = string
export type CodeSystemId = string
export type ActivityId = string
export type AgentId = string

export interface HasAliases  {
    aliases?: string,
};

export interface Friend  {
    name?: string,
};
/**
 * A person, living or dead
 */
export interface Person  extends HasAliases  {
    id: string,
    name?: string,
    has_employment_history?: EmploymentEvent[],
    has_familial_relationships?: FamilialRelationship[],
    has_medical_history?: MedicalEvent[],
    /** number of years since birth */
    age_in_years?: number,
    addresses?: Address[],
    has_birth_event?: BirthEvent,
    species_name?: string,
    stomach_count?: number,
    is_living?: string,
    aliases?: string,
};
/**
 * An organization.

This description
includes newlines

## Markdown headers

 * and
 * a
 * list
 */
export interface Organization  extends HasAliases  {
    id: string,
    name?: string,
    aliases?: string,
};

export interface Place  extends HasAliases  {
    id: string,
    name?: string,
    aliases?: string,
};

export interface Address  {
    street?: string,
    city?: string,
};

export interface Concept  {
    id: string,
    name?: string,
    in_code_system?: CodeSystemId,
};

export interface DiagnosisConcept  extends Concept  {
    id: string,
    name?: string,
    in_code_system?: CodeSystemId,
};

export interface ProcedureConcept  extends Concept  {
    id: string,
    name?: string,
    in_code_system?: CodeSystemId,
};

export interface Event  {
    started_at_time?: date,
    ended_at_time?: date,
    is_current?: boolean,
    /** Example of a slot that has an unconstrained range */
    metadata?: AnyObject,
};

export interface Relationship  {
    started_at_time?: date,
    ended_at_time?: date,
    related_to?: string,
    type?: string,
    cordialness?: string,
};

export interface FamilialRelationship  extends Relationship  {
    cordialness?: string,
    started_at_time?: date,
    ended_at_time?: date,
    related_to: PersonId,
    type: string,
};

export interface BirthEvent  extends Event  {
    in_location?: PlaceId,
    started_at_time?: date,
    ended_at_time?: date,
    is_current?: boolean,
    /** Example of a slot that has an unconstrained range */
    metadata?: AnyObject,
};

export interface EmploymentEvent  extends Event  {
    employed_at?: CompanyId,
    type?: string,
    started_at_time?: date,
    ended_at_time?: date,
    is_current?: boolean,
    /** Example of a slot that has an unconstrained range */
    metadata?: AnyObject,
};

export interface MedicalEvent  extends Event  {
    in_location?: PlaceId,
    diagnosis?: DiagnosisConcept,
    procedure?: ProcedureConcept,
    started_at_time?: date,
    ended_at_time?: date,
    is_current?: boolean,
    /** Example of a slot that has an unconstrained range */
    metadata?: AnyObject,
};

export interface WithLocation  {
    in_location?: PlaceId,
};

export interface MarriageEvent  extends Event, WithLocation  {
    married_to?: PersonId,
    in_location?: PlaceId,
    started_at_time?: date,
    ended_at_time?: date,
    is_current?: boolean,
    /** Example of a slot that has an unconstrained range */
    metadata?: AnyObject,
};

export interface Company  extends Organization  {
    ceo?: PersonId,
    id: string,
    name?: string,
    aliases?: string,
};

export interface CodeSystem  {
    id: string,
    name?: string,
};

export interface Dataset  {
    /** Example of a slot that has an unconstrained range */
    metadata?: AnyObject,
    persons?: Person[],
    companies?: Company[],
    activities?: Activity[],
    code_systems?: {[index: CodeSystemId]: CodeSystem },
};

export interface FakeClass  {
    test_attribute?: string,
};

export interface ClassWithSpaces  {
    slot_with_space_1?: string,
};

export interface SubclassTest  extends ClassWithSpaces  {
    slot_with_space_2?: ClassWithSpaces,
    slot_with_space_1?: string,
};

export interface SubSubClass2  extends SubclassTest  {
    slot_with_space_2?: ClassWithSpaces,
    slot_with_space_1?: string,
};
/**
 * Same depth as Sub sub class 1
 */
export interface TubSubClass1  extends SubclassTest  {
    slot_with_space_2?: ClassWithSpaces,
    slot_with_space_1?: string,
};
/**
 * Example of unconstrained class
 */
export interface AnyObject  {
};
/**
 * a provence-generating activity
 */
export interface Activity  {
    id: string,
    started_at_time?: date,
    ended_at_time?: date,
    was_informed_by?: ActivityId,
    was_associated_with?: AgentId,
    used?: string,
    description?: string,
};
/**
 * a provence-generating agent
 */
export interface Agent  {
    id: string,
    acted_on_behalf_of?: AgentId,
    was_informed_by?: ActivityId,
};
