# Inlining objects

In JSON/YAML, if one object is referenced by another, a decision is
made as to whether that object should be *inlined*, i.e. nested inside
of, or whether they should be referenced by key.

## Example

For example, given a model with a Person class that can reference other Person classes:

```yaml
classes:
  Person:
    attributes:
      id:
        identifier: true
      name:
      friend_of:
        range: Person
        multivalued: true
```

### No inlining, reference by key

```yaml
id: person001
name: Clark Kent
friend_of:
  - person002
  - person003
```

### Inlining as a list:

```yaml
id: person001
friend_of:
  - i
  - person003
```

 * All 
