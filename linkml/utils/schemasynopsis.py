from dataclasses import dataclass, field
from typing import Dict, Set, List, Union, cast
import logging

from rdflib import URIRef

from linkml_runtime.linkml_model.meta import SchemaDefinition, Element, Definition, ClassDefinition, SlotDefinitionName, \
    ClassDefinitionName, TypeDefinitionName, DefinitionName, SlotDefinition, ElementName, TypeDefinition, \
    SubsetDefinitionName, EnumDefinitionName, EnumDefinition
from linkml_runtime.utils.metamodelcore import empty_dict
from linkml.utils.typereferences import RefType, ClassType, TypeType, SlotType, References, SubsetType, EnumType
from linkml_runtime.utils.yamlutils import TypedNode


def empty_references() -> field:
    return field(default_factory=References)


ClassOrSlotName = Union[ClassDefinitionName, TypeDefinitionName]


@dataclass
class SchemaSynopsis:
    schema: SchemaDefinition = field(repr=False, compare=False)

    # References by type -- set by add_ref
    typerefs: Dict[TypeDefinitionName, References] = empty_dict()       # Type name to all references
    slotrefs: Dict[SlotDefinitionName, References] = empty_dict()       # Slot name to all references
    classrefs: Dict[ClassDefinitionName, References] = empty_dict()     # Class name to all references
    subsetrefs: Dict[SubsetDefinitionName, References] = empty_dict()   # Subset name to references
    enumrefs: Dict[EnumDefinitionName, References] = empty_dict()       # Enum name to references

    # Type specific
    typebases: Dict[str, Set[TypeDefinitionName]] = empty_dict()          # Base referencing types (direct and indirect)
    typeofs: Dict[TypeDefinitionName, TypeDefinitionName] = empty_dict()  # Type to specializations

    # Slot specific
    slotclasses: Dict[SlotDefinitionName, Set[ClassDefinitionName]] = empty_dict()    # Slot to including classes
    definingslots: Dict[SlotDefinitionName, Set[ClassDefinitionName]] = empty_dict()  # Slot to defining decls
    slotusages: Dict[SlotDefinitionName, Set[ClassDefinitionName]] = empty_dict()     # Slot to overriding classes
    owners: Dict[SlotDefinitionName, Set[ClassDefinitionName]] = empty_dict()         # Slot to owning classes (sb. 1)
    inverses: Dict[str, Set[str]] = empty_dict()                        # Slots declared as inverses of other slots

    # Class specific
    ownslots: Dict[ClassDefinitionName, Set[SlotDefinitionName]] = empty_dict() # Slots directly owned by class

    # Enum specific
    codesets: Dict[URIRef, Set[EnumDefinitionName]] = empty_dict()  # Code set URI to enumeration definition

    # Class to slot domains == class.slots

    # Slot or Class (Definition) specific
    roots: References = empty_references()                      # Definitions with no parents
    isarefs: Dict[DefinitionName, References] = empty_dict()    # Definition to isa references
    mixinrefs: Dict[DefinitionName, References] = empty_dict()  # Mixin to referencing classes or slots
    mixins: References = empty_references()                     # Definitions declared as mixin
    abstracts: References = empty_references()                  # Definitions declared as abstract
    applytos: References = empty_references()                   # Definitions that include applytos
    applytorefs: Dict[DefinitionName, References] = empty_dict()  # Definition to applyier

    # Slot or Type specific
    rangerefs: Dict[ElementName, Set[SlotDefinitionName]] = empty_dict()  # Type or class to range slot

    # Element - any type
    inschema: Dict[str, References] = empty_references()        # Schema name to elements

    def __post_init__(self):
        for k, v in self.schema.slots.items():
            self.summarize_slot_definition(k, v)
        for k, v in self.schema.types.items():
            self.summarize_type_definition(k, v)
        for k, v in self.schema.classes.items():
            self.summarize_class_definition(k, v)
        for k, v in self.schema.enums.items():
            self.summarize_enum_definition(k, v)

        # Generate a list of slots owned exclusively by cls
        for cls in self.schema.classes.values():
            non_owned_slots = set()
            if cls.is_a:
                non_owned_slots = set(self.schema.classes[cls.is_a].slots)
            for mixin in cls.mixins:
                non_owned_slots.update(set(self.schema.classes[mixin].slots))
            owned_slots = set(cls.slots) - non_owned_slots
            self.ownslots[cls.name] = set(cls.slots) - non_owned_slots
            for slotname in owned_slots:
                self.owners.setdefault(slotname, set()).add(cls.name)


    def summarize_slot_definition(self, k: SlotDefinitionName, v: SlotDefinition) -> None:
        """
        Summarize a slot definition
        :param k: slot name
        :param v: slot definition
        :return:
        """
        self.summarize_definition(SlotType, k, v)
        if v.domain:
            self.add_ref(SlotType, k, ClassType, v.domain)
        self.rangerefs.setdefault(v.range, set()).add(k)
        self.add_ref(SlotType, k, ClassType if v.range in self.schema.classes else
                                  EnumType if v.range in self.schema.enums else
                                  TypeType if v.range in self.schema.types else None, v.range)

    def summarize_type_definition(self, k: TypeDefinitionName, v: TypeDefinition):
        """
        Summarize type definition

        :param k: Type name
        :param v: Type definition
        :return:
        """
        self.summarize_element(TypeType, k, v)
        if v.typeof:
            self.typeofs.setdefault(v.typeof, set()).add(k)
            self.add_ref(TypeType, k, TypeType, v.typeof)
        if v.base:
            self.typebases.setdefault(v.base, set()).add(k)

    def summarize_class_definition(self, k: ClassDefinitionName, v: ClassDefinition) -> None:
        """
        Summarize class definition element

        :param k: Class name
        :param v: Class definition
        :return:
        """
        self.summarize_definition(ClassType, k, v)
        for slotname in v.slots:
            self.add_ref(ClassType, k, SlotType, slotname)
        for slotname, usage in v.slot_usage.items():
            self.slotusages.setdefault(slotname, set()).add(k)
            # self.add_ref(ClassType, k, SlotType, slotname)
            # slot_alias = self.schema.slots[slotname].alias
            # if slot_alias:
            #     self.add_ref(SlotType, slotname, SlotType, cast(SlotDefinitionName, slot_alias))
            #     self.add_ref(ClassType, k, SlotType, cast(SlotDefinitionName, slot_alias))

    def summarize_enum_definition(self, k: EnumDefinitionName, v: EnumDefinition):
        """
        Summarize enum definition

        :param k: Enum name
        :param v: Enum definition
        :return:
        """
        self.summarize_element(EnumType, k, v)


    def summarize_definition(self, typ: RefType, k: DefinitionName, v: Definition) -> None:
        """
        Summarize slot and class definitions

        :param typ: type (slot or class)
        :param k: name
        :param v: definition
        :return:
        """
        self.summarize_element(typ, k, v)
        if v.is_a:
            self.isarefs.setdefault(v.is_a, References()).addref(typ, k)
            self.add_ref(typ, k, typ, v.is_a)
        else:
            self.roots.addref(typ, k)
        if v.abstract:
            self.abstracts.addref(typ, k)
        if v.mixin:
            self.mixins.addref(typ, k)
        for mixin in v.mixins:
            self.mixinrefs.setdefault(mixin, References()).addref(typ, k)
            self.add_ref(typ, k, typ, mixin)
        if v.apply_to:
            self.applytos.addref(typ, k)
        for applyto in v.apply_to:
            self.applytorefs.setdefault(applyto, References()).addref(typ, k)
            self.add_ref(typ, k, typ, applyto)

    def summarize_element(self, typ: RefType, k: ElementName, v: Element) -> None:
        """
         Summarize element level items

        :param typ: element type
        :param k: element name
        :param v: element deffinition
        :return:
        """
        if k != v.name:
            raise ValueError("{typ} name mismatch: {k} != {v.name}")        # should never happen
        for subset in v.in_subset:
            self.add_ref(typ, k, SubsetType, subset)

    def add_ref(self, fromtype: RefType, fromname: ElementName, totype: RefType, toname: ElementName, ) -> None:
        """ Add an inverse reference, indicating that to type/name is referenced by from type/name

        :param fromtype: Referencer type
        :param fromname: Referencer name
        :param totype: Referencee type
        :param toname: Referencee name
        :return:
        """
        if totype is ClassType:
            self.classrefs.setdefault(ClassDefinitionName(toname), References()).addref(fromtype, fromname)
        elif totype is SlotType:
            self.slotrefs.setdefault(SlotDefinitionName(toname), References()).addref(fromtype, fromname)
        elif totype is TypeType:
            self.typerefs.setdefault(TypeDefinitionName(toname), References()).addref(fromtype, fromname)
        elif totype is SubsetType:
            self.subsetrefs.setdefault(SubsetDefinitionName(toname), References()).addref(fromtype, fromname)
        elif totype is EnumType:
            self.enumrefs.setdefault(SlotDefinitionName(toname), References()).addref(fromtype, fromname)
        else:
            raise TypeError("Unknown typ: {typ}")

    def _ancestor_is_owned(self, slot: SlotDefinition) -> bool:
        return bool(slot.is_a) and (slot.is_a in self.owners or self._ancestor_is_owned(self.schema.slots[slot.is_a]))

    def errors(self) -> List[str]:
        def format_undefineds(refs: Set[Union[str, TypedNode]]) -> List[str]:
            return [f'{TypedNode.yaml_loc(ref)}: {ref}' for ref in refs]

        rval = []
        undefined_classes = set(self.classrefs.keys()) - set(self.schema.classes.keys())
        if undefined_classes:
            rval += [f"\tUndefined class references: "
                     f"{', '.join(format_undefineds(undefined_classes))}"]
        undefined_slots = set(self.slotrefs.keys()) - set(self.schema.slots.keys())
        if undefined_slots:
            rval += [f"\tUndefined slot references: "
                     f"{', '.join(format_undefineds(undefined_slots))}"]
        undefined_types = set(self.typerefs.keys()) - set(self.schema.types.keys())
        if undefined_types:
            rval += [f"\tUndefined type references: "
                     f"{', '.join(format_undefineds(undefined_types))}"]
        undefined_subsets = set(self.subsetrefs.keys()) - set(self.schema.subsets.keys())
        if undefined_subsets:
            rval += [f"\tUndefined subset references: "
                     f"{', '.join(format_undefineds(undefined_subsets))}"]
        undefined_enums = set(self.enumrefs.keys()) - set(self.schema.enums.keys())
        if undefined_enums:
            rval += [f"\tUndefined enun references: "
                     f"{', '.join(format_undefineds(undefined_enums))}"]

        # Inlined slots must be multivalued (not a inviolable rule, but we make assumptions about this elsewhere in
        # the python generator
        for slot in self.schema.slots.values():
            if slot.inlined and not slot.multivalued and slot.identifier:
                rval += [f'\t{TypedNode.yaml_loc(slot.name)} Slot {slot.name} is declared inline but single valued']
        return rval

    def summary(self) -> str:

        def summarize_refs(refs: Dict[ElementName, References]) -> str:
            clsrefs, slotrefs, typerefs, enumrefs = set(), set(), set(), set()
            if refs is not None:
                for cr in refs.values():
                    clsrefs.update(cr.classrefs)
                    slotrefs.update(cr.slotrefs)
                    typerefs.update(cr.typerefs)
                    enumrefs.update(cr.enumrefs)
            return f"\tReferenced by: {len(clsrefs)} classes, {len(slotrefs)} slots, " \
                   f"{len(typerefs)} types, {len(enumrefs)} enums "

        def recurse_types(typ: TypeDefinitionName, indent: str='\t\t\t') -> List[str]:
            rval = [f"{indent}{typ}" + (':' if typ in self.typeofs else '')]
            if typ in sorted(self.typeofs):
                for tr in sorted(self.typeofs[typ]):
                    rval += recurse_types(tr, indent + '\t')
            return rval

        rval = ['']
        rval += [f"Classes: {len(self.schema.classes.keys())}"]
        rval += [summarize_refs(self.classrefs)]

        rval += [f"\tRoot: {len(self.roots.classrefs)}"]
        leaves = set(self.classrefs.keys()) - set(self.isarefs.keys())
        rval += [f"\tLeaf: {len(leaves)}"]
        # Standalone ar classes that are both roots and leaves
        rval += [f"\tStandalone: {len(set(self.roots.classrefs).union(set(leaves)))}"]
        rval += [f"\tDeclared mixin: {len(self.mixins.classrefs)}"]
        undeclared_mixins = set(self.mixinrefs.keys())\
            .intersection(set(self.schema.classes.keys()) - set(self.mixins.classrefs))
        rval += [f"\tUndeclared mixin: {len(undeclared_mixins)}"]
        if undeclared_mixins:
            for udm in sorted(undeclared_mixins):
                rval += [f"\t\t{udm}"]
        rval += [f"\tAbstract: {len(self.abstracts.classrefs)}"]
        undefined_classes = set(self.classrefs.keys()) - set(self.schema.classes.keys())
        if undefined_classes:
            rval += [f"\tUndefined references: {', '.join(undefined_classes)}"]

        rval += ['']
        rval += [f"Slots: {len(self.schema.slots.keys())}"]
        rval += [summarize_refs(self.slotrefs)]
        rval += [f"\tRoot: {len(self.roots.slotrefs)}"]
        leaves = set(self.slotrefs.keys()) - set(self.isarefs.keys())
        rval += [f"\tLeaf: {len(leaves)}"]
        rval += [f"\tStandalone: {len(set(self.roots.classrefs).union(set(leaves)))}"]
        rval += [f"\tDeclared mixin: {len(self.mixins.slotrefs)}"]
        undeclared_mixins = set(self.mixinrefs.keys()) \
            .intersection(set(self.schema.slots.keys()) - set(self.mixins.slotrefs))
        rval += [f"\tUndeclared mixin: {len(undeclared_mixins)}"]
        if undeclared_mixins:
            for udm in sorted(undeclared_mixins):
                rval += [f"\t\t{udm}"]
        rval += [f"\tAbstract: {len(self.abstracts.slotrefs)}"]

        # Slots that are referenced but not defined
        undefined_slots = set(self.slotrefs.keys()) - set(self.schema.slots.keys())
        if undefined_slots:
            rval += [f"\tUndefined: {len(undefined_slots)}"]

        # Slots that are defined but do not (directly) occur in any class
        n_unreferenced_descendants: int = 0
        unowned_slots: Set[SlotDefinitionName] = set()
        for slotname, slot in sorted(self.schema.slots.items(), key=lambda e: e[0]):
            if slotname not in self.owners:
                if slot.domain:
                    if self._ancestor_is_owned(slot):
                        n_unreferenced_descendants += 1
                    else:
                        unowned_slots.add(slotname)
        if n_unreferenced_descendants:
            rval += [f"\tUnreferenced descendants of owned slots: {n_unreferenced_descendants}"]
        if unowned_slots:
            rval += [f"\t* Unowned slots: {', '.join(sorted(unowned_slots))}"]


        not_in_domain: Set[SlotDefinitionName] = set()
        domain_mismatches: Set[SlotDefinitionName] = set()
        unkdomains: Set[SlotDefinitionName] = set()
        emptydomains: Set[SlotDefinitionName] = set()

        for slot in self.schema.slots.values():
            if not slot.domain:
                emptydomains.add(slot.name)
            elif slot.domain in self.schema.classes:
                if slot.name in self.schema.classes[slot.domain].slots:
                    pass
                elif slot.name not in self.slotclasses:
                    not_in_domain.add(slot.name)
                else:
                    domain_mismatches.add(slot.name)
            else:
                unkdomains.add(f"{slot.name}: {slot.domain}")
        if not_in_domain:
            rval += [f"\tNot in domain: {len(not_in_domain)}"]
            rval += ["\t\tslot.name: slot.domain"]
            rval += ["\t\t---------  -----------"]
            for slotname in sorted(not_in_domain):
                rval.append(f'\t\t"{slotname}": "{self.schema.slots[slotname].domain}"')
        if domain_mismatches:
            rval += [f"\t\tMismatches: {len(domain_mismatches)}"]
            for slotname in sorted(domain_mismatches):
                rval.append(f'\t\t\tSlot: "{slotname}" declared domain: "{self.schema.slots[slotname].domain}" '
                            f'actual domain(s): {", ".join(self.slotclasses[slotname])}')
        if unkdomains:
            rval += [f"\t* Unknown domain: {', '.join(sorted(unkdomains))}"]
        if emptydomains:
            rval += [f"\tDomain unspecified: {len(emptydomains)}"]

        rval += ["\tRanges:"]
        rval += ["\t\tType:"]
        for rng, slots in sorted(self.rangerefs.items()):
            if rng in self.schema.types:
                rval += [f"\t\t\t{rng}: {len(slots)}"]
        rval += ["\t\tClass:"]
        for rng, slots in sorted(self.rangerefs.items()):
            if rng in self.schema.classes:
                rval += [f"\t\t\t{rng}: {len(slots)}"]
        unknowns = []
        for rng, slots in sorted(self.rangerefs.items()):
            if rng not in self.schema.types and rng not in self.schema.classes:
                unknowns += [f"\t\t\t{rng}: {len(slots)}"]
        if unknowns:
            rval += ["\t\tUnknown:"] + unknowns

        shared_class_slots = set(self.schema.classes.keys()).intersection(set(self.schema.slots.keys()))
        if shared_class_slots:
            rval += ["\nClasses and Slots with the same name:"]
            for ssc in sorted(shared_class_slots):
                rval += [f"\t{ssc}"]

        rval += ['']
        rval += [f"Types: {len(self.schema.types)}"]
        rval += [summarize_refs(self.typerefs)]
        rval += ["\tBases:"]
        for base in sorted(self.typebases.keys()):
            rval += [f"\t\t{base}:"]
            for typ in sorted(self.typebases[base]):
                if not self.schema.types[typ].typeof:
                    rval += recurse_types(typ)

        return '\n'.join(rval)

