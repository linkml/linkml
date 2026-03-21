# Part 5: Using Python dataclasses

*If you are not a developer, you can skip this section*.

If you are a developer and favor a language other than python, you may
still be interested in this section. The use of generated code is an
optional but convenient part of LinkML. [We are actively adding support
for other languages](https://linkml.io/linkml/faq/general.html#is-linkml-only-for-python-developers).

## Generating a Python datamodel

For illustration, we will take the schema we developed in the last section:

personinfo.yaml:

```{literalinclude} ../../examples/tutorial/tutorial05/personinfo.yaml
:language: yaml
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

```{literalinclude} ../../examples/tutorial/tutorial05/test.py
:language: python
```

run this:

```bash
python test.py
```

Outputs:

```{literalinclude} ../../examples/tutorial/tutorial05/test-output.txt
:language: text
```

Hurray! Perhaps this is not very impressive in itself,
but having an object model that is guaranteed to be in sync with your data model can
help with productivity and robustness of code.

## The LinkML runtime

The LinkML runtime is a separate python library that provides methods needed by your generated datamodel classes, and utilities for converting your python objects into YAML, JSON, RDF, and TSV:

test_runtime.py:

```{literalinclude} ../../examples/tutorial/tutorial05/test_runtime.py
:language: python
```

```bash
python test_runtime.py
```

Outputs:

```{literalinclude} ../../examples/tutorial/tutorial05/test-runtime-output.txt
:language: text
```

## Alternatives

- LinkML also includes a more lightweight Python object model maker for [generating Pydantic datamodels](https://linkml.io/linkml/generators/pydantic.html)
- We also provide a generator for [creating SQL Alchemy models](https://linkml.io/linkml/generators/sqlalchemy.html)
- We are gradually adding support for other languages
   - [java](https://linkml.io/linkml/generators/java.html)
   - [typescript generators](https://linkml.io/linkml/generators/typescript.html) for javascript developers
- For a full list of generators see [generators](https://linkml.io/linkml/generators/index.html)


## Further reading

* Generators:
    - [Python Generator](../generators/python)
* Python [dataclasses](https://docs.python.org/3/library/dataclasses.html)

## Next

Next we will look at the *enumerations* feature of LinkML
