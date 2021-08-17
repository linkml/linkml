

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
