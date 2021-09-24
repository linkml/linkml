# Part 6: Basic Language Features

## Slots and attributes

Previously we have seen examples of schemas that declare fields/slots using an `attributes` slot under the relevant class.

In LinkML, "slots" (aka fields) are first-class entities that can be
declared outside of classes. The attribute syntax is just a convenient
layer on this, but explicit declaration of slots is often preferred
for reuse.

Let's see this in action:

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
    slots:   ## specified as a list
     - id
     - full_name
     - aliases
     - phone
     - age
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person

# slots are first-class entities in the metamodel
# delcaring them here allows them to be reused elsewhere
slots:
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
```

The JSON-Schema that is generated should be the same as in the previous example:

```bash
gen-json-schema personinfo.yaml
```

## Inheritance

LinkML provides mechanisms for inheritance/polymorphism

personinfo-with-inheritance.yaml:

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
  NamedThing:
    slots: 
     - id
     - full_name
    close_mappings:
     - schema:Thing
  
  Person:
    is_a: NamedThing
    mixins:
      - HasAliases
    class_uri: schema:Person             
    slots: 
     - id
     - full_name
     - phone
     - age
    id_prefixes:
      - ORCID

  Organization:
    description: >-
      An organization such as a company or university
    is_a: NamedThing
    class_uri: schema:Organization
    mixins:
      - HasAliases
    slots:
      - mission_statement
      
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person

  HasAliases:
    description: >-
      A mixin applied to any class that can have aliases/alternateNames
    mixin: true
    attributes:
      aliases:
        multivalued: true
        exact_mappings:
          - schema:alternateName

slots:
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
  mission_statement:
```

Now note when generating the JSON-Schema, slots from parent classes and mixins are "rolled down":

```bash
gen-json-schema personinfo-with-inheritance.yaml
```


