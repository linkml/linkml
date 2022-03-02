
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