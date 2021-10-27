
# Slot: all_members


the value of the multiavlued slot is a list where all elements conform to the specified values.
this defines a dynamic class with named slots according to matching constraints

E.g to state that all members of a list are between 1 and 10
```
all_members:
  x:
    range: integer
    minimum_value: 10
    maximum_value: 10
```

URI: [linkml:all_members](https://w3id.org/linkml/all_members)


## Domain and Range

None &#8594;  <sub>0..\*</sub> [SlotDefinition](SlotDefinition.md)

## Parents

 *  is_a: [list_value_specification_constant](list_value_specification_constant.md)

## Children


## Used by

 * [AnonymousSlotExpression](AnonymousSlotExpression.md)
 * [SlotDefinition](SlotDefinition.md)
 * [SlotExpression](SlotExpression.md)
