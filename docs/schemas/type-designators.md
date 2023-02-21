# Type designators

You can assign a slot in your schema "type designator" status
by setting [designates_type](https://w3id.org/linkml/designates_type) to `true`.

This means that the slot can be used to designate the type of an instance.

For example, in the following schema, the `type` slot is a type designator for the `Organization` class:

```yaml
classes:
  Organization:
    attributes:
      name:
      type:
        designates_type: true
        range: string
  Business:
    is_a: Organization
  EducationalOrganization:
    is_a: Organization
   ...
```

This means that if the `type` slot is present in data for an instance of a class
Organization, then the value of the `type` slot MUST be either "Organization" or any
of the transitive subclasses (by following `is_a` or `mixins`).

Additionally, if the instance instantiates a more specific class of Organization,
this must be consistent with the value of the `type` slot. The value of the type slot
must be in the set of reflexive descendants or ancestors of the instantiated class.

The type designator can also be used to *infer* the instantiated class.
For example, an instance `i` that instantiated `Organization` in the above schema
with a type value of `Business` would be inferred to be an instance of `Business`.

Type designators can also be assigned to multivalued slots. In this case the same
rules apply for each value of the slot. When performing inference, the most
specific class is chosen.

In the above example, the range of the type designator is `string`.
It could also be `uri`, `curie`, or `uriorcurie`, in which case
it should match value of the class_uri field normalized to the appropriate form.

