# LinkML Documentation Coverage Implementation Plan

## Goal
Ensure that all LinkML schema properties that are explicitly set in a model are displayed in the generated documentation, while maintaining usability and readability.

## Core Principle: **Only Show What's Set**

The documentation should only display properties that have been explicitly set in the schema. This keeps the documentation:
- Relevant (no noise from default/null values)
- Scannable (users see what the schema author actually configured)
- Maintainable (automatically adapts to schema complexity)

---

## Implementation Approach

### 1. Template Architecture

#### Current Structure
```
element.md.jinja2
├── Header (title, description)
├── Specific sections (Inheritance, Slots, etc.)
└── common_metadata.md.jinja2 (included)
```

#### Proposed Structure
```
element.md.jinja2
├── Header (title, description)
├── Specific sections (enhanced)
├── Properties section (NEW - conditional display)
│   ├── Core Properties
│   ├── Expression & Logic (collapsible)
│   ├── Constraints (collapsible)
│   └── Advanced (collapsible)
└── common_metadata.md.jinja2 (enhanced)
```

### 2. Progressive Disclosure Strategy

#### Tier 1: Always Visible (if set)
Properties that are commonly used and easy to understand:
- title
- description
- deprecated
- abstract
- status
- rank

#### Tier 2: Inline Display (if set)
Properties shown in relevant sections:
- In existing tables/lists
- Small, focused displays

#### Tier 3: Collapsible Sections (if any property in group is set)
Properties grouped by category in expandable sections:
- Expression & Logic
- Constraints & Validation
- Relationship Properties
- Provenance & Metadata

---

## Detailed Implementation by Element Type

### A. ClassDefinition Enhancements

#### 1. Enhanced Header Section
```jinja2
# Class: {{ title }}

{%- if element.deprecated %}
<span style="color: red;"><strong> (DEPRECATED) </strong></span>
{%- if element.deprecated_element_has_exact_replacement %}
  Replaced by: {{ gen.link(element.deprecated_element_has_exact_replacement) }}
{%- elif element.deprecated_element_has_possible_replacement %}
  See: {{ gen.link(element.deprecated_element_has_possible_replacement) }}
{%- endif %}
{%- endif %}

{%- if element.status %}
**Status:** {{ element.status }}
{%- endif %}

{%- if element.alt_descriptions %}
<details>
<summary>Alternative Descriptions</summary>

{%- for alt_desc in element.alt_descriptions.values() %}
- **{{ alt_desc.source }}**: {{ alt_desc.description }}
{%- endfor %}
</details>
{%- endif %}
```

#### 2. New "Class Properties" Section (after Inheritance, before Slots)
```jinja2
{%- set has_class_props = element.class_uri or element.tree_root or element.mixin
    or element.abstract or element.subclass_of or element.union_of
    or element.slot_names_unique or element.represents_relationship %}

{%- if has_class_props %}
## Class Properties

| Property | Value |
| --- | --- |
{%- if element.class_uri %}
| Class URI | {{ gen.uri_link(element.class_uri) }} |
{%- endif %}
{%- if element.abstract %}
| Abstract | Yes |
{%- endif %}
{%- if element.mixin %}
| Mixin | Yes |
{%- endif %}
{%- if element.tree_root %}
| Tree Root | Yes |
{%- endif %}
{%- if element.slot_names_unique %}
| Slot Names Unique | Yes |
{%- endif %}
{%- if element.represents_relationship %}
| Represents Relationship | Yes |
{%- endif %}
{%- if element.subclass_of %}
| Subclass Of | {{ element.subclass_of | map('gen.link') | join(', ') }} |
{%- endif %}
{%- if element.union_of %}
| Union Of | {{ element.union_of | map('gen.link') | join(', ') }} |
{%- endif %}
{%- if element.disjoint_with %}
| Disjoint With | {{ element.disjoint_with | map('gen.link') | join(', ') }} |
{%- endif %}
{%- if element.children_are_mutually_disjoint %}
| Children Are Mutually Disjoint | Yes |
{%- endif %}
{%- endif %}
```

#### 3. Unique Keys Section (if set)
```jinja2
{%- if element.unique_keys %}
## Unique Keys

{%- for uk in element.unique_keys %}
### {{ uk.unique_key_name }}
- **Slots:** {{ uk.unique_key_slots | join(', ') }}
{%- if uk.consider_nulls_inequal %}
- Considers nulls as inequal
{%- endif %}
{%- endfor %}
{%- endif %}
```

#### 4. Expressions & Logic Section (collapsible if set)
```jinja2
{%- set has_expressions = element.any_of or element.all_of or element.exactly_one_of
    or element.none_of or element.slot_conditions %}

{%- if has_expressions %}
<details>
<summary>Expressions & Logic</summary>

{%- if element.any_of %}
#### Any Of
The class must satisfy at least one of:
{%- for expr in element.any_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.all_of %}
#### All Of
The class must satisfy all of:
{%- for expr in element.all_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.exactly_one_of %}
#### Exactly One Of
The class must satisfy exactly one of:
{%- for expr in element.exactly_one_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.none_of %}
#### None Of
The class must not satisfy any of:
{%- for expr in element.none_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.slot_conditions %}
#### Slot Conditions
{%- for slot_name, conditions in element.slot_conditions.items() %}
- **{{ gen.link(slot_name) }}**: {{ conditions }}
{%- endfor %}
{%- endif %}

</details>
{%- endif %}
```

#### 5. Defining Slots (if set)
```jinja2
{%- if element.defining_slots %}
## Defining Slots

This class is defined by the following slots:
{%- for slot_name in element.defining_slots %}
- {{ gen.link(slot_name) }}
{%- endfor %}
{%- endif %}
```

### B. SlotDefinition Enhancements

#### 1. Enhanced Properties Section
Replace current minimal "Properties" section with comprehensive one:

```jinja2
## Properties

{%- if element.title and element.title != element.name %}
**Title:** {{ element.title }}
{%- endif %}

{%- if element.singular_name %}
**Singular Name:** {{ element.singular_name }}
{%- endif %}

### Type & Range

| Property | Value |
| --- | --- |
| Range | {{ compute_range(element) }} |
{%- if element.domain %}
| Domain | {{ gen.link(element.domain) }} |
{%- endif %}
{%- if element.domain_of %}
| Domain Of | {{ element.domain_of | map('gen.link') | join(', ') }} |
{%- endif %}
{%- if element.slot_uri %}
| Slot URI | {{ gen.uri_link(element.slot_uri) }} |
{%- endif %}
{%- if element.slot_group %}
| Slot Group | {{ gen.link(element.slot_group) }} |
{%- endif %}
{%- if element.is_grouping_slot %}
| Is Grouping Slot | Yes |
{%- endif %}

### Cardinality & Requirements

| Property | Value |
| --- | --- |
{%- if element.required %}
| Required | Yes |
{%- elif element.recommended %}
| Recommended | Yes |
{%- endif %}
{%- if element.multivalued %}
| Multivalued | Yes |
{%- endif %}
{%- if element.minimum_cardinality is not none %}
| Minimum Cardinality | {{ element.minimum_cardinality }} |
{%- endif %}
{%- if element.maximum_cardinality is not none %}
| Maximum Cardinality | {{ element.maximum_cardinality }} |
{%- endif %}
{%- if element.exact_cardinality is not none %}
| Exact Cardinality | {{ element.exact_cardinality }} |
{%- endif %}

{%- if element.multivalued %}
### List/Collection Properties

| Property | Value |
| --- | --- |
{%- if element.list_elements_unique %}
| Elements Must Be Unique | Yes |
{%- endif %}
{%- if element.list_elements_ordered %}
| Elements Are Ordered | Yes |
{%- endif %}
{%- endif %}

### Slot Characteristics

| Property | Value |
| --- | --- |
{%- if element.key %}
| Key | Yes |
{%- endif %}
{%- if element.identifier %}
| Identifier | Yes |
{%- endif %}
{%- if element.designates_type %}
| Designates Type | Yes |
{%- endif %}
{%- if element.inherited %}
| Inherited | Yes |
{%- endif %}
{%- if element.readonly %}
| Readonly | Yes |
{%- endif %}
{%- if element.ifabsent %}
| If Absent | `{{ element.ifabsent }}` |
{%- endif %}
{%- if element.owner %}
| Owner | {{ gen.link(element.owner) }} |
{%- endif %}
{%- if element.shared %}
| Shared | Yes |
{%- endif %}
{%- if element.is_class_field %}
| Is Class Field | Yes |
{%- endif %}
{%- if element.is_usage_slot %}
| Is Usage Slot | Yes |
{%- endif %}
{%- if element.usage_slot_name %}
| Usage Slot Name | {{ element.usage_slot_name }} |
{%- endif %}
```

#### 2. Value Constraints Section (collapsible if set)
```jinja2
{%- set has_constraints = element.minimum_value is not none or element.maximum_value is not none
    or element.pattern or element.structured_pattern or element.equals_string
    or element.equals_string_in or element.equals_number or element.enum_range %}

{%- if has_constraints %}
<details>
<summary>Value Constraints</summary>

{%- if element.minimum_value is not none or element.maximum_value is not none %}
**Numeric Range:**
{%- if element.minimum_value is not none and element.maximum_value is not none %}
{{ element.minimum_value }} to {{ element.maximum_value }}
{%- elif element.minimum_value is not none %}
≥ {{ element.minimum_value }}
{%- else %}
≤ {{ element.maximum_value }}
{%- endif %}
{%- endif %}

{%- if element.pattern %}
**Pattern:** `{{ element.pattern }}`
{%- endif %}

{%- if element.structured_pattern %}
**Structured Pattern:**
- Syntax: `{{ element.structured_pattern.syntax }}`
- Interpolated: {{ element.structured_pattern.interpolated }}
{%- if element.structured_pattern.partial_match %}
- Partial Match: Yes
{%- endif %}
{%- endif %}

{%- if element.equals_string %}
**Must Equal:** `{{ element.equals_string }}`
{%- endif %}

{%- if element.equals_string_in %}
**Must Be One Of:** {{ element.equals_string_in | join(', ') }}
{%- endif %}

{%- if element.equals_number %}
**Must Equal:** {{ element.equals_number }}
{%- endif %}

{%- if element.enum_range %}
**Enumeration Range:** {{ gen.link(element.enum_range) }}
{%- endif %}

{%- if element.unit %}
**Unit:** {{ gen.uri_link(element.unit) }}
{%- endif %}

{%- if element.implicit_prefix %}
**Implicit Prefix:** {{ element.implicit_prefix }}
{%- endif %}

</details>
{%- endif %}
```

#### 3. Relationship Properties Section (collapsible if set)
```jinja2
{%- set has_rel_props = element.symmetric or element.asymmetric or element.reflexive
    or element.locally_reflexive or element.irreflexive or element.transitive
    or element.inverse or element.transitive_form_of or element.reflexive_transitive_form_of
    or element.role or element.relational_role %}

{%- if has_rel_props %}
<details>
<summary>Relationship Properties</summary>

| Property | Value |
| --- | --- |
{%- if element.symmetric %}
| Symmetric | Yes |
{%- endif %}
{%- if element.asymmetric %}
| Asymmetric | Yes |
{%- endif %}
{%- if element.reflexive %}
| Reflexive | Yes |
{%- endif %}
{%- if element.locally_reflexive %}
| Locally Reflexive | Yes |
{%- endif %}
{%- if element.irreflexive %}
| Irreflexive | Yes |
{%- endif %}
{%- if element.transitive %}
| Transitive | Yes |
{%- endif %}
{%- if element.inverse %}
| Inverse | {{ gen.link(element.inverse) }} |
{%- endif %}
{%- if element.transitive_form_of %}
| Transitive Form Of | {{ gen.link(element.transitive_form_of) }} |
{%- endif %}
{%- if element.reflexive_transitive_form_of %}
| Reflexive Transitive Form Of | {{ gen.link(element.reflexive_transitive_form_of) }} |
{%- endif %}
{%- if element.role %}
| Role | {{ element.role }} |
{%- endif %}
{%- if element.relational_role %}
| Relational Role | {{ element.relational_role }} |
{%- endif %}

</details>
{%- endif %}
```

#### 4. Expression & Logic Section
```jinja2
{%- set has_expressions = element.any_of or element.all_of or element.exactly_one_of
    or element.none_of or element.equals_expression or element.has_member or element.all_members %}

{%- if has_expressions %}
<details>
<summary>Expressions & Logic</summary>

{%- if element.any_of %}
#### Any Of
Value must satisfy at least one of:
{%- for expr in element.any_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.all_of %}
#### All Of
Value must satisfy all of:
{%- for expr in element.all_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.exactly_one_of %}
#### Exactly One Of
Value must satisfy exactly one of:
{%- for expr in element.exactly_one_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.none_of %}
#### None Of
Value must not satisfy any of:
{%- for expr in element.none_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.equals_expression %}
#### Equals Expression
`{{ element.equals_expression }}`
{%- endif %}

{%- if element.has_member %}
#### Has Member
{{ element.has_member }}
{%- endif %}

{%- if element.all_members %}
#### All Members
{{ element.all_members }}
{%- endif %}

</details>
{%- endif %}
```

#### 5. Advanced Properties Section
```jinja2
{%- set has_advanced = element.path_rule or element.disjoint_with
    or element.children_are_mutually_disjoint or element.subproperty_of
    or element.array or element.bindings or element.type_mappings
    or element.value_presence or element.range_expression %}

{%- if has_advanced %}
<details>
<summary>Advanced Properties</summary>

{%- if element.subproperty_of %}
**Subproperty Of:** {{ gen.link(element.subproperty_of) }}
{%- endif %}

{%- if element.path_rule %}
**Path Rule:**
```
{{ element.path_rule }}
```
{%- endif %}

{%- if element.disjoint_with %}
**Disjoint With:** {{ element.disjoint_with | map('gen.link') | join(', ') }}
{%- endif %}

{%- if element.children_are_mutually_disjoint %}
**Children Are Mutually Disjoint:** Yes
{%- endif %}

{%- if element.array %}
**Array Configuration:**
- Dimensions: {{ element.array.dimensions | join(' x ') }}
{%- if element.array.exact_number_dimensions %}
- Exact Dimensions Required: Yes
{%- endif %}
{%- endif %}

{%- if element.range_expression %}
**Range Expression:** {{ element.range_expression }}
{%- endif %}

{%- if element.value_presence %}
**Value Presence:** {{ element.value_presence }}
{%- endif %}

{%- if element.bindings %}
**Term Bindings:**
{%- for binding in element.bindings %}
- {{ binding }}
{%- endfor %}
{%- endif %}

{%- if element.type_mappings %}
**Type Mappings:**
{%- for tm in element.type_mappings %}
- **Framework:** {{ tm.framework }}
  **Mapping:** {{ tm.mapping }}
{%- endfor %}
{%- endif %}

</details>
{%- endif %}
```

### C. EnumDefinition Enhancements

#### 1. Enhanced Header
```jinja2
# Enum: {{ gen.name(element) }}

{%- if element.title and element.title != element.name %}
**{{ element.title }}**
{%- endif %}

{%- if element.description %}
{{ element.description }}
{%- endif %}

{%- if element.enum_uri %}
**Enum URI:** {{ gen.uri_link(element.enum_uri) }}
{%- endif %}
```

#### 2. Enum Source Section (if using code sets or formulas)
```jinja2
{%- set has_enum_source = element.code_set or element.pv_formula or element.reachable_from
    or element.matches or element.concepts %}

{%- if has_enum_source %}
## Enumeration Source

{%- if element.code_set %}
**Code Set:** {{ gen.uri_link(element.code_set) }}
{%- if element.code_set_tag %}
- **Tag:** {{ element.code_set_tag }}
{%- endif %}
{%- if element.code_set_version %}
- **Version:** {{ element.code_set_version }}
{%- endif %}
{%- endif %}

{%- if element.pv_formula %}
**Permissible Value Formula:** {{ element.pv_formula }}
{%- endif %}

{%- if element.reachable_from %}
**Reachable From:**
- **Source:** {{ gen.link(element.reachable_from.source_ontology) }}
{%- if element.reachable_from.source_nodes %}
- **Nodes:** {{ element.reachable_from.source_nodes | join(', ') }}
{%- endif %}
{%- if element.reachable_from.relationship_types %}
- **Via:** {{ element.reachable_from.relationship_types | join(', ') }}
{%- endif %}
{%- endif %}

{%- if element.matches %}
**Matches:**
- **Expression:** `{{ element.matches.string_expression }}`
{%- endif %}

{%- if element.concepts %}
**Concepts:** {{ element.concepts | map('gen.uri_link') | join(', ') }}
{%- endif %}

{%- endif %}
```

#### 3. Enum Operations Section (if using set operations)
```jinja2
{%- set has_enum_ops = element.inherits or element.include or element.minus %}

{%- if has_enum_ops %}
## Enumeration Operations

{%- if element.inherits %}
**Inherits From:** {{ element.inherits | map('gen.link') | join(', ') }}
{%- endif %}

{%- if element.include %}
**Includes:** {{ element.include | map('gen.link') | join(', ') }}
{%- endif %}

{%- if element.minus %}
**Excludes:** {{ element.minus | map('gen.link') | join(', ') }}
{%- endif %}

{%- endif %}
```

#### 4. Enhanced Permissible Values Table
```jinja2
{%- if element.permissible_values %}
## Permissible Values

| Value | Meaning | Description | Additional Properties |
| --- | --- | --- | --- |
{%- for pv in element.permissible_values.values() %}
| {{ pv.text }} | {{ pv.meaning }} | {{ pv.description|enshorten }} |
{%- if pv.title %} Title: {{ pv.title }}<br>{% endif -%}
{%- if pv.is_a %} Is-A: {{ gen.link(pv.is_a) }}<br>{% endif -%}
{%- if pv.mixins %} Mixins: {{ pv.mixins | map('gen.link') | join(', ') }}<br>{% endif -%}
{%- if pv.deprecated %} **DEPRECATED**{% endif -%}
|
{%- endfor %}
{%- else %}
_This is a dynamic enum - permissible values are determined at runtime_
{%- endif %}
```

### D. TypeDefinition Enhancements

#### 1. Enhanced Properties Display
```jinja2
# Type: {{ gen.name(element) }}

{%- if element.title and element.title != element.name %}
**{{ element.title }}**
{%- endif %}

{%- if element.description %}
{{ element.description }}
{%- endif %}

## Type Properties

| Property | Value |
| --- | --- |
{%- if element.typeof %}
| Type Of | {{ gen.link(element.typeof) }} |
{%- endif %}
{%- if element.base %}
| Base | `{{ element.base }}` |
{%- endif %}
{%- if element.type_uri %}
| Type URI | {{ gen.uri_link(element.type_uri) }} |
{%- endif %}
{%- if element.repr %}
| Representation | `{{ element.repr }}` |
{%- endif %}
{%- if element.union_of %}
| Union Of | {{ element.union_of | map('gen.link') | join(', ') }} |
{%- endif %}
```

#### 2. Value Constraints (same pattern as slots)
```jinja2
{%- set has_constraints = element.minimum_value is not none or element.maximum_value is not none
    or element.pattern or element.structured_pattern or element.equals_string
    or element.equals_string_in or element.equals_number %}

{%- if has_constraints %}
## Value Constraints

{%- if element.minimum_value is not none or element.maximum_value is not none %}
**Numeric Range:** {{ gen.number_value_range(element) }}
{%- endif %}

{%- if element.pattern %}
**Pattern:** `{{ element.pattern }}`
{%- endif %}

{%- if element.structured_pattern %}
**Structured Pattern:**
- Syntax: `{{ element.structured_pattern.syntax }}`
- Interpolated: {{ element.structured_pattern.interpolated }}
{%- endif %}

{%- if element.equals_string %}
**Must Equal:** `{{ element.equals_string }}`
{%- endif %}

{%- if element.equals_string_in %}
**Must Be One Of:** {{ element.equals_string_in | join(', ') }}
{%- endif %}

{%- if element.equals_number %}
**Must Equal:** {{ element.equals_number }}
{%- endif %}

{%- if element.unit %}
**Unit:** {{ gen.uri_link(element.unit) }}
{%- endif %}

{%- if element.implicit_prefix %}
**Implicit Prefix:** {{ element.implicit_prefix }}
{%- endif %}

{%- endif %}
```

#### 3. Type Expressions Section
```jinja2
{%- set has_expressions = element.any_of or element.all_of or element.exactly_one_of or element.none_of %}

{%- if has_expressions %}
<details>
<summary>Type Expressions</summary>

{%- if element.any_of %}
**Any Of:** Value must satisfy at least one of these expressions
{%- for expr in element.any_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.all_of %}
**All Of:** Value must satisfy all of these expressions
{%- for expr in element.all_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.exactly_one_of %}
**Exactly One Of:** Value must satisfy exactly one of these expressions
{%- for expr in element.exactly_one_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

{%- if element.none_of %}
**None Of:** Value must not satisfy any of these expressions
{%- for expr in element.none_of %}
- {{ expr }}
{%- endfor %}
{%- endif %}

</details>
{%- endif %}
```

### E. Enhanced common_metadata.md.jinja2

Add missing properties to the common metadata template:

```jinja2
{%- if element.title and element.title != element.name %}
## Title
{{ element.title }}
{%- endif %}

{%- if element.status %}
## Status
{{ element.status }}
{%- endif %}

{%- if element.rank is not none %}
## Rank
{{ element.rank }}
{%- endif %}

{%- if element.categories %}
## Categories
{%- for cat in element.categories %}
* {{ cat }}
{%- endfor %}
{%- endif %}

{%- if element.keywords %}
## Keywords
{%- for kw in element.keywords %}
* {{ kw }}
{%- endfor %}
{%- endif %}

{%- if element.in_subset %}
## In Subsets
{%- for subset in element.in_subset %}
* {{ gen.link(subset) }}
{%- endfor %}
{%- endif %}

{%- if element.alt_descriptions %}
## Alternative Descriptions
{%- for source, alt_desc in element.alt_descriptions.items() %}
* **{{ source }}**: {{ alt_desc.description }}
{%- endfor %}
{%- endif %}

{%- if element.notes %}
## Notes
{%- for note in element.notes %}
* {{ note }}
{%- endfor %}
{%- endif %}

{# ... existing aliases, examples, comments, todos, see_also sections ... #}

{%- if element.source %}
## Source
{{ gen.uri_link(element.source) }}
{%- endif %}

{%- if element.in_language %}
## Language
{{ element.in_language }}
{%- endif %}

{%- if element.structured_aliases %}
## Structured Aliases
| Predicate | Value | Categories |
| --- | --- | --- |
{%- for sa in element.structured_aliases %}
| {{ sa.literal_form }} |
{%- if sa.predicate %} {{ sa.predicate }}{% endif %} |
{%- if sa.categories %} {{ sa.categories | join(', ') }}{% endif %} |
{%- endfor %}
{%- endif %}

{# ... existing id_prefixes, annotations sections ... #}

{%- set has_provenance = element.created_by or element.contributors or element.created_on
    or element.last_updated_on or element.modified_by %}

{%- if has_provenance %}
## Provenance

| Property | Value |
| --- | --- |
{%- if element.created_by %}
| Created By | {{ element.created_by }} |
{%- endif %}
{%- if element.created_on %}
| Created On | {{ element.created_on }} |
{%- endif %}
{%- if element.modified_by %}
| Modified By | {{ element.modified_by }} |
{%- endif %}
{%- if element.last_updated_on %}
| Last Updated | {{ element.last_updated_on }} |
{%- endif %}
{%- if element.contributors %}
| Contributors | {{ element.contributors | join(', ') }} |
{%- endif %}
{%- endif %}

{# ... existing schema source, mappings sections ... #}
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal:** Add high-value, commonly-used properties with minimal disruption

1. Enhance `common_metadata.md.jinja2`:
   - Add status, rank, categories, keywords
   - Add in_subset
   - Add notes section
   - Add provenance section (collapsible)
   - Add structured_aliases

2. Add title display to all element types (when different from name)

3. Add definition_uri display where missing

**Impact:** ~10-15 more properties visible, highly useful for most schemas

### Phase 2: Core Properties (Week 3-4)
**Goal:** Add element-specific core properties

**Classes:**
1. Add "Class Properties" section
2. Add "Unique Keys" section
3. Add "Defining Slots" section

**Slots:**
1. Enhance Properties section with full cardinality
2. Add domain/domain_of display
3. Add slot characteristics (key, identifier, etc.)
4. Add list/collection properties

**Enums:**
1. Add enum_uri display
2. Add title display

**Types:**
1. Add type_uri (fix current "uri" display)
2. Add union_of display
3. Enhance constraint display

**Impact:** ~20-30 more properties visible, covers most common use cases

### Phase 3: Expressions & Logic (Week 5-6)
**Goal:** Add support for validation expressions

1. Add Expression & Logic sections to all element types:
   - any_of, all_of, exactly_one_of, none_of
   - Make collapsible by default
   - Clear, structured display

2. For classes: add slot_conditions

3. For enums: add enum operations and sources

4. For slots: add has_member, all_members, equals_expression

**Impact:** ~15-20 more properties, critical for validation-heavy schemas

### Phase 4: Advanced Features (Week 7-8)
**Goal:** Complete coverage of all properties

**Slots:**
1. Add Value Constraints section (collapsible)
2. Add Relationship Properties section (collapsible)
3. Add Advanced Properties section (collapsible)

**Enums:**
1. Add Enum Source section
2. Enhance permissible values table with all PV properties

**Types:**
1. Add Type Expressions section

**Classes:**
1. Add remaining advanced properties (disjoint_with, etc.)

**Impact:** Remaining ~40-50 properties, complete coverage

---

## Testing Strategy

### 1. Test Schemas

Create test schemas that exercise different property combinations:

**test_simple.yaml** - Basic schema with only common properties
- Ensures existing docs still work
- Baseline for comparison

**test_comprehensive.yaml** - Schema using many advanced properties
- Classes with expressions, slot_conditions, unique_keys
- Slots with all cardinality types, relationship properties
- Enums with code sets and formulas
- Types with expressions

**test_real_world.yaml** - Based on actual production schemas
- NMDC schema
- Biolink model
- Other community schemas

### 2. Visual Review Checklist

For each phase:
- [ ] All set properties are visible
- [ ] No clutter from unset properties
- [ ] Collapsible sections work correctly
- [ ] Links are functional
- [ ] Tables are readable
- [ ] Progressive disclosure makes sense
- [ ] Mobile/responsive layout works

### 3. Automated Checks

Create test script:
```python
def test_property_coverage():
    """Ensure all set properties appear in rendered doc"""
    schema = load_schema('test_comprehensive.yaml')
    docs = generate_docs(schema)

    for element in schema.classes:
        set_props = get_set_properties(element)
        doc = docs[element.name]
        for prop in set_props:
            assert prop_visible_in_doc(doc, prop), \
                f"{prop} not visible in doc for {element.name}"
```

---

## Jinja2 Best Practices for Implementation

### 1. Check Before Display Pattern
```jinja2
{%- if element.property %}
**Property:** {{ element.property }}
{%- endif %}
```

### 2. Grouped Conditional Pattern
```jinja2
{%- set has_group = element.prop1 or element.prop2 or element.prop3 %}
{%- if has_group %}
## Group Title
[display properties]
{%- endif %}
```

### 3. Safe List Display
```jinja2
{%- if element.list_property %}
**Property:**
{%- for item in element.list_property %}
- {{ item }}
{%- endfor %}
{%- endif %}
```

### 4. Safe Link Display
```jinja2
{%- if element.ref_property %}
**Property:** {{ gen.link(element.ref_property) }}
{%- endif %}
```

### 5. Collapsible Sections
```jinja2
{%- if condition %}
<details>
<summary>Section Title</summary>

Content here...

</details>
{%- endif %}
```

---

## Success Metrics

### Quantitative
1. **Property Coverage:** % of set properties visible in docs
   - Target Phase 1: 50%
   - Target Phase 2: 70%
   - Target Phase 3: 85%
   - Target Phase 4: 100%

2. **Schema Coverage:** % of schemas where all set properties are visible
   - Target: 100% by Phase 4

### Qualitative
1. **Usability:** Docs remain scannable and not cluttered
2. **Discoverability:** Users can find property documentation without reading YAML
3. **Maintainability:** Templates remain maintainable
4. **Performance:** Doc generation time doesn't increase significantly

---

## Migration & Backwards Compatibility

### 1. No Breaking Changes
- All existing documentation continues to work
- Only additions, no removals
- No changes to CLI interface

### 2. Opt-in Advanced Features
Consider adding flags for users who want minimal docs:
```bash
gen-doc --minimal  # Only show Tier 1 properties
gen-doc --standard # Show Tier 1-2 (default)
gen-doc --complete # Show all properties (Tier 1-3)
```

### 3. Custom Templates
- Users with custom templates can adopt changes incrementally
- Provide migration guide
- Common metadata enhancements automatically benefit custom templates

---

## Documentation & User Guide

### 1. Update Generator Docs
- Document all new template sections
- Provide examples of each property type
- Explain progressive disclosure strategy

### 2. Template Development Guide
- How to add new properties
- Best practices for conditional display
- Testing new template features

### 3. Schema Author Guide
- Which properties affect documentation
- How to use advanced properties effectively
- Examples of well-documented schemas

---

## Maintenance Plan

### 1. Keep Templates in Sync with Metamodel
- When metamodel adds new properties, add to templates
- Automated check: compare metamodel properties vs template coverage
- Regular reviews (quarterly)

### 2. Community Feedback Loop
- Monitor issues about missing properties
- Collect feedback on usability of dense property displays
- Iterate on progressive disclosure strategy

### 3. Performance Monitoring
- Track doc generation time
- Optimize slow sections
- Consider lazy-loading for very large schemas
