
CREATE TABLE "Address" (
	id TEXT NOT NULL, 
	street_address TEXT, 
	city TEXT, 
	country TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "HasAliases" (
	id TEXT NOT NULL, 
	aliases TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Employee" (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	status VARCHAR(8), 
	has_address TEXT, 
	aliases TEXT, 
	start_date TEXT, 
	is_current TEXT, 
	scores FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_address) REFERENCES "Address" (id)
);

CREATE TABLE "HasAliases_to_aliases" (
	alias TEXT NOT NULL, 
	"ref_HasAliases" TEXT NOT NULL, 
	FOREIGN KEY("ref_HasAliases") REFERENCES "HasAliases" (id)
);

CREATE TABLE "Person" (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	status VARCHAR(8), 
	has_address TEXT, 
	aliases TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_address) REFERENCES "Address" (id)
);

CREATE TABLE "Employee_to_aliases" (
	alias TEXT NOT NULL, 
	"ref_Employee" TEXT NOT NULL, 
	FOREIGN KEY("ref_Employee") REFERENCES "Employee" (id)
);

CREATE TABLE "Employee_to_scores" (
	score FLOAT NOT NULL, 
	"ref_Employee" TEXT NOT NULL, 
	FOREIGN KEY("ref_Employee") REFERENCES "Employee" (id)
);

CREATE TABLE "Organization" (
	id TEXT NOT NULL, 
	has_employees TEXT, 
	aliases TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_employees) REFERENCES "Employee" (id)
);

CREATE TABLE "Person_to_aliases" (
	alias TEXT NOT NULL, 
	"ref_Person" TEXT NOT NULL, 
	FOREIGN KEY("ref_Person") REFERENCES "Person" (id)
);

CREATE TABLE "Organization_to_has_employees" (
	has_employees TEXT NOT NULL, 
	"ref_Organization" TEXT NOT NULL, 
	FOREIGN KEY("ref_Organization") REFERENCES "Organization" (id)
);

CREATE TABLE "Organization_to_aliases" (
	alias TEXT NOT NULL, 
	"ref_Organization" TEXT NOT NULL, 
	FOREIGN KEY("ref_Organization") REFERENCES "Organization" (id)
);
