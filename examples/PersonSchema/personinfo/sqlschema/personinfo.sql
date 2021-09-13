

CREATE TABLE "Address" (
	street TEXT, 
	city TEXT, 
	postal_code TEXT, 
	PRIMARY KEY (street, city, postal_code)
);

CREATE TABLE "Concept" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Container" (
	persons TEXT, 
	organizations TEXT, 
	PRIMARY KEY (persons, organizations)
);

CREATE TABLE "DiagnosisConcept" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Event" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	duration FLOAT, 
	is_current BOOLEAN, 
	PRIMARY KEY (started_at_time, ended_at_time, duration, is_current)
);

CREATE TABLE "NamedThing" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Person" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	primary_email TEXT, 
	birth_date TEXT, 
	age_in_years INTEGER, 
	gender VARCHAR(17), 
	current_address TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Place" (
	id TEXT NOT NULL, 
	name TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "ProcedureConcept" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Relationship" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	related_to TEXT, 
	type TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, related_to, type)
);

CREATE TABLE "FamilialRelationship" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	related_to TEXT NOT NULL, 
	type VARCHAR(10) NOT NULL, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, related_to, type, "Person_id"), 
	FOREIGN KEY(related_to) REFERENCES "Person" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "MedicalEvent" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	duration FLOAT, 
	is_current BOOLEAN, 
	in_location TEXT, 
	diagnosis TEXT, 
	procedure TEXT, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, duration, is_current, in_location, diagnosis, procedure, "Person_id"), 
	FOREIGN KEY(in_location) REFERENCES "Place" (id), 
	FOREIGN KEY(diagnosis) REFERENCES "DiagnosisConcept" (id), 
	FOREIGN KEY(procedure) REFERENCES "ProcedureConcept" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "Organization" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	mission_statement TEXT, 
	founding_date TEXT, 
	founding_location TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(founding_location) REFERENCES "Place" (id)
);

CREATE TABLE "Person_aliases" (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES "Person" (id)
);

CREATE TABLE "Place_aliases" (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES "Place" (id)
);

CREATE TABLE "EmploymentEvent" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	duration FLOAT, 
	is_current BOOLEAN, 
	employed_at TEXT, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, duration, is_current, employed_at, "Person_id"), 
	FOREIGN KEY(employed_at) REFERENCES "Organization" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "Organization_aliases" (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES "Organization" (id)
);
