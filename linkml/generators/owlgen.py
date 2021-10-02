"""Generate OWL ontology corresponding to information model

model classes are translated to OWL classes, slots to OWL properties.
"""
import os
from typing import Union, TextIO, Optional, cast
import logging

import click
from rdflib import Graph, URIRef, RDF, OWL, Literal, BNode
from rdflib.collection import Collection
from rdflib.namespace import RDFS, SKOS, DCTERMS
from rdflib.plugin import plugins as rdflib_plugins, Parser as rdflib_Parser

from linkml import LOCAL_METAMODEL_YAML_FILE, METAMODEL_NAMESPACE_NAME, METAMODEL_NAMESPACE, METAMODEL_YAML_URI, META_BASE_URI
from linkml_runtime.linkml_model.meta import ClassDefinitionName, SchemaDefinition, ClassDefinition, SlotDefinitionName, \
    TypeDefinitionName, SlotDefinition, TypeDefinition, Element, EnumDefinitionName, Definition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.schemaloader import SchemaLoader


class ElementDefinition(object):
    pass


class OwlSchemaGenerator(Generator):
    """
    Generates a schema-oriented OWL representation of a LinkML model

    `OWL Generator Docs <https://linkml.io/linkml/generators/owl>`_

    Attributes:
        type_objects    if True, represent TypeDefinitions as objects; if False, as literals
        metaclasses     if True, include OWL representations of ClassDefinition, SlotDefinition, etc. Introduces punning
    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['owl', 'ttl'] + [x.name for x in rdflib_plugins(None, rdflib_Parser) if '/' not in str(x.name)]
    visits_are_sorted = True

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], ontology_uri_suffix: str=None,
                 type_objects=True,
                 metaclasses=True,
                 add_ols_annotations=True,
                 **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.graph: Optional[Graph] = None
        self.metamodel = SchemaLoader(LOCAL_METAMODEL_YAML_FILE, importmap=kwargs.get('importmap', None),
                                      mergeimports=self.merge_imports) \
            if os.path.exists(LOCAL_METAMODEL_YAML_FILE) else\
            SchemaLoader(METAMODEL_YAML_URI, base_dir=META_BASE_URI, importmap=kwargs.get('importmap', None),
                         mergeimports=self.merge_imports)
        self.metamodel.resolve()
        self.emit_prefixes: Set[str] = set()
        self.top_value_uri: Optional[URIRef] = None
        self.ontology_uri_suffix = ontology_uri_suffix
        self.type_objects = type_objects
        self.metaclasses = metaclasses
        self.add_ols_annotations = add_ols_annotations

    def visit_schema(self, output: Optional[str] = None, **_):
        owl_id = self.schema.id
        if self.ontology_uri_suffix:
            owl_id = f'{owl_id}{self.ontology_uri_suffix}'
        base = URIRef(owl_id)
        self.graph = Graph(identifier=base)
        for prefix in self.metamodel.schema.emit_prefixes:
            self.graph.bind(prefix, self.metamodel.namespaces[prefix])
        for pfx in self.schema.prefixes.values():
            self.graph.namespace_manager.bind(pfx.prefix_prefix, URIRef(pfx.prefix_reference))

        self.graph.add((base, RDF.type, OWL.Ontology))
        self._add_element_properties(base, self.schema)

        if self.metaclasses:
            # add the model types; these will be instantiated under each individual visitor node
            for name in ['class_definition', 'type_definition', 'slot_definition', 'subset_definition']:
                self._add_metamodel_class(name)

        # add value placeholder
        if self.type_objects:
            # TODO: additional axioms, e.g. String subClassOf hasValue some string
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

    def add_metadata(self, e: Definition, uri: URIRef) -> None:
        """
        Add generic annotation properties

        :param e: schema element
        :param uri: URI representation of schema element
        :return:
        """
        # TODO: use metamodel annotations to drive this rather than hardcoding
        if e.aliases is not None:
            for s in e.aliases:
                self.graph.add((uri, SKOS.altLabel, Literal(s)))
        if e.title is not None:
            self.graph.add((uri, DCTERMS.title, Literal(s)))
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
        """
        Each ClassDefinition is represented as an OWL class

        * the OWL Class will instantiate ClassDefinition, if schema.metaclasses is true
        * the OWL Class will be annotated using the same properties as the source ClassDefinition
        * induced slots and their ranges added as OWL restrictions; note this will be under the Open World Assumption
        :param cls:
        :return:
        """
        # To understand how the RDF-level operations here related to the OWL
        # representation, consult https://www.w3.org/TR/owl2-mapping-to-rdf/
        self.add_mappings(cls)
        cls_uri = self._class_uri(cls.name)
        self.add_metadata(cls, cls_uri)
        # add declaration
        self.graph.add((cls_uri, RDF.type, OWL.Class))
        if self.metaclasses:
            # instantiate metaclasses -- introduces punning
            self.graph.add((cls_uri, RDF.type,
                            self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase('class definition')]))
        self._add_element_properties(cls_uri, cls)

        # Parent classes
        if cls.is_a:
            self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(cls.is_a)))
        if cls.mixin:
            self.graph.add((cls_uri, RDFS.subClassOf, METAMODEL_NAMESPACE.mixin))
        for mixin in sorted(cls.mixins):
            self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(mixin)))
        if cls.name in self.synopsis.applytorefs:
            for appl in sorted(self.synopsis.applytorefs[cls.name].classrefs):
                self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(appl)))
        if self.add_ols_annotations:
            # Add annotations for browser hints. See https://www.ebi.ac.uk/ols/docs/installation-guide
            if cls.is_a is None:
                if len(cls.mixins) == 0:
                    # Any class that is not a mixin and is a root serves as a potential entry point
                    self.graph.add((self.graph.identifier,
                                    URIRef('http://purl.obolibrary.org/obo/IAO_0000700'),
                                    cls_uri))
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
            slot = self.schema.slots[sn]
            slot_node = BNode()
            self.graph.add((cls_uri, RDFS.subClassOf, slot_node))

            if self._range_is_datatype(slot):
                cardinality_on = OWL.onDataRange
            else:
                cardinality_on = OWL.onClass
            slot_uri = self.namespaces.uri_for(slot.slot_uri)
            if slot_uri == 'rdf:type':
                logging.warning(f'rdflib may have issues serializing rdf:type with turtle serializer')
            if slot.required:
                if slot.multivalued:
                    #  intersectionOf(restriction(slot only type) restriction(slot some type)
                    restr1 = BNode()
                    self.graph.add((restr1, RDF.type, OWL.Restriction))
                    self.graph.add((restr1, OWL.allValuesFrom, self._range_uri(slot)))
                    self.graph.add((restr1, OWL.onProperty, slot_uri))

                    restr2 = BNode()
                    self.graph.add((restr2, RDF.type, OWL.Restriction))
                    self.graph.add((restr2, OWL.someValuesFrom, self._range_uri(slot)))
                    self.graph.add((restr2, OWL.onProperty, slot_uri))

                    coll_bnode = BNode()
                    Collection(self.graph, coll_bnode, [restr1, restr2])
                    self.graph.add((slot_node, OWL.intersectionOf, coll_bnode))
                    self.graph.add((slot_node, RDF.type, OWL.Class))
                else:
                    #    restriction(slot exactly 1 type)
                    self.graph.add((slot_node, RDF.type, OWL.Restriction))
                    self.graph.add((slot_node, OWL.qualifiedCardinality, Literal(1)))
                    self.graph.add((slot_node, OWL.onProperty, slot_uri))
                    self.graph.add((slot_node, cardinality_on, self._range_uri(slot)))
            else:
                if slot.multivalued:
                    #    restriction(slot only type)
                    self.graph.add((slot_node, RDF.type, OWL.Restriction))
                    self.graph.add((slot_node, OWL.allValuesFrom, self._range_uri(slot)))
                    self.graph.add((slot_node, OWL.onProperty, slot_uri))
                else:
                    #    intersectionOf(restriction(slot only type) restriction(slot max 1 type))
                    self.graph.add((slot_node, RDF.type, OWL.Restriction))
                    self.graph.add((slot_node, cardinality_on, self._range_uri(slot)))
                    self.graph.add((slot_node, OWL.maxQualifiedCardinality, Literal(1)))
                    self.graph.add((slot_node, OWL.onProperty, slot_uri))

        return True


    def visit_slot(self, slot_name: str, slot: SlotDefinition) -> None:
        """ Add a slot definition per slot

        Note: visit_slot may be called multiple times for the same slot_uri, as the same slot_uri can be used:
        * when the schema declares `attributes`
        * when `slot_usage` induces additional slots

        @param slot_name:
        @param slot:
        @return:
        """
        # determine if this is a slot that has been induced by slot_usage; if so the meaning of the slot is context-specific
        # and should not be used for global properties
        if slot.alias is not None and slot.alias != slot.name and slot.alias in self.schema.slots:
            logging.debug(f'SKIPPING slot induced by slot_usage: {slot.alias} // {slot.name} // {slot}')
            return

        slot_uri = self._prop_uri(slot.name)
        #logging.error(f'SLOT_URI={slot_uri}')

        # Slots may be modeled as Object or Datatype Properties
        # if type_objects is True, then ALL slots are ObjectProperties
        self.graph.add((slot_uri, RDF.type, self.slot_owl_type(slot)))
        if self.metaclasses:
            # add metaclass which this property instantiates -- induces punning
            self.graph.add((slot_uri, RDF.type,
                            self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase('slot definition')]))

        slots_with_same_uri = [s.name for s in self.schema.slots.values() if slot_uri == self._prop_uri(s.name)]
        if len(slots_with_same_uri) > 1:
            logging.error(f'Multiple slots with URI: {slot_uri}: {slots_with_same_uri}; consider giving each a unique slot_uri')
            return

        self.add_mappings(slot)
        self._add_element_properties(slot_uri, slot)


        self.graph.add((slot_uri, RDFS.range, self._range_uri(slot)))
        if slot.domain:
            self.graph.add((slot_uri, RDFS.domain, self._class_uri(slot.domain)))
        if slot.inverse:
            self.graph.add((slot_uri, OWL.inverseOf, self._prop_uri(slot.inverse)))
        if slot.symmetric:
            self.graph.add((slot_uri, RDF.type, OWL.SymmetricProperty))

        # Parent slots. Note that is_a and mixin both map to subPropertyOf,
        # and are not distinguishable
        # TODO: consider annotating axiom to indicate if this is is-a or mixin
        if slot.is_a:
            self.graph.add((slot_uri, RDFS.subPropertyOf, self._prop_uri(slot.is_a)))
        for mixin in slot.mixins:
            self.graph.add((slot_uri, RDFS.subPropertyOf, self._prop_uri(mixin)))
        if slot.name in self.synopsis.applytorefs:
            for appl in self.synopsis.applytorefs[slot.name].slotrefs:
                self.graph.add((slot_uri, RDFS.subClassOf, self._prop_uri(appl)))

    def visit_type(self, typ: TypeDefinition) -> None:
        type_uri = self._type_uri(typ.name)
        if not self.type_objects:
            return False
        if typ.from_schema == 'https://w3id.org/linkml/types':
            return
        self.graph.add((type_uri, RDF.type, OWL.Class))
        if self.metaclasses:
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
                        if k == 'name' and isinstance(el, SlotDefinition) and el.alias is not None:
                            prop_uri = RDFS.label
                            e = el.alias
                        else:
                            prop_uri = URIRef(self.metamodel.namespaces.uri_for(defining_slot.slot_uri))
                        self.graph.add((uri,
                                        prop_uri,
                                        Literal(e)))


    def _range_is_datatype(self, slot: SlotDefinition) -> bool:
        if self.type_objects:
            return False
        else:
            return slot.range in self.schema.types

    def _range_uri(self, slot: SlotDefinition) -> URIRef:
        if slot.range in self.schema.types:
            typ = self.schema.types[slot.range]
            if self.type_objects:
                return self._type_uri(typ.name)
            else:
                return self.namespaces.uri_for(typ.uri)
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
        if p is not None and p.slot_uri is not None:
            return self.namespaces.uri_for(p.slot_uri)
        else:
            raise Exception(f'No slot_uri for {pn} // {p}')

    def _type_uri(self, tn: TypeDefinitionName) -> URIRef:
        t = self.schema.types[tn]
        return URIRef(t.definition_uri)

    def _add_metamodel_class(self, cname: str) -> None:
        metac = self.metamodel.schema.classes[cname]
        metac_uri = self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase(metac.name)]
        self.graph.add((metac_uri, RDF.type, OWL.Class))
        self._add_element_properties(metac_uri, metac)

    def slot_owl_type(self, slot : SlotDefinition) -> URIRef:
        if self.type_objects:
            return OWL.ObjectProperty
        elif slot.range in self.schema.classes:
            return OWL.ObjectProperty
        elif slot.range in self.schema.enums:
            return OWL.ObjectProperty
        elif slot.range in self.schema.types:
            return OWL.DatatypeProperty
        else:
            raise Exception(f'Unknown range: {slot.range}')

    # @Deprecated
    def is_slot_object_property(self, slot : SlotDefinition) -> bool:
        if self.type_objects:
            return True
        elif slot.range in self.schema.classes:
            return True
        elif slot.range in self.schema.enums:
            return True
        elif slot.range in self.schema.types:
            return False
        else:
            raise Exception(f'Unknown range: {slot.range}')


@shared_arguments(OwlSchemaGenerator)
@click.command()
@click.option("-o", "--output",
              help="Output file name")
@click.option("--type-objects/--no-type-objects",
              default=True,
              help="If true, will model linkml types as objects, not literals")
@click.option("--metaclasses/--no-metaclasses",
              default=True,
              help="If true, include linkml metamodel classes as metaclasses. Note this introduces punning in OWL-DL")
@click.option("--add-ols-annotations/--no-add-ols-annotations",
              default=True,
              help="If true, auto-include annotations from https://www.ebi.ac.uk/ols/docs/installation-guide")
@click.option("--ontology-iri-suffix",
              default='.owl.ttl',
              help="Suffix to append to schema id to generate OWL Ontology IRI")
def cli(yamlfile, **kwargs):
    """ Generate an OWL representation of a LinkML model

    Examples:

        gen-owl --no-metaclasses --no-type-objects

    For more info, see: https://linkml.io/linkml/generators/owl
    """
    print(OwlSchemaGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == '__main__':
    cli()
