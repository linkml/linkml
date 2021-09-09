# Metadata

## aliases

The [aliases](https://w3id.org/linkml/aliases) slot can be used to define a list of aliases for a class or slot. This is useful for adding synonymous names to your class (or slot), that serve either as hints for human users, or to enhance search and findability over your model

Example:

```yaml
Person:
  aliases:
    - human being
    - individual
```

## description

The [description](https://w3id.org/linkml/description) slot can be used to provide a human-readable description of any schema element

```yaml
  Person:
    is_a: NamedThing
    description: >-
      A person (alive, dead, undead, or fictional).
```

descriptions can include markdown

```yaml
  Person:
    is_a: NamedThing
    description: :-
      A human being including those that are:
         * alive
         * dead
         * undead
         * fictional
```

However, this is only recommended for schema descriptions.

This [guide to yaml formatting](https://yaml-multiline.info/) may be helpful

## others slots

See [CommonMetadata](https://w3id.org/linkml/CommonMetadata) for other slots






