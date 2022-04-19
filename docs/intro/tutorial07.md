# Part 7: Slots and inheritance

## Slots and attributes

Previously we have seen examples of schemas that declare fields/slots using an `attributes` slot under the relevant class.

In LinkML, "slots" (aka fields) are first-class entities that can be
declared outside of classes. The attribute syntax is just a convenient
layer on this, but explicit declaration of slots is often preferred
for reuse.

(and yes, because LinkML is self-describing, we also talk about metamodel slots)

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

And just as a reminder, we can look at the UML for the schema:


```bash
gen-yuml personinfo.yaml
```

![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Container]++-%20persons%200..*%3E[Person%7Cid:string;full_name:string;aliases:string%20*;phone:string%20%3F;age:integer%20%3F],[Container])

See [FAQ: attributes vs slots](faq/modeling.html#when-should-i-use-attributes-vs-slots)


## Inheritance

Now let's say we want to extend the schema, and we want to include
another class `Organization`. Organizations may have different
properties from people, but they may also share slots in common - for
example, having a unique identifier and a name

LinkML provides mechanisms for *inheritance/polymorphism*, we can define a "superclass" called `NamedThing`, put shared slots in there, and *inherit* from it.

We also introduce a concept called "mixins" here, which allows for multiple inheritance:

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

  ## --
  ## New parent class
  ## --
  NamedThing:
    abstract: true     ## should not be instantiated directly
    slots: 
     - id
     - full_name
    close_mappings:
     - schema:Thing
  
  Person:
    is_a: NamedThing  ## inheritance
    mixins:
      - HasAliases
    class_uri: schema:Person             
    slots:            ## note we only have slots specific to people
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
    tree_root: true
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
      organizations:
        multivalued: true
        inlined_as_list: true
        range: Organization

  ## --
  ## New mixin class
  ## --
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

Note that our container object now contains two kinds of lists: people and organization

Here is the schema:

```bash
gen-yuml personinfo-with-inheritance.yaml
```

Renders as:

![img](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing%7Cid:string;full_name:string]%5E-[Person%7Cphone:string%20%3F;age:integer%20%3F;aliases:string%20*;id(i):string;full_name(i):string],[NamedThing]%5E-[Organization%7Cmission_statement:string%20%3F;aliases:string%20*;id(i):string;full_name(i):string],[Container]++-%20persons%200..*%3E[Person],[Person]uses%20-.-%3E[HasAliases%7Caliases:string%20*],[Container]++-%20organizations%200..*%3E[Organization],[Organization]uses%20-.-%3E[HasAliases],[Person]uses%20-.-%3E[HasAliases],[Organization]uses%20-.-%3E[HasAliases],[Container])


Let's take a look at the JSON schema:

```bash
gen-json-schema personinfo-with-inheritance.yaml > personinfo-with-inheritance.schema.json
```

You can see that even though JSON-Schema doesn't support inheritance, slots from is-a parents and mixins are "rolled down" to their children:


```json
...
      "Person": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "age": {
               "type": "integer"
            },
            "aliases": {
               "items": {
                  "type": "string"
               },
               "type": "array"
            },
            "full_name": {
               "description": "name of the person",
               "type": "string"
            },
            "id": {
               "type": "string"
            },
            "phone": {
               "pattern": "^[\\d\\(\\)\\-]+$",
               "type": "string"
            }
         },
         "required": [
            "id",
            "full_name"
         ],
         "title": "Person",
         "type": "object"
      }
...
```



## Customizing slots in the context of classes: Slot Usage

LinkML gives you the ability to reuse or inherit slots while customizing them for use in a particular class, using `slot_usage`

First let's create a schema where we introduce a new general class `Relationship` 

slot-usage-example.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:                                 
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
  
classes:
  NamedThing:
    slots: 
     - id
     - full_name
  Person:
    is_a: NamedThing
    attributes:
      has_familial_relationships:
        multivalued: true
        range: FamilialRelationship
        inlined_as_list: true
      has_organizational_relationships:
        multivalued: true
        range: OrganizationalRelationship
        inlined_as_list: true
    
  Organization:
    is_a: NamedThing

  Relationship:
    abstract: true
    attributes:
      duration:
        range: integer
      related_to:
        range: NamedThing
      relationship_type:

  FamilialRelationship:
    is_a: Relationship
    slot_usage:
      related_to:
        range: Person
        required: true
      relationship_type:
        range: FamilialRelationshipType
      

  OrganizationalRelationship:
    is_a: Relationship
    slot_usage:
      related_to:
        range: Organization
        required: true
      relationship_type:
        range: OrganizationalRelationshipType

  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
      organizations:
        multivalued: true
        inlined_as_list: true
        range: Organization

slots:
  id:
    identifier: true
  full_name:

enums:
  FamilialRelationshipType:
    permissible_values:
      SIBLING_OF:
      PARENT_OF:
      CHILD_OF:
  OrganizationalRelationshipType:
    permissible_values:
      EMPLOYED_BY:
      FOUNDED_BY:
      LEADER_OF:
      MEMBER_OF:

```

```bash
gen-yuml slot-usage-example.yaml
```

![img](https://yuml.me/diagram/nofunky;dir:TB/class/[NamedThing%7Cid:string;full_name:string%20%3F]%3Crelated_to%200..1-%20[Relationship%7Cduration:integer%20%3F;relationship_type:string%20%3F],[Relationship]%5E-[OrganizationalRelationship%7Crelationship_type:OrganizationalRelationshipType%20%3F;duration(i):integer%20%3F],[Relationship]%5E-[FamilialRelationship%7Crelationship_type:FamilialRelationshipType%20%3F;duration(i):integer%20%3F],[Organization%7Cid(i):string;full_name(i):string%20%3F]%3Crelated_to%201..1-%20[OrganizationalRelationship],[Person%7Cid(i):string;full_name(i):string%20%3F]++-%20has_organizational_relationships%200..*%3E[OrganizationalRelationship],[FamilialRelationship]%3Chas_familial_relationships%200..*-++[Person],[FamilialRelationship]-%20related_to%201..1%3E[Person],[Container]++-%20persons%200..*%3E[Person],[NamedThing]%5E-[Person],[OrganizationalRelationship]-%20related_to%201..1%3E[Organization],[Container]++-%20organizations%200..*%3E[Organization],[NamedThing]%5E-[Organization],[Relationship]-%20related_to%200..1%3E[NamedThing],[NamedThing]%5E-[Person],[NamedThing]%5E-[Organization],[Person]++-%20has_familial_relationships%200..*%3E[FamilialRelationship],[Container])


Here we have a fairly generic class `Relationship` that holds a relationship a person can hold to another entity such as another person or an organization.

there are two subclasses, or for personal relationships (e.g. siblings) and other for person-to-organization relationships. these use the same generic slots (duration, relationship)type, and related_to). However, the latter two are constrained in a class-specific way.

data.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Superman
    has_organizational_relationships:
      - related_to: ROR:1
        relationship_type: MEMBER_OF
  - id: ORCID:3000
    full_name: Jor El
    has_familial_relationships:
      - related_to: ORCID:1234
        relationship_type: PARENT_OF
organizations:
  - id: ROR:1
    full_name: Justice League
```    

```bash
linkml-validate data.yaml -s slot-usage-example.yaml
```

...
