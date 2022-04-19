# Part 5: Using Python dataclasses

If you are not a developer, you can skip this section.

If you are a developer and favor a language other than python, you may
still be interested in this section. The use of generated code is an
optional but convenient part of LinkML. We are actively adding support
for other languages.

## Generating a Python datamodel

For illustration, we will take the schema we developed in the last section:

personinfo.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:                                  ## Note are adding 3 new ones here
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
  personinfo: https://w3id.org/linkml/examples/personinfo/
  ORCID: https://orcid.org/
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    class_uri: schema:Person              ## reuse schema.org vocabulary
    attributes:
      id:
        identifier: true
      full_name:
        required: true
        description:
          name of the person
        slot_uri: schema:name             ## reuse schema.org vocabulary
      aliases:
        multivalued: true
        description:
          other names for the person
      phone:
        pattern: "^[\\d\\(\\)\\-]+$"
        slot_uri: schema:telephone       ## reuse schema.org vocabulary
      age:
        range: integer
        minimum_value: 0
        maximum_value: 200
    id_prefixes:
      - ORCID
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
```

We can use a script that is distributed with LinkML to generate a python dataclasses model:

```bash
gen-python personinfo.yaml > personinfo.py
```

This creates a python datamodel:

```python
@dataclass
class Person(NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    id: Union[str, PersonId] = None
    full_name: Optional[str] = None
    ...
```


Note you don't need to directly view the python - but your favorite IDE should be able to autocomplete and type check as expected


You can now write code like:

test.py:

```python
from personinfo import Person

p1 = Person(id='ORCID:9876', full_name='Lex Luthor')
print(p1)
```

run this:

```bash
python test.py
```

Outputs:

```text
Person(id='ORCID:9876', full_name='Lex Luthor', aliases=[], phone=None, age=None)
```

This is not very impressive in itself, but as your models get larger it can be very handy to have a python data model

## LinkML runtime

The LinkML runtime is a separate python library that provides methods needed by your generated datamodel classes, and utilities for converting your python objects into YAML, JSON, RDF, and TSV:

test_runtime.py:

```python
from linkml_runtime.dumpers import json_dumper

from personinfo import Person

p1 = Person(id='ORCID:9876', full_name='Lex Luthor', aliases=["Bad Guy"])

print(json_dumper.dumps(p1))
```

```bash
python test_runtime.py
```

Outputs:

```text
{
  "id": "ORCID:9876",
  "full_name": "Lex Luthor",
  "aliases": [
    "Bad Guy"
  ],
  "@type": "Person"
}
```

## Alternatives

- LinkML also includes a more lightweight Python object model maker for [generating Pydantic datamodels](https://linkml.io/linkml/generators/pydantic.html)
- We also provide a generator for [creating SQL Alchemy models](https://linkml.io/linkml/generators/sqlalchemy.html)
- We are gradually adding support for other languages
   - [java](https://linkml.io/linkml/generators/java.html)
   - [typescript generators](https://linkml.io/linkml/generators/java.html) for javascript developers
- For a full list of generators see [generators](https://linkml.io/linkml/generators/index.html)


## Further reading

* [linkml-runtime](https://github.com/linkml/linkml-runtime)
    - This repo has the minimal runtime required for a generated dataclasses model to work
* Generators:
    - [Python Generator](../generators/python)
* Python [dataclasses](https://docs.python.org/3/library/dataclasses.html)

## Next

Next we will look at the *enumerations* feature of LinkML

