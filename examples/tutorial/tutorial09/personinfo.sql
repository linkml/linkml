-- # Class: Person
--     * Slot: id
--     * Slot: full_name Description: name of the person
--     * Slot: phone
--     * Slot: age
--     * Slot: Container_id Description: Autocreated FK slot
-- # Class: Container
--     * Slot: id
-- # Class: Person_aliases
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: aliases Description: other names for the person

CREATE TABLE "Container" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Container_id" ON "Container" (id);

CREATE TABLE "Person" (
	id TEXT NOT NULL,
	full_name TEXT NOT NULL,
	phone TEXT,
	age INTEGER,
	"Container_id" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY("Container_id") REFERENCES "Container" (id)
);
CREATE INDEX "ix_Person_id" ON "Person" (id);

CREATE TABLE "Person_aliases" (
	"Person_id" TEXT,
	aliases TEXT,
	PRIMARY KEY ("Person_id", aliases),
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE INDEX "ix_Person_aliases_aliases" ON "Person_aliases" (aliases);
CREATE INDEX "ix_Person_aliases_Person_id" ON "Person_aliases" ("Person_id");
