# LinkML specification

## Introduction

This document specifies the LinkML language. LinkML is a modeling language that allows the construction of a *model* (aka schema) which specifies a set of constraints over a object *graph*. 

A LinkML model is typically expressed as a YAML structure, and instance trees are also typically specified as JSON or YAML structures. However, the specification is independent of any particular serialization.

## LinkML Models

A LinkML **model** `M` consists of the following model elements/definitions:

 * classes `MC = {c1,...}`, which group *objects*
 * class references `MR = {r1,...}`, which group *pointers to objects*
 * slots `MS = {s1, ...}`, which describe how objects relate to other objects
 * enums `ME = {e1, ...}`, enumerated values (value sets)
 * types `MT = {t1, ...}`, scalar/atomic types, such as integers, strings
 * subsets `MP = {p1, ..}`, which partition model elements into groupings or views

_Note_: class references are not declared directly, but are induced (see below)

|Example Model: Organization Schema|
|---|
|Classes: *Person*, *Organization*, *Address*, ...|
|Slots: *id*, *name*, *date_of_birth*, *employed_at*, *lives_at*, ...|
|Enums: *JobCode*, ...|
|Types: *Date*, *String*, ...|

To help understand the basic concepts, it can be helpful to think about analogous structures in other frameworks. However, it should be understood these are not equivalents.

 * Classes are analogous to classes in object-oriented languages, tables in relational databases and spreadsheets, and classes in RDFS/OWL
 * Slots are analogous to attributes in object oriented languages, columns or fields in relational databases and spreadsheets, and properties in RDFS/OWL
 * Enums are analogous to enums in programming languages and some relational systems. However, in LinkML enums are optionally backed by stronger semantics with enum elements mapped to vocabularies or ontologies
 * Types are analogous to builtin types in most OO languages and database systems, or extensible types in some systems. They correspond to literals in RDF/OWL

## LinkML Objects


A LinkML **object** `o` ranges over a *Domain of Discourse* `O`, i.e. `o ∈ O`. Each object *directly instantiates* exactly one of the following:

 * A class in `MC`
 * A class reference in `MR`
 * A scalar type (literal) in `MT`
 * An enum in `ME`
 * The distinguished value `None`, indicating a lack of a value

The function `instantiates` maps each object to exactly one model element, i.e `instantiates(o) ∈ MC ∪ MR ∪ MT ∪ ME`

_Note_: in LinkML, everything is an object. The string `"foo"` is an instance of a string type. The LinkML concept of an object maps to the term "element" in the [JSON spec](https://www.json.org/json-en.html). Here we use the term *compound object* to denote an object that instantiates a class.

Each `o ∈ O` has a list of slot-value *assignments* `A(o)`, where each assignment is a pair `s, V`, with the following constraints.

 * `s ∈ MS`, i.e. `s` is a slot declared in the model
 * `V` is either a list of objects `v1, ..., vn` (each of which can be any LinkML object) for any non-negative integer n, or a singular object `v`, or the atom `None`.

Formally, `A(o) ⊆ MS x O ∪ P(O)`, where `P` denotes the set of all possible lists formed from elements of `O`.

Here we use dot notation to indicate assignments, e.g. `o.s` indicates the value or values of slot `s` in object `o`

|Example Object Graph: Organization Schema|
|---|
|Objects: *Jane* instantiates *Person*, *Acme* instantiates *Organization*, *JanesAddress* instantiates *Address* ...|
|*Jane*`.name` = "Jane Li" (instance of *String* type) |
|*Jane*`.employed_at` = IdentifierOf(Acme) (instance of *Object Reference* type) |
|*Jane*`.lives_at` = [*JanesAddress*] (list of instances of *Class* type) |

"IdentifierOf" -- in Python constructed from ClassName[classid] (e.g. If "Person" has the identifier "Foo", Ref is "PersonFoo")

An *object tree* is a collection of objects organized in a tree structure such that each object is a node in the tree, and each assignment forms a child edge, where the edge is labeled with the slot. The tree is a strict hierarchy and has a single root.

A *resolved object graph* is an object graph in which every (resolvable) instance of a reference in `MR` is replaced by the corresponding instance of a class in `MC`. For example, in the example above, the node for *Acme* and *Ref(Acme)* would be merged. Unlike the native object graph this need not form a tree structure.


## LinkML Metamodel

Every LinkML Model is itself an object, instantiating the [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition) class in the LinkML *metamodel*. The object tree rooted in the model is formed of objects that instantiate metamodel classes.

Each of these model objects, including the model itself, can have a set of slot-value assignments, where the slots are drawn from the LinkML metamodel.

The complete LinkML metamodel is spelled out in the metamodel documentation; see [SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)

We introduce here key metamodel components necessary for understanding structural constraints:

 * Each class `c` has a collection of slots, `c.slots`, which are the slots that are applicable to that class.
 * Each slot `s` has a *range* indicated `s.range`, which identifies the set of valid assignments for a slot.
 * Slots may have other assignments for indicating cardinality, value constraints, etc
 * Each enum `o` has a collection of permissible values `o.permissible_values`, each corresponding to a controlled term.

|Example Model: Organization Schema|
|---|
|*Person*.slots = [id, name, data_of_birth, employed_at, resides_in, ...]|
|*Organization*.slots = [id, name, ...]|
|*name*.range = *String*|
|*employed_at*.range = *Organization*|
|*resides_in*.range = *States*
|*states.permissible_values* = "AK", "AL", "AR", "AZ", ...
|...|

## Induced Models

Instance graphs are validated against *induced models*. An induced model is derived from an *asserted model*. We describe this process in terms of copy operations but it is up to individual implementations how to handle this - the induced model could be a virtual view over the asserted model.

First the asserted model is copied to create the induced model seed, then the following rules are applied. The rules are applied recursively, in any order. Then post-processing steps are applied.



### Rule: Model Import Copying

Each model imports zero to many imports, indicated by the [imports](https://w3id.org/linkml/imports) metaslot on the model.

When calculating the induced model, all elements from the imported model are copied to the importing model. this is applied recursively, such that if `m1` imports `m2`, and `m2` imports `m3`, all elements of `m3` will be copied to `m1`.

**Note**: If two or more models import the same target (e.g. `m1` imports `m2` and `m3` and `m2` imports `m3`), `m3` will be only be resolved once.  

**Note**: Two models are considered to be "identical" if they both 
have the same `id`.  If `m2` and `m3` both have `id: http://models-r.us/modelA`, it is assumed that, despite the different location, they represent the same thing.  LinkML _will_ check the model `version` field and will raise an error if `m2` has `version: 1.0.0` and `m3` has `version: 1.0.1`


### Rule: Induced Class-Slots

Each class `c` can have zero to many slots declared using the `slots` metaslot.

If a slot `s` is used in a class `c` via `slots` declarations on that class, then an induced slot `c!s` is created.

When an induced slot `c!s` is created, then all metaslots from `c` are copied to `c!s`.

A class `c` can declare any number of [slot_usage](https://w3id.org/linkml/slot_usage)s, which will allow assignment of metaslots in `c!s`. All metaslots from the slot_usage object is copied to the induced slot.


### Rule: Inheritance

Each class has zero or one *is_a* parent, and zero to many *mixin* parents.

`Parents(c) = { c.is_a } ∪ c.mixins `

All metaslots of the parent are copied to the child, if the metaslot is declared inheritable. 

This is applied recursively, such that a class inherits all slots of its ancestors

For example, if the model contains class *Person* such that *Person.slots = [name,  ]*, and Employee isa Person,  then Employee will have also that slot. 

|Asserted Model|Induced Model|
|---|---|
|`Employee.is_a=Person` <br/> `Person.slots = [name, ...]` <br/> `Employee.slots = [employed_by]` | `Employee.slots = [employed_by, name, ...]` |
|...|...|

the same applies to slots. heritable metaslots are copied from parent slots.

__semantics of copying from parents__:

If a metaslot `s` is declared `multivalued` then when copying `s` from a parent to a child, the values are appended.

If a metaslot `s` is declared `multivalued` 

if a slot is multi valued then copying will append, unless the element already exists.

if the slot is single valued, and intersection rules can be applied to the slot, then these are performed on all values

if the slot is single valued, and intersection rules cannot be applied to the slot, then the following precedence rules are applied:

 * metaslot values from slot_usage take the highest priority
 * metaslot values from the slot definition take the next highest priority
 * direct mixins take the next highest priority. where multiple direct mixins are provided as a list, the last element takes highest priority
 * direct is_as take the next highest priority
 * the above two rules are applied one level up, and then recursively applied

Intersection rules

|metaslot|rule|
|---|---|
|`maximum_value`|`min(v1,v2)`|
|`minimum_value`|`max(v1,v2)`|
|`pattern`|TBD|
|`range`|`IF subsumes(v1,v2) then v2` <br/> `ELSE IF subsumes(v2,v1) then v2 ELSE UNDEFINED` |

If the result of applying any intersection rule is UNDEFINED then we fall back on precedence rules

## Structural conformance of object trees

Any object `o` can be evaluated for structural conformance to an induced model `M`

 * For each `o ∈ O`, where `o` directly instantiates `C`:
    * For each `s,V ∈ A(o)`:
        * Let `c!s` be the class slot of `s` for class `C`
        * Perform structural checks on `c!s` for `V`


### Multivalued check

 * if `c!s.multivalued` is True, then `V` must be a list
 * If `c!s.multivalued` is False, then `V` must be a single value

### Minimum and Maximum Values checks

 * if `c!s.maximum_value` is assigned, then `V` must be a singular integer and must be less that or equal to the maximum value
 * if `c!s.minimum_value` is assigned, then `V` must be a singular integer and must be greater that or equal to the minimum value


### Range checks

Depending on the range of `c!s` a particular check is applied on each `c ∈ V` (if V is multivalued) or `v=V`

|condition|check|
|---|---|
|`c!s.range ∈ MC`|class instantiation check|
|`c!s.range ∈ MT`|type check|
|`c!s.range ∈ ME`|enum check|



#### Range class instantiation check

if `s.range ∈ MC`: `v` must be either:
 * an object that instantiates a class `c ∈ DESC*(s.range)`
 * a reference to an object that instantiates a class `c ∈ DESC*(s.range)`

Here `DESC*` is the reflexive closure of the `child` function, where `child(p) = { c : c.is_a = p or p ∈  c.mixins }`

Additional checks MAY be performed based on whether `s.inlined` is True

 * if `s.inlined`, then `v` SHOULD NOT be a Reference
 * if `s.inlined` is False, then EITHER:
     * `v` SHOULD be a Reference
     * OR `v` instantiates a class `R` such that R has no slot `rs` that is declared to be an identifier. i.e. `rs.identifier = True`

#### Range type check

if `s.range ∈ MT`: `v` must be a literal of type `MT`

#### Range enum check

if `s.range ∈ MO`: `v` must be a member of the permissible value in `MO`

TODO: other enum types

### abstract classes and slots

a class instance SHOULD not instantiate a class that is declared abstract. 

an assignment s,V SHOULD not have s declared abstract. 

### Required value checks

 * For each `o ∈ O`, where `o` directly instantiates `C`:
    * For each `s ∈ C.slots`:
        * If `s.required` is True, then there MUST exist a value `o.s`
        * If `s.recommended` is True, then there SHOULD exist a value `o.s`

### Constraints on instantiation of classes

* For each `o ∈ O`, where `o` directly instantiates `C`:
   * `c.abstract` MUST be false
   * `c.mixin` SHOULD be false

Note in future versions we may introduce model level metaslots that allow these to be relaxred

## constraints on models
 
### stratification of isa and mixin hierarchies

is_a and mixin hierarchies SHOULD be stratified:

 * if `c.mixin = True` then all parents p of c SHOULD have `p.mixin = True`
 * if `c.mixin = False` and c.is_a is provided, then `c.is_a.mixin` SHOULD be set to True
 * for all p in `c.mixins`, p.mixin SHOULD be set to True




## Glossary of terms (Information)

 * assignment
 * class
 * class slot
 * element (of schema):
 * enum
 * inheritance
 * is_a
 * model (aka schema)
 * mixin
 * object (aka *instance*):
 * range
 * required
 * slot
 * type (aka scalar value, literal, atom): 

