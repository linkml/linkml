# Using yq for querying and manipulating schemas

[yq](https://mikefarah.gitbook.io/yq/) is a command-line YAML processor, based on [jq](https://stedolan.github.io/jq/).

As LinkML schemas are typically stored as YAML, it's possible to use yq as a way of querying and manipulating them.

**Note:** yq operates at the level of schema yaml document structure, not the *meaning* of a schema. It has no knowledge of:

 * imports
 * inheritance and inference of slots over class hierarchies
 * inlining as dicts

If you want to do semantics-aware schema processing then we recommend you use [SchemaView](/developers/manipulating-schemas)

However, for certain kinds of quick and dirty low-level operations, yq
provides a fast, flexible, and easy way to query schema yaml files.

You could also choose to use jq, but this requires a (trivial)
intermediate step of converting yaml to json (and back to yaml, if you
are performing write operations), so we recommend yq over jq since it
works on YAML as a native form

This guide is mostly in the form of cookbook examples. If you wish to
perform operations that don't fit a template here, then you will need
to consult the (excellent) yq docs, and also have some awareness of
how LinkML schemas are rendered as YAML.

If you have your own cookbook examples, please contribute them as pull requests!

The examples here make use of the [PersonInfo](https://github.com/linkml/linkml/blob/main/examples/PersonSchema/personinfo.yaml) schema

## top level lookups

Fetch the schema identifier:

```bash
$ yq e '.id' personinfo.yaml
https://w3id.org/linkml/examples/personinfo
```

## all class names

```bash
✗ yq e '.classes | keys' personinfo.yaml
- NamedThing
- Person
- HasAliases
- Organization
- Place
- Address
- Event
- Concept
- DiagnosisConcept
- ProcedureConcept
- Relationship
- FamilialRelationship
- EmploymentEvent
- MedicalEvent
- WithLocation
# TODO: annotate that this is a container/root class
- Container
```

## classes with their is-a parents

```bash
$ yq e '.classes | to_entries | .[] | {"child": .key, "parent": .value.is_a}' personinfo.yaml
child: NamedThing
parent: null
child: Person
parent: NamedThing
child: HasAliases
parent: null
child: Organization
parent: NamedThing
child: Place
parent: null
child: Address
parent: null
child: Event
parent: null
child: Concept
parent: NamedThing
child: DiagnosisConcept
parent: Concept
child: ProcedureConcept
parent: Concept
child: Relationship
parent: null
child: FamilialRelationship
parent: Relationship
child: EmploymentEvent
parent: Event
child: MedicalEvent
parent: Event
child: WithLocation
```

TODO

## setting top level slots

Set the schema name:

```
$ yq e '.name = "NEW NAME"' personinfo.yaml
id: https://w3id.org/linkml/examples/personinfo
name: NEW NAME
description: |-
  Information about people, based on [schema.org](http://schema.org)
...
```

## lookup a class by name

Lookup the class Person:

```bash
✗ yq e '.classes.Person' personinfo.yaml
is_a: NamedThing
description: >-
  A person (alive, dead, undead, or fictional).
class_uri: schema:Person
mixins:
  - HasAliases
slots:
  - primary_email
  - birth_date
  - age_in_years
  - gender
  - current_address
  - has_employment_history
  - has_familial_relationships
  - has_medical_history
slot_usage:
  primary_email:
    pattern: "^\\S+@[\\S+\\.]+\\S+"
```

Looking up a particular slot:
```bash
✗ yq e '.classes.Person.is_a' personinfo.yaml | less
NamedThing
```

## Setting the is_a value of a class:

```
yq e '.classes.Person.is_a="Agent"' personinfo.yaml
```

Note that in LinkML schemas, classes, slots, etc are `inlined_as_dict`, meaning you can't access these by array indices

## prefixes

```
✗ yq e '.prefixes' personinfo.yaml
personinfo: https://w3id.org/linkml/examples/personinfo/
linkml: https://w3id.org/linkml/
schema: http://schema.org/
rdfs: http://www.w3.org/2000/01/rdf-schema#
prov: http://www.w3.org/ns/prov#
GSSO: http://purl.obolibrary.org/obo/GSSO_
famrel: https://example.org/FamilialRelations#
# DATA PREFIXES
P: http://example.org/P/
ROR: http://example.org/ror/
CODE: http://example.org/code/
GEO: http://example.org/geoloc/
```

Gotchas:

 - this will not include *imported* prefixes. Use SchemaView to get these.

just the keys:

```bash
✗ yq e '.prefixes | keys' personinfo.yaml | less
- personinfo
- linkml
- schema
- rdfs
- prov
- GSSO
- famrel
# DATA PREFIXES
- P
- ROR
- CODE
- GEO
```

just the values:

```bash
yq e '.prefixes | to_entries | .[].value' personinfo.yaml
https://w3id.org/linkml/examples/personinfo/
https://w3id.org/linkml/
http://schema.org/
http://www.w3.org/2000/01/rdf-schema#
http://www.w3.org/ns/prov#
http://purl.obolibrary.org/obo/GSSO_
https://example.org/FamilialRelations#
http://example.org/P/
http://example.org/ror/
http://example.org/code/
http://example.org/geoloc/
```

Gotchas:

 - the key value form above is a common shorthand, but prefixes can also be stored in expanded form
