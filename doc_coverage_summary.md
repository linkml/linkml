# LinkML Documentation Coverage Analysis - Executive Summary

## Overview

This analysis examined the coverage of LinkML metamodel properties in the `gen-doc` generated documentation. The goal is to ensure that all explicitly set schema properties are visible in the documentation, regardless of which metamodel features are used.

## Key Findings

### Current Coverage Gaps

| Element Type | Total Properties | Currently Documented | Coverage | Missing |
|--------------|------------------|---------------------|----------|---------|
| **ClassDefinition** | 72 | ~25 (35%) | ⚠️ Low | 47 |
| **SlotDefinition** | 117 | ~20 (17%) | 🔴 Very Low | 97 |
| **EnumDefinition** | 65 | ~12 (18%) | 🔴 Very Low | 53 |
| **TypeDefinition** | 61 | ~10 (16%) | 🔴 Very Low | 51 |

### Critical Gaps Identified

1. **Common Metadata (Universal Gap)** - 17 properties defined in common_metadata mixin are never shown:
   - Provenance: created_by, contributors, created_on, last_updated_on, modified_by
   - Organization: status, rank, categories, keywords, in_subset
   - Documentation: notes, alt_descriptions, structured_aliases
   - Deprecation: exact/possible replacements

2. **Slot Properties (Largest Gap)** - 97 missing properties including:
   - Cardinality: minimum/maximum/exact_cardinality
   - Relationship semantics: symmetric, transitive, reflexive, inverse
   - Constraints: structured_pattern, value_presence
   - Advanced features: path_rule, bindings, array configuration

3. **Expression & Logic (All Types)** - Validation expressions poorly covered:
   - Class: slot_conditions, any_of, all_of, exactly_one_of, none_of
   - Slot: expression operators and constraints
   - Enum: pv_formula, code_set, reachable_from, set operations
   - Type: logical operators

4. **Class Constraints** - Advanced class features not shown:
   - unique_keys, defining_slots, tree_root
   - union_of, disjoint_with, subclass_of
   - classification_rules, slot_names_unique

5. **Enum Dynamics** - Dynamic enumeration features missing:
   - Code set integration (code_set, code_set_tag, code_set_version)
   - Set operations (include, minus, inherits)
   - Formula-based enums (pv_formula)

## Complete Analysis Documents

Three comprehensive documents have been created:

### 1. metamodel_doc_coverage_analysis.md
**Detailed gap analysis for each element type**
- Complete list of all 72 ClassDefinition properties (25 documented, 47 missing)
- Complete list of all 117 SlotDefinition properties (20 documented, 97 missing)
- Complete list of all 65 EnumDefinition properties (12 documented, 53 missing)
- Complete list of all 61 TypeDefinition properties (10 documented, 51 missing)
- Identification of common patterns and universally missing properties

### 2. doc_coverage_implementation_plan.md
**Phased implementation plan with code examples**
- **Phase 1 (Weeks 1-2):** Foundation - Add high-value common properties (~10-15 properties)
- **Phase 2 (Weeks 3-4):** Core Properties - Element-specific essentials (~20-30 properties)
- **Phase 3 (Weeks 5-6):** Expressions & Logic - Validation support (~15-20 properties)
- **Phase 4 (Weeks 7-8):** Advanced Features - Complete coverage (~40-50 properties)
- Complete Jinja2 template examples for each enhancement
- Testing strategy and success metrics
- Migration and backwards compatibility plan

### 3. This Summary Document
Quick reference and decision-making guide

## Recommended Approach: Progressive Disclosure

### Core Principle
**Only show properties that are explicitly set in the schema**

This ensures:
- ✅ No clutter from null/default values
- ✅ Documentation scales with schema complexity
- ✅ Simple schemas get simple docs
- ✅ Complex schemas show all relevant details
- ✅ Users see what authors actually configured

### Display Strategy

**Tier 1: Always Visible (if set)**
- title, description, deprecated, abstract, status, rank
- Commonly used, easy to understand

**Tier 2: Inline Display (if set)**
- Shown in existing sections/tables
- Small, focused displays
- Examples: required, multivalued, range

**Tier 3: Collapsible Sections (if any in group is set)**
- Grouped by category in expandable sections
- Examples:
  - Expression & Logic
  - Constraints & Validation
  - Relationship Properties
  - Provenance & Metadata

## Quick Start: Immediate Actions

### For Schema Authors (Current Workaround)
Until improvements are implemented, to ensure properties are visible:
1. Check the YAML source dumps at bottom of each doc page
2. Add custom annotations or extensions for critical undocumented properties
3. Use description field to document important property values

### For LinkML Maintainers (Implementation Priority)

**High Priority (Do First):**
1. Add common_metadata properties (status, rank, categories, keywords, in_subset, notes)
2. Show title when different from name
3. Display full cardinality for slots (minimum/maximum/exact_cardinality)
4. Add slot characteristics (key, identifier, owner, readonly)

**Medium Priority (Do Next):**
1. Add expression & logic sections for all types
2. Show class constraints (unique_keys, defining_slots)
3. Display enum operations and code set integration
4. Add relationship properties for slots

**Lower Priority (Complete Coverage):**
1. Advanced slot features (path_rule, bindings, array)
2. Provenance information
3. Remaining specialized properties

## Example Impact

### Before (Current State)
A slot with these properties set:
```yaml
slots:
  age:
    range: integer
    required: true
    minimum_value: 0
    maximum_value: 150
    minimum_cardinality: 1
    maximum_cardinality: 1
    unit: UO:0000036  # year
    ifabsent: "int(0)"
    status: stable
    rank: 100
```

**Currently shown:** range, required, minimum_value, maximum_value (4 of 10)
**Missing:** minimum_cardinality, maximum_cardinality, unit, ifabsent, status, rank (6 of 10)

### After (With Improvements)
**All 10 properties clearly visible in documentation**, organized in sections:
- Type & Range section: range, unit
- Cardinality & Requirements section: required, minimum/maximum cardinality
- Value Constraints section: minimum/maximum value
- Slot Characteristics section: ifabsent
- Metadata section: status, rank

## Testing & Validation

### Test Schemas Needed
1. **test_simple.yaml** - Baseline, only basic properties
2. **test_comprehensive.yaml** - Exercises all property types
3. **test_real_world.yaml** - Based on production schemas (NMDC, Biolink)

### Success Criteria
- ✅ All explicitly set properties visible in docs
- ✅ No clutter from unset properties
- ✅ Documentation remains scannable
- ✅ Progressive disclosure works intuitively
- ✅ No breaking changes to existing docs

## Timeline Estimate

### Conservative Estimate (8 weeks)
- Week 1-2: Phase 1 (Foundation)
- Week 3-4: Phase 2 (Core Properties)
- Week 5-6: Phase 3 (Expressions & Logic)
- Week 7-8: Phase 4 (Advanced Features)

### Aggressive Estimate (4 weeks)
- Week 1: Phases 1-2 combined
- Week 2: Phase 3
- Week 3: Phase 4
- Week 4: Testing and refinement

## Risk Assessment

### Low Risk
- Adding new sections to templates (only affects docs)
- Conditional display (only shows if set)
- No changes to schema validation or processing
- Backwards compatible

### Medium Risk
- Template complexity may increase maintenance burden
- Need to balance completeness vs readability
- Performance impact on very large schemas (needs monitoring)

### Mitigation Strategies
1. **Modular templates** - Break into reusable components
2. **Comprehensive testing** - Test suite for property coverage
3. **Documentation** - Clear template development guide
4. **Community feedback** - Iterate on display choices

## Next Steps

### Immediate (This Week)
1. Review and validate the analysis with team
2. Prioritize which properties are most important for Phase 1
3. Set up test schemas
4. Choose aggressive or conservative timeline

### Short Term (Next 2-4 Weeks)
1. Implement Phase 1 enhancements
2. Test with real schemas
3. Gather initial feedback
4. Adjust plan based on learning

### Long Term (Next 2 Months)
1. Complete all 4 phases
2. Comprehensive testing across community schemas
3. Documentation and migration guides
4. Release and announce improvements

## Questions for Decision Making

1. **Scope:** Do we want complete coverage (100%) or focus on most-used properties (70-80%)?
   - Recommendation: Complete coverage, but phased implementation

2. **Display Strategy:** How aggressive should progressive disclosure be?
   - Recommendation: Start conservative (more collapsible sections), gather feedback, adjust

3. **Timeline:** Aggressive (4 weeks) or conservative (8 weeks)?
   - Recommendation: Conservative to ensure quality and testing

4. **Breaking Changes:** Are any breaking changes acceptable?
   - Recommendation: No breaking changes, only additions

5. **Configuration:** Should there be flags for minimal vs complete documentation?
   - Recommendation: Add in Phase 3-4 based on feedback

## Conclusion

The current LinkML documentation generator covers only **16-35%** of available metamodel properties. This analysis provides:

1. ✅ **Complete inventory** of all properties for each element type
2. ✅ **Detailed gap analysis** showing what's missing
3. ✅ **Comprehensive implementation plan** with code examples
4. ✅ **Clear success metrics** and testing strategy
5. ✅ **Risk assessment** and mitigation strategies

The recommended approach uses **progressive disclosure** to show all set properties while maintaining usability. Implementation can be done in **4 phases over 4-8 weeks** with no breaking changes.

**Key Insight:** Most schemas likely use only a small fraction of available properties. By showing only what's set, documentation will automatically scale from simple (few properties shown) to comprehensive (all set properties shown), ensuring both usability and completeness.

---

## Files Created

All analysis and planning documents are in the linkml repository root:

1. **metamodel_doc_coverage_analysis.md** - Detailed gap analysis
2. **doc_coverage_implementation_plan.md** - Implementation plan with code
3. **doc_coverage_summary.md** - This executive summary

## Contact & Questions

For questions about this analysis:
- Review the detailed documents
- Check the implementation plan for specific code examples
- Refer to testing strategy for validation approach
