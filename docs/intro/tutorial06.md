# Part 6: Enumerations

Now we will extend our schema with a new slot `status` which records the vital status of a person, i.e whether they are living or dead.

We could do this by making the range of `status` a string, and
allowing the data provider to fill this with any value. However, this
will result in messy data that will need to cleaned up before any analysis is performed, e.g. to harmonize strings such as "alive" and "living"

LinkML allows you to provide *enumerations*, collections of controlled string values. Here is our example schema, with an example enumeration:

personinfo.yaml:

```{literalinclude} ../../examples/tutorial/tutorial06/personinfo.yaml
:language: yaml
```

Now let's collect some data!

data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial06/data.yaml
:language: yaml
```

We can run our data through the linkml validator (which just wraps a jsonschema validator by default)

<!-- FAIL -->
```bash
linkml-validate -s personinfo.yaml data.yaml
```

If you run this you should see that it throws an error with the message:

```text
[ERROR] [data.yaml/0] 'UNDEAD' is not one of ['ALIVE', 'DEAD', 'UNKNOWN'] in /persons/1/status
```

<!-- TODO: use schematools to patch the data -->

Let's go ahead and fix the data, changing Dracula's vital status from UNDEAD to UNKNOWN:

data-fixed.yaml:

```{literalinclude} ../../examples/tutorial/tutorial06/data-fixed.yaml
:language: yaml
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

```{literalinclude} ../../examples/tutorial/tutorial06/personinfo-mapped.yaml
:language: yaml
```


```bash
linkml-convert -s personinfo-mapped.yaml data-fixed.yaml
```

Outputs:

```{literalinclude} ../../examples/tutorial/tutorial06/data-fixed.json
:language: json
```

<!-- TODO: RDF docs -->

## Use in Python

(you can skip this section if you are not concerned with interacting with data instances via Python)

```bash
gen-python personinfo-mapped.yaml > personinfo.py
```

then use this code:

test.py:

```{literalinclude} ../../examples/tutorial/tutorial06/test.py
:language: python
```

```bash
python test.py
```

Outputs:

```{literalinclude} ../../examples/tutorial/tutorial06/test-output.txt
:language: text
```

Next we will explore more aspects of the modeling language

## Further reading

* {ref}`LinkML Schemas: Enums <schemas/models:enums>`
* Metamodel Specification
    * [Enum Definition](https://w3id.org/linkml/EnumDefinition) class
* FAQ:
    - {ref}`Enums vs strings <faq/modeling:why would i want to use enums over strings?>`
