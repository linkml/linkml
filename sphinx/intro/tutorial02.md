# Part 2: Adding a container object

In part 1 of this tutorial we created a schema for describing people,
and showed how we could use this to validate YAML or JSON files with a
single person instance.

In practice our data files will rarely be at the level of a single instance. Instead we might have a file that contains a *list* of people, or a more complex document that contains a variety of different heterogeneous objects.

## Example data file

Let's start with a simple data file that contains more than one instance of person. We choose to structure this as a YAML/JSON dictionary, with an "index slot" called `persons`:

data.yaml:

```yaml
persons:
  - id: ORCID:1234
    full_name: Clark Kent
    age: 32
    phone: 555-555-5555
  - id: ORCID:4567
    full_name: Lois Lane
    age: 33
```

(later on we will see how to express this same thing as a TSV)

## Nesting lists of objects

We can describe this data using the following schema.

personinfo.yaml:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string
  
classes:
  Person:
    attributes:
      id:
      full_name:
      aliases:
      phone:
      age:
  Container:
    attributes:
      persons:
        multivalued: true
        inlined_as_list: true
        range: Person
```

We introduce a class called `Container`. This doesn't necessarily
reflect a "real world" entity in our domain, it's just a convenient
holder for our data.

Right now it is holding instances of `Person` but it could hold other kinds of data.

The container has a single attribute/slot called "persons". This has 3
crucial characteristics:

 - it is *multivalued* - i.e. it holds a list
 - the *range* is Person - i.e. the expected values in the data should be people
 - it is *inlined* - i.e. the values are nested underneath the container

Later on we will explore these in more detail

## Validating

We can validate this to make sure we got it right:

```bash
linkml-validate -s personinfo.yaml data.yaml 
```

This should report no errors.

## Visualizing

We can use yUML to visualize the schema. The `gen-yuml` command can generate REST URLs that can be fed into

```bash
gen-yuml -f yuml personinfo.yaml 
```

Outputs:

```text
https://yuml.me/diagram/nofunky;dir:TB/class/[Container]++- persons 0..*>[Person|id:string %3F;full_name:string %3F;aliases:string %3F;phone:string %3F;age:string %3F],[Container]
```

Which renders as:

![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Container]++-%20persons%200..*>[Person|id:string%20%3F;full_name:string%20%3F;aliases:string%20%3F;phone:string%20%3F;age:string%20%3F],[Container])

You can also generate a png directly

```bash
gen-yuml -f png personinfo.yaml  > personinfo.png
```

## Exercises

1. Extend the container object to include dataset-level metadata:
   - `description` of the dataset
   - `name` of the dataset
2. Modify the schema to allow multiple aliases
3. Modify the test dataset to include multiple aliases for Clark Kent: "Superman" and "Man of Steel"
4. Validate the data

## Further reading

* Metamodel Specification
   * [multivalued](https://w3id.org/linkml/multivalued) slot
   * [range](https://w3id.org/linkml/range) slot   

## Next

Next we will explore how to add constraints to the schema
