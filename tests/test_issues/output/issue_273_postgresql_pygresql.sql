
CREATE TYPE val_enum AS ENUM ('1', '2', '3');

CREATE TABLE foo (
	prop1 TEXT, 
	prop2 TEXT, 
	prop3 val_enum, 
	PRIMARY KEY (prop1, prop2, prop3)
);
