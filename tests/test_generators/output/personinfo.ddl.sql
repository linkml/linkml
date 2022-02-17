
CREATE TABLE "NamedThing" (
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
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
	started_at_time DATE, 
	ended_at_time DATE, 
	duration FLOAT, 
	is_current BOOLEAN, 
	PRIMARY KEY (started_at_time, ended_at_time, duration, is_current)
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
	started_at_time DATE, 
	ended_at_time DATE, 
	related_to TEXT, 
	type TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, related_to, type)
);
CREATE TABLE "Container" (
	id INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE "Person" (
	primary_email TEXT, 
	birth_date TEXT, 
	age_in_years INTEGER, 
	gender VARCHAR(17), 
	current_address TEXT, 
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	"Container_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(current_address) REFERENCES "Address" (id), 
	FOREIGN KEY("Container_id") REFERENCES "Container" (id)
);
CREATE TABLE "Organization" (
	mission_statement TEXT, 
	founding_date TEXT, 
	founding_location TEXT, 
	id TEXT, 
	name TEXT, 
	description TEXT, 
	image TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(founding_location) REFERENCES "Place" (id)
);
CREATE TABLE "Place_aliases" (
	"Place_id" TEXT, 
	aliases TEXT, 
	PRIMARY KEY ("Place_id", aliases), 
	FOREIGN KEY("Place_id") REFERENCES "Place" (id)
);
CREATE TABLE "FamilialRelationship" (
	id INTEGER, 
	started_at_time DATE, 
	ended_at_time DATE, 
	related_to TEXT, 
	type VARCHAR(10) NOT NULL, 
	"Person_id" TEXT, 
	PRIMARY KEY (id), 
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
CREATE TABLE "Person_aliases" (
	"Person_id" TEXT, 
	aliases TEXT, 
	PRIMARY KEY ("Person_id", aliases), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE TABLE "Organization_aliases" (
	"Organization_id" TEXT, 
	aliases TEXT, 
	PRIMARY KEY ("Organization_id", aliases), 
	FOREIGN KEY("Organization_id") REFERENCES "Organization" (id)
);
CREATE TABLE "Container_organizations" (
	"Container_id" TEXT, 
	organizations_id TEXT, 
	PRIMARY KEY ("Container_id", organizations_id), 
	FOREIGN KEY("Container_id") REFERENCES "Container" (id), 
	FOREIGN KEY(organizations_id) REFERENCES "Organization" (id)
);