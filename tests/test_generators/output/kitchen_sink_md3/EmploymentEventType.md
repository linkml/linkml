# Enum: EmploymentEventType


_codes for different kinds of employment/HR related events_


URI: [EmploymentEventType](EmploymentEventType)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| HIRE | bizcodes:001 | event for a new employee |
| FIRE | bizcodes:002 |  |
| PROMOTION | bizcodes:003 | promotion event |
| TRANSFER | bizcodes:004 | transfer internally |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/kitchen_sink




## LinkML Source

<details>
```yaml
name: EmploymentEventType
description: codes for different kinds of employment/HR related events
from_schema: https://w3id.org/linkml/tests/kitchen_sink
aliases:
- HR code
rank: 1000
permissible_values:
  HIRE:
    text: HIRE
    description: event for a new employee
    meaning: bizcodes:001
  FIRE:
    text: FIRE
    meaning: bizcodes:002
    annotations:
      biolink:opposite:
        tag: biolink:opposite
        value: HIRE
  PROMOTION:
    text: PROMOTION
    description: promotion event
    meaning: bizcodes:003
  TRANSFER:
    text: TRANSFER
    description: transfer internally
    meaning: bizcodes:004

```
</details>
