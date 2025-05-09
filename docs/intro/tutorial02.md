# Part 2: Adding a container object

In part 1 of this tutorial we created a schema for describing a person,
and showed how we could use this to validate YAML or JSON files with a
single person instance.
In this tutorial we address collections and hierarchy.

In practice our data will typically contain multiple instances, for example we might want to describe a *list* of persons (people).
How do we express that? We need a way to group the instances together.
For this purpose, we can define a class with a multivalued slot and use `range` to specify the type of the object we want to collect.

More complex data are also often hierarchical.
In order to express hierarchies, multivalued slots alone are not enough.
We also need a way to mark which class is the root of our hierarchy.
In LinkML, the `tree_root` slot is used to designate a class as the root of a tree structure.
Only one class in a schema can be set as root.
If more than one class is marked as `tree_root`, a validation error will occur.

Marking one class to serve as the root of the tree (as "container" of the other classes) is especially important when serializing and deserializing data.
The class marked as `tree_root` will be the top-level object in the serialized data.

## Example data file

Let's start with a simple data file that contains more than one instance of person. We choose to structure this as a YAML/JSON dictionary, with an **index slot** called `persons`:

data.yaml:

```{literalinclude} ../../examples/tutorial/tutorial02/data.yaml
:language: yaml
```

In [Working with Data](../data/csvs) we will learn how to express such data in TSV format.

## Nesting lists of objects

We can describe this data using the following schema.

personinfo.yaml:

```{literalinclude} ../../examples/tutorial/tutorial02/personinfo.yaml
:language: yaml
```

We introduce a class called `Container`.
This doesn't necessarily reflect a "real world" entity in our domain, it's just a convenient holder for our data.
Right now the container has only a single attribute/slot called "persons" because it just need to holding instances of `Person`.
But it could hold other kinds of data, too.

The `Container` class has three crucial characteristics:

- it is *multivalued* - i.e. it holds a list
- it is *inlined* - i.e. the values are nested underneath the container
- the *range* is Person - i.e. the expected values in the data are persons (people)

Moreover, the `Container` class is also marked as root class of our model.
In this simple schema setting `tree_root` is not strictly necessary.
LinkML is able to infer that the class `Container` is the root class because it is not referenced as a range in any other class.
However, it is good practice to nevertheless mark the root class explicitly.

Later on we will explore these in more detail.

## Validating

We can validate this to make sure we got it right:

```bash
linkml-validate -s personinfo.yaml data.yaml
```

This should report no errors.

## Visualizing

We can use yUML to visualize the schema. The `gen-yuml` command can generate REST URLs.

```bash
gen-yuml -f yuml personinfo.yaml
```

Outputs:

```text
https://yuml.me/diagram/nofunky;dir:TB/class/[Container]++- persons 0..*>[Person|id:string %3F;full_name:string %3F;aliases:string %3F;phone:string %3F;age:string %3F],[Container]
```

Requesting the URL gives the schema as svg image:

![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Container]++-%20persons%200..*>[Person|id:string%20%3F;full_name:string%20%3F;aliases:string%20%3F;phone:string%20%3F;age:string%20%3F],[Container])

We can alternatively let yUML generate the visualization in png, jpg or pdf format.
In this case a download directory must be passed to  the command.
To get the visualization as file `personinfo.png` downloaded to the current directory run

```bash
gen-yuml -f png -d . personinfo.yaml
```

Besides yUML, linkML supports visualizations with [Mermaid](#../generators/erdiagram) (`gen-erdiagram`) and [plantuml](https://plantuml.com/) (`gen-plantuml`).

## Exercises

1. Extend the container object to include dataset-level metadata:
   - `description` of the dataset
   - `name` of the dataset
2. Modify the schema to allow multiple aliases
3. Modify the test dataset to include multiple aliases for Clark Kent: "Superman" and "Man of Steel"
4. Validate the data

## Further reading

- Metamodel Specification
  - [tree_root](https://w3id.org/linkml/tree_root) slot
  - [multivalued](https://w3id.org/linkml/multivalued) slot
  - [inlined_as_list](https://w3id.org/linkml/inlined_as_list) slot
  - [range](https://w3id.org/linkml/range) slot

## Next

Next we will explore how to add constraints to the schema.
