
# Slot: apply_to


Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.

URI: [linkml:apply_to](https://w3id.org/linkml/apply_to)


## Domain and Range

[Definition](Definition.md) &#8594;  <sub>0..\*</sub> [Definition](Definition.md)

## Parents


## Children

 *  [class_definition➞apply_to](class_definition_apply_to.md)
 *  [slot_definition➞apply_to](slot_definition_apply_to.md)

## Used by

 * [Definition](Definition.md)
