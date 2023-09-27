
# Enum: relational_role_enum


enumeration of roles a slot on a relationship class can play

URI: [linkml:relational_role_enum](https://w3id.org/linkml/relational_role_enum)


## Other properties

|  |  |  |
| --- | --- | --- |

## Permissible Values

| Text | Description | Meaning | Other Information |
| :--- | :---: | :---: | ---: |
| SUBJECT | a slot with this role connects a relationship to its subject/source node | rdf:subject | {'exact_mappings': ['owl:annotatedSource']} |
| OBJECT | a slot with this role connects a relationship to its object/target node | rdf:object | {'exact_mappings': ['owl:annotatedTarget']} |
| PREDICATE | a slot with this role connects a relationship to its predicate/property | rdf:predicate | {'exact_mappings': ['owl:annotatedProperty']} |
| NODE | a slot with this role connects a symmetric relationship to a node that represents either subject or object node |  |  |
| OTHER_ROLE | a slot with this role connects a relationship to a node that is not subject/object/predicate |  |  |

