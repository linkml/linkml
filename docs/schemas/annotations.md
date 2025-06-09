# Annotations

## Background

The LinkML model provides a fixed set of metamodel slots which can be applied to any schema element.

Examples of these are:

* [description](https://w3id.org/linkml/description) - a human readable description of the element
* [comments](https://w3id.org/linkml/comments) - a human readable comment about the element
* [aliases](https://w3id.org/linkml/aliases) - a set of alternative names for the element
* [deprecated](https://w3id.org/linkml/deprecated) - a boolean flag indicating that the element is deprecated
* [seeAlso](https://w3id.org/linkml/seeAlso) - a set of URIs that provide additional information about the element

If you attempt to assign a slot that is not in the metamodel, you will get an error. For example,
if you wanted to add a `review` slot to the `Person` class like this:

```yaml
classes:
  Person:
    description: A person, living or dead
    review: A very useful class that is well defined
    attributes:
      id: ...
```

This will result in an error, because `review` is not a metamodel slot.

This conformance to a single metamodel can be useful for ensuring consistency and interoperability
among LinkML schemas. However, it can be too constraining in some cases. To get around this,
the LinkML metamodel has a generic [annotations](https://w3id.org/linkml/annotations) slot that can be used
to assign arbitrary tags and values to any schema element.

## Adding your own annotations

In the above case, we can add the `review` annotation to the `Person` class like this:

```yaml
classes:
  Person:
    annotations:
      review: A very useful class that is well defined
      ...
```

Note that in the underlying metamodel, the range of [annotations](https://w3id.org/linkml/annotations) is
an [Annotation](https://w3id.org/linkml/Annotation) class, which has two slots: `tag` and `value`. This is
usually written in *compact form* as `tag: value`, as in the above.

Note also that prior to LinkML 1.6, the range of the annotation value was `string`, but in 1.6 and higher,
the range can be any object.

## Annotation validation

By default, all annotation tags and values are valid. Feel free to add whatever annotations you like
to any schema element - classes, enums, permissible values, slots, even schemas themselves.

However, if you want to restrict the set of valid annotations, you can do this starting from LinkMK 1.6,
where you can treat annotation tags as if they were slots in your own metamodel extension.

This is done by adding an [instantiates](https://w3id.org/linkml/instantiates) slot-value assignment onto any schema element. The range of
the `instantiates` slot is a `uriorcurie` that references a class that serves as a metamodel extension class.

For example, given our example schema fragment, we can add an `instantiates` slot to the `Person` class,
stating that this class is an instance of the `Reviewable` metamodel extension class:

```yaml
classes:
  Person:
    instantiates:
      - mymetamodel:Reviewable
    annotations:
      review: A very useful class that is well defined
      ...
```

This metaclass extension can live in the same schema, or in a different schema. This is why they are referenced
by `uriorcurie` rather than a local name.

The `Reviewable` class might be defined as follows:

```yaml
id: https://example.org/mymetamodel/
name: mymetamodel
...
classes:
  Reviewable:
    class_uri: mymetamodel:Reviewable
    attributes:
      review:
        description: an expert review of a schema element
        range: string
```

This can be thought of as a schema element mixin class - the class defines the extra slots that can be
attached to schema elements via annotations.

Other schema elements can also instantiate the `Reviewable` class:

```yaml
classes:
  Person:
    instantiates:
      - mymetamodel:Reviewable
    annotations:
      review: A very useful class that is well defined
      ...
    attributes:
      name:
        description: the name of a person
        instantiates: mymetamodel:Reviewable
        annotations:
          review: A very useful attribute that is well defined
          ...
```

Note that here the `attributes` section of the `Person` definition is the attributes that an
instance of `Person` may have. The `annotations` section pertains to the *class* Person, not instances.

## Validation of annotations

If a schema element does not instantiate a metamodel extension class, then any annotation tag is valid.
(this is already the case for all pre 1.6 schemas, since the `instantiates` slot is not defined in previous
versions of the metamodel).

If a schema element does instantiate a metamodel extension class, then the set of valid annotation tags
should conform to the slots defined in the metamodel extension class, as if the annotation tags were
first-class slots, and instantiates value was a mixin.

However, this is not yet supported in the current LinkML validator, so using `instantiates` indicates your
intent, but does not yet enforce validation.

## Other uses of instantiates

The `instantiates` slot can also be used constrain rather than extend.

For example, to define a *strict* metamodel element that must have a description:

```yaml
id: https://example.org/mymetamodel/
name: mymetamodel
...
classes:
  StrictElement:
    class_uri: mymetamodel:StrictClassDefinition
    slot_usage:
      description:
        required: true
```

Any schema element that instantiates `StrictElement` must have a description:

```yaml
classes:
  Person:
    instantiates:
      - mymetamodel:StrictElement
    description: A person, living or dead   ## must be provided
```
