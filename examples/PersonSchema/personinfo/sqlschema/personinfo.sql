-- # Class: NamedThing Description: A generic grouping for any identifiable entity
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: image
-- # Class: Person Description: A person (alive, dead, undead, or fictional).
--     * Slot: primary_email
--     * Slot: birth_date
--     * Slot: age_in_years
--     * Slot: gender
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: image
--     * Slot: Container_id Description: Autocreated FK slot
--     * Slot: current_address_id Description: The address at which a person currently lives
-- # Class: HasAliases Description: A mixin applied to any class that can have aliases/alternateNames
--     * Slot: id
-- # Class: Organization Description: An organization such as a company or university
--     * Slot: mission_statement
--     * Slot: founding_date
--     * Slot: founding_location
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: image
--     * Slot: Container_id Description: Autocreated FK slot
-- # Class: Place
--     * Slot: id
--     * Slot: name
-- # Class: Address
--     * Slot: id
--     * Slot: street
--     * Slot: city
--     * Slot: postal_code
-- # Class: Event
--     * Slot: id
--     * Slot: started_at_time
--     * Slot: ended_at_time
--     * Slot: duration
--     * Slot: is_current
-- # Class: Concept
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: image
-- # Class: DiagnosisConcept
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: image
-- # Class: ProcedureConcept
--     * Slot: id
--     * Slot: name
--     * Slot: description
--     * Slot: image
-- # Class: Relationship
--     * Slot: id
--     * Slot: started_at_time
--     * Slot: ended_at_time
--     * Slot: related_to
--     * Slot: type
-- # Class: FamilialRelationship
--     * Slot: id
--     * Slot: started_at_time
--     * Slot: ended_at_time
--     * Slot: related_to
--     * Slot: type
--     * Slot: Person_id Description: Autocreated FK slot
-- # Class: EmploymentEvent
--     * Slot: id
--     * Slot: employed_at
--     * Slot: started_at_time
--     * Slot: ended_at_time
--     * Slot: duration
--     * Slot: is_current
--     * Slot: Person_id Description: Autocreated FK slot
-- # Class: MedicalEvent
--     * Slot: id
--     * Slot: in_location
--     * Slot: started_at_time
--     * Slot: ended_at_time
--     * Slot: duration
--     * Slot: is_current
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: diagnosis_id
--     * Slot: procedure_id
-- # Class: WithLocation
--     * Slot: id
--     * Slot: in_location
-- # Class: Container
--     * Slot: id
-- # Class: Person_aliases
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: aliases
-- # Class: HasAliases_aliases
--     * Slot: HasAliases_id Description: Autocreated FK slot
--     * Slot: aliases
-- # Class: Organization_aliases
--     * Slot: Organization_id Description: Autocreated FK slot
--     * Slot: aliases
-- # Class: Place_aliases
--     * Slot: Place_id Description: Autocreated FK slot
--     * Slot: aliases

CREATE TABLE "NamedThing" (
	id TEXT NOT NULL,
	name TEXT,
	description TEXT,
	image TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_NamedThing_id" ON "NamedThing" (id);
CREATE TABLE "HasAliases" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_HasAliases_id" ON "HasAliases" (id);
CREATE TABLE "Place" (
	id TEXT NOT NULL,
	name TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Place_id" ON "Place" (id);
CREATE TABLE "Address" (
	id INTEGER NOT NULL,
	street TEXT,
	city TEXT,
	postal_code TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Address_id" ON "Address" (id);
CREATE TABLE "Event" (
	id INTEGER NOT NULL,
	started_at_time DATE,
	ended_at_time DATE,
	duration FLOAT,
	is_current BOOLEAN,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Event_id" ON "Event" (id);
CREATE TABLE "Concept" (
	id TEXT NOT NULL,
	name TEXT,
	description TEXT,
	image TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Concept_id" ON "Concept" (id);
CREATE TABLE "DiagnosisConcept" (
	id TEXT NOT NULL,
	name TEXT,
	description TEXT,
	image TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_DiagnosisConcept_id" ON "DiagnosisConcept" (id);
CREATE TABLE "ProcedureConcept" (
	id TEXT NOT NULL,
	name TEXT,
	description TEXT,
	image TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_ProcedureConcept_id" ON "ProcedureConcept" (id);
CREATE TABLE "Relationship" (
	id INTEGER NOT NULL,
	started_at_time DATE,
	ended_at_time DATE,
	related_to TEXT,
	type TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Relationship_id" ON "Relationship" (id);
CREATE TABLE "Container" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Container_id" ON "Container" (id);
CREATE TABLE "Person" (
	primary_email TEXT,
	birth_date TEXT,
	age_in_years INTEGER,
	gender VARCHAR(17),
	id TEXT NOT NULL,
	name TEXT,
	description TEXT,
	image TEXT,
	"Container_id" INTEGER,
	current_address_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("Container_id") REFERENCES "Container" (id),
	FOREIGN KEY(current_address_id) REFERENCES "Address" (id)
);CREATE INDEX "ix_Person_id" ON "Person" (id);
CREATE TABLE "Organization" (
	mission_statement TEXT,
	founding_date TEXT,
	founding_location TEXT,
	id TEXT NOT NULL,
	name TEXT,
	description TEXT,
	image TEXT,
	"Container_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(founding_location) REFERENCES "Place" (id),
	FOREIGN KEY("Container_id") REFERENCES "Container" (id)
);CREATE INDEX "ix_Organization_id" ON "Organization" (id);
CREATE TABLE "WithLocation" (
	id INTEGER NOT NULL,
	in_location TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(in_location) REFERENCES "Place" (id)
);CREATE INDEX "ix_WithLocation_id" ON "WithLocation" (id);
CREATE TABLE "HasAliases_aliases" (
	"HasAliases_id" INTEGER,
	aliases TEXT,
	PRIMARY KEY ("HasAliases_id", aliases),
	FOREIGN KEY("HasAliases_id") REFERENCES "HasAliases" (id)
);CREATE INDEX "ix_HasAliases_aliases_HasAliases_id" ON "HasAliases_aliases" ("HasAliases_id");CREATE INDEX "ix_HasAliases_aliases_aliases" ON "HasAliases_aliases" (aliases);
CREATE TABLE "Place_aliases" (
	"Place_id" TEXT,
	aliases TEXT,
	PRIMARY KEY ("Place_id", aliases),
	FOREIGN KEY("Place_id") REFERENCES "Place" (id)
);CREATE INDEX "ix_Place_aliases_aliases" ON "Place_aliases" (aliases);CREATE INDEX "ix_Place_aliases_Place_id" ON "Place_aliases" ("Place_id");
CREATE TABLE "FamilialRelationship" (
	id INTEGER NOT NULL,
	started_at_time DATE,
	ended_at_time DATE,
	related_to TEXT NOT NULL,
	type VARCHAR(10) NOT NULL,
	"Person_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(related_to) REFERENCES "Person" (id),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);CREATE INDEX "ix_FamilialRelationship_id" ON "FamilialRelationship" (id);
CREATE TABLE "EmploymentEvent" (
	id INTEGER NOT NULL,
	employed_at TEXT,
	started_at_time DATE,
	ended_at_time DATE,
	duration FLOAT,
	is_current BOOLEAN,
	"Person_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(employed_at) REFERENCES "Organization" (id),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);CREATE INDEX "ix_EmploymentEvent_id" ON "EmploymentEvent" (id);
CREATE TABLE "MedicalEvent" (
	id INTEGER NOT NULL,
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
);CREATE INDEX "ix_MedicalEvent_id" ON "MedicalEvent" (id);
CREATE TABLE "Person_aliases" (
	"Person_id" TEXT,
	aliases TEXT,
	PRIMARY KEY ("Person_id", aliases),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);CREATE INDEX "ix_Person_aliases_aliases" ON "Person_aliases" (aliases);CREATE INDEX "ix_Person_aliases_Person_id" ON "Person_aliases" ("Person_id");
CREATE TABLE "Organization_aliases" (
	"Organization_id" TEXT,
	aliases TEXT,
	PRIMARY KEY ("Organization_id", aliases),
	FOREIGN KEY("Organization_id") REFERENCES "Organization" (id)
);CREATE INDEX "ix_Organization_aliases_aliases" ON "Organization_aliases" (aliases);CREATE INDEX "ix_Organization_aliases_Organization_id" ON "Organization_aliases" ("Organization_id");
