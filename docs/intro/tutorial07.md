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

```{literalinclude} ../../examples/tutorial/tutorial07/personinfo.yaml
:language: yaml
```

The JSON-Schema that is generated should be the same as in the previous example:

```bash
gen-json-schema personinfo.yaml
```

You can visualize the schema using `gen-erdiagram` or `gen-doc`.

See {ref}`FAQ: attributes vs slots <faq/modeling:when should i use attributes vs slots?>`


## Inheritance

Now let's say we want to extend the schema, and we want to include
another class `Organization`. Organizations may have different
properties from people, but they may also share slots in common - for
example, having a unique identifier and a name

LinkML provides mechanisms for *inheritance/polymorphism*, we can define a "superclass" called `NamedThing`, put shared slots in there, and *inherit* from it.

We also introduce a concept called "mixins" here, which allows for multiple inheritance:

personinfo-with-inheritance.yaml:

```{literalinclude} ../../examples/tutorial/tutorial07/personinfo-with-inheritance.yaml
:language: yaml
```

Note that our container object now contains two kinds of lists: people and organization

You can visualize this schema using `gen-erdiagram personinfo-with-inheritance.yaml`.

Let's take a look at the JSON schema:

```bash
gen-json-schema personinfo-with-inheritance.yaml > personinfo-with-inheritance.schema.json
```

You can see that even though JSON-Schema doesn't support inheritance, slots from is-a parents and mixins are "rolled down" to their children:


```json
{
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
}
```



## Customizing slots in the context of classes: Slot Usage

LinkML gives you the ability to reuse or inherit slots while customizing them for use in a particular class, using `slot_usage`

First let's create a schema where we introduce a new general class `Relationship`

slot-usage-example.yaml:

```{literalinclude} ../../examples/tutorial/tutorial07/slot-usage-example.yaml
:language: yaml
```

You can visualize this schema using

```bash
gen-erdiagram slot-usage-example.yaml
```

Here we have a fairly generic class `Relationship` that holds a relationship a person can hold to another entity such as another person or an organization.

there are two subclasses, or for personal relationships (e.g. siblings) and other for person-to-organization relationships. these use the same generic slots (duration, relationship)type, and related_to). However, the latter two are constrained in a class-specific way.

data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial07/slot-usage-data.yaml
:language: yaml
```

```bash
linkml-validate data.yaml -s slot-usage-example.yaml
```

...
