import logging
from copy import copy
from dataclasses import dataclass, field
from enum import unique
from typing import List, Dict

from sqlalchemy import *

from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition, SlotDefinition, Annotation, \
    ClassDefinitionName, Prefix, Definition
from linkml_runtime.utils.formatutils import underscore, camelcase
from linkml_runtime.utils.schemaview import SchemaView


class ForeignKeyPolicy(Enum):
    ALL_REFS_ARE_FKS = "all_refs_are_fks"
    INJECT_FK_FOR_NESTED = "inject_fk_for_nested"
    INJECT_FK_FOR_ALL_REFS = "inject_fk_for_all_refs"

@dataclass
class Link:
    """
    Foreign key reference
    """
    source_class: str
    source_slot: str
    target_class: str
    target_slot: str = None

@dataclass
class RelationalMapping:
    source_class: str = None
    source_slot: str = None
    target_class: str = None
    target_slot: str = None
    uses_join_table: bool = None

def add_attribute(attributes: Dict[str, SlotDefinition], tgt_slot: SlotDefinition) -> None:
    attributes[tgt_slot.name] = tgt_slot

def add_annotation(element: Definition, tag: str, value: str) -> None:
    ann = Annotation(tag, value)
    element.annotations[ann.tag] = ann

@dataclass
class TransformationResult:
    schema: SchemaDefinition
    mappings: List[RelationalMapping]

@dataclass
class RelationalModelTransformer:
    """
    Transforms the source schema into a relational schema
    """

    schemaview: SchemaView = None
    dialect: str = field(default_factory=lambda : 'sqlite')
    skip_tree_root: bool = field(default_factory=lambda: True)
    skip_abstract: bool = field(default_factory=lambda: True)
    skip_mixins: bool = field(default_factory=lambda: True)
    join_table_separator: str = field(default_factory=lambda: '_')
    foreign_key_policy: ForeignKeyPolicy = field(default_factory=lambda: ForeignKeyPolicy.INJECT_FK_FOR_NESTED)

    def transform(self, tgt_schema_name: str = None, top_class: ClassDefinitionName = None) -> TransformationResult:
        """
        Transforms the source schema into a relational schema

        :return:
        """
        links = self.get_reference_map()
        source_sv = self.schemaview
        source = source_sv.schema
        src_schema_name = source.name
        mappings = []
        if tgt_schema_name is None:
            tgt_schema_name = f'{src_schema_name}_relational'
        tgt_schema_id = f'{source.id}_relational'
        target = SchemaDefinition(id=tgt_schema_id,
                                  name=tgt_schema_name,
                                  default_range=source.default_range,
                                  prefixes=source.prefixes,
                                  imports=['linkml:types'],
                                  types=source.types,
                                  subsets=source.subsets,
                                  enums=source.enums)
        target.prefixes['rr'] = Prefix('rr', 'http://www.w3.org/ns/r2rml#')

        # copy source -> target
        # roll-down all slots and create an attribute-only model
        for cn, c in source_sv.all_classes().items():
            c = ClassDefinition(name=cn,
                                class_uri=source_sv.get_uri(c, expand=False),
                                mixin=c.mixin,
                                tree_root=c.tree_root,
                                abstract=c.abstract,
                                description=c.description)
            for slot in source_sv.class_induced_slots(cn):
                tgt_slot = copy(slot)
                #TODO: attrs not indexed
                #tgt_slot.slot_uri = sv.get_uri(slot, expand=False)
                add_attribute(c.attributes, tgt_slot)
            target.classes[c.name] = c

        target_sv = SchemaView(target)
        join_sep = self.join_table_separator
        # create primary keys
        for link in links:
            pk = target_sv.get_identifier_slot(link.target_class)
            if pk is None:
                pk = self.add_primary_key(link.target_class, target_sv)
                #pk = SlotDefinition(name='id', identifier=True)
                #add_attribute(sv.get_class(link.target_class).attributes, pk)
                #sv.set_modified()
                logging.info(f'Added primary key {link.target_class}.{pk.name}, referenced in {link}')
            link.target_slot = pk.name

        # post-process target
        for cn, c in target_sv.all_classes().items():
            links_to_tgt_class = [link for link in links if link.target_class == cn]
            pk_slot = target_sv.get_identifier_slot(cn)
            if self.is_skip(c) and len(links_to_tgt_class) == 0:
                logging.info(f'Skipping class: {c.name}')
                del target.classes[cn]
                continue
            for src_slot in list(c.attributes.values()):
                slot = copy(src_slot)
                slot_range = slot.range
                links_to_range = [link for link in links if link.target_class == slot_range]
                is_only_ref_to_range = len(links_to_range) == 1
                if slot.multivalued:
                    slot.multivalued = False
                    slot_name = slot.name
                    sn_singular = slot.singular_name if slot.singular_name else slot.name
                    if pk_slot is None:
                        pk_slot = self.add_primary_key(c.name, target_sv)
                    backref_slot = SlotDefinition(name=f'{c.name}_id',
                                                  range=c.name,
                                                  slot_uri='rdf:subject',
                                                  #close_mappings=[pk_slot.slot_uri],
                                                  annotations=[Annotation('rdfs:subPropertyOf',
                                                                          'rdf:subject')])
                    if is_only_ref_to_range:
                        # e.g. if Person->Address, and only Person has Address,
                        # we can make Address.Person_id
                        backref_slot.inverse = slot_name
                        backref_class = target.classes[slot_range]
                        add_attribute(backref_class.attributes, backref_slot)
                        mappings.append(RelationalMapping(source_class=cn,
                                                          source_slot=src_slot.name,
                                                          target_class=backref_class.name,
                                                          target_slot=backref_slot.name,
                                                          uses_join_table=False,
                                                          ))
                    else:
                        # create new linking table
                        ann = Annotation(tag='', value='')
                        linker_class = ClassDefinition(name=f'{cn}{join_sep}{sn_singular}',
                                                       from_schema=target.id,
                                                       class_uri='rdf:Statement',
                                                       annotations=[Annotation('linkml:derived_from', cn),
                                                                    Annotation('dcterms:conformsTo','linkml:JoinTable')],
                                                       comments=[f'Generated from {cn}.{slot_name}'])
                        slot.name = sn_singular
                        add_attribute(linker_class.attributes, backref_slot)
                        add_attribute(linker_class.attributes, slot)
                        slot.slot_uri = 'rdf:object'
                        target.classes[linker_class.name] = linker_class
                        mappings.append(RelationalMapping(source_class=cn,
                                                          source_slot=src_slot.name,
                                                          target_class=linker_class.name,
                                                          target_slot=slot.name,
                                                          uses_join_table=True,
                                                          ))
                    # we delete the slot from the set of attributes for the class,
                    # but leave it present as a 'dangling' slot, where it can
                    # be referenced for mapping purposes
                    target.slots[slot_name] = src_slot
                    src_slot.owner = None
                    del c.attributes[slot_name]
            target.classes[c.name] = c

        # add PK and FK anns
        fk_policy = self.foreign_key_policy
        for c in target.classes.values():
            pk_slot = target_sv.get_identifier_slot(c.name)
            for a in list(c.attributes.values()):
                if pk_slot is None or a.name == pk_slot.name:
                    ann = Annotation('primary_key', "true")
                    a.annotations[ann.tag] = ann
                if a.range in target.classes:
                    tc = target.classes[a.range]
                    tc_pk_id = target_sv.get_identifier_slot(tc.name)
                    if (fk_policy == ForeignKeyPolicy.INJECT_FK_FOR_NESTED and a.inlined and not a.multivalued) or \
                        (fk_policy == ForeignKeyPolicy.INJECT_FK_FOR_ALL_REFS):
                        del c.attributes[a.name]
                        add_annotation(a, 'original_slot', a.name)
                        a.alias = f'{a.name}_{tc_pk_id.name}'
                        a.name = a.alias
                        c.attributes[a.name] = a
                    ann = Annotation('foreign_key', f'{tc.name}.{tc_pk_id.name}')
                    a.annotations[ann.tag] = ann

        result = TransformationResult(target, mappings=mappings)
        return result

    def get_reference_map(self) -> List[Link]:
        """
        Extract all class-slot-range references
        :return:
        """
        # TODO: move this to schemaview
        links = []
        sv = self.schemaview
        for cn, c in sv.all_classes().items():
            for slot in sv.class_induced_slots(cn):
                range = slot.range
                if range in sv.all_classes():
                    links.append(Link(source_class=cn,
                                      source_slot=slot.name,
                                      target_class=range))
        return links

    def is_skip(self, c: ClassDefinition) -> bool:
        return (c.abstract and self.skip_abstract) or\
               (c.mixin and self.skip_mixins) or\
               (c.tree_root and self.skip_tree_root)


    # TODO
    def add_primary_key(self, cn: str, sv: SchemaView) -> SlotDefinition:
        pk = SlotDefinition(name='id',
                            identifier=True,
                            range='integer')
        add_annotation(pk, 'dcterms:conformsTo', 'rr:BlankNode')
        add_annotation(pk, 'autoincrement', 'true')
        c = sv.get_class(cn)
        # add PK to start of attributes
        atts = copy(c.attributes)
        c.attributes.clear()    ## See https://github.com/linkml/linkml/issues/370
        add_attribute(c.attributes, pk)  ## add to start
        c.attributes.update(atts)
        sv.set_modified()
        return pk






