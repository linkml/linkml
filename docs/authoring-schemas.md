# Schemas

A LinkML *Schema* is...

```yaml
id: http://example.org/sample/organization
name: organization

types:
  yearCount:
    base: int
    uri: xsd:int
  string:
    base: str
    uri: xsd:string

classes:

  organization:
    slots:
      - id
      - name
      - has boss

  employee:
    description: A person
    slots:
      - id
      - first name
      - last name
      - aliases
      - age in years
    slot_usage:
      last name:
        required: true

  manager:
    description: An employee who manages others
    is_a: employee
    slots:
      - has employees

slots:
  id:
    description: Unique identifier of a person
    identifier: true

  name:
    description: human readable name
    range: string

  aliases:
    is_a: name
    description: An alternative name
    multivalued: true

  first name:
    is_a: name
    description: The first name of a person

  last name:
    is_a: name
    description: The last name of a person

  age in years:
    description: The age of a person if living or age of death if not
    range: yearCount

  has employees:
    range: employee
    multivalued: true
    inlined: true

  has boss:
    range: manager
    inlined: true
```
