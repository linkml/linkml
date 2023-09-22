"""Generate OWL ontology corresponding to information model

model classes are translated to OWL classes, slots to OWL properties.
"""
import logging
import os
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Optional, TextIO, Union, List, Mapping, Set

import click
import rdflib
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    Definition,
    Element,
    ElementName,
    EnumDefinition,
    EnumDefinitionName,
    SchemaDefinition,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
    TypeDefinitionName, AnonymousClassExpression, AnonymousSlotExpression,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.introspection import package_schemaview
from rdflib import OWL, RDF, BNode, Graph, Literal, URIRef, XSD
from rdflib.collection import Collection
from rdflib.namespace import DCTERMS, RDFS, SKOS
from rdflib.plugin import Parser as rdflib_Parser
from rdflib.plugin import plugins as rdflib_plugins

from linkml import METAMODEL_NAMESPACE, METAMODEL_NAMESPACE_NAME
from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments


@unique
class MetadataProfile(Enum):
    """
    An enumeration of the different kinds of profiles used for
    metadata of generated OWL elements
    """

    linkml = "linkml"
    rdfs = "rdfs"
    ols = "ols"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, MetadataProfile))


@unique
class OWLProfile(Enum):
    """
    An enumeration of OWL Profiles
    """

    dl = "dl"
    full = "full"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, MetadataProfile))


class ElementDefinition(object):
    pass


@dataclass
class OwlSchemaGenerator(Generator):
    """
    Generates a schema-oriented OWL representation of a LinkML model

    `OWL Generator Docs <https://linkml.io/linkml/generators/owl>`_

    Attributes:
        type_objects    if True, represent TypeDefinitions as objects; if False, as literals
        metaclasses     if True, include OWL representations of ClassDefinition, SlotDefinition, etc. Introduces punning
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["owl", "ttl"] + [
        x.name for x in rdflib_plugins(None, rdflib_Parser) if "/" not in str(x.name)
    ]
    file_extension = "owl"
    uses_schemaloader = False

    # ObjectVars
    metadata_profile: MetadataProfile = None
    """Deprecated - use metadata_profiles."""
    metadata_profiles: List[MetadataProfile] = field(default_factory=lambda: [])
    ontology_uri_suffix: str = None
    metaclasses: bool = field(default_factory=lambda: True)
    add_ols_annotations: bool = field(default_factory=lambda: True)
    graph: Optional[Graph] = None
    top_value_uri: Optional[URIRef] = None
    type_objects: bool = field(default_factory=lambda: True)
    assert_equivalent_classes: bool = field(default_factory=lambda: False)
    use_native_uris: bool = field(default_factory=lambda: True)
    mixins_as_expressions: bool = None
    slot_is_literal_map: Mapping[str, Set[bool]]  = field(default_factory=lambda: defaultdict(set))
    node_owltypes: Mapping[Union[BNode, URIRef], Set[URIRef]] = field(default_factory=lambda: defaultdict(set))
    """rdfs:Datatype, owl:Thing"""

    simplify: bool = field(default_factory=lambda: True)
    """Reduce complex expressions to simpler forms"""

    target_profile: OWLProfile = field(default_factory=lambda: OWLProfile.dl)

    metamodel_schemaview: SchemaView = field(default_factory=lambda: package_schemaview("linkml_runtime.linkml_model.meta"))

    def as_graph(self) -> Graph:
        sv = self.schemaview
        schema = sv.schema
        owl_id = schema.id
        mergeimports = self.mergeimports
        if self.ontology_uri_suffix:
            owl_id = f"{owl_id}{self.ontology_uri_suffix}"
        base = URIRef(owl_id)
        graph = Graph(identifier=base)
        self.graph = graph
        for prefix in self.metamodel.schema.emit_prefixes:
            self.graph.bind(prefix, self.metamodel.namespaces[prefix])
        for pfx in schema.prefixes.values():
            self.graph.namespace_manager.bind(pfx.prefix_prefix, URIRef(pfx.prefix_reference))
        graph.add((base, RDF.type, OWL.Ontology))

        for cls in sv.all_classes(imports=mergeimports).values():
            self.add_class(cls)
            for a in cls.attributes.values():
                self.add_slot(a, attribute=True)
        for slot in sv.all_slots(imports=mergeimports, attributes=False).values():
            self.add_slot(slot, attribute=False)
        for typ in sv.all_types(imports=mergeimports).values():
            self.add_type(typ)
        for enm in sv.all_enums(imports=mergeimports).values():
            self.add_enum(enm)

        self.add_metadata(schema, base)
        return graph

    def serialize(self, **kwargs) -> str:
        graph = self.as_graph()
        data = self.graph.serialize(
            format="turtle" if self.format in ["owl", "ttl"] else self.format
        )
        return data

    def end_schema(self, output: Optional[str] = None, **_) -> None:
        data = self.graph.serialize(
            format="turtle" if self.format in ["owl", "ttl"] else self.format
        )
        if output:
            with open(output, "w", encoding="UTF-8") as outf:
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

        msv = self.metamodel_schemaview
        this_sv = self.schemaview
        sn_mappings = msv.slot_name_mappings()

        for metaslot_name, metaslot_value in vars(e).items():
            if not metaslot_value:
                continue
            metaslot_name = sn_mappings.get(metaslot_name).name
            metaslot = msv.induced_slot(metaslot_name, e.class_name)
            metaslot_curie = msv.get_uri(metaslot, native=False, expand=False)
            if metaslot_curie.startswith("linkml:"):
                # only mapped properties
                continue
            metaslot_uri = URIRef(msv.get_uri(metaslot, native=False, expand=True))
            if metaslot_name == "description" and self.has_profile(MetadataProfile.rdfs):
                metaslot_uri = RDFS.comment
            metaslot_range = metaslot.range
            if not isinstance(metaslot_value, list):
                metaslot_value = [metaslot_value]
            for v in metaslot_value:
                if metaslot_range in msv.all_types():
                    if metaslot_range == "uri":
                        obj = URIRef(v)
                    elif metaslot_range == "uriorcurie":
                        obj = URIRef(this_sv.expand_curie(v))
                    else:
                        obj = Literal(v)
                elif metaslot_range in msv.all_subsets():
                    obj = Literal(v)  # TODO
                elif metaslot_range in msv.all_classes():
                    continue
                    #if isinstance(v, str):
                    #    obj = URIRef(msv.expand_curie(v))
                    #else:
                    #    logging.debug(f"Skipping {uri} {metaslot_uri} => {v}")
                else:
                    obj = Literal(v)
                self.graph.add((uri, metaslot_uri, obj))

        for k, v in e.annotations.items():
            if ":" not in k:
                default_prefix = this_sv.schema.default_prefix
                if default_prefix in this_sv.schema.prefixes:
                    default_prefix = this_sv.schema.prefixes[default_prefix].prefix_reference
                k = default_prefix + k
                k_uri = this_sv.expand_curie(k)
            else:
                k_uri = this_sv.expand_curie(k)
                if k_uri == k:
                    k_uri = None
            if k_uri:
                self.graph.add((uri, URIRef(k_uri), Literal(v.value)))

    def _some_values_from(self, property: URIRef, filler: Union[URIRef, BNode]) -> BNode:
        node = BNode()
        self.graph.add((node, RDF.type, OWL.Restriction))
        self.graph.add((node, OWL.onProperty, property))
        self.graph.add((node, OWL.someValuesFrom, filler))
        return node

    def add_class(self, cls: ClassDefinition) -> bool:
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
        sv = self.schemaview
        cls_uri = self._class_uri(cls.name)
        self.add_metadata(cls, cls_uri)
        # add declaration
        self.graph.add((cls_uri, RDF.type, OWL.Class))
        if self.metaclasses:
            # instantiate metaclasses -- introduces punning
            self.graph.add(
                (
                    cls_uri,
                    RDF.type,
                    ClassDefinition.class_class_uri,
                )
            )
        #self._add_element_properties(cls_uri, cls)

        # Parent classes
        if cls.is_a:
            self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(cls.is_a)))
        for mixin in sorted(cls.mixins):
            parent = self._class_uri(mixin)
            if self.mixins_as_expressions:
                parent = self._some_values_from(self._metaslot_uri("mixin"), parent)
            self.graph.add((cls_uri, RDFS.subClassOf, parent))
        if self.has_profile(MetadataProfile.ols):
            # Add annotations for browser hints. See https://www.ebi.ac.uk/ols/docs/installation-guide
            if cls.is_a is None:
                if len(cls.mixins) == 0:
                    # Any class that is not a mixin and is a root serves as a potential entry point
                    self.graph.add(
                        (
                            self.graph.identifier,
                            URIRef("http://purl.obolibrary.org/obo/IAO_0000700"),
                            cls_uri,
                        )
                    )

        if cls.class_uri:
            mapped_uri = sv.get_uri(cls, expand=True, native=not self.use_native_uris)
            if cls_uri != mapped_uri:
                p = OWL.equivalentClass if self.assert_equivalent_classes else SKOS.exactMatch
                self.graph.add((URIRef(cls_uri), p, URIRef(mapped_uri)))
        superclass_expr = self.transform_class_expression(cls)
        if superclass_expr:
            ixn_listnodes = []
            if isinstance(superclass_expr, BNode):
                ixn_listnodes = list(self.graph.objects(superclass_expr, OWL.intersectionOf))
            if self.simplify and ixn_listnodes:
                # simplify
                if len(ixn_listnodes) > 1:
                    raise AssertionError
                for x in Collection(self.graph, ixn_listnodes[0]):
                    self.graph.add((cls_uri, RDFS.subClassOf, x))
                self._remove_list(ixn_listnodes[0])
                self.graph.remove((superclass_expr, OWL.intersectionOf, ixn_listnodes[0]))
            else:
                self.graph.add((cls_uri, RDFS.subClassOf, superclass_expr))

    def _remove_list(self, listnode: BNode) -> None:
        graph = self.graph
        triples = list(graph.triples((listnode, None, None)))
        while triples:
            t = triples.pop(0)
            subj, pred, obj = t
            if pred not in [RDF.first, RDF.rest]:
                continue
            graph.remove(t)
            if isinstance(obj, BNode):
                triples.extend(graph.triples((obj, None, None)))

    def transform_class_expression(self, cls: Union[ClassDefinition, AnonymousClassExpression]) -> BNode:
        graph = self.graph
        sv = self.schemaview
        own_slots = list(cls.slot_usage.values()) + list(cls.attributes.values())
        # sort by name
        own_slots.sort(key=lambda x: x.name)
        owl_exprs = []
        if cls.any_of:
            owl_exprs.append(self._union_of([self.transform_class_expression(x) for x in cls.any_of]))
        if cls.exactly_one_of:
            sub_exprs = [self.transform_class_expression(x) for x in cls.exactly_one_of]
            if isinstance(cls, ClassDefinition):
                cls_uri = self._class_uri(cls.name)
                listnode = BNode()
                Collection(graph, listnode, sub_exprs)
                graph.add((cls_uri, OWL.disjointUnionOf, listnode))
            else:
                sub_sub_exprs = []
                for i, x in enumerate(sub_exprs):
                    rest = sub_exprs[0:i] + sub_exprs[i+1:]
                    neg_expr = self._complement_of_union_of(rest)
                    sub_sub_exprs.append(self._intersection_of([x, neg_expr]))
                sub_exprs.append(self._union_of(sub_sub_exprs))
        if cls.all_of:
            owl_exprs.append(self._intersection_of([self.transform_class_expression(x) for x in cls.all_of]))
        if cls.none_of:
            owl_exprs.append(self._complement_of_union_of([self.transform_class_expression(x) for x in cls.any_of]))
        for slot in own_slots:
            x = self.transform_class_slot_expression(cls, slot, slot)
            if not x:
                range = sv.schema.default_range
                if range:
                    if range in sv.all_types():
                        x = self._type_uri(range)
                    else:
                        x = self._class_uri(range)
                else:
                    x = OWL.Thing
            slot_uri = self._prop_uri(slot)
            if slot.name in sv.all_slots():
                top_slot = sv.get_slot(slot.name)
            else:
                top_slot = slot
            avf = BNode()
            graph.add((avf, RDF.type, OWL.Restriction))
            graph.add((avf, OWL.allValuesFrom, x))
            graph.add((avf, OWL.onProperty, slot_uri))
            owl_exprs.append(avf)
            min_card_expr = BNode()
            owl_exprs.append(min_card_expr)
            min_card = 1 if slot.required or top_slot.required else 0
            graph.add((min_card_expr, RDF.type, OWL.Restriction))
            graph.add((min_card_expr, OWL.minCardinality, Literal(min_card)))
            graph.add((min_card_expr, OWL.onProperty, slot_uri))
            if not slot.multivalued and not top_slot.multivalued:
                max_card_expr = BNode()
                owl_exprs.append(max_card_expr)
                graph.add((max_card_expr, RDF.type, OWL.Restriction))
                graph.add((max_card_expr, OWL.maxCardinality, Literal(1)))
                graph.add((max_card_expr, OWL.onProperty, slot_uri))
        return self._intersection_of(owl_exprs)


    def transform_class_slot_expression(self, cls: Union[ClassDefinition, AnonymousClassExpression], slot: Union[SlotDefinition, AnonymousSlotExpression], main_slot: SlotDefinition=None) -> Union[BNode, URIRef]:
        sv = self.schemaview
        if main_slot is None:
            if not isinstance(slot, SlotDefinition):
                raise ValueError(f"Must pass main slot for {slot}")
            main_slot = slot

        owl_exprs = []
        graph = self.graph

        if slot.any_of:
            owl_exprs.append(self._union_of([self.transform_class_slot_expression(cls, x, main_slot) for x in slot.any_of]))
        if slot.all_of:
            owl_exprs.append(self._intersection_of([self.transform_class_slot_expression(cls, x, main_slot) for x in slot.all_of]))
        if slot.none_of:
            owl_exprs.append(self._complement_of_union_of([self.transform_class_slot_expression(cls, x, main_slot) for x in slot.none_of]))
        if slot.exactly_one_of:
            owl_exprs.append(self._exactly_one_of([self.transform_class_slot_expression(cls, x, main_slot) for x in slot.exactly_one_of]))
        range = slot.range
        #if not range and not owl_exprs:
        #    range = sv.schema.default_range
        owl_types = set()
        if range:
            if range in sv.all_types(imports=True):
                self.slot_is_literal_map[main_slot.name].add(True)
                owl_types.add(RDFS.Literal)
                typ = sv.get_type(range)
                if self.type_objects:
                    # TODO
                    owl_exprs.append(self._type_uri(typ.name))
                else:
                    owl_exprs.append(self._type_uri(typ.name))
            elif range in self.schema.enums:
                # TODO: enums fill this in
                owl_exprs.append(self._enum_uri(EnumDefinitionName(range)))
            else:
                owl_types.add(OWL.Thing)
                self.slot_is_literal_map[main_slot.name].add(False)
                owl_exprs.append(self._class_uri(ClassDefinitionName(range)))
        constraints = {
            XSD.minInclusive: slot.minimum_value,
            XSD.maxInclusive: slot.maximum_value,
        }
        constraints = {k: v for k, v in constraints.items() if v is not None}
        if constraints:
            dr = BNode()
            listnode = BNode()
            graph.add((dr, RDF.type, RDFS.Datatype))
            graph.add((dr, OWL.onDatatype, RDFS.Literal))
            graph.add((dr, OWL.withRestrictions, listnode))
            dr_exprs = []
            for prop, val in constraints.items():
                x = BNode()
                graph.add((x, prop, Literal(val)))
                dr_exprs.append(x)
            Collection(graph, listnode, dr_exprs)
            owl_exprs.append(dr)
        this_expr = self._intersection_of(owl_exprs)
        self.node_owltypes[this_expr].update(self._get_owltypes(owl_types, owl_exprs))
        return this_expr

    def _get_owltypes(self, current: Set[URIRef], exprs: List[Union[BNode, URIRef]]) -> Set[URIRef]:
        owltypes = set()
        for x in exprs:
            x_owltypes = self.node_owltypes.get(x, None)
            if x_owltypes:
                owltypes.update(x_owltypes)
        owltypes.update(current)
        if len(owltypes) > 1:
            logging.warning(f"Multiple owl types {owltypes}")
            #if self.target_profile == OWLProfile.dl:
        return owltypes

    def _complement_of_union_of(self, exprs: List[Union[BNode, URIRef]], **kwargs) -> Optional[Union[BNode, URIRef]]:
        if not exprs:
            raise ValueError("Must pass at least one")
        neg_expr = BNode()
        self.graph.add((neg_expr, OWL.complementOf, self._union_of(exprs)), **kwargs)
        return neg_expr

    def _intersection_of(self, exprs: List[Union[BNode, URIRef]], **kwargs) -> Optional[Union[BNode, URIRef]]:
        return self._boolean_expression(exprs, OWL.intersectionOf, **kwargs)

    def _union_of(self, exprs: List[Union[BNode, URIRef]], **kwargs) -> Optional[Union[BNode, URIRef]]:
        return self._boolean_expression(exprs, OWL.unionOf, **kwargs)

    def _exactly_one_of(self, exprs: List[Union[BNode, URIRef]]) -> Optional[Union[BNode, URIRef]]:
        if not exprs:
            raise ValueError("Must pass at least one")
        if len(exprs) == 1:
            return exprs[0]
        sub_exprs = []
        for i, x in enumerate(exprs):
            rest = exprs[0:i] + exprs[i + 1:]
            neg_expr = self._complement_of_union_of(rest)
            sub_exprs.append(self._intersection_of([x, neg_expr]))
        return self._union_of(sub_exprs)

    def _boolean_expression(self, exprs: List[Union[BNode, URIRef]], predicate: URIRef, node: Optional[URIRef] = None) -> Optional[Union[BNode, URIRef]]:
        graph = self.graph
        if len(exprs) == 0:
            return None
        elif len(exprs) == 1:
            return exprs[0]
        else:
            if node is None:
                node = BNode()
            listnode = BNode()
            Collection(graph, listnode, exprs)
            graph.add((node, predicate, listnode))
            owl_types = self._get_owltypes(set(), exprs)
            if len(owl_types) == 1:
                if RDFS.Literal in owl_types:
                    graph.add((node, RDF.type, RDFS.Datatype))
            return node

    def add_slot(self, slot: SlotDefinition, attribute=False) -> None:
        # determine if this is a slot that has been induced by slot_usage; if so
        # the meaning of the slot is context-specific and should not be used for
        # global properties

        slot_uri = self._prop_uri(slot)
        logging.error(f"A{attribute} {slot_uri}")

        # Slots may be modeled as Object or Datatype Properties
        # if type_objects is True, then ALL slots are ObjectProperties
        self.graph.add((slot_uri, RDF.type, self.slot_owl_type(slot)))
        if self.metaclasses:
            # add metaclass which this property instantiates -- induces punning
            self.graph.add(
                (
                    slot_uri,
                    RDF.type,
                    SlotDefinition.class_class_uri,
                )
            )

        if attribute:
            n = 0
            for c in self.schemaview.all_classes().values():
                for a in c.attributes.values():
                    att_uri = self.schemaview.get_uri(a, native=False, expand=True)
                    if slot_uri == URIRef(att_uri):
                        n += 1
            if n > 1:
                logging.warning(f"Ambiguous attribute: {slot.name} {slot_uri}")
                return

        self.add_metadata(slot, slot_uri)

        if attribute:
            return

        range_expr = self.transform_class_slot_expression(None, slot)
        if range_expr:
            self.graph.add((slot_uri, RDFS.range, range_expr))
        if slot.domain:
            self.graph.add((slot_uri, RDFS.domain, self._class_uri(slot.domain)))
        if slot.inverse:
            self.graph.add((slot_uri, OWL.inverseOf, self._prop_uri(slot.inverse)))
        characteristics = {
            "symmetric": OWL.SymmetricProperty,
            "transitive": OWL.TransitiveProperty,
            "reflexive": OWL.ReflexiveProperty,
        }
        for metaslot, uri in characteristics.items():
            if getattr(slot, metaslot, False):
                self.graph.add((slot_uri, RDF.type, uri))

        if slot.is_a:
            self.graph.add((slot_uri, RDFS.subPropertyOf, self._prop_uri(slot.is_a)))
        for mixin in slot.mixins:
            self.graph.add((slot_uri, RDFS.subPropertyOf, self._prop_uri(mixin)))

    def add_type(self, typ: TypeDefinition) -> None:
        type_uri = self._type_uri(typ.name)
        if typ.from_schema == "https://w3id.org/linkml/types":
            return

        if self.metaclasses:
            self.graph.add(
                (
                    type_uri,
                    RDF.type,
                    self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][
                        camelcase("type definition")
                    ],
                )
            )
        #self._add_element_properties(type_uri, typ)
        if self.type_objects:
            self.graph.add((type_uri, RDF.type, OWL.Class))
            if typ.typeof:
                self.graph.add((type_uri, RDFS.subClassOf, self._type_uri(typ.typeof)))
            else:
                if not  self.top_value_uri:
                    self.top_value_uri = self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME]["topValue"]
                    self.graph.add((self.top_value_uri, RDF.type, OWL.DatatypeProperty))
                    self.graph.add((self.top_value_uri, RDFS.label, Literal("value")))
                restr = BNode()
                self.graph.add((restr, RDF.type, OWL.Restriction))
                self.graph.add((restr, OWL.qualifiedCardinality, Literal(1)))
                self.graph.add((restr, OWL.onProperty, self.top_value_uri))
                self.graph.add((restr, OWL.onDataRange, self._type_uri(typ.name)))
                self.graph.add((type_uri, RDFS.subClassOf, restr))
        else:
            self.graph.add((type_uri, RDF.type, RDFS.Datatype))
            if typ.typeof:
                self.graph.add((type_uri, OWL.equivalentClass, self._type_uri(typ.typeof)))
            if typ.uri:
                self.graph.add((type_uri, OWL.equivalentClass, URIRef(self.schemaview.expand_curie(typ.uri))))


    def add_enum(self, e: EnumDefinition) -> None:
        g = self.graph
        enum_uri = self._enum_uri(e.name)
        g.add((enum_uri, RDF.type, OWL.Class))
        if self.metaclasses:
            g.add(
                (
                    enum_uri,
                    RDF.type,
                    self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][
                        camelcase("enum definition")
                    ],
                )
            )
        #self._add_element_properties(enum_uri, e)
        pv_uris = []
        for pv in e.permissible_values.values():
            if pv.meaning:
                pv_uri = self.namespaces.uri_for(pv.meaning)
            else:
                pv_uri = enum_uri + "#" + pv.text.replace(" ", "+")
                # pv_uri = self.namespaces.uri_for(downcase(pv.text))
                # pv_uri = None
            pv_uris.append(pv_uri)
            if pv_uri:
                g.add((pv_uri, RDF.type, OWL.Class))
                g.add((pv_uri, RDFS.label, Literal(pv.text)))
                g.add(
                    (
                        enum_uri,
                        self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME]["permissible_values"],
                        pv_uri,
                    )
                )
                #self._add_element_properties(pv_uri, pv)
                if self.metaclasses:
                    g.add((pv_uri, RDF.type, enum_uri))
        if all([pv is not None for pv in pv_uris]):
            self._union_of(pv_uris, node=enum_uri)

    def has_profile(self, profile: MetadataProfile, default=False) -> bool:
        if default and not self.metadata_profile and not self.metadata_profiles:
            return True
        return profile in self.metadata_profiles or profile == self.metadata_profile


    def _add_element_properties(self, uri: URIRef, el: Element) -> None:
        metamodel = self.metamodel
        for k, v in el.__dict__.items():
            if k in metamodel.schema.slots:
                defining_slot = self.metamodel.schema.slots[k]
                if v is not None and (
                    "owl" in defining_slot.in_subset or "OwlProfile" in defining_slot.in_subset
                ):
                    if isinstance(v, list):
                        ve = v
                    elif isinstance(v, dict):
                        ve = v.values()
                    else:
                        ve = [v]
                    for e in ve:
                        if isinstance(
                            e,
                            (
                                ClassDefinition,
                                SlotDefinition,
                                TypeDefinition,
                                EnumDefinition,
                            ),
                        ):
                            return
                        if k == "name" and isinstance(el, SlotDefinition) and el.alias is not None:
                            prop_uri = RDFS.label
                            e = el.alias
                        else:
                            prop_uri = URIRef(
                                self.metamodel.namespaces.uri_for(defining_slot.slot_uri)
                            )
                        object = self._as_rdf_element(e, defining_slot)
                        if object is not None:
                            self.graph.add((uri, prop_uri, object))

    def _as_rdf_element(
        self, element: Union[ElementName, Element], parent_slot: SlotDefinition
    ) -> Optional[Union[URIRef, Literal]]:
        if parent_slot.range in self.metamodel.schema.types:
            return Literal(element)
        elif parent_slot.range in self.metamodel.schema.enums:
            return Literal(element)
        elif parent_slot.range in self.metamodel.schema.classes:
            if parent_slot.inlined:
                element_name = element.name
            else:
                element_name = element
            if element_name in self.metamodel.schema.classes:
                return self._class_uri(element_name)
            elif element_name in self.metamodel.schema.types:
                return self._type_uri(element_name)
            elif element_name in self.metamodel.schema.enums:
                return self._enum_uri(element_name)
        else:
            logging.warning(f"Unknown range {parent_slot.range}")
            return None

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

    def _class_uri(self, cn: Union[str, ClassDefinitionName]) -> URIRef:
        c = self.schemaview.get_class(cn)
        return URIRef(self.schemaview.get_uri(c, expand=True, native=self.use_native_uris))

    def _enum_uri(self, en:  Union[str, EnumDefinitionName]) -> URIRef:
        sv = self.schemaview
        e = sv.get_enum(en)
        uri = e.enum_uri
        if not uri:
            uri = f'{sv.schema.default_prefix}:{camelcase(en)}'
        # TODO: allow control over URIs
        return URIRef(self.schemaview.expand_curie(uri))

    def _prop_uri(self, pn: Union[SlotDefinition, SlotDefinitionName]) -> URIRef:
        if isinstance(pn, SlotDefinition):
            p = pn
        else:
            p = self.schemaview.get_slot(pn, attributes=True)
        if not p:
            raise ValueError(f"No such slot or attribute: {pn}")
        return URIRef(self.schemaview.get_uri(p, expand=True, native=False))

    def _type_uri(self, tn: TypeDefinitionName) -> URIRef:
        t = self.schemaview.get_type(tn)
        return URIRef(self.schemaview.get_uri(t, expand=True, native=True))

    def _add_metamodel_class(self, cname: str) -> None:
        metac = self.metamodel.schema.classes[cname]
        metac_uri = self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME][camelcase(metac.name)]
        self.graph.add((metac_uri, RDF.type, OWL.Class))
        # self._add_element_properties(metac_uri, metac)

    def slot_owl_type(self, slot: SlotDefinition) -> URIRef:
        sv = self.schemaview
        if slot.range is None:
            range = self.schemaview.schema.default_range
        else:
            range = slot.range
        if self.type_objects:
            return OWL.ObjectProperty
        is_literal_vals = self.slot_is_literal_map[slot.name]
        if len(is_literal_vals) > 1:
            logging.warning(f"Ambiguous type for: {slot.name}")
        if range is None:
            if not is_literal_vals:
                logging.warning(f"Guessing type for {slot.name}")
                return OWL.ObjectProperty
            if (list(is_literal_vals))[0]:
                return OWL.DatatypeProperty
            else:
                return OWL.ObjectProperty
        elif range in sv.all_classes():
            return OWL.ObjectProperty
        elif range in sv.all_enums():
            return OWL.ObjectProperty
        elif range in sv.all_types():
            return OWL.DatatypeProperty
        else:
            raise Exception(f"Unknown range: {slot.range}")



@shared_arguments(OwlSchemaGenerator)
@click.command()
@click.option("-o", "--output", help="Output file name")
@click.option(
    "--metadata-profile",
    default=MetadataProfile.linkml.value,
    show_default=True,
    type=click.Choice(MetadataProfile.list()),
    help="What kind of metadata profile to use for annotations on generated OWL objects",
)
@click.option(
    "--type-objects/--no-type-objects",
    default=False,
    show_default=True,
    help="If true, will model linkml types as objects, not literals",
)
@click.option(
    "--metaclasses/--no-metaclasses",
    default=False,
    show_default=True,
    help="If true, include linkml metamodel classes as metaclasses. Note this introduces punning in OWL-DL",
)
@click.option(
    "--add-ols-annotations/--no-add-ols-annotations",
    default=True,
    show_default=True,
    help="If true, auto-include annotations from https://www.ebi.ac.uk/ols/docs/installation-guide",
)
@click.option(
    "--ontology-uri-suffix",
    default=".owl.ttl",
    show_default=True,
    help="Suffix to append to schema id to generate OWL Ontology IRI",
)
@click.option(
    "--assert-equivalent-classes/--no-assert-equivalent-classes",
    default=False,
    show_default=True,
    help="If true, add owl:equivalentClass between a class and a class_uri",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, metadata_profile: str, **kwargs):
    """Generate an OWL representation of a LinkML model

    Examples:

        Generate OWL using default parameters:

            gen-owl --no-metaclasses --no-type-objects my_schema.yaml

        Generate OWL utilizing datatype properties for type slots and excluding metaclasses:

            gen-owl --no-metaclasses --no-type-objects my_schema.yaml

    For more info, see: https://linkml.io/linkml/generators/owl
    """
    if metadata_profile is not None:
        metadata_profiles = [MetadataProfile(metadata_profile)]
    else:
        metadata_profiles = [MetadataProfile.linkml]
    print(
        OwlSchemaGenerator(yamlfile, metadata_profiles=metadata_profiles, **kwargs).serialize(
            **kwargs
        )
    )


if __name__ == "__main__":
    cli()
