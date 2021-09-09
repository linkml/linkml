# FAQ: Modeling

## What is the difference between is_a and mixins?

LinkML allows any class to have:

 - zero or one *is_a* parents, declared using the [is_a](https://w3id.org/linkml/is_a) slot
 - any number of *mixin* parents, declared using the [mixins](https://w3id.org/linkml/mixins) slot

Semantically these are the same - all inheritable slots are inherited through is_a and mixins.

Classes *should* have a single inheritance backbone, with `is_a`
representing the "main" parent. Generally the mixin and is_a
hierarchies should be stratified.

See these wikipedia pages for more information.

 - [mixins](https://en.wikipedia.org/wiki/Mixin)
 - [traits](https://en.wikipedia.org/wiki/Trait_(computer_programming))

## Didn't you know composition is favored over inheritance these days?

Wikipedia [composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance)

We have certainly seen cases where inheritance is abused in programming languages, especially when it comes to behavioral classes.

However, in our experience inheritance is still very useful when used for data classes. We trust the users of LinkML to create schemas to design schemas carefully.

## When should I use attributes vs slots?

The [attributes](https://w3id.org/linkml/attributes) metamodel slot is really just a convenient shorthand for being able to declare slots "inline".

LinkML treats slots as first class entities. They are defined in their own section of a schema, and can be reused by any number of classes (and refined, using slot_usage). This can be bery powerful for reuse.

However, this can also be slightly inconvenient for simple schemas, especially those where we have classes with slots that are completely "owned" by that class. The attribute slot can be used to avoid having to specify the slot separately

## What are induced slots?

Because the same slot can be reused in different classes (with each class potentially refining semantics using slot_usage), it can be useful to give a new "name" for the implicit class-specific version of that slot.

For example, if you have a slot `name`, and this is used in classes `Person` and `Organization`, and these are refined for each class (for example, "Organization" may refine the name slot to follow a particular regular expression). In some generators such as the markdown generator, you will see "induced" slots such as `Organization_name`.

The extent to which these are made visible is currently the subject of some discussion, see GitHub for details.

## Why would I need to define my own types?

Types are scalar values such as integers or strings. They are also known as "literals" in RDF.

Strictly speaking it is not necessary to define your own types, you can just use the builtin types.

However, defining your own types can be good practice, as it can make
your intent clearer. For example, if you have a slot `description` you
may want to specify the range as your own type `NarrativeText` that
maps to string behind the scenes. But this provides additional cues,
e.g. that the value of this field is intended to be human-readable
text.

Some applications may choose to interpret this in particular ways. E.g. you may want to define all narrative text fields as being amenable to spellchecking, or machine learning natual language processing, or special kinds of indexing in ElasticSearch/Solr

## Why would I want to use enums over strings?

Enums provide a more controlled vocabulary than strings. You can validate categorical fields using enums, whereas with basic strings you don't have a built in way of validating if a string is valid.

Enums also give you hooks into ontologies and vocabulaies.

More on enums:

<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vQyQsRIBjSxhaDie5ASDAOTfJO9JqFjYmdoBHgCVVKMHzKo0AyL04lGNqWdgbCnyV8a-syk1U81tRXg/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
