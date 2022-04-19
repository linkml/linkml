# Part 6: Enumerations

Now we will extend our schema with a new slot `status` which records the vital status of a person, i.e whether they are living or dead.

We could do this by making the range of `status` a string, and
allowing the data provider to fill this with any value. However, this
will result in messy data that will need to cleaned up before any analysis is performed, e.g. to harmonize strings such as "alive" and "living"

LinkML allows you to provide *enumerations*, collections of controlled string values. Here is our example schema, with an example enumeration:

personinfo.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:                                  
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  personinfo: https://w3id.org/linkml/examples/personinfo/
  ORCID: https://orcid.org/
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    class_uri: schema:Person             
    attributes:
      id:
        identifier: true
      full_name:
        required: true
        description:
          name of the person
        slot_uri: schema:name            
      aliases:
        multivalued: true
        description:
          other names for the person
      phone:
        pattern: "^[\\d\\(\\)\\-]+$"
        slot_uri: schema:telephone       
      age:
        range: integer
        minimum_value: 0
        maximum_value: 200
      status:
        description: >-
          vital status of the person
        range: PersonStatus       ## see "enums" section below
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person

enums:
  PersonStatus:
    permissible_values:
      ALIVE:
      DEAD:
      UNKNOWN:
```

Now let's collect some data!

data.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 33
    phone: 555-555-5555
    status: ALIVE
  - id: ORCID:2222
    full_name: Count Dracula
    status: UNDEAD
```

We can run our data through the linkml validator (which just wraps a jsonschema validator by default)

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml data.yaml
```

If you run this you should see that it throws an error with the message:

```test
ValueError: Unknown PersonStatus enumeration code: UNDEAD
```

<!-- TODO: use schematools to patch the data -->

Let's go ahead and fix the data, changing Dracula's vital status from UNDEAD to UNKNOWN:

data-fixed.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 33
    phone: 555-555-5555
    status: ALIVE
  - id: ORCID:2222
    full_name: Count Dracula
    status: UNKNOWN
```

This should now validate successfully:

```bash
linkml-validate -s personinfo.yaml data-fixed.yaml
```

## Mapping Enums to vocabularies

We will now enhance our enums and map the different values to terms
from vocabularies or ontologies. This doesn't affect the basic
behavior of tools that use the schema - however, it does provide a
better basis for schema mapping, and it does affect the behavior of
generated RDF.

Here we use the biomedical ontology PATO to provide codes/terms for statuses like living and dead:

personinfo-mapped.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:                                  
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  personinfo: https://w3id.org/linkml/examples/personinfo/
  ORCID: https://orcid.org/
  PATO: http://purl.obolibrary.org/obo/PATO_
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    class_uri: schema:Person             
    attributes:
      id:
        identifier: true
      full_name:
        required: true
        description:
          name of the person
        slot_uri: schema:name            
      aliases:
        multivalued: true
        description:
          other names for the person
      phone:
        pattern: "^[\\d\\(\\)\\-]+$"
        slot_uri: schema:telephone       
      age:
        range: integer
        minimum_value: 0
        maximum_value: 200
      status:
        description: >-
          vital status of the person
        range: PersonStatus
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person

enums:
  PersonStatus:
    permissible_values:
      ALIVE:
        description: the person is living
        meaning: PATO:0001421 
      DEAD:
        description: the person is deceased
        meaning: PATO:0001422
      UNKNOWN:
        description: the vital status is not known
        todos:
          - map this to an ontology
```


```bash
linkml-convert -s personinfo-mapped.yaml data-fixed.yaml
```

Outputs:

```json
{
  "persons": [
    {
      "id": "ORCID:1234",
      "full_name": "Clark Kent",
      "phone": "555-555-5555",
      "age": 33,
      "status": "ALIVE"
    },
    {
      "id": "ORCID:2222",
      "full_name": "Count Dracula",
      "status": "UNKNOWN"
    }
  ],
  "@type": "Container"
}
```

<!-- TODO: RDF docs -->

## Use in Python

(you can skip this section if you are not concerned with interacting with data instances via Python)

```bash
gen-python personinfo-mapped.yaml > personinfo.py
```

then use this code:

test.py:

```python
from personinfo import Person, PersonStatus

person = Person(id='P1', full_name='Julius Caesar', status="DEAD")
print(f'STATUS={person.status}')
print(f'MEANING={person.status.meaning}')
```

```bash
python test.py
```

Outputs:

```text
STATUS=DEAD
MEANING=http://purl.obolibrary.org/obo/PATO_0001422
```

Next we will explore more aspects of the modeling language

## Further reading

* [LinkML Schemas: Enums](../schemas/models.html#enums)
* Metamodel Specification
    * [Enum Definition](https://w3id.org/linkml/EnumDefinition) class
* FAQ:
    - [Enums vs strings](../modeling.html#why-would-i-want-to-use-enums-over-strings)
