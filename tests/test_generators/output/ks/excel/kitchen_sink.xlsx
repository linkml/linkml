

CREATE TABLE activity (
	id TEXT NOT NULL, 
	started_at_time DATE, 
	ended_at_time DATE, 
	was_informed_by TEXT, 
	was_associated_with TEXT, 
	used TEXT, 
	description TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(was_informed_by) REFERENCES activity (id), 
	FOREIGN KEY(was_associated_with) REFERENCES agent (id)
);

CREATE TABLE agent (
	id TEXT NOT NULL, 
	acted_on_behalf_of TEXT, 
	was_informed_by TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(acted_on_behalf_of) REFERENCES agent (id), 
	FOREIGN KEY(was_informed_by) REFERENCES activity (id)
);

CREATE TABLE class_with_spaces (
	slot_with_space_1 TEXT, 
	PRIMARY KEY (slot_with_space_1)
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

CREATE TABLE "Event" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current)
);

CREATE TABLE "FakeClass" (
	test_attribute TEXT, 
	PRIMARY KEY (test_attribute)
);

CREATE TABLE "Organization" (
	id TEXT NOT NULL, 
	name TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Person" (
	id TEXT NOT NULL, 
	name TEXT, 
	age_in_years INTEGER, 
	has_birth_event TEXT, 
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
	PRIMARY KEY (id)
);

CREATE TABLE "Relationship" (
	started_at_time DATE, 
	ended_at_time DATE, 
	related_to TEXT, 
	type TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, related_to, type)
);

CREATE TABLE subclass_test (
	slot_with_space_1 TEXT, 
	slot_with_space_2 TEXT, 
	PRIMARY KEY (slot_with_space_1, slot_with_space_2)
);

CREATE TABLE "Address" (
	street TEXT, 
	city TEXT, 
	"Person_id" TEXT, 
	PRIMARY KEY (street, city, "Person_id"), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "BirthEvent" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	in_location TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, in_location), 
	FOREIGN KEY(in_location) REFERENCES "Place" (id)
);

CREATE TABLE "Company" (
	id TEXT NOT NULL, 
	name TEXT, 
	ceo TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ceo) REFERENCES "Person" (id)
);

CREATE TABLE "FamilialRelationship" (
	started_at_time DATE, 
	ended_at_time DATE, 
	type VARCHAR(10) NOT NULL, 
	related_to TEXT NOT NULL, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, type, related_to, "Person_id"), 
	FOREIGN KEY(related_to) REFERENCES "Person" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "MarriageEvent" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	married_to TEXT, 
	in_location TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, married_to, in_location), 
	FOREIGN KEY(married_to) REFERENCES "Person" (id), 
	FOREIGN KEY(in_location) REFERENCES "Place" (id)
);

CREATE TABLE "MedicalEvent" (
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	in_location TEXT, 
	diagnosis TEXT, 
	procedure TEXT, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, in_location, diagnosis, procedure, "Person_id"), 
	FOREIGN KEY(in_location) REFERENCES "Place" (id), 
	FOREIGN KEY(diagnosis) REFERENCES "DiagnosisConcept" (id), 
	FOREIGN KEY(procedure) REFERENCES "ProcedureConcept" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "Organization_aliases" (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES "Organization" (id)
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
	started_at_time DATE, 
	ended_at_time DATE, 
	is_current BOOLEAN, 
	employed_at TEXT, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, employed_at, "Person_id"), 
	FOREIGN KEY(employed_at) REFERENCES "Company" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "Company_aliases" (
	backref_id TEXT, 
	aliases TEXT, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES "Company" (id)
);
