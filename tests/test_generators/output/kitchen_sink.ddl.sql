

CREATE TABLE activity (
	id TEXT NOT NULL, 
	started_at_time TEXT, 
	ended_at_time TEXT, 
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

CREATE TABLE "Dataset" (
	persons TEXT, 
	companies TEXT, 
	activities TEXT, 
	PRIMARY KEY (persons, companies, activities)
);

CREATE TABLE "Event" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	is_current BOOLEAN, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current)
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
	PRIMARY KEY (id)
);

CREATE TABLE "Place" (
	id TEXT NOT NULL, 
	name TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Relationship" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	related_to TEXT, 
	type TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, related_to, type)
);

CREATE TABLE "Address" (
	street TEXT, 
	city TEXT, 
	"Person_id" TEXT, 
	PRIMARY KEY (street, city, "Person_id"), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "Company" (
	id TEXT NOT NULL, 
	name TEXT, 
	ceo TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ceo) REFERENCES "Person" (id)
);

CREATE TABLE "FamilialRelationship" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	type VARCHAR(10) NOT NULL, 
	related_to TEXT NOT NULL, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, type, related_to, "Person_id"), 
	FOREIGN KEY(related_to) REFERENCES "Person" (id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);

CREATE TABLE "MarriageEvent" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	is_current BOOLEAN, 
	married_to TEXT, 
	in_location TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, married_to, in_location), 
	FOREIGN KEY(married_to) REFERENCES "Person" (id), 
	FOREIGN KEY(in_location) REFERENCES "Place" (id)
);

CREATE TABLE "MedicalEvent" (
	started_at_time TEXT, 
	ended_at_time TEXT, 
	is_current BOOLEAN, 
	"Person_id" TEXT, 
	PRIMARY KEY (started_at_time, ended_at_time, is_current, "Person_id"), 
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
	started_at_time TEXT, 
	ended_at_time TEXT, 
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
