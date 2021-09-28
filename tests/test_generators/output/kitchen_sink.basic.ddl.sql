

CREATE TABLE activity (
	id TEXT NOT NULL, 
	started_at_time DATE, 
	ended_at_time DATE, 
	was_informed_by TEXT, 
	was_associated_with TEXT, 
	used TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Address" (
	street TEXT, 
	city TEXT, 
	PRIMARY KEY (street, city)
);

CREATE TABLE agent (
	id TEXT NOT NULL, 
	acted_on_behalf_of TEXT, 
	was_informed_by TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "BirthEvent" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	in_location TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, in_location)
);

CREATE TABLE "Company" (
	id TEXT NOT NULL, 
	name TEXT, 
	aliases TEXT, 
	ceo TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Concept" (
	id TEXT NOT NULL, 
	name TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Dataset" (
	persons TEXT, 
	companies TEXT, 
	activities TEXT, 
	PRIMARY KEY (persons, companies, activities)
);

CREATE TABLE "DiagnosisConcept" (
	id TEXT NOT NULL, 
	name TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "EmploymentEvent" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	employed_at TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, employed_at)
);

CREATE TABLE "Event" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current)
);

CREATE TABLE "FamilialRelationship" (
	started_at_time DATE, 
	ended_at_time DATE, 
	type VARCHAR(10) NOT NULL, 
	related_to TEXT NOT NULL, 
	PRIMARY KEY (started_at_time, ended_at_time, type, related_to)
);

CREATE TABLE "MarriageEvent" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	married_to TEXT, 
	in_location TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, married_to, in_location)
);

CREATE TABLE "MedicalEvent" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	in_location TEXT, 
	diagnosis TEXT, 
	procedure TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, in_location, diagnosis, procedure)
);

CREATE TABLE "Organization" (
	id TEXT NOT NULL, 
	name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Person" (
	id TEXT NOT NULL, 
	name TEXT, 
	has_employment_history TEXT, 
	has_familial_relationships TEXT, 
	has_medical_history TEXT, 
	age_in_years INTEGER, 
	addresses TEXT, 
	has_birth_event TEXT, 
	aliases TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Place" (
	id TEXT NOT NULL, 
	name TEXT, 
	aliases TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "ProcedureConcept" (
	id TEXT NOT NULL, 
	name TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Relationship" (
	started_at_time DATE, 
	ended_at_time DATE, 
	related_to TEXT, 
	type TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, related_to, type)
);
