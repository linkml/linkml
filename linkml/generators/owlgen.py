"""Generate OWL ontology corresponding to information model

model classes are translated to OWL classes, slots to OWL properties.
"""
import os
from typing import Union, TextIO, Optional, cast
import logging

import click
from rdflib import Graph, URIRef, RDF, OWL, Literal, BNode
from rdflib.collection import Collection
from rdflib.namespace import RDFS, SKOS
from rdflib.plugin import plugins as rdflib_plugins, Parser as rdflib_Parser

from linkml import LOCAL_METAMODEL_YAML_FILE, METAMODEL_NAMESPACE_NAME, METAMODEL_NAMESPACE, METAMODEL_YAML_URI, META_BASE_URI
from linkml_model.meta import ClassDefinitionName, SchemaDefinition, ClassDefinition, SlotDefinitionName, \
    TypeDefinitionName, SlotDefinition, TypeDefinition, Element, EnumDefinitionName
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.schemaloader import SchemaLoader


class ElementDefinition(object):
    pass


class OwlSchemaGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['owl', 'ttl'] + [x.name for x in rdflib_plugins(None, rdflib_Parser) if '/' not in str(x.name)]
    visits_are_sorted = True

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.graph: Optional[Graph] = None
        self.metamodel = SchemaLoader(LOCAL_METAMODEL_YAML_FILE, importmap=kwargs.get('importmap', None),
                                      mergeimports=self.merge_imports) \
            if os.path.exists(LOCAL_METAMODEL_YAML_FILE) else\
            SchemaLoader(METAMODEL_YAML_URI, base_dir=META_BASE_URI, importmap=kwargs.get('importmap', None),
                         mergeimports=self.merge_imports)
        self.metamodel.resolve()
        self.top_value_uri: Optional[URIRef] = None

    def visit_schema(self, output: Optional[str] = None, **_):
        base = URIRef(self.schema.id)
        self.graph = Graph(identifier=base)
        for prefix in self.metamodel.schema.emit_prefixes:
            self.graph.bind(prefix, self.metamodel.namespaces[prefix])

        self.graph.add((base, RDF.type, OWL.Ontology))
        self._add_element_properties(base, self.schema)

        # add the model types
        for name in ['class_definition', 'type_definition', 'slot_definition', 'subset_definition']:
            self._add_metamodel_class(name)

        # add value placeholder
        self.top_value_uri = self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME]['topValue']
        self.graph.add((self.top_value_uri, RDF.type, OWL.DatatypeProperty))
        self.graph.add((self.top_value_uri, RDFS.label, Literal("value")))

    def end_schema(self, output: Optional[str] = None, **_) -> None:
        data = self.graph.serialize(format='turtle' if self.format in ['owl', 'ttl'] else self.format).decode()
        if output:
            with open(output, 'w') as outf:
                outf.write(data)
        else:
            print(data)

    def add_metadata(self, e: SchemaDefinition, uri: URIRef) -> None:
        if e.aliases is not None:
            for s in e.aliases:
                self.graph.add((uri, SKOS.altLabel, Literal(s)))
        if e.mappings is not None:
            for m in e.mappings:
                m_uri = self.namespaces.uri_for(m)
                if m_uri is not None:
                    self.graph.add((uri, SKOS.exactMatch, m_uri))
                else:
                    logging.warning(f'No URI for {m}')
        if e.exact_mappings is not None:
            for m in e.exact_mappings:
                m_uri = self.namespaces.uri_for(m)
                if m_uri is not None:
                    self.graph.add((uri, SKOS.exactMatch, m_uri))
                else:
                    logging.warning(f'No URI for {m}')
        if e.close_mappings is not None:
            for m in e.close_mappings:
                m_uri = self.namespaces.uri_for(m)
                if m_uri is not None:
                    self.graph.add((uri, SKOS.closeMatch, m_uri))
                else:
                    logging.warning(f'No URI for {m}')
        if e.narrow_mappings is not None:
            for m in e.narrow_mappings:
                m_uri = self.namespaces.uri_for(m)
                if m_uri is not None:
                    self.graph.add((uri, SKOS.narrowMatch, m_uri))
                else:
                    logging.warning(f'No URI for {m}')
        if e.broad_mappings is not None:
            for m in e.broad_mappings:
                m_uri = self.namespaces.uri_for(m)
                if m_uri is not None:
                    self.graph.add((uri, SKOS.broadMatch, m_uri))
                else:
                    logging.warning(f'No URI for {m}')
        if e.related_mappings is not None:
            for m in e.related_mappings:
                m_uri = self.namespaces.uri_for(m)
                if m_uri is not None:
                    self.graph.add((uri, SKOS.relatedMatch, m_uri))
                else:
                    logging.warning(f'No URI for {m}')

    def visit_class(self, cls: ClassDefinition) -> bool:
        cls_uri = self._class_uri(cls.name)
        self.add_metadata(cls, cls_uri)
        self.graph.add((cls_uri, RDF.type, OWL.Class))
        self.graph.add((cls_uri, RDF.type,
                        self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase('class definition')]))
        self._add_element_properties(cls_uri, cls)

        # Parent classes
        # TODO: reintroduce this
        # if not cls.defining_slots:
        if True:
            if cls.is_a:
                self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(cls.is_a)))
            if cls.mixin:
                self.graph.add((cls_uri, RDFS.subClassOf, METAMODEL_NAMESPACE.mixin))
            for mixin in sorted(cls.mixins):
                self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(mixin)))
            if cls.name in self.synopsis.applytorefs:
                for appl in sorted(self.synopsis.applytorefs[cls.name].classrefs):
                    self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(appl)))
        else:
            raise NotImplementedError("Defining slots need to be implemented")
            # If defining slots, we generate an equivalentClass entry
            # equ_node = BNode()
            # self.graph.add((cls_uri, OWL.equivalentClass, equ_node))
            # self.graph.add((equ_node, RDF.type, OWL.Class))
            #
            # elts = []
            # if cls.is_a:
            #     elts.append(self._class_uri(cls.is_a))
            # if cls.mixin:
            #     self.graph.add((cls_uri, RDFS.subClassOf, META_NS.mixin))
            # for mixin in cls.mixins:
            #     self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(mixin)))
            # if cls.name in self.synopsis.applytorefs:
            #     for appl in self.synopsis.applytorefs[cls.name].classrefs:
            #         self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(appl)))
            #
            # for slotname in cls.defining_slots:
            #     restr_node = BNode()
            #     slot = self.schema.slots[slotname]
            #
            #     self.graph.add((restr_node, RDF.type, OWL.Restriction))
            #     self.graph.add((restr_node, OWL.onProperty, self._prop_uri(slotname)))
            #     self._add_cardinality(restr_node, slot)
            #     # TODO: fix this
            #     # self.graph.add((restr_node, OWL.someValuesFrom, self._build_range(slot)))
            #     elts.append(restr_node)
            #
            # coll_bnode = BNode()
            # Collection(self.graph, coll_bnode, elts)
            # self.graph.add((equ_node, OWL.intersectionOf, coll_bnode))

        # TODO: see whether unions belong
        # if cls.union_of:
        #     union_node = BNode()
        #     Collection(self.graph, union_coll, [self.class_uri(union_node) for union_node in cls.union_of])
        #     self.graph.add((union_node, OWL.unionOf, union_coll))
        #     self.graph.add((cls_uri, RDFS.subClassOf, union_node))

        for sn in sorted(self.own_slot_names(cls)):
            # Defining_slots are covered above
            if sn not in cls.defining_slots:
                slot = self.schema.slots[sn]
                # Non-inherited slots are annotation properties
                if self.is_slot_object_property(slot):
                    slot_node = BNode()
                    self.graph.add((cls_uri, RDFS.subClassOf, slot_node))

                    #         required multivalued
                    if slot.required:
                        if slot.multivalued:
                            #    y         y     intersectionOf(restriction(slot only type) restriction(slot some type)
                            restr1 = BNode()
                            self.graph.add((restr1, RDF.type, OWL.Restriction))
                            self.graph.add((restr1, OWL.allValuesFrom, self._range_uri(slot)))
                            self.graph.add((restr1, OWL.onProperty, self._prop_uri(self.aliased_slot_name(slot))))

                            restr2 = BNode()
                            self.graph.add((restr2, RDF.type, OWL.Restriction))
                            self.graph.add((restr2, OWL.someValuesFrom, self._range_uri(slot)))
                            self.graph.add((restr2, OWL.onProperty, self._prop_uri(self.aliased_slot_name(slot))))

                            coll_bnode = BNode()
                            Collection(self.graph, coll_bnode, [restr1, restr2])
                            self.graph.add((slot_node, OWL.intersectionOf, coll_bnode))
                            self.graph.add((slot_node, RDF.type, OWL.Class))
                        else:
                            #    y         n      restriction(slot exactly 1 type)
                            self.graph.add((slot_node, RDF.type, OWL.Restriction))
                            self.graph.add((slot_node, OWL.qualifiedCardinality, Literal(1)))
                            self.graph.add((slot_node, OWL.onProperty, self._prop_uri(self.aliased_slot_name(slot))))
                            self.graph.add((slot_node, OWL.onClass, self._range_uri(slot)))
                    else:
                        if slot.multivalued:
                            #    n         y      restriction(slot only type)
                            self.graph.add((slot_node, RDF.type, OWL.Restriction))
                            self.graph.add((slot_node, OWL.allValuesFrom, self._range_uri(slot)))
                            self.graph.add((slot_node, OWL.onProperty, self._prop_uri(self.aliased_slot_name(slot))))
                        else:
                            #    n         n      intersectionOf(restriction(slot only type) restriction(slot max 1 type))
                            self.graph.add((slot_node, RDF.type, OWL.Restriction))
                            self.graph.add((slot_node, OWL.onClass, self._range_uri(slot)))
                            self.graph.add((slot_node, OWL.maxQualifiedCardinality, Literal(1)))
                            self.graph.add((slot_node, OWL.onProperty, self._prop_uri(self.aliased_slot_name(slot))))

        return True


    def visit_slot(self, slot_name: str, slot: SlotDefinition) -> None:
        """ Add a slot definition per slot

        @param slot_name:
        @param slot:
        @return:
        """
        # Note: We use the raw name in OWL and add a subProperty arc
        slot_uri = self._prop_uri(slot.name)
        self._add_element_properties(slot_uri, slot)
        # Inherited slots are object or data properties
        # All others are annotation properties
        self.graph.add((slot_uri, RDF.type, OWL.ObjectProperty if self.is_slot_object_property(slot) else OWL.AnnotationProperty))
        self.graph.add((slot_uri, RDF.type,
                        self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase('slot definition')]))
        self.graph.add((slot_uri, RDFS.range, self._range_uri(slot)))
        if slot.domain:
            self.graph.add((slot_uri, RDFS.domain, self._class_uri(slot.domain)))
        if slot.inverse:
            self.graph.add((slot_uri, OWL.inverseOf, self._prop_uri(slot.inverse)))
        if slot.symmetric:
            self.graph.add((slot_uri, RDF.type, OWL.SymmetricProperty))

        # Parent slots
        if slot.is_a:
            self.graph.add((slot_uri, RDFS.subPropertyOf, self._prop_uri(slot.is_a)))
        for mixin in slot.mixins:
            self.graph.add((slot_uri, RDFS.subPropertyOf, self._prop_uri(mixin)))
        if slot.name in self.synopsis.applytorefs:
            for appl in self.synopsis.applytorefs[slot.name].slotrefs:
                self.graph.add((slot_uri, RDFS.subClassOf, self._prop_uri(appl)))

    def visit_type(self, typ: TypeDefinition) -> None:
        type_uri = self._type_uri(typ.name)
        self.graph.add((type_uri, RDF.type, OWL.Class))
        self.graph.add((type_uri, RDF.type,
                        self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase('type definition')]))
        self._add_element_properties(type_uri, typ)
        if typ.typeof:
            self.graph.add((type_uri, RDFS.subClassOf, self._type_uri(typ.typeof)))
        else:
            restr = BNode()
            self.graph.add((restr, RDF.type, OWL.Restriction))
            self.graph.add((restr, OWL.qualifiedCardinality, Literal(1)))
            self.graph.add((restr, OWL.onProperty, self.top_value_uri))
            self.graph.add((restr, OWL.onDataRange, self.namespaces.uri_for(typ.uri)))
            self.graph.add((type_uri, RDFS.subClassOf, restr))

    def _add_element_properties(self, uri: URIRef, el: Element) -> None:
        for k, v in el.__dict__.items():
            if k in self.metamodel.schema.slots:
                defining_slot = self.metamodel.schema.slots[k]
                if v is not None and 'owl' in defining_slot.in_subset:
                    ve = v if isinstance(v, list) else [v]
                    for e in ve:
                        self.graph.add((uri,
                                        URIRef(self.metamodel.namespaces.uri_for(defining_slot.slot_uri)),
                                        Literal(e)))

    def _add_cardinality(self, subj: Union[BNode, URIRef], slot) -> None:
        """ Add cardinality restrictions to node """
        if slot.required:
            if slot.multivalued:
                self.graph.add((subj, OWL.minCardinality, Literal(1)))
            else:
                self.graph.add((subj, OWL.cardinality, Literal(1)))
        elif not slot.multivalued:
            self.graph.add((subj, OWL.maxCardinality, Literal(1)))

    def _range_uri(self, slot: SlotDefinition) -> URIRef:
        if slot.range in self.schema.types:
            return self._type_uri(TypeDefinitionName(slot.range))
        elif slot.range in self.schema.enums:
            # TODO: enums fill this in
            return self._enum_uri(EnumDefinitionName(slot.range))
        else:
            return self._class_uri(ClassDefinitionName(slot.range))

    def _class_uri(self, cn: ClassDefinitionName) -> URIRef:
        c = self.schema.classes[cn]
        return URIRef(c.definition_uri)

    def _enum_uri(self, en: EnumDefinitionName) -> URIRef:
        # TODO: enums
        e = self.schema.enums[en]
        return URIRef(f"http://UNKNOWN.org/{en}")

    def _prop_uri(self, pn: SlotDefinitionName) -> URIRef:
        p = self.schema.slots.get(pn, None)
        if p is None or p.definition_uri is None:
            return self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][underscore(pn)]
        else:
            return URIRef(p.definition_uri)

    def _type_uri(self, tn: TypeDefinitionName) -> URIRef:
        t = self.schema.types[tn]
        return URIRef(t.definition_uri)

    def _add_metamodel_class(self, cname: str) -> None:
        metac = self.metamodel.schema.classes[cname]
        metac_uri = self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase(metac.name)]
        self.graph.add((metac_uri, RDF.type, OWL.Class))
        self._add_element_properties(metac_uri, metac)


    def is_slot_object_property(self, slot : SlotDefinition) -> bool:
        return True


@shared_arguments(OwlSchemaGenerator)
@click.command()
@click.option("-o", "--output", help="Output file name")
def cli(yamlfile, **kwargs):
    """ Generate an OWL representation of a biolink model """
    print(OwlSchemaGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == '__main__':
    cli()
