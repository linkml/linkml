"""Generate JSONld from a LinkML schema."""

import os
from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

import click
from jsonasobj2 import as_json, items, loads

from linkml import METAMODEL_CONTEXT_URI
from linkml._version import __version__
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.utils.deprecation import deprecated_fields
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    ElementName,
    EnumDefinition,
    SchemaDefinition,
    SlotDefinition,
    SlotDefinitionName,
    SubsetDefinition,
    SubsetDefinitionName,
    TypeDefinition,
    TypeDefinitionName,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.yamlutils import YAMLRoot


@deprecated_fields({"emit_metadata": "metadata"})
@dataclass
class JSONLDGenerator(Generator):
    """
    Generates JSON-LD from a Schema

    Status: incompletely implemented

    Note: this is distinct from
    :class:`~linkml.generators.jsonldcontextgen.ContextGenerator`, which generates a JSON-LD context
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = [
        "jsonld",
        "json",
    ]  # jsonld includes @type and @context.  json is pure JSON
    uses_schemaloader = False
    requires_metamodel = True
    file_extension = "jsonld"

    # ObjectVars
    original_schema: SchemaDefinition = None
    """See https://github.com/linkml/linkml/issues/871"""

    context: Sequence[str] | None = field(default_factory=list)
    """Path to a JSONLD context file"""

    metamodel_context: str = None
    """Override for metamodel context URI/path. When None, uses METAMODEL_CONTEXT_URI."""

    def __post_init__(self) -> None:
        if self.uses_schemaloader:
            raise ValueError(
                f"{type(self).__name__} is a SchemaView-only generator and does not support the "
                "SchemaLoader path; 'uses_schemaloader' must remain False."
            )
        self.original_schema = deepcopy(self.schema)
        super().__post_init__()
        # super().__post_init__() takes the SchemaView path (uses_schemaloader is False)
        # and always assigns self.schemaview, so it is guaranteed non-None from here on.
        # Trigger imports_closure so that inject_metadata runs and populates
        # from_schema on all elements (SchemaView only does this lazily).
        self.schemaview.imports_closure()
        # SchemaLoader merges imported elements into self.schema.{types,slots,classes,subsets,enums}
        # so the visitor can iterate them.  Replicate that here via SchemaView.
        self.schema.types.update(self.schemaview.all_types())
        self.schema.slots.update(self.schemaview.all_slots(attributes=False))
        self.schema.classes.update(self.schemaview.all_classes())
        self.schema.subsets.update(self.schemaview.all_subsets())
        self.schema.enums.update(self.schemaview.all_enums())
        # Materialise reverse inverses, mirroring SchemaLoader (schemaloader.py:304-317):
        # for every slot declaring ``inverse``, set the inverse relationship on the target
        # slot when it does not already declare one. SchemaView does not do this, so the
        # reverse direction would otherwise be lost from the serialised output.
        for slot in self.schema.slots.values():
            if slot.inverse:
                inverse_slot = self.schema.slots.get(slot.inverse)
                if inverse_slot is not None and not inverse_slot.inverse:
                    inverse_slot.inverse = slot.name
        # Merge parent type information into child types via ``typeof``, mirroring
        # SchemaLoader.merge_type (schemaloader.py:988-1005): recursively copy every
        # metaslot except ``imported_from`` from the parent type when unset on the child.
        # SchemaView does not materialise inherited type ``base``/``repr``/etc.
        from linkml.utils.mergeutils import merge_slots as _merge_slots

        merged_types: set[str] = set()

        def _merge_type(typ: TypeDefinition) -> None:
            if typ.name in merged_types:
                return
            if typ.typeof and typ.typeof in self.schema.types:
                parent = self.schema.types[typ.typeof]
                _merge_type(parent)
                _merge_slots(typ, parent, ["imported_from"])
            merged_types.add(typ.name)

        for typ in self.schema.types.values():
            _merge_type(typ)
        # Capture each slot's NATIVE domain (as declared, before is_a inheritance copies
        # ``domain`` down the chain). SchemaLoader applies its first domain check
        # (schemaloader.py:254-258) on the raw slot, i.e. against the native domain.
        native_slot_domain: dict[str, str | None] = {name: slot.domain for name, slot in self.schema.slots.items()}
        # Save original class slots BEFORE any slot_usage processing modifies cls.slots.
        # These are used later for domain_of population (which should use original slots
        # matching SchemaLoader's order of operations).
        original_cls_slots: dict[str, list[str]] = {cls.name: list(cls.slots) for cls in self.schema.classes.values()}
        # SchemaLoader expands schema.imports to include the full transitive closure
        # (mergeutils.py:322-351), using BFS order.
        visited_imports: set[str] = set(self.schema.imports)
        queue_imports: list[str] = list(self.schema.imports)
        while queue_imports:
            imp = queue_imports.pop(0)
            imp_schema = self.schemaview.schema_map.get(imp)
            if imp_schema is None:
                continue
            for sub_imp in imp_schema.imports:
                if sub_imp not in visited_imports:
                    visited_imports.add(sub_imp)
                    self.schema.imports.append(sub_imp)
                    queue_imports.append(sub_imp)
        # Reorder schema element dicts to match SchemaLoader insertion order:
        # own elements first (declaration order), then imported elements in the BFS
        # import order (matching self.schema.imports expansion order above).
        # This ensures as_json() serialises elements in the same order as SchemaLoader.
        # Build a map: schema_id → position in import order
        import_order = {str(self.schema.id): 0}
        for i, imp_name in enumerate(self.schema.imports, start=1):
            imp_s = self.schemaview.schema_map.get(imp_name)
            if imp_s:
                import_order[str(imp_s.id)] = i

        def _reorder_inplace(collection: dict) -> None:
            items = list(collection.items())
            items.sort(key=lambda kv: import_order.get(str(getattr(kv[1], "from_schema", "") or ""), 999))
            collection.clear()
            for k, v in items:
                collection[k] = v

        _reorder_inplace(self.schema.types)
        _reorder_inplace(self.schema.slots)
        _reorder_inplace(self.schema.classes)
        _reorder_inplace(self.schema.subsets)
        _reorder_inplace(self.schema.enums)
        # SchemaLoader promotes class attributes and slot_usage entries to top-level slots
        # AFTER the regular slots (schemaloader.py:208-228 and 866-925).
        # Do this after _reorder_inplace so these promoted slots appear last,
        # matching SchemaLoader's insertion order.
        from linkml.utils.mergeutils import merge_slots, slot_usage_name
        from linkml_runtime.utils.formatutils import mangled_attribute_name

        for cls in self.schema.classes.values():
            for attribute in cls.attributes.values():
                mangled_name = mangled_attribute_name(cls.name, attribute.name)
                if mangled_name not in self.schema.slots:
                    new_slot = SlotDefinition(**attribute.__dict__)
                    new_slot.owner = cls.name
                    new_slot.domain_of = list(attribute.domain_of)  # copy, not shared reference
                    new_slot.domain_of.append(cls.name)
                    new_slot.imported_from = cls.imported_from
                    new_slot.from_schema = cls.from_schema
                    if not new_slot.alias:
                        new_slot.alias = attribute.name
                    new_slot.name = mangled_name
                    self.schema.slots[new_slot.name] = new_slot
                    cls.slots.append(mangled_name)
        # Snapshot cls.slots after attribute promotion (attr-promoted names are present)
        # but before slot_usage mangling — used for SchemaLoader's domain check below.
        slots_after_attr_promotion = {cls.name: list(cls.slots) for cls in self.schema.classes.values()}
        for cls in self.schema.classes.values():
            for slotname, slot_usage in cls.slot_usage.items():
                if slotname not in self.schema.slots:
                    continue
                child_name = slot_usage_name(slotname, cls)
                if child_name in self.schema.slots:
                    continue
                # Find the most proximal ancestor definition for this slot, mirroring
                # SchemaLoader.slot_definition_for (schemaloader.py:1010-1036): search the
                # is_a/mixin ancestor classes' slots for a slot whose usage_slot_name (or
                # name) matches, so multi-level slot_usage chains point is_a at the correct
                # ancestor-mangled slot rather than the bare base slot.
                parent_slot = self._proximal_slot_definition(slotname, cls) or self.schema.slots[slotname]
                slot_alias = parent_slot.alias if parent_slot.alias else slotname
                new_slot = SlotDefinition(
                    name=child_name,
                    alias=slot_alias,
                    domain=cls.name,
                    is_usage_slot=True,
                    usage_slot_name=slotname,
                    owner=cls.name,
                    domain_of=[cls.name],
                    imported_from=cls.imported_from,
                    # from_schema intentionally omitted so merge_slots can inherit it from parent
                )
                merge_slots(
                    new_slot,
                    slot_usage,
                    inheriting=False,
                    skip=["name", "alias", "domain", "is_usage_slot", "usage_slot_name", "owner", "domain_of"],
                )
                # Merge from parent slot to inherit definition_uri, from_schema, rank, etc.
                # (schemaloader.py:928-930). rank is not in _inherited_slots so merge_slots
                # won't copy it — do it explicitly. Set is_a after merge_slots since
                # merge_slots resets non-inherited fields to None.
                merge_slots(new_slot, parent_slot)
                new_slot.is_a = parent_slot.name
                if new_slot.rank is None and parent_slot.rank is not None:
                    new_slot.rank = parent_slot.rank
                if not new_slot.range:
                    new_slot.range = self.schema.default_range
                # Re-apply slot_usage fields that merge_slots(inheriting=True) cleared:
                # merge_slots resets non-_inherited_slots fields to None, but slot_usage
                # may declare them (e.g. description, in_subset, exact_mappings).
                merge_slots(
                    new_slot,
                    slot_usage,
                    inheriting=False,
                    skip=[
                        "name",
                        "alias",
                        "domain",
                        "is_usage_slot",
                        "usage_slot_name",
                        "owner",
                        "domain_of",
                        "is_a",
                        "rank",
                        "range",
                    ],
                )
                # Copy base slot values: SchemaLoader (schemaloader.py:980-986) copies all
                # non-None, non-inverse fields from the original base slot to the new slot
                # AFTER the parent merge. This restores non-_inherited_slots fields like
                # description, in_subset, see_also, exact_mappings that merge_slots cleared.
                base_slot = self.schema.slots[slotname]
                for metaslot_name in base_slot.__dict__.keys():
                    current_val = getattr(new_slot, metaslot_name)
                    if not current_val and metaslot_name not in ["inverse"]:
                        new_val = deepcopy(getattr(base_slot, metaslot_name))
                        if new_val:
                            setattr(new_slot, metaslot_name, new_val)
                self.schema.slots[child_name] = new_slot
                # Replace the bare slot name with the mangled name in cls.slots
                # (schemaloader.py:965-974). Use original_cls_slots for lookup.
                if slotname in cls.slots:
                    # Replace in-place, whether it was original or inherited
                    cls.slots[cls.slots.index(slotname)] = child_name
                elif child_name not in cls.slots:
                    cls.slots.append(child_name)
        # SchemaLoader also creates slot_usage-derived slots for INHERITED slots
        # when a subclass has those slots in cls.slots and the parent class had a
        # slot_usage for them (creating ClassName_slotname chains).
        # Walk all classes and create derived slot_usage slots for inherited slot_usages
        # that appear in cls.slots. Use original_cls_slots to avoid processing
        # already-mangled names.
        for cls in self.schema.classes.values():
            if not cls.is_a:
                continue
            parent_cls = self.schema.classes.get(cls.is_a)
            if parent_cls is None:
                continue
            for slotname in original_cls_slots.get(cls.name, []):
                # Check if the parent has a mangled slot_usage for this slot
                parent_mangled = slot_usage_name(slotname, parent_cls)
                if parent_mangled not in self.schema.slots:
                    continue
                # Check the class doesn't already have its own slot_usage for this slot
                if slotname in cls.slot_usage:
                    continue
                child_name = slot_usage_name(slotname, cls)
                if child_name in self.schema.slots:
                    continue
                parent_slot = self.schema.slots[parent_mangled]
                new_slot = SlotDefinition(
                    name=child_name,
                    alias=parent_slot.alias if parent_slot.alias else slotname,
                    domain=cls.name,
                    is_usage_slot=True,
                    usage_slot_name=slotname,
                    owner=cls.name,
                    domain_of=[cls.name],
                    imported_from=cls.imported_from,
                )
                new_slot.is_a = parent_mangled
                merge_slots(new_slot, parent_slot)
                # Restore is_a — merge_slots resets non-inherited fields to None
                new_slot.is_a = parent_mangled
                if new_slot.rank is None and parent_slot.rank is not None:
                    new_slot.rank = parent_slot.rank
                self.schema.slots[child_name] = new_slot
                # Replace in cls.slots using current state (slotname was from original_cls_slots)
                if slotname in cls.slots:
                    cls.slots[cls.slots.index(slotname)] = child_name
                elif child_name not in cls.slots:
                    cls.slots.append(child_name)
        # SchemaLoader merges license and emit_prefixes from imported schemas
        # (mergeutils.py:37-49) and sets default_range to "string" if unspecified
        # (schemaloader.py:126-127).
        for s in self.schemaview.all_schema():
            if self.schema.license is None and s.license:
                self.schema.license = s.license
            for pfx in s.emit_prefixes:
                if pfx not in self.schema.emit_prefixes:
                    self.schema.emit_prefixes.append(pfx)
        if not self.schema.default_range:
            self.schema.default_range = "string"
        # SchemaLoader sets imported_from on elements that come from imported schemas,
        # using the CURIE form of the source schema id (e.g. "linkml:types").
        # Replicate that here: build a map from schema id URI → CURIE for all imports.
        from linkml_runtime.linkml_model.meta import Prefix as MetaPrefix

        id_to_curie: dict[str, str] = {}
        # Also track which schema IDs are "linkml" imports (start with "linkml:" or biolink URI)
        # — only these get imported_from set, matching mergeutils.merge_dicts (mergeutils.py:146-151).
        linkml_schema_ids: set[str] = set()
        for imp_name, imp_schema in self.schemaview.schema_map.items():
            if imp_name.startswith("linkml:") or str(imp_schema.id).startswith("https://w3id.org/biolink/linkml"):
                linkml_schema_ids.add(str(imp_schema.id))
        for s in self.schemaview.all_schema():
            for pfx, ns in self.schemaview.namespaces().items():
                # ns may be a linkml Prefix object or a plain string/rdflib Namespace
                ns_uri = ns.prefix_reference if isinstance(ns, MetaPrefix) else str(ns)
                if str(s.id).startswith(ns_uri) and pfx not in ("@base", "@default"):
                    id_to_curie[str(s.id)] = f"{pfx}:{str(s.id)[len(ns_uri) :]}"
                    break
            else:
                id_to_curie[str(s.id)] = str(s.id)
        for collection in [
            self.schema.types,
            self.schema.slots,
            self.schema.classes,
            self.schema.subsets,
            self.schema.enums,
        ]:
            for element in collection.values():
                # slot_usage-derived slots already received the correct ``imported_from``
                # from their owning class (SchemaLoader attributes a usage slot to the
                # schema that declares the class, not the base slot's schema). Do not
                # overwrite it from ``from_schema`` (which is inherited from the base slot).
                if getattr(element, "is_usage_slot", False):
                    continue
                if (
                    element.from_schema
                    and str(element.from_schema) != str(self.schema.id)
                    and str(element.from_schema) in linkml_schema_ids
                ):
                    element.imported_from = id_to_curie.get(str(element.from_schema), str(element.from_schema))
        # Now that every class has its resolved ``imported_from`` CURIE, propagate it to
        # slot_usage-derived slots. SchemaLoader attributes a usage slot to the schema
        # that declares its owning class (e.g. UnitOfMeasure_exact_mappings -> linkml:units),
        # not to the schema of the base slot.
        for slot in self.schema.slots.values():
            if getattr(slot, "is_usage_slot", False) and slot.owner:
                owner_cls = self.schema.classes.get(slot.owner)
                if owner_cls is not None and owner_cls.imported_from:
                    slot.imported_from = owner_cls.imported_from
        # Materialise inherited slot properties by walking the is_a chain and copying
        # fields from ancestor slots.  SchemaLoader did this via a full resolution pass;
        # here we replicate it without using induced_slot() (which has side-effects on
        # domain_of via _slot_class_map).
        # IMPORTANT: this must run BEFORE the cls.slots expansion below.
        _inherited_slot_names = set(SlotDefinition("_test")._inherited_slots)
        all_slots_map = dict(self.schema.slots)  # snapshot to avoid modification during iteration
        for slot in all_slots_map.values():
            if slot.is_a is None:
                continue
            # Walk the is_a chain and collect ancestor slot objects
            ancestors: list[SlotDefinition] = []
            parent_name = slot.is_a
            while parent_name:
                parent = all_slots_map.get(parent_name)
                if parent is None:
                    break
                ancestors.append(parent)
                parent_name = parent.is_a
            # Copy any _inherited_slots field that is None on this slot from the
            # first ancestor that has it set.
            for slot_name in _inherited_slot_names:
                if getattr(slot, slot_name, None) is None:
                    for ancestor in ancestors:
                        ancestor_val = getattr(ancestor, slot_name, None)
                        if ancestor_val is not None:
                            setattr(slot, slot_name, ancestor_val)
                            break
        # Apply inlined/inlined_as_list inference, mirroring SchemaLoader (schemaloader.py:436-509).
        # Only auto-set inlined/inlined_as_list when they are None; NEVER clobber an explicit
        # value declared in the schema. inlined_as_list is inferred from whether the range class
        # has an identifier or key slot.
        for slot in self.schema.slots.values():
            range_cls = self.schema.classes.get(str(slot.range) if slot.range else "")
            if range_cls is None:
                continue
            # Determine whether the range class has an identifier/key slot, taking
            # inheritance into account. SchemaLoader ran this check after is_a slot
            # merging, so inherited identifiers count. We walk the is_a chain manually
            # over the merged schema instead of using SchemaView.get_identifier_slot,
            # which has the side effect of populating ``domain_of`` on slots (via
            # induced_slot) in import order, corrupting later serialisation.
            range_has_identifier = self._class_has_identifier(range_cls.name)
            if range_has_identifier:
                # Range HAS an identifier: default to dictionary inlining (inlined_as_list=False)
                # only when inlined=True was requested and inlined_as_list is unspecified.
                if slot.inlined is True and slot.inlined_as_list is None:
                    slot.inlined_as_list = False
                elif slot.inlined is None and slot.inlined_as_list is True:
                    slot.inlined = True
                elif slot.inlined is False and slot.inlined_as_list is True:
                    slot.inlined = True
            else:
                # Range has NO identifier: it MUST be inlined.
                if slot.inlined is True:
                    if slot.inlined_as_list is None:
                        slot.inlined_as_list = True
                elif slot.inlined is False:
                    slot.inlined = True
                else:
                    slot.inlined = True
                    if slot.inlined_as_list is None:
                        slot.inlined_as_list = True
        # SchemaLoader sets slot.range to default_range ("string") when unspecified
        # (schemaloader.py:329). Apply for slots not covered by the is_a traversal.
        if self.schema.default_range:
            for slot in self.schema.slots.values():
                if slot.range is None:
                    slot.range = self.schema.default_range
        # Expand cls.slots to include inherited (is_a) and mixin slots, mirroring
        # SchemaLoader.merge_class + mergeutils.merge_classes (schemaloader.py:785-809,
        # mergeutils.py:230-253):
        #   * recurse into is_a parent first, prepend its slots (reversed) to the front,
        #   * then recurse into each mixin, append its slots to the end,
        #   * dedup by alias-root (bare slot name); when the target class has a slot_usage
        #     for that root, use the class-mangled name instead.
        # ``own_slots_map`` holds each class's declared slots AFTER attribute promotion and
        # slot_usage mangling, i.e. the state SchemaLoader starts merge_class from.
        own_slots_map = {cls.name: list(cls.slots) for cls in self.schema.classes.values()}
        expanded_slots: dict[str, list[str]] = {}

        def _alias_root(slotname: str) -> str:
            slot = self.schema.slots.get(slotname)
            alias = slot.alias if slot is not None else None
            if alias and alias != slotname:
                return _alias_root(alias)
            return slotname

        def _merge_class_slots(cls_name: str, merging: set[str]) -> list[str]:
            if cls_name in expanded_slots:
                return expanded_slots[cls_name]
            cls = self.schema.classes.get(cls_name)
            if cls is None or cls_name in merging:
                return list(own_slots_map.get(cls_name, []))
            merging.add(cls_name)
            target: list[str] = list(own_slots_map.get(cls_name, []))
            target_roots: set[str] = {_alias_root(s) for s in target}

            def _merge_source(source_name: str, at_end: bool) -> None:
                source_slots = _merge_class_slots(source_name, merging)
                seq = source_slots if at_end else source_slots[::-1]
                for slotname in seq:
                    slotbase = _alias_root(slotname)
                    effective = slotname
                    if slotbase in cls.slot_usage:
                        effective = slot_usage_name(slotbase, cls)
                    if slotbase not in target_roots:
                        if at_end:
                            target.append(effective)
                        else:
                            target.insert(0, effective)
                        target_roots.add(slotbase)

            if cls.is_a:
                _merge_source(cls.is_a, at_end=False)
            for mixin in cls.mixins or []:
                _merge_source(mixin, at_end=True)
            merging.discard(cls_name)
            expanded_slots[cls_name] = target
            return target

        for cls in self.schema.classes.values():
            cls.slots = _merge_class_slots(cls.name, set())
        # Set owner and domain_of using original (pre-replacement) slots, iterating
        # classes in dict order (matching SchemaLoader schemaloader.py:241-246).
        for cls in self.schema.classes.values():
            for slot_name in original_cls_slots.get(cls.name, []):
                slot = self.schema.slots.get(slot_name)
                if slot is not None:
                    slot.owner = cls.name
                    if cls.name not in slot.domain_of:
                        slot.domain_of.append(cls.name)
                mangled = slot_usage_name(slot_name, cls)
                if mangled in self.schema.slots and mangled != slot_name:
                    ms = self.schema.slots[mangled]
                    if cls.name not in ms.domain_of:
                        ms.domain_of.append(cls.name)
        # SchemaLoader applies two domain checks that assign ``owner = slot.name``:
        #
        # 1. Early check (schemaloader.py:254-258): runs on the RAW slot before is_a
        #    domain inheritance, so it uses the NATIVE domain and has no owner guard.
        #    It overrides an owner already set from a class slots list.
        # 2. Late check (schemaloader.py:385-388): runs after domain inheritance, uses
        #    the (possibly inherited) domain, and only fires when the slot has NO owner.
        #
        # In both cases the slot's own name is used as owner when the domain class does
        # not list the slot. slot_usage-derived slots are created later and excluded.
        for slot in self.schema.slots.values():
            if getattr(slot, "is_usage_slot", False):
                continue
            native_domain = native_slot_domain.get(slot.name)
            if native_domain and native_domain in self.schema.classes:
                if slot.name not in slots_after_attr_promotion.get(native_domain, []):
                    slot.owner = slot.name
        for slot in self.schema.slots.values():
            if getattr(slot, "is_usage_slot", False):
                continue
            if slot.domain and slot.domain in self.schema.classes and not slot.owner:
                if slot.name not in slots_after_attr_promotion.get(slot.domain, []):
                    slot.owner = slot.name
        # SchemaLoader marks key/identifier slots as required (schemaloader.py:370-373).
        for slot in self.schema.slots.values():
            if (slot.key or slot.identifier) and slot.required is None:
                slot.required = True

    def _proximal_slot_definition(self, slotname: str, cls: ClassDefinition) -> "SlotDefinition | None":
        """Find the most proximal definition for ``slotname`` in the context of ``cls``.

        Port of SchemaLoader.slot_definition_for (schemaloader.py:1010-1036): walk the
        is_a and mixin ancestors, returning the first slot whose ``usage_slot_name`` (or
        bare ``name``) matches ``slotname``. Resolves the parent of a slot_usage override
        to the correct ancestor-mangled slot in multi-level chains.
        """
        if cls.is_a and cls.is_a in self.schema.classes:
            for sn in self.schema.classes[cls.is_a].slots:
                slot = self.schema.slots.get(sn)
                if slot is None:
                    continue
                if (slot.usage_slot_name and slotname == slot.usage_slot_name) or (
                    not slot.usage_slot_name and slotname == slot.name
                ):
                    return slot
        for mixin in cls.mixins or []:
            if mixin in self.schema.classes:
                for sn in self.schema.classes[mixin].slots:
                    slot = self.schema.slots.get(sn)
                    if slot is None:
                        continue
                    if (slot.alias and slotname == slot.alias) or slotname == slot.name:
                        return slot
        if cls.is_a and cls.is_a in self.schema.classes:
            defn = self._proximal_slot_definition(slotname, self.schema.classes[cls.is_a])
            if defn:
                return defn
        for mixin in cls.mixins or []:
            if mixin in self.schema.classes:
                defn = self._proximal_slot_definition(slotname, self.schema.classes[mixin])
                if defn:
                    return defn
        return None

    def _class_has_identifier(self, class_name: str) -> bool:
        """Return True if ``class_name`` or any of its ``is_a`` ancestors declares a
        slot marked as ``identifier`` or ``key``.

        This is a side-effect-free replacement for
        :meth:`SchemaView.get_identifier_slot`, which mutates slot ``domain_of``
        lists via ``induced_slot`` and therefore cannot be used inside the
        serialisation pipeline without corrupting element ordering.
        """
        seen: set[str] = set()
        current: str | None = class_name
        while current and current not in seen:
            seen.add(current)
            cls = self.schema.classes.get(current)
            if cls is None:
                break
            for slot_name in cls.slots:
                slot = self.schema.slots.get(slot_name)
                if slot is not None and (slot.identifier or slot.key):
                    return True
            for attr in cls.attributes.values():
                if attr.identifier or attr.key:
                    return True
            current = cls.is_a
        return False

    def _slot_uri_for(self, slot: SlotDefinition) -> str:
        """Compute the slot_uri for a slot with no declared slot_uri.

        Replicates SchemaLoader's ``slot_name_for`` (schemaloader.py:1082): uses
        ``alias`` when present, otherwise ``name``, with :func:`underscore` casing.
        The namespace comes from the slot's source schema default prefix.
        """
        alias_or_name = underscore(slot.alias if slot.alias else slot.name)
        src_schema_id = slot.from_schema or self.schema.id
        src_schema = next(
            (s for s in self.schemaview.all_schema() if str(s.id) == str(src_schema_id)),
            self.schemaview.schema,
        )
        if src_schema.default_prefix and src_schema.default_prefix in src_schema.prefixes:
            ns = src_schema.prefixes[src_schema.default_prefix].prefix_reference
        else:
            ns = str(src_schema.id) + "/"
        return f"{ns}{alias_or_name}"

    def _add_type(self, node: YAMLRoot) -> dict:
        if self.format == "jsonld":
            typ = node.__class__.__name__
            node = node.__dict__
            node["@type"] = typ
        return node

    def _visit(self, node: Any) -> Any | None:
        if isinstance(node, YAMLRoot | dict):
            if isinstance(node, YAMLRoot):
                node = self._add_type(node)
            for k, v in list(items(node)):
                if v:
                    new_v = self._visit(v)
                    if new_v is not None:
                        node[k] = new_v
        elif isinstance(node, list):
            for i in range(0, len(node)):
                new_v = self._visit(node[i])
                if new_v is not None:
                    node[i] = new_v
        elif isinstance(node, set):
            for v in list(node):
                new_v = self._visit(v)
                if new_v is not None:
                    node.remove(v)
                    node.add(new_v)
        elif isinstance(node, ClassDefinitionName):
            return ClassDefinitionName(camelcase(node))
        elif isinstance(node, SlotDefinitionName):
            return SlotDefinitionName(underscore(node))
        elif isinstance(node, TypeDefinitionName):
            return TypeDefinitionName(underscore(node))
        elif isinstance(node, SubsetDefinitionName):
            return SubsetDefinitionName(underscore(node))
        elif isinstance(node, ElementName):
            return (
                ClassDefinitionName(camelcase(node))
                if node in self.schema.classes
                else (
                    SlotDefinitionName(underscore(node))
                    if node in self.schema.slots
                    else (
                        SubsetDefinitionName(camelcase(node))
                        if node in self.schema.subsets
                        else TypeDefinitionName(underscore(node))
                        if node in self.schema.types
                        else None
                    )
                )
            )
        return None

    def adjust_slot(self, slot: SlotDefinition) -> None:
        if slot.range in self.schema.classes:
            slot.range = ClassDefinitionName(camelcase(slot.range))
        elif slot.range in self.schema.slots:
            slot.range = SlotDefinitionName(underscore(slot.range))
        elif slot.range in self.schema.types:
            slot.range = TypeDefinitionName(underscore(slot.range))
        # SchemaLoader inserts the original slot_uri into mappings before overwriting it
        # (schemaloader.py:517-518), then synthesises slot_uri from default prefix + alias_or_name
        # when slot_uri is None (schemaloader.py:520-524, slot_name_for:1082-1083). Replicate both here.
        if slot.slot_uri is not None:
            slot.mappings.insert(0, slot.slot_uri)
        elif getattr(slot, "is_usage_slot", False) and slot.is_a:
            # Inherit slot_uri from the already-resolved parent slot
            parent = self.schema.slots.get(slot.is_a)
            if parent is not None and parent.slot_uri is not None:
                slot.slot_uri = parent.slot_uri
            else:
                slot.slot_uri = self._slot_uri_for(slot)
        else:
            slot.slot_uri = self._slot_uri_for(slot)
        slot.slot_uri = self.schemaview.namespaces().uri_for(slot.slot_uri)
        for f in [
            "mappings",
            "exact_mappings",
            "broad_mappings",
            "close_mappings",
            "narrow_mappings",
            "related_mappings",
        ]:
            setattr(slot, f, [self.schemaview.namespaces().uri_for(v) for v in getattr(slot, f)])

    def visit_class(self, cls: ClassDefinition) -> bool:
        cls.definition_uri = self.schemaview.get_uri(cls.name, native=True, expand=True)
        # SchemaLoader synthesises class_uri when missing (schemaloader.py:291-302) then
        # inserts it into exact_mappings (schemaloader.py:289-290 and 302).
        # get_uri(native=False) already implements this: it returns the declared class_uri
        # when set, otherwise constructs {default_prefix}:{camelcase(name)} — exactly
        # what SchemaLoader's uri_or_curie_for does.
        cls.exact_mappings.insert(0, cls.class_uri or self.schemaview.get_uri(cls.name, native=False))
        self._visit(cls)
        if hasattr(cls, "class_uri"):
            delattr(cls, "class_uri")
        # Slot usage is a construction artifact
        # TODO: Figure out why this is here.  It isn't good form to alter a schema that may be used by other things
        cls.slot_usage = {}
        return False

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        # Mangled attribute slots (class__attribute format) are promoted by SchemaLoader
        # without a definition_uri; skip it for them to match SchemaLoader output.
        # slot_usage-derived slots (ClassName_slotname, is_usage_slot=True) inherit
        # definition_uri from their base slot via get_uri(native=True, expand=True).
        if "__" not in slot.name and not getattr(slot, "is_usage_slot", False):
            slot.definition_uri = self.schemaview.get_uri(slot.name, native=True, expand=True)
        elif getattr(slot, "is_usage_slot", False) and slot.is_a:
            parent = self.schema.slots.get(slot.is_a)
            if parent is not None:
                # Use the base slot's definition_uri (already computed if visited) or
                # compute via SchemaView using the base slot name.
                base_slot_name = getattr(slot, "usage_slot_name", None) or slot.alias or slot.name
                base_slot = self.schema.slots.get(base_slot_name)
                if base_slot is not None:
                    slot.definition_uri = base_slot.definition_uri or self.schemaview.get_uri(
                        base_slot.name, native=True, expand=True
                    )
                    if slot.from_schema is None:
                        slot.from_schema = base_slot.from_schema
                elif parent.definition_uri:
                    slot.definition_uri = parent.definition_uri
                    if slot.from_schema is None and parent.from_schema:
                        slot.from_schema = parent.from_schema
        self._visit(slot)
        self.adjust_slot(slot)

    def visit_type(self, typ: TypeDefinition) -> None:
        typ.definition_uri = self.schemaview.get_uri(typ.name, native=True, expand=True)
        self._visit(typ)
        typ.uri = self.schemaview.namespaces().uri_for(typ.uri)

    def visit_subset(self, ss: SubsetDefinition) -> None:
        ss.definition_uri = self.schemaview.get_uri(ss.name, native=True, expand=True)
        self._visit(ss)

    def visit_enum(self, enum: EnumDefinition) -> None:
        enum.definition_uri = self.schemaview.get_uri(enum.name, native=True, expand=True)

    def end_schema(
        self, context: str | list[str] | tuple[str, ...] = [], context_kwargs: dict | None = None, **_
    ) -> str:
        default_context_kwargs = {"model": False}
        if context_kwargs is None:
            context_kwargs = default_context_kwargs
        else:
            context_kwargs = {**default_context_kwargs, **context_kwargs}

        self._add_type(self.schema)
        base_prefix = self.default_prefix()

        # `context` can be a `str`, a `list[str]` or a `tuple[str]`
        # since the context might need to get extended, `context_list` must be `list[str]`
        context_list: list[str] = []
        # TODO: fix this, see https://github.com/linkml/linkml/issues/871
        # JSON LD adjusts context reference using '@base'.  If context is supplied and not a URI, generate an
        # absolute URI for it
        if not context and self.format == "jsonld":
            # TODO: Once we get pyld running w/ relative contexts, we need to figure out how to generate and add
            #       the relative (?) context reference below
            # model_context = self.schema.source_file.replace('.yaml', '.prefixes.context.jsonld')
            # context = [METAMODEL_CONTEXT_URI, f'file://./{model_context}']
            # TODO: The _visit function above alters the schema in situ
            # force some context_kwargs
            context_kwargs["metadata"] = False
            # Forward importmap/base_dir so the spawned ContextGenerator can
            # re-resolve any URI-style imports in ``self.original_schema``
            # through the same ``--importmap`` the caller supplied.
            context_kwargs.setdefault("importmap", self.importmap)
            context_kwargs.setdefault("base_dir", self.base_dir)
            add_prefixes = ContextGenerator(self.original_schema, **context_kwargs).serialize()
            add_prefixes_json = loads(add_prefixes)
            metamodel_ctx = self.metamodel_context or METAMODEL_CONTEXT_URI
            context_list = [metamodel_ctx, add_prefixes_json["@context"]]
        elif isinstance(context, str):  # Some of the older code doesn't do multiple contexts
            context_list = [context]
        elif isinstance(context, tuple):
            context_list = list(context)
        else:
            context_list = context

        # Add context entries for all imported schemas, replicating the self.loaded approach.
        # SchemaLoader populated self.loaded in breadth-first order: direct imports of the
        # main schema first (in listed order), then their transitive dependencies.
        # Local schema references are kept relative; linkml: ones are expanded to full URL.
        visited: set[str] = {self.schemaview.schema.name}
        queue: list[str] = list(self.schemaview.schema.imports)
        while queue:
            imp = queue.pop(0)
            if imp in visited:
                continue
            visited.add(imp)
            imp_schema = self.schemaview.schema_map.get(imp)
            if imp_schema is None:
                continue
            if imp.startswith("linkml:") or "://" in imp:
                ref = str(imp_schema.id)
            else:
                ref = imp
            context_list.append(ref + ".context.jsonld")
            for sub_imp in imp_schema.imports:
                if sub_imp not in visited:
                    queue.append(sub_imp)

        # Absolute file paths have to have a prefix
        for ci in range(0, len(context_list)):
            if isinstance(context_list[ci], str) and context_list[ci].startswith(
                "/"
            ):  # TODO: how do we deal with absolute DOS paths?
                context_list[ci] = "file://" + context_list[ci]

        if self.format == "jsonld":
            self.schema["@context"] = context_list[0] if len(context_list) == 1 and not base_prefix else context_list
            if base_prefix:
                self.schema["@context"].append({"@base": base_prefix})
        # json_obj["@id"] = self.schema.id
        # SchemaLoader strips source_file to basename (schemaloader.py:705).
        # Do this here (after all imports are resolved) rather than in __post_init__,
        # so that SchemaView can still locate imported schemas via source_file during
        # the serialization pipeline.
        if isinstance(self.schema, dict) and "source_file" in self.schema:
            sf = self.schema["source_file"]
            if sf and "://" not in str(sf):
                self.schema["source_file"] = os.path.basename(str(sf))
        elif hasattr(self.schema, "source_file") and self.schema.source_file:
            if "://" not in self.schema.source_file:
                self.schema.source_file = os.path.basename(self.schema.source_file)
        out = str(as_json(self.schema, indent="  ")) + "\n"
        self.schema = self.original_schema
        return out

    def serialize(self, context: Sequence[str] | None = None, context_kwargs: dict | None = None, **kwargs) -> str:
        """
        Serialize the model to JSON-LD

        Args:
            context (str, list[str], None): If ``None``, use context from schema,
                otherwise replace context with this.
            context_kwargs (dict, None): Keyword arguments forwarded to the JSON-LD Context generator
        """
        return super().serialize(context=context, context_kwargs=context_kwargs, **kwargs)


# Option "context" can be specified multiple times.
@shared_arguments(JSONLDGenerator)
@click.command(name="jsonld")
@click.option(
    "--context",
    multiple=True,
    type=click.STRING,
    help=f"JSONLD context file (default: {METAMODEL_CONTEXT_URI} and <model>.prefixes.context.jsonld)",
)
@click.option(
    "--context-kwargs",
    "-k",
    type=(str, bool),
    multiple=True,
    help="kwargs passed to the JSONLD Context generator when instantiated. "
    "Since the context is embedded within the JSON-LD document, "
    "only the boolean instance attributes are formally supported, "
    'e.g. "output" and "base" are not applicable. '
    "The `emit_metadata` value is forced to be False.\n\n"
    "multiple kwargs like `-k {key} {value}` can be passed",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, context_kwargs: list[tuple[str, bool]], context: tuple[str], **kwargs):
    """Generate JSONLD file from LinkML schema.

    Status: incomplete
    """
    if context_kwargs:
        context_kwargs = dict(context_kwargs)
    else:
        context_kwargs = {}

    print(JSONLDGenerator(yamlfile, **kwargs).serialize(context=context, context_kwargs=context_kwargs, **kwargs))


if __name__ == "__main__":
    cli()
