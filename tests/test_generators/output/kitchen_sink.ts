

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




/**
 * None
 */

export interface HasAliases  {
    
    
    /**
     * None
     */
    aliases?: string,
    
}


/**
 * None
 */

export interface Friend  {
    
    
    /**
     * None
     */
    name?: string,
    
}


/**
 * A person, living or dead
 */

export interface Person  extends HasAliases  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
    
    /**
     * None
     */
    has_employment_history?: EmploymentEvent[],
    
    
    /**
     * None
     */
    has_familial_relationships?: FamilialRelationship[],
    
    
    /**
     * None
     */
    has_medical_history?: MedicalEvent[],
    
    
    /**
     * number of years since birth
     */
    age_in_years?: number,
    
    
    /**
     * None
     */
    addresses?: Address[],
    
    
    /**
     * None
     */
    has_birth_event?: BirthEvent,
    
    
    /**
     * None
     */
    aliases?: string,
    
}


/**
 * None
 */

export interface Organization  extends HasAliases  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
    
    /**
     * None
     */
    aliases?: string,
    
}


/**
 * None
 */

export interface Place  extends HasAliases  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
    
    /**
     * None
     */
    aliases?: string,
    
}


/**
 * None
 */

export interface Address  {
    
    
    /**
     * None
     */
    street?: string,
    
    
    /**
     * None
     */
    city?: string,
    
}


/**
 * None
 */

export interface Concept  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
    
    /**
     * None
     */
    in_code_system?: CodeSystemId,
    
}


/**
 * None
 */

export interface DiagnosisConcept  extends Concept  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
    
    /**
     * None
     */
    in_code_system?: CodeSystemId,
    
}


/**
 * None
 */

export interface ProcedureConcept  extends Concept  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
    
    /**
     * None
     */
    in_code_system?: CodeSystemId,
    
}


/**
 * None
 */

export interface Event  {
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    is_current?: boolean,
    
    
    /**
     * Example of a slot that has an unconstrained range
     */
    metadata?: AnyObject,
    
}


/**
 * None
 */

export interface Relationship  {
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    related_to?: string,
    
    
    /**
     * None
     */
    type?: string,
    
}


/**
 * None
 */

export interface FamilialRelationship  extends Relationship  {
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    related_to?: PersonId,
    
    
    /**
     * None
     */
    type?: string,
    
}


/**
 * None
 */

export interface BirthEvent  extends Event  {
    
    
    /**
     * None
     */
    in_location?: PlaceId,
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    is_current?: boolean,
    
    
    /**
     * Example of a slot that has an unconstrained range
     */
    metadata?: AnyObject,
    
}


/**
 * None
 */

export interface EmploymentEvent  extends Event  {
    
    
    /**
     * None
     */
    employed_at?: CompanyId,
    
    
    /**
     * None
     */
    type?: string,
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    is_current?: boolean,
    
    
    /**
     * Example of a slot that has an unconstrained range
     */
    metadata?: AnyObject,
    
}


/**
 * None
 */

export interface MedicalEvent  extends Event  {
    
    
    /**
     * None
     */
    in_location?: PlaceId,
    
    
    /**
     * None
     */
    diagnosis?: DiagnosisConcept,
    
    
    /**
     * None
     */
    procedure?: ProcedureConcept,
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    is_current?: boolean,
    
    
    /**
     * Example of a slot that has an unconstrained range
     */
    metadata?: AnyObject,
    
}


/**
 * None
 */

export interface WithLocation  {
    
    
    /**
     * None
     */
    in_location?: PlaceId,
    
}


/**
 * None
 */

export interface MarriageEvent  extends Event, WithLocation  {
    
    
    /**
     * None
     */
    married_to?: PersonId,
    
    
    /**
     * None
     */
    in_location?: PlaceId,
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    is_current?: boolean,
    
    
    /**
     * Example of a slot that has an unconstrained range
     */
    metadata?: AnyObject,
    
}


/**
 * None
 */

export interface Company  extends Organization  {
    
    
    /**
     * None
     */
    ceo?: PersonId,
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
    
    /**
     * None
     */
    aliases?: string,
    
}


/**
 * None
 */

export interface CodeSystem  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    name?: string,
    
}


/**
 * None
 */

export interface Dataset  {
    
    
    /**
     * None
     */
    persons?: Person[],
    
    
    /**
     * None
     */
    companies?: Company[],
    
    
    /**
     * None
     */
    activities?: Activity[],
    
    
    /**
     * None
     */
    code_systems?: {[index: CodeSystemId]: CodeSystem },
    
}


/**
 * None
 */

export interface FakeClass  {
    
    
    /**
     * None
     */
    test_attribute?: string,
    
}


/**
 * None
 */

export interface ClassWithSpaces  {
    
    
    /**
     * None
     */
    slot_with_space_1?: string,
    
}


/**
 * None
 */

export interface SubclassTest  extends ClassWithSpaces  {
    
    
    /**
     * None
     */
    slot_with_space_2?: ClassWithSpaces,
    
    
    /**
     * None
     */
    slot_with_space_1?: string,
    
}


/**
 * Example of unconstrained class
 */

export interface AnyObject  {
    
}


/**
 * a provence-generating activity
 */

export interface Activity  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    started_at_time?: date,
    
    
    /**
     * None
     */
    ended_at_time?: date,
    
    
    /**
     * None
     */
    was_informed_by?: ActivityId,
    
    
    /**
     * None
     */
    was_associated_with?: AgentId,
    
    
    /**
     * None
     */
    used?: string,
    
    
    /**
     * None
     */
    description?: string,
    
}


/**
 * a provence-generating agent
 */

export interface Agent  {
    
    
    /**
     * None
     */
    id?: string,
    
    
    /**
     * None
     */
    acted_on_behalf_of?: AgentId,
    
    
    /**
     * None
     */
    was_informed_by?: ActivityId,
    
}
