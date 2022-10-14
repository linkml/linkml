# Slot: startedAtTime

URI: [prov:startedAtTime](http://www.w3.org/ns/prov#startedAtTime)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Event](Event.md) | None
[Relationship](Relationship.md) | None
[Activity](Activity.md) | a provence-generating activity
[FamilialRelationship](FamilialRelationship.md) | None
[BirthEvent](BirthEvent.md) | None
[EmploymentEvent](EmploymentEvent.md) | None
[MedicalEvent](MedicalEvent.md) | None
[MarriageEvent](MarriageEvent.md) | None






## Properties

* Range: [xsd:date](http://www.w3.org/2001/XMLSchema#date)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/tests/core




## LinkML Source

<details>
```yaml
name: started at time
from_schema: https://w3id.org/linkml/tests/core
rank: 1000
slot_uri: prov:startedAtTime
alias: started_at_time
domain_of:
- Event
- Relationship
- activity
range: date

```
</details>