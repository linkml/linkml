-- # Class: "NamedThing" Description: "A generic grouping for any identifiable entity"
--     * Slot: id Description: 
--     * Slot: name Description: 
--     * Slot: description Description: 
--     * Slot: image Description: 
-- # Class: "Person" Description: "A person (alive, dead, undead, or fictional)."
--     * Slot: primary_email Description: 
--     * Slot: birth_date Description: 
--     * Slot: age_in_years Description: 
--     * Slot: gender Description: 
--     * Slot: id Description: 
--     * Slot: name Description: 
--     * Slot: description Description: 
--     * Slot: image Description: 
--     * Slot: Container_id Description: Autocreated FK slot
--     * Slot: current_address_id Description: The address at which a person currently lives
-- # Class: "HasAliases" Description: "A mixin applied to any class that can have aliases/alternateNames"
--     * Slot: id Description: 
-- # Class: "HasNewsEvents" Description: ""
--     * Slot: id Description: 
-- # Class: "Organization" Description: "An organization such as a company or university"
--     * Slot: mission_statement Description: 
--     * Slot: founding_date Description: 
--     * Slot: founding_location Description: 
--     * Slot: id Description: 
--     * Slot: name Description: 
--     * Slot: description Description: 
--     * Slot: image Description: 
--     * Slot: Container_id Description: Autocreated FK slot
--     * Slot: current_address_id Description: The address at which a person currently lives
-- # Class: "Place" Description: ""
--     * Slot: id Description: 
--     * Slot: name Description: 
-- # Class: "Address" Description: ""
--     * Slot: id Description: 
--     * Slot: street Description: 
--     * Slot: city Description: 
--     * Slot: postal_code Description: 
-- # Class: "Event" Description: ""
--     * Slot: id Description: 
--     * Slot: started_at_time Description: 
--     * Slot: ended_at_time Description: 
--     * Slot: duration Description: 
--     * Slot: is_current Description: 
-- # Class: "Concept" Description: ""
--     * Slot: id Description: 
--     * Slot: name Description: 
--     * Slot: description Description: 
--     * Slot: image Description: 
-- # Class: "DiagnosisConcept" Description: ""
--     * Slot: id Description: 
--     * Slot: name Description: 
--     * Slot: description Description: 
--     * Slot: image Description: 
-- # Class: "ProcedureConcept" Description: ""
--     * Slot: id Description: 
--     * Slot: name Description: 
--     * Slot: description Description: 
--     * Slot: image Description: 
-- # Class: "Relationship" Description: ""
--     * Slot: id Description: 
--     * Slot: started_at_time Description: 
--     * Slot: ended_at_time Description: 
--     * Slot: related_to Description: 
--     * Slot: type Description: 
-- # Class: "FamilialRelationship" Description: ""
--     * Slot: id Description: 
--     * Slot: started_at_time Description: 
--     * Slot: ended_at_time Description: 
--     * Slot: related_to Description: 
--     * Slot: type Description: 
--     * Slot: Person_id Description: Autocreated FK slot
-- # Class: "EmploymentEvent" Description: ""
--     * Slot: id Description: 
--     * Slot: employed_at Description: 
--     * Slot: started_at_time Description: 
--     * Slot: ended_at_time Description: 
--     * Slot: duration Description: 
--     * Slot: is_current Description: 
--     * Slot: Person_id Description: Autocreated FK slot
-- # Class: "MedicalEvent" Description: ""
--     * Slot: id Description: 
--     * Slot: in_location Description: 
--     * Slot: started_at_time Description: 
--     * Slot: ended_at_time Description: 
--     * Slot: duration Description: 
--     * Slot: is_current Description: 
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: diagnosis_id Description: 
--     * Slot: procedure_id Description: 
-- # Class: "NewsEvent" Description: ""
--     * Slot: id Description: 
--     * Slot: headline Description: 
--     * Slot: started_at_time Description: 
--     * Slot: ended_at_time Description: 
--     * Slot: duration Description: 
--     * Slot: is_current Description: 
-- # Class: "WithLocation" Description: ""
--     * Slot: id Description: 
--     * Slot: in_location Description: 
-- # Class: "Container" Description: ""
--     * Slot: id Description: 
--     * Slot: name Description: 
-- # Class: "Person_alias" Description: ""
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: alias Description: 
-- # Class: "Person_has_news_event" Description: ""
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: has_news_event_id Description: 
-- # Class: "HasAliases_alias" Description: ""
--     * Slot: HasAliases_id Description: Autocreated FK slot
--     * Slot: alias Description: 
-- # Class: "HasNewsEvents_has_news_event" Description: ""
--     * Slot: HasNewsEvents_id Description: Autocreated FK slot
--     * Slot: has_news_event_id Description: 
-- # Class: "Organization_alias" Description: ""
--     * Slot: Organization_id Description: Autocreated FK slot
--     * Slot: alias Description: 
-- # Class: "Organization_has_news_event" Description: ""
--     * Slot: Organization_id Description: Autocreated FK slot
--     * Slot: has_news_event_id Description: 
-- # Class: "Place_alias" Description: ""
--     * Slot: Place_id Description: Autocreated FK slot
--     * Slot: alias Description: 

CREATE TABLE "NamedThing" (
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "HasAliases" (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE "HasNewsEvents" (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE "Place" (
	id TEXT, 
	name TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Address" (
	id INTEGER, 
	street TEXT, 
	city TEXT, 
	postal_code TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Event" (
	id INTEGER, 
	started_at_time DATE, 
	ended_at_time DATE, 
	duration FLOAT, 
	is_current BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE "Concept" (
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "DiagnosisConcept" (
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "ProcedureConcept" (
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Relationship" (
	id INTEGER, 
	started_at_time DATE, 
	ended_at_time DATE, 
	related_to TEXT, 
	type TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "NewsEvent" (
	id INTEGER, 
	headline TEXT, 
	started_at_time DATE, 
	ended_at_time DATE, 
	duration FLOAT, 
	is_current BOOLEAN, 
	PRIMARY KEY (id)
);
CREATE TABLE "Container" (
	id INTEGER, 
	name TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Person" (
	primary_email TEXT, 
	birth_date TEXT, 
	age_in_years INTEGER, 
	gender VARCHAR(17), 
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	"Container_id" TEXT, 
	current_address_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("Container_id") REFERENCES "Container" (id), 
	FOREIGN KEY(current_address_id) REFERENCES "Address" (id)
);
CREATE TABLE "Organization" (
	mission_statement TEXT, 
	founding_date TEXT, 
	founding_location TEXT, 
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	"Container_id" TEXT, 
	current_address_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(founding_location) REFERENCES "Place" (id), 
	FOREIGN KEY("Container_id") REFERENCES "Container" (id), 
	FOREIGN KEY(current_address_id) REFERENCES "Address" (id)
);
CREATE TABLE "WithLocation" (
	id INTEGER, 
	in_location TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(in_location) REFERENCES "Place" (id)
);
CREATE TABLE "HasAliases_alias" (
	"HasAliases_id" TEXT, 
	alias TEXT, 
	PRIMARY KEY ("HasAliases_id", alias), 
	FOREIGN KEY("HasAliases_id") REFERENCES "HasAliases" (id)
);
CREATE TABLE "HasNewsEvents_has_news_event" (
	"HasNewsEvents_id" TEXT, 
	has_news_event_id TEXT, 
	PRIMARY KEY ("HasNewsEvents_id", has_news_event_id), 
	FOREIGN KEY("HasNewsEvents_id") REFERENCES "HasNewsEvents" (id), 
	FOREIGN KEY(has_news_event_id) REFERENCES "NewsEvent" (id)
);
CREATE TABLE "Place_alias" (
	"Place_id" TEXT, 
	alias TEXT, 
	PRIMARY KEY ("Place_id", alias), 
	FOREIGN KEY("Place_id") REFERENCES "Place" (id)
);
CREATE TABLE "FamilialRelationship" (
	id INTEGER, 
	started_at_time DATE, 
	ended_at_time DATE, 
	related_to TEXT NOT NULL, 
	type VARCHAR(10) NOT NULL, 
	"Person_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(related_to) REFERENCES "Person" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE TABLE "EmploymentEvent" (
	id INTEGER, 
	employed_at TEXT, 
	started_at_time DATE, 
	ended_at_time DATE, 
	duration FLOAT, 
	is_current BOOLEAN, 
	"Person_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(employed_at) REFERENCES "Organization" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE TABLE "MedicalEvent" (
	id INTEGER, 
	in_location TEXT, 
	started_at_time DATE, 
	ended_at_time DATE, 
	duration FLOAT, 
	is_current BOOLEAN, 
	"Person_id" TEXT, 
	diagnosis_id TEXT, 
	procedure_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(in_location) REFERENCES "Place" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id), 
	FOREIGN KEY(diagnosis_id) REFERENCES "DiagnosisConcept" (id), 
	FOREIGN KEY(procedure_id) REFERENCES "ProcedureConcept" (id)
);
CREATE TABLE "Person_alias" (
	"Person_id" TEXT, 
	alias TEXT, 
	PRIMARY KEY ("Person_id", alias), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE TABLE "Person_has_news_event" (
	"Person_id" TEXT, 
	has_news_event_id TEXT, 
	PRIMARY KEY ("Person_id", has_news_event_id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id), 
	FOREIGN KEY(has_news_event_id) REFERENCES "NewsEvent" (id)
);
CREATE TABLE "Organization_alias" (
	"Organization_id" TEXT, 
	alias TEXT, 
	PRIMARY KEY ("Organization_id", alias), 
	FOREIGN KEY("Organization_id") REFERENCES "Organization" (id)
);
CREATE TABLE "Organization_has_news_event" (
	"Organization_id" TEXT, 
	has_news_event_id TEXT, 
	PRIMARY KEY ("Organization_id", has_news_event_id), 
	FOREIGN KEY("Organization_id") REFERENCES "Organization" (id), 
	FOREIGN KEY(has_news_event_id) REFERENCES "NewsEvent" (id)
);