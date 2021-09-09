# Python

## Dataclasses

Python dataclasses can be generated from any LinkML model (see [generators/python](../generators/python)).

For example, for the personinfo schema, a Person dataclass is created:

```python
@dataclass
class Person(NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Person
    class_class_curie: ClassVar[str] = "schema:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person

    id: Union[str, PersonId] = None
    primary_email: Optional[str] = None
    birth_date: Optional[str] = None
    age_in_years: Optional[int] = None
    gender: Optional[str] = None
    current_address: Optional[Union[dict, "Address"]] = None
    has_employment_history: Optional[Union[Union[dict, "EmploymentEvent"], List[Union[dict, "EmploymentEvent"]]]] = empty_list()
    has_familial_relationships: Optional[Union[Union[dict, "FamilialRelationship"], List[Union[dict, "FamilialRelationship"]]]] = empty_list()
    has_medical_history: Optional[Union[Union[dict, "MedicalEvent"], List[Union[dict, "MedicalEvent"]]]] = empty_list()
    aliases: Optional[Union[str, List[str]]] = empty_list()
```

## Use in programs

This can be used for programmatic manipulation, e.g:

```python
>>> from personinfo import Person
>>> p1 = Person('P1', name='joe schmoe')
```

## Loaders and dumpers

The linkml_runtime framework is included by default, allowing for dynamic conversion to and from other formats:

```python
>>> from linkml_runtime.dumpers import json_dumper
>>> print(json_dumper.dumps(p1))
{
  "id": "P1",
  "name": "joe schmoe",
  "@type": "Person"
}
```
