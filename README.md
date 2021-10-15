[![Pyversions](https://img.shields.io/pypi/pyversions/linkml.svg)](https://pypi.python.org/pypi/linkml)
![](https://github.com/linkml/linkml/workflows/Build/badge.svg)
[![PyPi](https://img.shields.io/pypi/v/linkml.svg)](https://pypi.python.org/pypi/linkml)
[![badge](https://img.shields.io/badge/launch-binder-579ACA.svg)](https://mybinder.org/v2/gh/linkml/linkml/main?filepath=notebooks)

# LinkML - Linked Data Modeling Language

LinkML is a linked data modeling language following object-oriented and ontological principles. LinkML models are typically authored in YAML, and can be converted to other schema representation formats such as JSON or RDF.

LinkML is bundled with a number of generators which will take LinkML YAML schemas as input and output schemas in one of the following formats:

- [ShEx](https://linkml.io/linkml/generators/shex.html)
- [JSON Schema](https://linkml.io/linkml/generators/json-schema.html)
- [OWL](https://linkml.io/linkml/generators/owl.html)
- [Python dataclasses](https://linkml.io/linkml/generators/python.html)
- [Java](https://linkml.io/linkml/generators/java.html)
- [SPARQL](https://linkml.io/linkml/generators/sparql.html)
- [SQL DDL](https://linkml.io/linkml/generators/sqlddl.html)
- [Markdown](https://linkml.io/linkml/generators/markdown.html) (for deployment in a GitHub pages site)

...and more.

More details about the the usage of different types of [Generators](https://linkml.io/linkml/generators/index.html) can be viewed on the docs site.

You can browse the metamodel component documentation [here](https://linkml.github.io/linkml-model/docs). LinkML is self-describing, but a few important vocabulary terms to keep in mind are:
- [ClassDefinition](https://linkml.github.io/linkml-model/docs/ClassDefinition): Component for defining Classes
- [SlotDefinition](https://linkml.github.io/linkml-model/docs/SlotDefinition): Component for defining Class Properties (or Slots)
- [TypeDefinition](https://linkml.github.io/linkml-model/docs/TypeDefinition): Component for defining Data Types
- [SchemaDefinition](https://linkml.github.io/linkml-model/docs/SchemaDefinition): Component for defining Schemas (combination of subset, type, slot, class)

As an example, LinkML has been used for the development of the [Biolink Model](https://biolink.github.io/biolink-model/), but the framework itself is general purpose and can be used for any kind of modeling. For an example Biolink metamodel, see this [Jupyter Notebook](https://github.com/linkml/linkml/blob/main/notebooks/examples.ipynb).

## Installation

This project uses [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) for installation. Some IDE's like PyCharm also have direct [support](https://www.jetbrains.com/help/pycharm/pipenv.html) for pipenv.

```bash
> pipenv install linkml
```

Additional [installation](https://linkml.io/linkml/intro/install.html) instructions can be found on the LinkML docs site.

## Generators

In the following sections we will use the [Person](https://linkml.io/linkml/intro/tutorial01.html#your-first-schema) example schema, which consists of a single class `Person` with a number of slots, to demonstrate the usage of various generators:

### JSON Schema

[JSON Schema](https://json-schema.org/) is a schema language for JSON documents.

To autogenerate JSON Schema output for the `Person` schema, run the following command:

```bash
pipenv run gen-json-schema examples/PersonSchema/personinfo.yaml
```

<details>
<summary>JSON Schema output for Person schema</summary>

```
{
   "$id": "https://w3id.org/linkml/examples/personinfo",
   "$schema": "http://json-schema.org/draft-07/schema#",
   "additionalProperties": true,
   "definitions": {
      "Address": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "city": {
               "type": "string"
            },
            "postal_code": {
               "type": "string"
            },
            "street": {
               "type": "string"
            }
         },
         "required": [],
         "title": "Address",
         "type": "object"
      },
      "Concept": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "description": {
               "type": "string"
            },
            "id": {
               "type": "string"
            },
            "image": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "id"
         ],
         "title": "Concept",
         "type": "object"
      },
      "Container": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "organizations": {
               "items": {
                  "$ref": "#/definitions/Organization"
               },
               "type": "array"
            },
            "persons": {
               "items": {
                  "$ref": "#/definitions/Person"
               },
               "type": "array"
            }
         },
         "required": [],
         "title": "Container",
         "type": "object"
      },
      "DiagnosisConcept": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "description": {
               "type": "string"
            },
            "id": {
               "type": "string"
            },
            "image": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "id"
         ],
         "title": "DiagnosisConcept",
         "type": "object"
      },
      "DiagnosisType": {
         "description": "",
         "enum": [],
         "title": "DiagnosisType",
         "type": "string"
      },
      "EmploymentEvent": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "duration": {
               "type": "number"
            },
            "employed_at": {
               "type": "string"
            },
            "ended_at_time": {
               "format": "date",
               "type": "string"
            },
            "is_current": {
               "type": "boolean"
            },
            "started_at_time": {
               "format": "date",
               "type": "string"
            }
         },
         "required": [],
         "title": "EmploymentEvent",
         "type": "object"
      },
      "Event": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "duration": {
               "type": "number"
            },
            "ended_at_time": {
               "format": "date",
               "type": "string"
            },
            "is_current": {
               "type": "boolean"
            },
            "started_at_time": {
               "format": "date",
               "type": "string"
            }
         },
         "required": [],
         "title": "Event",
         "type": "object"
      },
      "FamilialRelationship": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "ended_at_time": {
               "format": "date",
               "type": "string"
            },
            "related_to": {
               "type": "string"
            },
            "started_at_time": {
               "format": "date",
               "type": "string"
            },
            "type": {
               "$ref": "#/definitions/FamilialRelationshipType"
            }
         },
         "required": [
            "type",
            "related_to"
         ],
         "title": "FamilialRelationship",
         "type": "object"
      },
      "FamilialRelationshipType": {
         "description": "",
         "enum": [
            "SIBLING_OF",
            "PARENT_OF",
            "CHILD_OF"
         ],
         "title": "FamilialRelationshipType",
         "type": "string"
      },
      "GenderType": {
         "description": "",
         "enum": [
            "nonbinary man",
            "nonbinary woman",
            "transgender woman",
            "transgender man",
            "cisgender man",
            "cisgender woman"
         ],
         "title": "GenderType",
         "type": "string"
      },
      "MedicalEvent": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "diagnosis": {
               "$ref": "#/definitions/DiagnosisConcept"
            },
            "duration": {
               "type": "number"
            },
            "ended_at_time": {
               "format": "date",
               "type": "string"
            },
            "in_location": {
               "type": "string"
            },
            "is_current": {
               "type": "boolean"
            },
            "procedure": {
               "$ref": "#/definitions/ProcedureConcept"
            },
            "started_at_time": {
               "format": "date",
               "type": "string"
            }
         },
         "required": [],
         "title": "MedicalEvent",
         "type": "object"
      },
      "NamedThing": {
         "additionalProperties": false,
         "description": "A generic grouping for any identifiable entity",
         "properties": {
            "description": {
               "type": "string"
            },
            "id": {
               "type": "string"
            },
            "image": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "id"
         ],
         "title": "NamedThing",
         "type": "object"
      },
      "Organization": {
         "additionalProperties": false,
         "description": "An organization such as a company or university",
         "properties": {
            "aliases": {
               "items": {
                  "type": "string"
               },
               "type": "array"
            },
            "description": {
               "type": "string"
            },
            "founding_date": {
               "type": "string"
            },
            "founding_location": {
               "type": "string"
            },
            "id": {
               "type": "string"
            },
            "image": {
               "type": "string"
            },
            "mission_statement": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "id"
         ],
         "title": "Organization",
         "type": "object"
      },
      "Person": {
         "additionalProperties": false,
         "description": "A person (alive, dead, undead, or fictional).",
         "properties": {
            "age_in_years": {
               "type": "integer"
            },
            "aliases": {
               "items": {
                  "type": "string"
               },
               "type": "array"
            },
            "birth_date": {
               "type": "string"
            },
            "current_address": {
               "$ref": "#/definitions/Address",
               "description": "The address at which a person currently lives"
            },
            "description": {
               "type": "string"
            },
            "gender": {
               "$ref": "#/definitions/GenderType"
            },
            "has_employment_history": {
               "items": {
                  "$ref": "#/definitions/EmploymentEvent"
               },
               "type": "array"
            },
            "has_familial_relationships": {
               "items": {
                  "$ref": "#/definitions/FamilialRelationship"
               },
               "type": "array"
            },
            "has_medical_history": {
               "items": {
                  "$ref": "#/definitions/MedicalEvent"
               },
               "type": "array"
            },
            "id": {
               "type": "string"
            },
            "image": {
               "type": "string"
            },
            "name": {
               "type": "string"
            },
            "primary_email": {
               "pattern": "^\\S+@[\\S+\\.]+\\S+",
               "type": "string"
            }
         },
         "required": [
            "id"
         ],
         "title": "Person",
         "type": "object"
      },
      "Place": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "aliases": {
               "items": {
                  "type": "string"
               },
               "type": "array"
            },
            "id": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "id"
         ],
         "title": "Place",
         "type": "object"
      },
      "ProcedureConcept": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "description": {
               "type": "string"
            },
            "id": {
               "type": "string"
            },
            "image": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "id"
         ],
         "title": "ProcedureConcept",
         "type": "object"
      },
      "Relationship": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "ended_at_time": {
               "format": "date",
               "type": "string"
            },
            "related_to": {
               "type": "string"
            },
            "started_at_time": {
               "format": "date",
               "type": "string"
            },
            "type": {
               "type": "string"
            }
         },
         "required": [],
         "title": "Relationship",
         "type": "object"
      }
   },
   "properties": {},
   "title": "personinfo",
   "type": "object"
}
```
</details>

Note that any JSON that conforms to the derived JSON Schema can be converted to RDF using the derived JSON-LD context.

### JSON-LD Context

[JSON-LD context](https://www.w3.org/TR/json-ld/#the-context) provides mapping from JSON to RDF.

To autogenerate JSON LD context output for the `Person` schema, run the following command:

```bash
pipenv run gen-jsonld-context examples/PersonSchema/personinfo.yaml
```

<details>
<summary>JSON LD Context output for Person schema</summary>

```
{
   "_comments": "Auto generated from personinfo.yaml by jsonldcontextgen.py version: 0.1.1\n    Generation date: 2021-09-13 12:01\n    Schema: personinfo\n    \n    id: https://w3id.org/linkml/examples/personinfo\n    description: Information about people, based on [schema.org](http://schema.org)\n    license: https://creativecommons.org/publicdomain/zero/1.0/\n    ",
   "@context": {
      "GSSO": {
         "@id": "http://purl.obolibrary.org/obo/GSSO_",
         "@prefix": true
      },
      "famrel": "https://example.org/FamilialRelations#",
      "linkml": "https://w3id.org/linkml/",
      "personinfo": "https://w3id.org/linkml/examples/personinfo/",
      "prov": "http://www.w3.org/ns/prov#",
      "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
      "schema": "http://schema.org/",
      "skos": "http://example.org/UNKNOWN/skos/",
      "xsd": "http://www.w3.org/2001/XMLSchema#",
      "@vocab": "https://w3id.org/linkml/examples/personinfo/",
      "age_in_years": {
         "@type": "xsd:integer"
      },
      "birth_date": {
         "@id": "schema:birthDate"
      },
      "current_address": {
         "@type": "@id"
      },
      "description": {
         "@id": "schema:description"
      },
      "diagnosis": {
         "@type": "@id"
      },
      "duration": {
         "@type": "xsd:float"
      },
      "employed_at": {
         "@type": "@id"
      },
      "ended_at_time": {
         "@type": "xsd:date",
         "@id": "prov:endedAtTime"
      },
      "founding_location": {
         "@type": "@id"
      },
      "gender": {
         "@context": {
            "@vocab": "@null",
            "text": "skos:notation",
            "description": "skos:prefLabel",
            "meaning": "@id"
         },
         "@id": "schema:gender"
      },
      "has_employment_history": {
         "@type": "@id"
      },
      "has_familial_relationships": {
         "@type": "@id"
      },
      "has_medical_history": {
         "@type": "@id"
      },
      "id": "@id",
      "image": {
         "@id": "schema:image"
      },
      "in_location": {
         "@type": "@id"
      },
      "is_current": {
         "@type": "xsd:boolean"
      },
      "name": {
         "@id": "schema:name"
      },
      "organizations": {
         "@type": "@id"
      },
      "persons": {
         "@type": "@id"
      },
      "primary_email": {
         "@id": "schema:email"
      },
      "procedure": {
         "@type": "@id"
      },
      "related_to": {
         "@type": "@id"
      },
      "started_at_time": {
         "@type": "xsd:date",
         "@id": "prov:startedAtTime"
      },
      "Address": {
         "@id": "schema:PostalAddress"
      },
      "Organization": {
         "@id": "schema:Organization"
      },
      "Person": {
         "@id": "schema:Person"
      }
   }
}
```
</details>

You can control the output via [prefixes](https://linkml.io/linkml-model/docs/prefixes.html) declarations and [default_curi_maps](https://linkml.io/linkml-model/docs/default_curi_maps.html).

Any JSON that conforms to the derived JSON Schema (see above) can be converted to RDF using this context.

### Python Dataclasses

To autogenerate Python dataclasses output for the `Person` schema, run the following command:

```bash
pipenv run gen-py-classes examples/PersonSchema/personinfo.yaml > examples/PersonSchema/personinfo.py
```

<details>
<summary>Python dataclass output for Person schema</summary>

```python
@dataclass
class NamedThing(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.NamedThing
    class_class_curie: ClassVar[str] = "personinfo:NamedThing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.NamedThing

    id: Union[str, NamedThingId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.image is not None and not isinstance(self.image, str):
            self.image = str(self.image)

        super().__post_init__(**kwargs)
```
</details>

For more details see [PythonGenNotes](linkml/generators/PythonGenNotes.md).

The python object can be directly serialized as RDF.

### ShEx

[ShEx](http://shex.io/shex-semantics/index.html), short for Shape Expressions Language is a modeling language for RDF files.

To autogenerate ShEx output for the `Person` schema, run the following command:

```bash
pipenv run gen-shex examples/PersonSchema/personinfo.yaml > examples/PersonSchema/personinfo.shexj
```

<details>
<summary>ShEx output for Person schema</summary>

```
BASE <https://w3id.org/linkml/examples/personinfo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX linkml: <https://w3id.org/linkml/>
PREFIX schema: <http://schema.org/>
PREFIX prov: <http://www.w3.org/ns/prov#>


linkml:String xsd:string

linkml:Integer xsd:integer

linkml:Boolean xsd:boolean

linkml:Float xsd:float

linkml:Double xsd:double

linkml:Decimal xsd:decimal

linkml:Time xsd:dateTime

linkml:Date xsd:date

linkml:Datetime xsd:dateTime

linkml:Uriorcurie IRI

linkml:Uri IRI

linkml:Ncname xsd:string

linkml:Objectidentifier IRI

linkml:Nodeidentifier NONLITERAL

<Address> CLOSED {
    (  $<Address_tes> (  <street> @linkml:String ? ;
          <city> @linkml:String ? ;
          <postal_code> @linkml:String ?
       ) ;
       rdf:type [ schema:PostalAddress ] ?
    )
}

<Concept>  (
    CLOSED {
       (  $<Concept_tes> (  &<NamedThing_tes> ;
             rdf:type [ <NamedThing> ] ?
          ) ;
          rdf:type [ <Concept> ]
       )
    } OR @<DiagnosisConcept> OR @<ProcedureConcept>
)

<Container> CLOSED {
    (  $<Container_tes> (  <persons> @<Person> * ;
          <organizations> @<Organization> *
       ) ;
       rdf:type [ <Container> ] ?
    )
}

<DiagnosisConcept> CLOSED {
    (  $<DiagnosisConcept_tes> (  &<Concept_tes> ;
          rdf:type [ <Concept> ] ?
       ) ;
       rdf:type [ <DiagnosisConcept> ]
    )
}

<EmploymentEvent> CLOSED {
    (  $<EmploymentEvent_tes> (  &<Event_tes> ;
          rdf:type [ <Event> ] ? ;
          <employed_at> @<Organization> ?
       ) ;
       rdf:type [ <EmploymentEvent> ] ?
    )
}

<Event>  (
    CLOSED {
       (  $<Event_tes> (  prov:startedAtTime @linkml:Date ? ;
             prov:endedAtTime @linkml:Date ? ;
             <duration> @linkml:Float ? ;
             <is_current> @linkml:Boolean ?
          ) ;
          rdf:type [ <Event> ] ?
       )
    } OR @<EmploymentEvent> OR @<MedicalEvent>
)

<FamilialRelationship> CLOSED {
    (  $<FamilialRelationship_tes> (  &<Relationship_tes> ;
          rdf:type [ <Relationship> ] ? ;
          <type> @<FamilialRelationshipType> ;
          <related_to> @<Person>
       ) ;
       rdf:type [ <FamilialRelationship> ] ?
    )
}

<HasAliases> {
    (  $<HasAliases_tes> <aliases> @linkml:String * ;
       rdf:type [ <HasAliases> ] ?
    )
}

<MedicalEvent> CLOSED {
    (  $<MedicalEvent_tes> (  &<Event_tes> ;
          rdf:type [ <Event> ] ? ;
          <in_location> @<Place> ? ;
          <diagnosis> @<DiagnosisConcept> ? ;
          <procedure> @<ProcedureConcept> ?
       ) ;
       rdf:type [ <MedicalEvent> ] ?
    )
}

<NamedThing>  (
    CLOSED {
       (  $<NamedThing_tes> (  schema:name @linkml:String ? ;
             schema:description @linkml:String ? ;
             schema:image @linkml:String ?
          ) ;
          rdf:type [ <NamedThing> ]
       )
    } OR @<Concept> OR @<Organization> OR @<Person>
)

<Organization> CLOSED {
    (  $<Organization_tes> (  &<NamedThing_tes> ;
          rdf:type [ <NamedThing> ] ? ;
          &<HasAliases_tes> ;
          rdf:type [ <HasAliases> ] ? ;
          <mission_statement> @linkml:String ? ;
          <founding_date> @linkml:String ? ;
          <founding_location> @<Place> ? ;
          <aliases> @linkml:String *
       ) ;
       rdf:type [ schema:Organization ]
    )
}

<Person> CLOSED {
    (  $<Person_tes> (  &<NamedThing_tes> ;
          rdf:type [ <NamedThing> ] ? ;
          &<HasAliases_tes> ;
          rdf:type [ <HasAliases> ] ? ;
          <primary_email> @linkml:String ? ;
          schema:birthDate @linkml:String ? ;
          <age_in_years> @linkml:Integer ? ;
          schema:gender @<GenderType> ? ;
          <current_address> @<Address> ? ;
          <has_employment_history> @<EmploymentEvent> * ;
          <has_familial_relationships> @<FamilialRelationship> * ;
          <has_medical_history> @<MedicalEvent> * ;
          <aliases> @linkml:String *
       ) ;
       rdf:type [ schema:Person ]
    )
}

<Place> CLOSED {
    (  $<Place_tes> (  &<HasAliases_tes> ;
          rdf:type [ <HasAliases> ] ? ;
          schema:name @linkml:String ? ;
          <aliases> @linkml:String *
       ) ;
       rdf:type [ <Place> ]
    )
}

<ProcedureConcept> CLOSED {
    (  $<ProcedureConcept_tes> (  &<Concept_tes> ;
          rdf:type [ <Concept> ] ?
       ) ;
       rdf:type [ <ProcedureConcept> ]
    )
}

<Relationship>  (
    CLOSED {
       (  $<Relationship_tes> (  prov:startedAtTime @linkml:Date ? ;
             prov:endedAtTime @linkml:Date ? ;
             <related_to> @linkml:String ? ;
             <type> @linkml:String ?
          ) ;
          rdf:type [ <Relationship> ] ?
       )
    } OR @<FamilialRelationship>
)

<WithLocation> {
    (  $<WithLocation_tes> <in_location> @<Place> ? ;
       rdf:type [ <WithLocation> ] ?
    )
}
```
</details>

### OWL

Web Ontology Language [OWL](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/) is modeling language used to author ontologies.

To autogenerate OWL output for the `Person` schema, run the following command:

```bash
pipenv run gen-owl examples/PersonSchema/personinfo.yaml > examples/PersonSchema/personinfo.owl.ttl
```

<details>
<summary>OWL output for Person schema</summary>

```turtle
<https://w3id.org/linkml/examples/personinfo/Person> a owl:Class,
        linkml:ClassDefinition ;
    rdfs:label "Person" ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:maxQualifiedCardinality 1 ;
            owl:onClass linkml:Integer ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/age_in_years> ],
        [ a owl:Restriction ;
            owl:allValuesFrom <https://w3id.org/linkml/examples/personinfo/EmploymentEvent> ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/has_employment_history> ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality 1 ;
            owl:onClass linkml:String ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/primary_email> ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality 1 ;
            owl:onClass linkml:String ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/birth_date> ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality 1 ;
            owl:onClass <http://UNKNOWN.org/GenderType> ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/gender> ],
        [ a owl:Restriction ;
            owl:allValuesFrom <https://w3id.org/linkml/examples/personinfo/MedicalEvent> ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/has_medical_history> ],
        [ a owl:Restriction ;
            owl:allValuesFrom <https://w3id.org/linkml/examples/personinfo/FamilialRelationship> ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/has_familial_relationships> ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality 1 ;
            owl:onClass <https://w3id.org/linkml/examples/personinfo/Address> ;
            owl:onProperty <https://w3id.org/linkml/examples/personinfo/current_address> ],
        [ a owl:Restriction ;
            owl:allValuesFrom linkml:String ;
            owl:onProperty linkml:aliases ],
        <https://w3id.org/linkml/examples/personinfo/HasAliases>,
        <https://w3id.org/linkml/examples/personinfo/NamedThing> ;
    skos:definition "A person (alive, dead, undead, or fictional)." ;
    skos:exactMatch <http://schema.org/Person> .
```
</details>

## Generating Markdown documentation

The below command will generate a Markdown document for every class and slot in the model which can be used in a static site for ex., GitHub pages.

```bash
pipenv run gen-markdown examples/PersonSchema/personinfo.yaml -d examples/PersonSchema/personinfomd
```

## Specification

See [specification](https://linkml.io/linkml/specifications/linkml-spec.html). Also see the [semantics](semantics) folder for an experimental specification in terms of FOL.

## Developer Notes

### Release to PyPI

A Github action is set up to automatically release the package to PyPI. When it is ready for a new release, create a [Github release](https://github.com/linkml/releases). The version should be in the vX.X.X format following [the semantic versioning specification](https://semver.org/).

After the release is created, the GitHub action will be triggered to publish to PyPI. The release version will be used to create the PyPI package.

If the PyPI release failed, make fixes, [delete](https://docs.github.com/en/enterprise/2.16/user/github/administering-a-repository/editing-and-deleting-releases#deleting-a-release) the GitHub release, and recreate a release with the same version again.

## Additional Documentation

[LinkML for environmental and omics metadata](https://docs.google.com/presentation/d/1xK__vZdv0jHtOu0eOTzGUJeDt9YMVOGR1jxIXTtdXDM/edit?usp=sharing)

## History

This framework used to be called BiolinkML. LinkML replaces BiolinkML. For assistance in migration, see [Migration.md](Migration.md).
