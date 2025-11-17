# LinkML Documentation Coverage Analysis

## Executive Summary

This analysis compares the metamodel properties available for LinkML schema elements (classes, slots, enums, types) against what is currently documented by the `gen-doc` generator.

### Coverage Overview

| Element Type | Total Properties | Currently Documented | Coverage % | Gap |
|--------------|------------------|---------------------|------------|-----|
| ClassDefinition | 72 | ~25 | ~35% | 47 |
| SlotDefinition | 117 | ~20 | ~17% | 97 |
| EnumDefinition | 65 | ~12 | ~18% | 53 |
| TypeDefinition | 61 | ~10 | ~16% | 51 |

---

## 1. ClassDefinition (72 total properties)

### Currently Documented Properties (~25 properties)

#### Explicitly shown in template:
1. **name** - shown in title
2. **title** - shown in title if present
3. **description** - shown as element description
4. **deprecated** - shown with DEPRECATED flag
5. **abstract** - shown with NOTE about abstract class

#### In "Inheritance" section:
6. **is_a** - shown in inheritance tree
7. **mixins** - shown in inheritance tree

#### In "Slots" table:
8. **slots** - direct slots shown in table
9. **attributes** - shown in table
10. **slot_usage** - implicitly shown through induced slots

#### In "Rules" section (if present):
11. **rules** - shown in Rules section

#### In common_metadata.md.jinja2:
12. **aliases** - shown in Aliases section
13. **examples** - shown in Examples section
14. **comments** - shown in Comments section
15. **todos** - shown in TODOs section
16. **see_also** - shown in See Also section
17. **id_prefixes** - shown in Valid ID Prefixes
18. **annotations** - shown in Annotations table
19. **from_schema** - shown in Schema Source
20. **imported_from** - shown in Schema Source
21. **mappings** - shown in Mappings table
22. **exact_mappings** - shown in Mappings table
23. **close_mappings** - shown in Mappings table
24. **related_mappings** - shown in Mappings table
25. **narrow_mappings** - shown in Mappings table
26. **broad_mappings** - shown in Mappings table

#### In YAML source (everything visible):
All 72 properties shown in YAML dump

### Missing from Main Documentation (47 properties)

#### Core Class Properties:
- **class_uri** - URI for the class
- **subclass_of** - RDF subclass relationships
- **union_of** - union of classes
- **defining_slots** - slots that define this class
- **tree_root** - whether this is a tree root
- **unique_keys** - unique key constraints
- **classification_rules** - classification rules
- **slot_names_unique** - whether slot names must be unique
- **represents_relationship** - whether represents a relationship
- **disjoint_with** - disjoint classes
- **children_are_mutually_disjoint** - whether children are disjoint
- **extra_slots** - extra slots allowed
- **alias** - alias for the class

#### From definition:
- **mixin** - whether this is a mixin
- **apply_to** - what this applies to
- **values_from** - enumeration values source
- **string_serialization** - serialization pattern

#### From element:
- **id_prefixes_are_closed** - whether ID prefixes are closed
- **definition_uri** - definition URI
- **local_names** - local names
- **conforms_to** - what this conforms to
- **implements** - what this implements
- **instantiates** - what this instantiates

#### From class_expression:
- **any_of** - any of these conditions
- **exactly_one_of** - exactly one of these
- **none_of** - none of these
- **all_of** - all of these
- **slot_conditions** - slot-based conditions

#### From extensible:
- **extensions** - tag/value extensions

#### From common_metadata:
- **alt_descriptions** - alternative descriptions
- **notes** - editorial notes
- **in_subset** - subset membership
- **source** - original source
- **in_language** - language code
- **deprecated_element_has_exact_replacement** - exact replacement
- **deprecated_element_has_possible_replacement** - possible replacement
- **structured_aliases** - structured aliases
- **created_by** - creator
- **contributors** - contributors list
- **created_on** - creation timestamp
- **last_updated_on** - last update timestamp
- **modified_by** - last modifier
- **status** - status
- **rank** - ordering rank
- **categories** - categories
- **keywords** - keywords

---

## 2. SlotDefinition (117 total properties)

### Currently Documented Properties (~20 properties)

#### Explicitly shown in template:
1. **name** - shown in title
2. **title** - shown in title if present
3. **description** - shown as element description
4. **deprecated** - shown with DEPRECATED flag
5. **abstract** - shown with NOTE about abstract slot
6. **alias** - shown explicitly

#### In "Inheritance" section:
7. **is_a** - shown in inheritance tree
8. **mixins** - shown in inheritance tree

#### In "Properties" section:
9. **range** - shown as Range
10. **multivalued** - shown if true
11. **required** - shown if true
12. **recommended** - shown if true (alternative to required)
13. **minimum_value** - shown if set
14. **maximum_value** - shown if set
15. **pattern** - shown as regex pattern
16. **mixin** - shown if is mixin
17. **any_of** - shown through compute_range macro
18. **exactly_one_of** - shown through compute_range macro

#### In common_metadata.md.jinja2 (same 12 as classes):
19. **aliases**
20. **examples**
21. **comments**
22. **todos**
23. **see_also**
24. **id_prefixes**
25. **annotations**
26. **from_schema**
27. **imported_from**
28. **mappings** (and all mapping subtypes)

### Missing from Main Documentation (97 properties)

#### Core Slot Properties:
- **domain** - domain class
- **domain_of** - classes this is a slot of
- **slot_uri** - URI for the slot
- **slot_group** - slot group membership
- **owner** - owning class
- **singular_name** - singular form of name
- **inherited** - whether inherited
- **readonly** - whether readonly
- **ifabsent** - default value expression
- **list_elements_unique** - whether list elements must be unique
- **list_elements_ordered** - whether list is ordered
- **shared** - whether shared across classes
- **key** - whether this is a key
- **identifier** - whether this is an identifier
- **designates_type** - whether designates type
- **subproperty_of** - RDF subproperty
- **symmetric** - whether symmetric
- **reflexive** - whether reflexive
- **locally_reflexive** - whether locally reflexive
- **irreflexive** - whether irreflexive
- **asymmetric** - whether asymmetric
- **transitive** - whether transitive
- **inverse** - inverse slot
- **is_class_field** - whether is class field
- **transitive_form_of** - transitive form of
- **reflexive_transitive_form_of** - reflexive transitive form
- **role** - role in relationship
- **is_usage_slot** - whether is usage slot
- **usage_slot_name** - usage slot name
- **relational_role** - relational role
- **slot_group** - group membership
- **is_grouping_slot** - whether groups slots
- **path_rule** - path expression
- **disjoint_with** - disjoint slots
- **children_are_mutually_disjoint** - whether children disjoint

#### Cardinality:
- **minimum_cardinality** - minimum cardinality
- **maximum_cardinality** - maximum cardinality
- **exact_cardinality** - exact cardinality

#### Range & Values:
- **enum_range** - enumeration range
- **range_expression** - range expression
- **inlined** - whether inlined
- **inlined_as_list** - whether inlined as list
- **unit** - unit of measurement
- **implicit_prefix** - implicit prefix
- **value_presence** - value presence requirement
- **equals_string** - string equality constraint
- **equals_string_in** - string in list constraint
- **equals_number** - numeric equality
- **structured_pattern** - structured pattern
- **type_mappings** - type mappings
- **bindings** - term bindings

#### Expression & Logic:
- **all_of** - all of these conditions
- **none_of** - none of these
- **equals_expression** - equals expression
- **has_member** - has member constraint
- **all_members** - all members constraints

#### Arrays & Collections:
- **array** - array configuration

#### From definition:
- **abstract** - whether abstract
- **apply_to** - what this applies to
- **values_from** - enum values source
- **string_serialization** - serialization pattern
- **union_of** - union of slots

#### From element (missing):
- **id_prefixes_are_closed**
- **definition_uri**
- **local_names**
- **conforms_to**
- **implements**
- **instantiates**

#### From common_metadata (missing):
- **alt_descriptions**
- **notes**
- **in_subset**
- **source**
- **in_language**
- **deprecated_element_has_exact_replacement**
- **deprecated_element_has_possible_replacement**
- **structured_aliases**
- **created_by**
- **contributors**
- **created_on**
- **last_updated_on**
- **modified_by**
- **status**
- **rank**
- **categories**
- **keywords**

---

## 3. EnumDefinition (65 total properties)

### Currently Documented Properties (~12 properties)

#### Explicitly shown:
1. **name** - shown in title
2. **description** - shown as element description
3. **deprecated** - shown with DEPRECATED flag
4. **permissible_values** - shown in Permissible Values table (with text, meaning, description)

#### In common_metadata.md.jinja2:
5. **aliases**
6. **examples**
7. **comments**
8. **todos**
9. **see_also**
10. **id_prefixes**
11. **annotations**
12. **from_schema**
13. **imported_from**
14. **mappings** (and all mapping subtypes)

### Missing from Main Documentation (53 properties)

#### Core Enum Properties:
- **enum_uri** - URI for the enum
- **title** - human-readable title

#### From enum_expression:
- **code_set** - code set URI
- **code_set_tag** - code set tag
- **code_set_version** - code set version
- **pv_formula** - permissible value formula
- **include** - include from other enums
- **minus** - exclude permissible values
- **inherits** - inherit from other enums
- **reachable_from** - reachable from source
- **matches** - pattern matching
- **concepts** - concept URIs

#### From definition:
- **is_a** - parent enum
- **abstract** - whether abstract
- **mixin** - whether mixin
- **mixins** - mixin enums
- **apply_to** - what applies to
- **values_from** - values source
- **string_serialization** - serialization

#### From element:
- **id_prefixes_are_closed**
- **definition_uri**
- **local_names**
- **conforms_to**
- **implements**
- **instantiates**

#### From common_metadata (missing):
- **alt_descriptions**
- **notes**
- **in_subset**
- **source**
- **in_language**
- **deprecated_element_has_exact_replacement**
- **deprecated_element_has_possible_replacement**
- **structured_aliases**
- **created_by**
- **contributors**
- **created_on**
- **last_updated_on**
- **modified_by**
- **status**
- **rank**
- **categories**
- **keywords**

---

## 4. TypeDefinition (61 total properties)

### Currently Documented Properties (~10 properties)

#### Explicitly shown:
1. **name** - shown in title
2. **description** - shown as element description
3. **deprecated** - shown with DEPRECATED flag
4. **base** - shown via bullet()
5. **uri** - shown via bullet() (note: should be **type_uri**)
6. **repr** - shown via bullet()
7. **typeof** - shown via bullet()
8. **pattern** - shown via bullet()

#### Range (via number_value_range):
9. **minimum_value**
10. **maximum_value**

#### In common_metadata.md.jinja2:
11. **aliases**
12. **examples**
13. **comments**
14. **todos**
15. **see_also**
16. **id_prefixes**
17. **annotations**
18. **from_schema**
19. **imported_from**
20. **mappings** (and all mapping subtypes)

### Missing from Main Documentation (51 properties)

#### Core Type Properties:
- **type_uri** - URI for the type (NOTE: "uri" is shown but type_uri is the actual slot name)
- **union_of** - union of types
- **title** - human-readable title

#### From type_expression:
- **structured_pattern** - structured pattern
- **unit** - unit of measurement
- **implicit_prefix** - implicit prefix
- **equals_string** - string equality
- **equals_string_in** - string in list
- **equals_number** - numeric equality
- **none_of** - none of these
- **exactly_one_of** - exactly one of
- **any_of** - any of these
- **all_of** - all of these

#### From element:
- **id_prefixes_are_closed**
- **definition_uri**
- **local_names**
- **conforms_to**
- **implements**
- **instantiates**

#### From common_metadata (missing):
- **alt_descriptions**
- **notes**
- **in_subset**
- **source**
- **in_language**
- **deprecated_element_has_exact_replacement**
- **deprecated_element_has_possible_replacement**
- **structured_aliases**
- **created_by**
- **contributors**
- **created_on**
- **last_updated_on**
- **modified_by**
- **status**
- **rank**
- **categories**
- **keywords**

---

## Common Patterns

### Universally Missing Properties (across all element types)

These common_metadata properties are defined but never shown in main documentation:

1. **alt_descriptions** - alternative descriptions
2. **notes** - editorial notes
3. **in_subset** - subset membership
4. **source** - original source
5. **in_language** - language code
6. **deprecated_element_has_exact_replacement** - exact replacement
7. **deprecated_element_has_possible_replacement** - possible replacement
8. **structured_aliases** - structured aliases
9. **created_by** - creator
10. **contributors** - contributors
11. **created_on** - creation date
12. **last_updated_on** - last update date
13. **modified_by** - last modifier
14. **status** - status
15. **rank** - rank
16. **categories** - categories
17. **keywords** - keywords

### Properties Shown in YAML But Not in Main Doc

All properties are visible in the "LinkML Source" YAML dumps at the bottom of each page, but this is:
- Not easily scannable
- Requires YAML knowledge
- Hidden in collapsed details section
- Shows both set and unset values

---

## Key Findings

### 1. Common Metadata Gap
The most significant gap is in **common_metadata** properties. 17 properties that are part of the common_metadata mixin are never shown in the main documentation body, only in YAML dumps.

### 2. Slot Definition Has Largest Gap
SlotDefinition has 117 properties but only ~17% are documented, making it the biggest coverage gap.

### 3. Expression Logic Mostly Missing
Properties related to expressions and logical constraints (any_of, all_of, none_of, exactly_one_of) are poorly covered:
- Classes: slot_conditions, logical operators not shown
- Slots: any_of/exactly_one_of only shown in range computation
- Enums: Formula and set operations not shown
- Types: Logical operators not shown

### 4. Relationship Properties Missing
For SlotDefinition, key relationship properties are not shown:
- symmetric, reflexive, transitive, etc.
- inverse
- role properties

### 5. Cardinality Incomplete
While some cardinality is shown (via the cardinality() function for required/multivalued), explicit cardinality properties are missing:
- minimum_cardinality
- maximum_cardinality
- exact_cardinality

### 6. Provenance Never Shown
Schema provenance and versioning properties are never shown:
- created_by, created_on
- modified_by, last_updated_on
- contributors
- status

---

## Recommendations Summary

### Phase 1: High-Value Quick Wins
1. Add title display (when different from name)
2. Show definition_uri
3. Display status, rank, categories, keywords
4. Show in_subset
5. Add notes and alt_descriptions

### Phase 2: Expression & Logic
1. Display any_of, all_of, none_of, exactly_one_of for all types
2. Show slot_conditions for classes
3. Display enum formulas and set operations
4. Show structured_pattern

### Phase 3: Advanced Properties
1. Relationship properties (symmetric, transitive, etc.)
2. Full cardinality properties
3. Provenance information (created_by, etc.)
4. Advanced constraints and validations

### Implementation Strategy
- **Progressive Disclosure**: Use collapsible sections for less common properties
- **Only Show Set Values**: Don't show properties that are null/empty
- **Grouping**: Group related properties in sections
- **Tooltips/Help**: Add explanations for complex properties
