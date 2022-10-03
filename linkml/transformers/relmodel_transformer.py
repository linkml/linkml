import logging
from copy import copy
from dataclasses import dataclass, field
from enum import unique
from typing import Dict, List, Optional

from linkml_runtime.linkml_model import (Annotation, ClassDefinition,
                                         ClassDefinitionName, Definition,
                                         Prefix, SchemaDefinition,
                                         SlotDefinition)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView, SlotDefinitionName
from sqlalchemy import *


class RelationalAnnotations(Enum):
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"


class ForeignKeyPolicy(Enum):
    ALL_REFS_ARE_FKS = "all_refs_are_fks"
    INJECT_FK_FOR_NESTED = "inject_fk_for_nested"
    INJECT_FK_FOR_ALL_REFS = "inject_fk_for_all_refs"
    NO_FOREIGN_KEYS = "no_foreign_keys"


@dataclass
class Link:
    """
    Foreign key reference
    """

    source_class: Optional[str]  # optional for top-level slots
    source_slot: str
    target_class: str
    target_slot: str = None


@dataclass
class RelationalMapping:
    """
    Mapping between slot in source model and target in relational model

    Example, with join table created:

        RelationalMapping(source_class='Person',
            source_slot='aliases',
            target_class='Person_aliases',
            target_slot='aliases',
            uses_join_table=True)
    """

    source_class: str = None
    source_slot: str = None
    mapping_type: str = None
    target_class: str = None
    target_slot: str = None  # /
    join_class: str = None  # /
    uses_join_table: bool = None  # /  ## True if extra join table is created


@dataclass
class OneToAnyMapping(RelationalMapping):
    """
    A one-to-one or one-to-many mapping from a source class+slot to
    a target class+slot
    """

    target_class: str = None
    target_slot: str = None
    multivalued: bool = False


@dataclass
class ManyToManyMapping(RelationalMapping):
    """
    A many-to-many relationship introduces a join class/table

    See:

    - https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#relationships-many-to-many
    - https://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
    """

    join_class: str = None  # aka secondary
    target_class: str = None  # actual target
    mapping_type: str = "ManyToMany"


@dataclass
class MultivaluedScalar(RelationalMapping):
    """
    See: https://docs.sqlalchemy.org/en/14/orm/extensions/associationproxy.html
    """

    join_class: str = None
    target_slot: str = None
    mapping_type: str = "MultivaluedScalar"


def add_attribute(
    attributes: Dict[str, SlotDefinition], tgt_slot: SlotDefinition
) -> None:
    attributes[tgt_slot.name] = tgt_slot


def add_annotation(element: Definition, tag: str, value: str) -> None:
    ann = Annotation(tag, value)
    element.annotations[ann.tag] = ann


def get_primary_key_attributes(cls: ClassDefinition) -> List[SlotDefinitionName]:
    return [
        a.name
        for a in cls.attributes.values()
        if RelationalAnnotations.PRIMARY_KEY in a.annotations
    ]


def get_foreign_key_map(cls: ClassDefinition) -> Dict[SlotDefinitionName, str]:
    return {
        a.name: a.annotations[RelationalAnnotations.FOREIGN_KEY].value
        for a in cls.attributes.values()
        if RelationalAnnotations.FOREIGN_KEY in a.annotations
    }


@dataclass
class TransformationResult:
    """
    The result of a transformation is a target schema plus a collection of mappings
    """

    schema: SchemaDefinition
    mappings: List[RelationalMapping]


@dataclass
class RelationalModelTransformer:
    """
    Transforms the source schema into a relational schema
    """

    schemaview: SchemaView = None
    # dialect: str = field(default_factory=lambda : 'sqlite')
    skip_tree_root: bool = field(default_factory=lambda: False)
    skip_abstract: bool = field(default_factory=lambda: True)
    skip_mixins: bool = field(default_factory=lambda: True)
    join_table_separator: str = field(default_factory=lambda: "_")
    foreign_key_policy: ForeignKeyPolicy = field(
        default_factory=lambda: ForeignKeyPolicy.INJECT_FK_FOR_NESTED
    )

    def transform(
        self, tgt_schema_name: str = None, top_class: ClassDefinitionName = None
    ) -> TransformationResult:
        """
        Transforms the source schema into a relational schema

        :param tgt_schema_name:
        :param top_class:
        :return:
        """
        join_sep = self.join_table_separator
        links = self.get_reference_map()
        source_sv = self.schemaview
        source_sv.merge_imports()
        source = source_sv.schema
        src_schema_name = source.name
        mappings = []
        if tgt_schema_name is None:
            tgt_schema_name = f"{src_schema_name}_relational"
        tgt_schema_id = f"{source.id}_relational"
        # TODO: recursively transform imports
        target = SchemaDefinition(
            id=tgt_schema_id,
            name=tgt_schema_name,
            default_range=source.default_range,
            prefixes=source.prefixes,
            imports=source.imports,
            # imports=['linkml:types'],
            from_schema=source.from_schema,
            source_file=source.source_file,
            types=source.types,
            subsets=source.subsets,
            enums=source.enums,
        )
        target.prefixes["rr"] = Prefix("rr", "http://www.w3.org/ns/r2rml#")

        # copy source -> target
        # roll-down all slots and create an attribute-only model
        for cn, c in source_sv.all_classes().items():
            c = ClassDefinition(
                name=cn,
                class_uri=source_sv.get_uri(c, expand=False),
                mixin=c.mixin,
                is_a=c.is_a,
                tree_root=c.tree_root,
                abstract=c.abstract,
                description=c.description,
            )
            for slot in source_sv.class_induced_slots(cn):
                tgt_slot = copy(slot)
                if slot.alias:
                    tgt_slot.name = slot.alias
                # TODO: attrs not indexed
                # tgt_slot.slot_uri = sv.get_uri(slot, expand=False)
                tgt_slot.is_a = None
                tgt_slot.mixins = []
                add_attribute(c.attributes, tgt_slot)
            # this is required in case an attribute inherits from a slot
            for sn in source_sv.all_slots(attributes=False):
                slot = source_sv.get_slot(sn)
                # target.slots[slot.name] = copy(slot)
            target.classes[c.name] = c

        target_sv = SchemaView(target)
        # create surrogate/autoincrement primary keys for any class (originally: that is referenced)
        # for link in links:
        for cn in target_sv.all_classes():
            pk = self.get_direct_identifier_attribute(target_sv, cn)
            if self.foreign_key_policy == ForeignKeyPolicy.NO_FOREIGN_KEYS:
                logging.info(
                    f"Will not inject any PKs, and policy == {self.foreign_key_policy}"
                )
            else:
                if pk is None:
                    pk = self.add_primary_key(cn, target_sv)
                    logging.info(f"Added primary key {cn}.{pk.name}")
                for link in links:
                    if link.target_class == cn:
                        link.target_slot = pk.name

        # TODO: separate out the logic into separate testable methods
        target_sv.set_modified()
        # post-process target schema
        for cn, c in target_sv.all_classes().items():
            if self.foreign_key_policy == ForeignKeyPolicy.NO_FOREIGN_KEYS:
                continue
            incoming_links = [link for link in links if link.target_class == cn]
            pk_slot = self.get_direct_identifier_attribute(target_sv, cn)
            # if self.is_skip(c) and len(incoming_links) == 0:
            #    logging.info(f'Skipping class: {c.name}')
            #    del target.classes[cn]
            #    continue
            for src_slot in list(c.attributes.values()):
                slot = copy(src_slot)
                slot_range = slot.range
                slot_range_is_class = slot_range in target_sv.all_classes()
                links_to_range = [
                    link for link in links if link.target_class == slot_range
                ]
                is_only_ref_to_range = len(links_to_range) == 1
                is_shared = slot_range_is_class and (
                    slot.inlined or slot.inlined_as_list or "shared" in slot.annotations
                )
                if slot.multivalued:
                    slot.multivalued = False
                    slot_name = slot.name
                    sn_singular = (
                        slot.singular_name if slot.singular_name else slot.name
                    )
                    if pk_slot is None:
                        pk_slot = self.add_primary_key(c.name, target_sv)
                    backref_slot = SlotDefinition(
                        name=f"{c.name}_{pk_slot.name}",
                        description=f"Autocreated FK slot",
                        range=c.name,
                        slot_uri="rdf:subject",
                        # close_mappings=[pk_slot.slot_uri],
                        annotations=[
                            Annotation("backref", "true"),
                            Annotation("rdfs:subPropertyOf", "rdf:subject"),
                        ],
                    )
                    # if is_only_ref_to_range and slot_range_is_class:
                    if is_shared:
                        # ONE-TO-MANY
                        # e.g. if Person->Address, and only Person has Address,
                        # we can make Address.Person_id
                        backref_slot.inverse = slot_name
                        backref_class = target.classes[slot_range]
                        add_attribute(backref_class.attributes, backref_slot)
                        # In SQLA, corresponds to source_class.source_slot = relationship(target_class)
                        mappings.append(
                            OneToAnyMapping(
                                source_class=cn,
                                source_slot=src_slot.name,
                                target_class=backref_class.name,
                                target_slot=backref_slot.name,
                            )
                        )
                    else:
                        # MANY-TO-MANY
                        # create new linking table
                        linker_class = ClassDefinition(
                            name=f"{cn}{join_sep}{sn_singular}",
                            from_schema=target.id,
                            class_uri="rdf:Statement",
                            annotations=[
                                Annotation("linkml:derived_from", cn),
                                Annotation("dcterms:conformsTo", "linkml:JoinTable"),
                            ],
                            comments=[f"Linking class generated from {cn}.{slot_name}"],
                        )
                        slot.name = sn_singular
                        add_attribute(linker_class.attributes, backref_slot)
                        add_attribute(linker_class.attributes, slot)
                        slot.slot_uri = "rdf:object"
                        target.classes[linker_class.name] = linker_class
                        if slot_range_is_class:
                            fwdann = Annotation("forwardref", "true")
                            slot.annotations[fwdann.tag] = fwdann
                            mappings.append(
                                ManyToManyMapping(
                                    source_class=cn,
                                    source_slot=src_slot.name,
                                    target_class=slot_range,
                                    # target_slot=backref_slot.name,
                                    join_class=linker_class.name,
                                    # target_slot=slot.name,
                                    # uses_join_table=True,
                                )
                            )
                        else:
                            mappings.append(
                                MultivaluedScalar(
                                    source_class=cn,
                                    source_slot=src_slot.name,
                                    target_slot=slot.name,
                                    join_class=linker_class.name,
                                )
                            )
                    # we delete the slot from the set of attributes for the class,
                    # but leave it present as a 'dangling' slot, where it can
                    # be referenced for mapping purposes
                    target.slots[slot_name] = src_slot
                    src_slot.owner = None
                    del c.attributes[slot_name]
                    target_sv.set_modified()
            target.classes[c.name] = c

        # add PK and FK anns
        target_sv.set_modified()
        fk_policy = self.foreign_key_policy
        for c in target.classes.values():
            if self.foreign_key_policy == ForeignKeyPolicy.NO_FOREIGN_KEYS:
                continue
            pk_slot = target_sv.get_identifier_slot(c.name)
            for a in list(c.attributes.values()):
                if pk_slot is None or a.name == pk_slot.name:
                    ann = Annotation("primary_key", "true")
                    a.annotations[ann.tag] = ann
                if a.range in target.classes:
                    tc = target.classes[a.range]
                    # tc_pk_slot = target_sv.get_identifier_slot(tc.name)
                    tc_pk_slot = self.get_direct_identifier_attribute(
                        target_sv, tc.name
                    )
                    if tc_pk_slot is None:
                        raise ValueError(
                            f"No PK for attribute {a.name} range {a.range}"
                        )
                    is_inlined = a.inlined or not source_sv.get_identifier_slot(tc.name)
                    if (
                        fk_policy == ForeignKeyPolicy.INJECT_FK_FOR_NESTED
                        and is_inlined
                        and not a.multivalued
                    ) or (fk_policy == ForeignKeyPolicy.INJECT_FK_FOR_ALL_REFS):
                        # if it is already an injected backref, no need to re-inject
                        if "backref" not in a.annotations:
                            del c.attributes[a.name]
                            if "forwardref" not in a.annotations:
                                add_annotation(a, "original_slot", a.name)
                            a.alias = f"{a.name}_{tc_pk_slot.name}"
                            a.name = a.alias
                            c.attributes[a.name] = a
                    ann = Annotation("foreign_key", f"{tc.name}.{tc_pk_slot.name}")
                    a.annotations[ann.tag] = ann
                    target_sv.set_modified()

        result = TransformationResult(target, mappings=mappings)
        return result

    def get_direct_identifier_attribute(
        self, sv: SchemaView, cn: ClassDefinitionName
    ) -> Optional[SlotDefinition]:
        c = sv.get_class(cn)
        for a in c.attributes.values():
            if a.identifier:
                return a
            if a.key:
                return a
        return None

    def get_reference_map(self) -> List[Link]:
        """
        Extract all class-slot-range references

        :return: list of links
        """
        # TODO: move this to schemaview
        links = []
        sv = self.schemaview
        for cn, c in sv.all_classes().items():
            for slot in sv.class_induced_slots(cn):
                if slot.range in sv.all_classes():
                    links.append(
                        Link(
                            source_class=cn,
                            source_slot=slot.name,
                            target_class=slot.range,
                        )
                    )
        for sn, slot in sv.all_slots().items():
            if slot.range in sv.all_classes():
                links.append(
                    Link(
                        source_class=None,
                        source_slot=slot.name,
                        target_class=slot.range,
                    )
                )
        return links

    def is_skip(self, c: ClassDefinition) -> bool:
        return (
            (c.abstract and self.skip_abstract)
            or (c.mixin and self.skip_mixins)
            or (c.tree_root and self.skip_tree_root)
        )

    def add_primary_key(self, cn: str, sv: SchemaView) -> SlotDefinition:
        """
        Adds a surrogate/autoincrement primary key to a class

        :param cn:
        :param sv:
        :return:
        """
        pk = SlotDefinition(name="id", identifier=True, range="integer")
        add_annotation(pk, "dcterms:conformsTo", "rr:BlankNode")
        add_annotation(pk, "autoincrement", "true")
        c = sv.get_class(cn)
        if pk.name in c.attributes:
            raise ValueError(
                f"Cannot inject primary key {pk.name} as a non-unique attribute with this name already exists in {cn}"
            )
        # add PK to start of attributes
        atts = copy(c.attributes)
        c.attributes.clear()  ## See https://github.com/linkml/linkml/issues/370
        add_attribute(c.attributes, pk)  ## add to start
        c.attributes.update(atts)
        sv.set_modified()
        return pk
