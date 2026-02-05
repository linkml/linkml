-- ====================================================================
-- SQL Validation Queries
-- Generated from LinkML schema
-- LinkML v0.0.0.post3958.dev0+0979fc25
-- Generator: sqlvalidationgen.py v0.1.0
-- Dialect: sqlite
-- ====================================================================

SELECT 'NamedThing' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "NamedThing"
WHERE "NamedThing".id IS NULL

UNION ALL

SELECT 'NamedThing' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "NamedThing"
WHERE "NamedThing".id IN (SELECT id
FROM "NamedThing" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'NamedThing' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "NamedThing"
WHERE "NamedThing".name IS NULL

UNION ALL

SELECT 'Person' AS table_name, 'primary_email' AS column_name, 'pattern' AS constraint_type, id AS record_id, primary_email AS invalid_value
FROM "Person"
WHERE "Person".primary_email IS NOT NULL AND NOT (REGEXP('^\S+@[\S+\.]+\S+', primary_email) = 1)

UNION ALL

SELECT 'Person' AS table_name, 'age' AS column_name, 'range' AS constraint_type, id AS record_id, age AS invalid_value
FROM "Person"
WHERE "Person".age < 0 OR "Person".age > 999

UNION ALL

SELECT 'Person' AS table_name, 'gender' AS column_name, 'enum' AS constraint_type, id AS record_id, gender AS invalid_value
FROM "Person"
WHERE "Person".gender IS NOT NULL AND ("Person".gender NOT IN ('nonbinary man', 'nonbinary woman', 'transgender woman', 'transgender man', 'cisgender man', 'cisgender woman'))

UNION ALL

SELECT 'Person' AS table_name, 'telephone' AS column_name, 'pattern' AS constraint_type, id AS record_id, telephone AS invalid_value
FROM "Person"
WHERE "Person".telephone IS NOT NULL AND NOT (REGEXP('^[\d\(\)\-]+$', telephone) = 1)

UNION ALL

SELECT 'Person' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Person"
WHERE "Person".id IS NULL

UNION ALL

SELECT 'Person' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "Person"
WHERE "Person".id IN (SELECT id
FROM "Person" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'Person' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Person"
WHERE "Person".name IS NULL

UNION ALL

SELECT 'Organization' AS table_name, 'categories' AS column_name, 'enum' AS constraint_type, id AS record_id, categories AS invalid_value
FROM "Organization"
WHERE "Organization".categories IS NOT NULL AND ("Organization".categories NOT IN ('non profit', 'for profit', 'offshore', 'charity', 'shell company', 'loose organization'))

UNION ALL

SELECT 'Organization' AS table_name, 'score' AS column_name, 'range' AS constraint_type, id AS record_id, score AS invalid_value
FROM "Organization"
WHERE "Organization".score < 0.0 OR "Organization".score > 5.0

UNION ALL

SELECT 'Organization' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Organization"
WHERE "Organization".id IS NULL

UNION ALL

SELECT 'Organization' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "Organization"
WHERE "Organization".id IN (SELECT id
FROM "Organization" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'Organization' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Organization"
WHERE "Organization".name IS NULL

UNION ALL

SELECT 'Place' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Place"
WHERE "Place".id IS NULL

UNION ALL

SELECT 'Place' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "Place"
WHERE "Place".id IN (SELECT id
FROM "Place" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'Place' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Place"
WHERE "Place".name IS NULL

UNION ALL

SELECT 'Concept' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Concept"
WHERE "Concept".id IS NULL

UNION ALL

SELECT 'Concept' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "Concept"
WHERE "Concept".id IN (SELECT id
FROM "Concept" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'Concept' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "Concept"
WHERE "Concept".name IS NULL

UNION ALL

SELECT 'DiagnosisConcept' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "DiagnosisConcept"
WHERE "DiagnosisConcept".id IS NULL

UNION ALL

SELECT 'DiagnosisConcept' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "DiagnosisConcept"
WHERE "DiagnosisConcept".id IN (SELECT id
FROM "DiagnosisConcept" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'DiagnosisConcept' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "DiagnosisConcept"
WHERE "DiagnosisConcept".name IS NULL

UNION ALL

SELECT 'ProcedureConcept' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "ProcedureConcept"
WHERE "ProcedureConcept".id IS NULL

UNION ALL

SELECT 'ProcedureConcept' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "ProcedureConcept"
WHERE "ProcedureConcept".id IN (SELECT id
FROM "ProcedureConcept" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'ProcedureConcept' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "ProcedureConcept"
WHERE "ProcedureConcept".name IS NULL

UNION ALL

SELECT 'IntegerPrimaryKeyObject' AS table_name, 'int_id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "IntegerPrimaryKeyObject"
WHERE "IntegerPrimaryKeyObject".int_id IS NULL

UNION ALL

SELECT 'IntegerPrimaryKeyObject' AS table_name, 'int_id' AS column_name, 'identifier' AS constraint_type, id AS record_id, int_id AS invalid_value
FROM "IntegerPrimaryKeyObject"
WHERE "IntegerPrimaryKeyObject".int_id IN (SELECT int_id
FROM "IntegerPrimaryKeyObject" GROUP BY int_id
HAVING count(*) > 1)

UNION ALL

SELECT 'OperationProcedureConcept' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "OperationProcedureConcept"
WHERE "OperationProcedureConcept".id IS NULL

UNION ALL

SELECT 'OperationProcedureConcept' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "OperationProcedureConcept"
WHERE "OperationProcedureConcept".id IN (SELECT id
FROM "OperationProcedureConcept" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'OperationProcedureConcept' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "OperationProcedureConcept"
WHERE "OperationProcedureConcept".name IS NULL

UNION ALL

SELECT 'ImagingProcedureConcept' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "ImagingProcedureConcept"
WHERE "ImagingProcedureConcept".id IS NULL

UNION ALL

SELECT 'ImagingProcedureConcept' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "ImagingProcedureConcept"
WHERE "ImagingProcedureConcept".id IN (SELECT id
FROM "ImagingProcedureConcept" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'ImagingProcedureConcept' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "ImagingProcedureConcept"
WHERE "ImagingProcedureConcept".name IS NULL

UNION ALL

SELECT 'code system' AS table_name, 'id' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "code system"
WHERE "code system".id IS NULL

UNION ALL

SELECT 'code system' AS table_name, 'id' AS column_name, 'identifier' AS constraint_type, id AS record_id, id AS invalid_value
FROM "code system"
WHERE "code system".id IN (SELECT id
FROM "code system" GROUP BY id
HAVING count(*) > 1)

UNION ALL

SELECT 'code system' AS table_name, 'name' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "code system"
WHERE "code system".name IS NULL

UNION ALL

SELECT 'FamilialRelationship' AS table_name, 'type' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "FamilialRelationship"
WHERE "FamilialRelationship".type IS NULL

UNION ALL

SELECT 'FamilialRelationship' AS table_name, 'type' AS column_name, 'enum' AS constraint_type, id AS record_id, type AS invalid_value
FROM "FamilialRelationship"
WHERE "FamilialRelationship".type IS NOT NULL AND ("FamilialRelationship".type NOT IN ('SIBLING_OF', 'PARENT_OF', 'CHILD_OF'))

UNION ALL

SELECT 'InterPersonalRelationship' AS table_name, 'type' AS column_name, 'required' AS constraint_type, id AS record_id, NULL AS invalid_value
FROM "InterPersonalRelationship"
WHERE "InterPersonalRelationship".type IS NULL;
