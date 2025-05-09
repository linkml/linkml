# Python

## Dataclasses

Python dataclasses can be generated from any LinkML model (see [generators/python](/generators/python)).

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

You can also use the [pydantic generator](../generators/pydantic) for a different style of data classes.

The generated python classes have additional functionality to help with serializing/deserializing.

## Use in programs

This can be used for programmatic manipulation, e.g:

```python
>>> from personinfo import Person
>>> p1 = Person('P1', name='joe schmoe')
```

## Loaders and dumpers

The [linkml-runtime](https://github.com/linkml/linkml-runtime) framework is included by default, allowing for dynamic conversion to and from other formats:

The core LinkML formats are:

* json_loader/json_dumper: to export to and from JSON
* yaml_loader/yaml_dumper: to export to and from YAML
* rdflib_loader/rdflib_dumper: to export to and from any rdflib-supported serialization (e.g. .ttl)

We also provide a csv loader/dumper, see [CSVs](csvs) section of the docs

Dumping:

```python
>>> from linkml_runtime.dumpers import json_dumper
>>> from personinfo import Person
>>> p1 = Person('P1', name='joe schmoe')
>>> print(json_dumper.dumps(p1))
{
  "id": "P1",
  "name": "joe schmoe",
  "@type": "Person"
}
```

Loading:

```python
>>> from linkml_runtime.loaders import json_loader
>>> from personinfo import Person
>>> p1 = json_loader.load('person_data.json')
```

For more developer documentations, see the [loaders-and-dumpers](/developers/loaders-and-dumpers) section of the developer docs

