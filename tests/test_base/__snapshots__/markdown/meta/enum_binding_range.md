
# Slot: range

defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2

URI: [linkml:enum_binding_range](https://w3id.org/linkml/enum_binding_range)


## Domain and Range

[EnumBinding](EnumBinding.md) &#8594;  <sub>0..1</sub> [EnumDefinition](EnumDefinition.md)

## Parents

 *  is_a: [range](range.md)

## Children


## Used by

 * [EnumBinding](EnumBinding.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | value domain |
| **Comments:** | | range is underspecified, as not all elements can appear as the range of a slot. |
| **In Subsets:** | | SpecificationSubset |
|  | | MinimalSubset |
|  | | BasicSubset |
|  | | RelationalModelProfile |
|  | | ObjectOrientedProfile |