

CREATE TABLE address (
	id TEXT NOT NULL, 
	street_address TEXT NULL, 
	city TEXT NULL, 
	country TEXT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE organization (
	id TEXT NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE employee (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	status VARCHAR(8) NULL, 
	has_address TEXT NULL, 
	start_date DATETIME NULL, 
	is_current TEXT NULL, 
	organization_id TEXT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_address) REFERENCES address (id), 
	FOREIGN KEY(organization_id) REFERENCES organization (id)
);

CREATE TABLE person (
	id TEXT NOT NULL, 
	name TEXT NOT NULL, 
	status VARCHAR(8) NULL, 
	has_address TEXT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(has_address) REFERENCES address (id)
);

CREATE TABLE organization_aliases (
	backref_id TEXT NOT NULL, 
	aliases TEXT NOT NULL, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES organization (id)
);

CREATE TABLE employee_aliases (
	backref_id TEXT NOT NULL, 
	aliases TEXT NOT NULL, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES employee (id)
);

CREATE TABLE employee_scores (
	backref_id TEXT NOT NULL, 
	scores FLOAT NOT NULL, 
	PRIMARY KEY (backref_id, scores), 
	FOREIGN KEY(backref_id) REFERENCES employee (id)
);

CREATE TABLE person_aliases (
	backref_id TEXT NOT NULL, 
	aliases TEXT NOT NULL, 
	PRIMARY KEY (backref_id, aliases), 
	FOREIGN KEY(backref_id) REFERENCES person (id)
);
