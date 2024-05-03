"""Generate OWL ontology representation of a LinkML schema."""

import logging
import os
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, List, Mapping, Optional, Set, Tuple, Union

import click
import rdflib
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousSlotExpression,
    AnonymousTypeExpression,
    ClassDefinition,
    ClassDefinitionName,
    ClassRule,
    Definition,
    EnumDefinition,
    EnumDefinitionName,
    PermissibleValue,
    SchemaDefinitionName,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
    TypeDefinitionName,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.introspection import package_schemaview
from rdflib import DCTERMS, OWL, RDF, XSD, BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDFS, SKOS
from rdflib.plugin import Parser as rdflib_Parser
from rdflib.plugin import plugins as rdflib_plugins

from linkml import METAMODEL_NAMESPACE_NAME
from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

OWL_TYPE = URIRef  ## RDFS.Literal or OWL.Thing

SWRL = rdflib.Namespace("http://www.w3.org/2003/11/swrl#")
SWRLB = rdflib.Namespace("http://www.w3.org/2003/11/swrlb#")


@unique
class MetadataProfile(Enum):
    """
    An enumeration of the different kinds of profiles used for
    metadata of generated OWL elements
    """

    linkml = "linkml"
    """Default, uses the slot URIs from the LinkML metamodel"""

    rdfs = "rdfs"
    """RDFS conventions, using core RDFS properties preferentially"""

    ols = "ols"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, MetadataProfile))


@unique
class OWLProfile(Enum):
    """
    An enumeration of OWL Profiles.
    """

    dl = "dl"
    """Here this means strict OWL DL, with no punning."""

    full = "full"
    """May include punning (metaclasses)."""

    @staticmethod
    def list():
        return list(map(lambda c: c.value, MetadataProfile))


@dataclass
class OwlSchemaGenerator(Generator):
    """
    Generates a schema-oriented OWL representation of a LinkML model

    `OWL Generator Docs <https://linkml.io/linkml/generators/owl>`_

    .

    - LinkML ClassDefinitions are translated to OWL Classes
    - LinkML SlotDefinitions are translated to OWL Properties
    - LinkML Enumerations are translated to OWL Classes
    - LinkML TypeDefinitions are translated to OWL Datatypes

    The translation aims to be as faithful as possible. But note that OWL is open-world,
    whereas LinkML is closed-world
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["owl", "ttl"] + [x.name for x in rdflib_plugins(None, rdflib_Parser) if "/" not in str(x.name)]
    file_extension = "owl"
    uses_schemaloader = False

    ontology_uri_suffix: str = None
    """Suffix to add to the schema name to create the ontology URI, e.g. .owl.ttl"""

    # ObjectVars
    metadata_profile: MetadataProfile = None
    """Deprecated - use metadata_profiles."""

    metadata_profiles: List[MetadataProfile] = field(default_factory=lambda: [])
    """By default, use the linkml metadata profile,
    this allows for overrides."""

    metaclasses: bool = True
    """if True, include OWL representations of ClassDefinition, SlotDefinition, etc. Introduces punning"""

    add_root_classes: bool = False

    add_ols_annotations: bool = True
    graph: Optional[Graph] = None
    """Mutable graph that is being built up during OWL generation."""

    top_value_uri: Optional[URIRef] = None
    """If metaclasses=True, then this property is used to connect object shadows to literals"""

    type_objects: bool = True
    """if True, represents types as classes (and thus all slots are object properties);
    typed object classes effectively shadow the main xsd literal types.
    The purpose of this is to allow a uniform ObjectProperty representation for all slots,
    without having to commit to being either Data or Object property (OWL-DL does not
    allow a property to be both."""

    assert_equivalent_classes: bool = False
    """If True, assert equivalence between definition_uris and class_uris"""

    use_native_uris: bool = True
    """If True, use the definition_uris, otherwise use class_uris."""

    mixins_as_expressions: bool = None
    """EXPERIMENTAL: If True, use OWL existential restrictions to represent mixins"""

    default_permissible_value_type: Union[str, URIRef] = field(default_factory=lambda: OWL.Class)

    slot_is_literal_map: Mapping[str, Set[bool]] = field(default_factory=lambda: defaultdict(set))
    """DEPRECATED: use node_owltypes"""

    node_owltypes: Mapping[Union[BNode, URIRef], Set[OWL_TYPE]] = field(default_factory=lambda: defaultdict(set))
    """rdfs:Datatype, owl:Thing"""

    simplify: bool = True
    """Reduce complex expressions to simpler forms"""

    use_swrl: bool = False
    """Use of SWRL is experimental"""

    target_profile: OWLProfile = field(default_factory=lambda: OWLProfile.dl)
    """Target OWL profile. Currently the only distinction is between DL and Full"""

    metamodel_schemaview: SchemaView = field(
        default_factory=lambda: package_schemaview("linkml_runtime.linkml_model.meta")
    )

    def as_graph(self) -> Graph:
        """
        Generate an rdflib Graph from the LinkML schema.

        :return:
        """
        sv = self.schemaview
        schema = sv.schema
        owl_id = schema.id
        if self.ontology_uri_suffix:
            owl_id = f"{owl_id}{self.ontology_uri_suffix}"
        mergeimports = self.mergeimports
        base = URIRef(owl_id)
        # initialize the rdflib Graph where all axiom triples will be added
        graph = Graph(identifier=base)
        self.graph = graph
        for prefix in self.metamodel.schema.emit_prefixes:
            self.graph.bind(prefix, self.metamodel.namespaces[prefix])
        for pfx in schema.prefixes.values():
            self.graph.namespace_manager.bind(pfx.prefix_prefix, URIRef(pfx.prefix_reference))
        graph.add((base, RDF.type, OWL.Ontology))

        # Add main schema elements
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

        if not mergeimports:
            for imp in schema.imports:
                if imp == "linkml:types":
                    continue
                graph.add((base, OWL.imports, self._schema_uri(imp)))

        # Add metadata as annotation properties
        self.add_metadata(schema, base)
        return graph

    def serialize(self, **kwargs) -> str:
        """
        Serialize the OWL triple graph to a standard RDF serialization format.

        :param kwargs:
        :return:
        """
        self.as_graph()
        data = self.graph.serialize(format="turtle" if self.format in ["owl", "ttl"] else self.format)
        return data

    def add_metadata(self, e: Definition, uri: URIRef) -> None:
        """
        Add annotation properties.

        Set the profile attribute to the appropriate OWL profile.

        :param e: schema element
        :param uri: URI representation of schema element
        :return:
        """

        msv = self.metamodel_schemaview
        this_sv = self.schemaview
        sn_mappings = msv.slot_name_mappings()

        # iterate through all the assigned metamodel slots
        for metaslot_name, metaslot_value in vars(e).items():
            if not metaslot_value:
                # ignore if unset or an empty list
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
                    # if isinstance(v, str):
                    #    obj = URIRef(msv.expand_curie(v))
                    # else:
                    #    logging.debug(f"Skipping {uri} {metaslot_uri} => {v}")
                else:
                    obj = Literal(v)
                self.graph.add((uri, metaslot_uri, obj))

        for k, v in e.annotations.items():
            if isinstance(v, dict) or isinstance(v, list):
                continue
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

    def add_class(self, cls: ClassDefinition) -> None:
        """
        Each ClassDefinition is represented as an OWL class.

        * the OWL Class will instantiate ClassDefinition, if schema.metaclasses is true
        * the OWL Class will be annotated using the same properties as the source ClassDefinition
        * induced slots and their ranges added as OWL restrictions; note this will be under the Open World Assumption

        This method works by generating an OWL ontology via populating triples in a graph.
        To understand how the RDF-level operations here related to the OWL
        representation, consult https://www.w3.org/TR/owl2-mapping-to-rdf/

        :param cls:
        :return:
        """
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

        # Parent classes: is_a and mixins
        has_parent = False
        if cls.is_a:
            self.graph.add((cls_uri, RDFS.subClassOf, self._class_uri(cls.is_a)))
            has_parent = True
        for mixin in sorted(cls.mixins):
            parent = self._class_uri(mixin)
            if self.mixins_as_expressions:
                parent = self._some_values_from(self._metaslot_uri("mixins"), parent)
            else:
                has_parent = True
            self.graph.add((cls_uri, RDFS.subClassOf, parent))
        if not has_parent and self.add_root_classes:
            # If user selects add_root_classes, then all classes will be subclasses of LinkML:ClassDefinition
            if cls.mixin and self.mixins_as_expressions:
                self.graph.add((cls_uri, RDFS.subClassOf, self._mixin_grouping_class_uri()))
            else:
                self.graph.add((cls_uri, RDFS.subClassOf, URIRef(ClassDefinition.class_class_uri)))
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
            # If a class_ur is assigned, and it is different from model class_uri, then
            # Add an assertion that links the two
            mapped_uri = sv.get_uri(cls, expand=True, native=not self.use_native_uris)
            if cls_uri != mapped_uri:
                p = OWL.equivalentClass if self.assert_equivalent_classes else SKOS.exactMatch
                self.graph.add((URIRef(cls_uri), p, URIRef(mapped_uri)))
        subject_expr = URIRef(cls_uri)
        if self.mixins_as_expressions and cls.mixin:
            subject_expr = self._some_values_from(self._metaslot_uri("mixins"), subject_expr)
        # type designator yield GCI rules
        # E.g. if C has a type designator slot t,
        # then create an axiom: (t some C) subClassOf C.
        type_designator = sv.get_type_designator_slot(cls.name)
        if type_designator:
            td_prop = self._prop_uri(type_designator.name)
            restr = self._some_values_from(td_prop, subject_expr)
            self.graph.add((restr, RDFS.subClassOf, subject_expr))
        # unique key constraints are mapped to OWL hasKey
        if cls.unique_keys:
            for uk in cls.unique_keys.values():
                uk_props = [self._prop_uri(slot) for slot in uk.unique_key_slots]
                uk_props_listnode = BNode()
                Collection(self.graph, uk_props_listnode, uk_props)
                self.graph.add((subject_expr, OWL.hasKey, uk_props_listnode))

        def condition_to_bnode(expr: AnonymousClassExpression) -> Optional[BNode]:
            # inner function: translate a LinkML class expression to an OWL class expression.
            ixn_listnode = self.transform_class_expression(expr, quantifier_predicate=OWL.someValuesFrom)
            if not ixn_listnode:
                return None
            if expr.is_a:
                ixn_listnode = self._intersection_of([ixn_listnode, self._class_uri(expr.is_a)])
            return ixn_listnode

        # rules yield OWL GCI subClassOf axioms
        for rule in cls.rules:
            pre_node = condition_to_bnode(rule.preconditions)
            if not pre_node:
                continue
            pre_node = self._intersection_of([pre_node, subject_expr])
            post_node = condition_to_bnode(rule.postconditions)
            if not post_node:
                continue
            self.graph.add((pre_node, RDFS.subClassOf, post_node))
        # classification rules yield OWL GCI subClassOf axioms
        for expr in cls.classification_rules:
            ixn_listnode = condition_to_bnode(expr)
            self.graph.add((ixn_listnode, RDFS.subClassOf, subject_expr))
        # Other axioms, including those from anonymous expressions
        superclass_expr = self.transform_class_expression(cls)
        if superclass_expr:
            ixn_listnodes = []
            if isinstance(superclass_expr, BNode):
                ixn_listnodes = list(self.graph.objects(superclass_expr, OWL.intersectionOf))
            if self.simplify and ixn_listnodes:
                # simplify
                if len(ixn_listnodes) > 1:
                    raise AssertionError
                ixn_listnode = ixn_listnodes[0]
                if not isinstance(ixn_listnode, BNode):
                    raise AssertionError
                for x in Collection(self.graph, ixn_listnode):
                    self.graph.add((subject_expr, RDFS.subClassOf, x))
                self._remove_list(ixn_listnode)
                self.graph.remove((superclass_expr, OWL.intersectionOf, ixn_listnodes[0]))
            else:
                self.graph.add((subject_expr, RDFS.subClassOf, superclass_expr))

    def get_own_slots(self, cls: Union[ClassDefinition, AnonymousClassExpression]) -> List[SlotDefinition]:
        """
        Get the slots that are defined on a class, excluding those that are inherited.

        :param cls:
        :return:
        """
        sv = self.schemaview
        if isinstance(cls, ClassDefinition):
            own_slots = (
                list(cls.slot_usage.values()) + list(cls.attributes.values()) + list(cls.slot_conditions.values())
            )
            for slot_name in cls.slots:
                # if slot_name not in cls.slot_usage:
                slot = sv.get_slot(slot_name)
                if slot:
                    own_slots.append(slot)
                else:
                    logging.warning(f"Unknown top-level slot {slot_name}")
        else:
            own_slots = []
        own_slots.extend(cls.slot_conditions.values())
        # merge slots with the same name
        slot_map = {}
        for slot in own_slots:
            if slot.name in slot_map:
                for k, v in slot.__dict__.items():
                    curr = slot_map[slot.name].get(k, None)
                    if v and not curr:
                        slot_map[slot.name][k] = v
            else:
                slot_map[slot.name] = copy(slot.__dict__)
        own_slots = [SlotDefinition(**v) for v in slot_map.values()]
        # sort by name
        own_slots.sort(key=lambda x: x.name)
        return own_slots

    def transform_class_expression(
        self,
        cls: Union[ClassDefinition, AnonymousClassExpression],
        quantifier_predicate: URIRef = OWL.allValuesFrom,
    ) -> BNode:
        """
        Transform a LinkML class expression into an OWL expression.

        If the class includes boolean expressions, then these
        are recursively transformed (each such inner expression is
        an anonymous expression)

        :param cls: LinkML class expression (anonymous if called recursively)
        :param quantifier_predicate:
        :return: blank node representing the OWL expression
        """
        if cls is None:
            cls = AnonymousClassExpression()
        graph = self.graph
        sv = self.schemaview
        own_slots = self.get_own_slots(cls)
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
                for i, x in enumerate(cls.exactly_one_of):
                    rest = cls.exactly_one_of[0:i] + cls.exactly_one_of[i + 1 :]
                    neg_expr = self._complement_of_union_of([self.transform_class_expression(nx) for nx in rest])
                    pos_expr = self._intersection_of([self.transform_class_expression(x), neg_expr])
                    sub_sub_exprs.append(pos_expr)
                owl_exprs.append(self._union_of(sub_sub_exprs))
                # owl_exprs.extend(sub_exprs)
        if cls.all_of:
            owl_exprs.append(self._intersection_of([self.transform_class_expression(x) for x in cls.all_of]))
        if cls.none_of:
            owl_exprs.append(self._complement_of_union_of([self.transform_class_expression(x) for x in cls.none_of]))
        for slot in own_slots:
            if slot.name:
                owltypes = self.slot_node_owltypes(sv.get_slot(slot.name))
            else:
                owltypes = self.slot_node_owltypes(slot)
            x = self.transform_class_slot_expression(cls, slot, slot, owltypes)
            if not x:
                range = sv.schema.default_range
                if range and OWL.Thing not in owltypes:
                    if range in sv.all_types():
                        x = self._type_uri(range)
                    elif range in sv.all_enums():
                        x = self._enum_uri(range)
                    elif range in sv.all_classes():
                        x = self._class_uri(range)
                    else:
                        raise ValueError(f"Unknown range {range}")
                        # x = self._class_uri(range)
                else:
                    x = OWL.Thing
            slot_uri = self._prop_uri(slot)
            if slot.name in sv.all_slots():
                top_slot = sv.get_slot(slot.name)
            else:
                top_slot = slot
            avf = BNode()
            graph.add((avf, RDF.type, OWL.Restriction))
            graph.add((avf, quantifier_predicate, x))
            graph.add((avf, OWL.onProperty, slot_uri))
            owl_exprs.append(avf)
            if isinstance(cls, AnonymousClassExpression):
                # cardinality constraints only belong at the top level
                continue
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
            if slot.has_member:
                has_member_expr = self.transform_class_slot_expression(cls, slot.has_member, slot)
                if has_member_expr:
                    owl_exprs.append(self._some_values_from(slot_uri, has_member_expr))
        return self._intersection_of(owl_exprs)

    def slot_node_owltypes(self, slot: Union[SlotDefinition, AnonymousSlotExpression]) -> Set[URIRef]:
        sv = self.schemaview
        node_types = set()
        if isinstance(slot, SlotDefinition):
            if slot.range in sv.all_classes():
                range_class = sv.get_class(slot.range)
                if not (range_class and range_class.class_uri == "linkml:Any"):
                    node_types.add(OWL.Thing)
            if slot.range in sv.all_types():
                node_types.add(RDFS.Datatype)
        for k in ["any_of", "all_of", "exactly_one_of", "none_of"]:
            subslot = getattr(slot, k, None)
            if subslot:
                node_types.update(self.slot_node_owltypes(subslot))
        return node_types

    def transform_class_slot_expression(
        self,
        cls: Optional[Union[ClassDefinition, AnonymousClassExpression]],
        slot: Union[SlotDefinition, AnonymousSlotExpression],
        main_slot: SlotDefinition = None,
        owl_types: Set[OWL_TYPE] = None,
    ) -> Optional[Union[BNode, URIRef]]:
        """
        Take a ClassExpression and SlotExpression combination and transform to a node.

        :param cls:
        :param slot:
        :param main_slot:
        :param owl_types:
        :return:
        """
        sv = self.schemaview
        if main_slot is None:
            if not isinstance(slot, SlotDefinition):
                raise ValueError(f"Must pass main slot for {slot}")
            main_slot = slot

        owl_exprs = []

        if slot.all_members:
            owl_exprs.append(self.transform_class_slot_expression(cls, slot.all_members, main_slot, owl_types))

        if slot.any_of:
            owl_exprs.append(
                self._union_of(
                    [self.transform_class_slot_expression(cls, x, main_slot, owl_types) for x in slot.any_of]
                )
            )
        if slot.all_of:
            owl_exprs.append(
                self._intersection_of(
                    [self.transform_class_slot_expression(cls, x, main_slot, owl_types) for x in slot.all_of]
                )
            )
        if slot.none_of:
            owl_exprs.append(
                self._complement_of_union_of(
                    [self.transform_class_slot_expression(cls, x, main_slot, owl_types) for x in slot.none_of]
                )
            )
        if slot.exactly_one_of:
            disj_exprs = []
            for i, operand in enumerate(slot.exactly_one_of):
                rest = slot.exactly_one_of[0:i] + slot.exactly_one_of[i + 1 :]
                neg_expr = self._complement_of_union_of(
                    [self.transform_class_slot_expression(cls, x, main_slot, owl_types) for x in rest],
                    owl_types=owl_types,
                )
                pos_expr = self._intersection_of(
                    [self.transform_class_slot_expression(cls, operand, main_slot, owl_types), neg_expr],
                    owl_types=owl_types,
                )
                disj_exprs.append(pos_expr)
            owl_exprs.append(self._union_of(disj_exprs, owl_types=owl_types))
        range = slot.range
        # if not range and not owl_exprs:
        #    range = sv.schema.default_range
        this_owl_types = set()
        if range:
            if range in sv.all_types(imports=True):
                self.slot_is_literal_map[main_slot.name].add(True)
                this_owl_types.add(RDFS.Literal)
                typ = sv.get_type(range)
                if self.type_objects:
                    # TODO
                    owl_exprs.append(self._type_uri(typ.name))
                else:
                    owl_exprs.append(self._type_uri(typ.name))
            elif range in sv.all_enums(imports=True):
                # TODO: enums fill this in
                owl_exprs.append(self._enum_uri(EnumDefinitionName(range)))
            elif range in sv.all_classes(imports=True):
                this_owl_types.add(OWL.Thing)
                self.slot_is_literal_map[main_slot.name].add(False)
                owl_exprs.append(self._class_uri(ClassDefinitionName(range)))
            else:
                raise ValueError(f"Unknown range {range}")
        is_literal = None
        if owl_types:
            is_literal = RDFS.Datatype in owl_types
        constraints_exprs, constraints_owltypes = self.add_constraints(slot, is_literal=is_literal)
        this_owl_types.update(constraints_owltypes)
        owl_exprs.extend(constraints_exprs)
        this_expr = self._intersection_of(owl_exprs, owl_types=this_owl_types)
        self.node_owltypes[this_expr].update(self._get_owltypes(this_owl_types, owl_exprs))
        return this_expr

    def add_constraints(
        self,
        element: Union[SlotDefinition, AnonymousSlotExpression, TypeDefinition, AnonymousTypeExpression],
        is_literal: Optional[bool] = None,
    ) -> Tuple[List[BNode], Set[OWL_TYPE]]:
        owl_types = set()
        owl_exprs = []
        graph = self.graph
        constraints = {
            XSD.minInclusive: element.minimum_value,
            XSD.maxInclusive: element.maximum_value,
            XSD.pattern: element.pattern,  # TODO: map between ECMAScript and XSD regular expressions
        }
        if element.equals_number is not None:
            constraints[XSD.minInclusive] = element.equals_number
            constraints[XSD.maxInclusive] = element.equals_number
        if element.equals_string is not None:
            equals_string = element.equals_string
            if is_literal is None:
                logging.warning(f"ignoring equals_string={equals_string} as unable to tell if literal")
            elif is_literal:
                constraints[XSD.pattern] = equals_string
            else:
                eq_uri = URIRef(self.schemaview.expand_curie(equals_string))
                owl_exprs.append(eq_uri)
        if element.equals_string_in:
            equals_string_in = element.equals_string_in
            if is_literal is None:
                logging.warning(f"ignoring equals_string={equals_string_in} as unable to tell if literal")
            elif is_literal:
                dt_exprs = [
                    self._datatype_restriction(XSD.string, [self._facet(XSD.pattern, s)]) for s in equals_string_in
                ]
                union_expr = self._union_of(dt_exprs, owl_types={RDFS.Literal})
                owl_exprs.append(union_expr)
                owl_types.add(RDFS.Literal)
            else:
                eq_uris = [URIRef(self.schemaview.expand_curie(s)) for s in equals_string_in]
                owl_exprs.append(self._union_of(eq_uris))
        for constraint_prop, constraint_val in constraints.items():
            if is_literal is not None and not is_literal:
                # In LinkML, it is permissible to have a literal constraints on slots that refer to
                # other objects. E.g. a pattern on a in_organization slot which refers to an Organization
                # will be applied to the id of that Organization.
                # To support this in OWL we would need to change this to a complex expression - for
                # now we will skip this.
                # See: https://github.com/linkml/linkml/issues/1841
                continue
            if constraint_val is not None:
                owl_types.add(RDFS.Literal)
                dr = BNode()
                graph.add((dr, RDF.type, RDFS.Datatype))
                if isinstance(constraint_val, float):
                    graph.add((dr, OWL.onDatatype, XSD.float))
                elif isinstance(constraint_val, int):
                    graph.add((dr, OWL.onDatatype, XSD.integer))
                else:
                    graph.add((dr, OWL.onDatatype, XSD.string))
                listnode = BNode()
                x = BNode()
                Collection(graph, listnode, [x])
                graph.add((dr, OWL.withRestrictions, listnode))
                graph.add((x, constraint_prop, Literal(constraint_val)))
                owl_exprs.append(dr)
        return owl_exprs, owl_types

    def add_slot(self, slot: SlotDefinition, attribute=False) -> None:
        # determine if this is a slot that has been induced by slot_usage; if so
        # the meaning of the slot is context-specific and should not be used for
        # global properties

        slot_uri = self._prop_uri(slot)

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
            "asymmetric": OWL.AsymmetricProperty,
            "transitive": OWL.TransitiveProperty,
            "reflexive": OWL.ReflexiveProperty,
            "irreflexive": OWL.IrreflexiveProperty,
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
                    URIRef(TypeDefinition.class_class_uri),
                )
            )
        # self._add_element_properties(type_uri, typ)
        if self.type_objects:
            self.graph.add((type_uri, RDF.type, OWL.Class))
            if typ.typeof:
                self.graph.add((type_uri, RDFS.subClassOf, self._type_uri(typ.typeof)))
            else:
                if not self.top_value_uri:
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
            eq_conjunctions = []
            if typ.typeof and type_uri != self._type_uri(typ.typeof):
                # self.graph.add((type_uri, OWL.equivalentClass, self._type_uri(typ.typeof)))
                eq_conjunctions.append(self._type_uri(typ.typeof))
                # self.graph.add((type_uri, RDFS.subClassOf, self._type_uri(typ.typeof)))
            if typ.uri and type_uri != URIRef(self.schemaview.expand_curie(typ.uri)):
                eq_conjunctions.append(URIRef(self.schemaview.expand_curie(typ.uri)))
                # self.graph.add(
                #    (type_uri, OWL.equivalentClass, URIRef(self.schemaview.expand_curie(typ.uri)))
                # )
            constraints_exprs, _ = self.add_constraints(typ, is_literal=True)
            eq_conjunctions.extend(constraints_exprs)
            ixn = self._intersection_of(eq_conjunctions)
            if ixn:
                self.graph.add((type_uri, OWL.equivalentClass, ixn))

    def _get_metatype(
        self, element: Union[Definition, PermissibleValue], default_value: Optional[Union[str, URIRef]] = None
    ) -> Optional[URIRef]:
        impls = []
        if isinstance(element, Definition):
            impls.extend(element.implements)
        if isinstance(element, PermissibleValue):
            if "implements" in element.annotations:
                ann = element.annotations["implements"]
                v = ann.value
                if not isinstance(v, list):
                    v = [v]
                impls.extend(v)
        for impl in impls:
            if impl.startswith("owl:"):
                return OWL[impl.split(":")[1]]
            if impl.startswith("rdfs:"):
                return RDFS[impl.split(":")[1]]
        if isinstance(default_value, str):
            return URIRef(default_value)
        return default_value

    def add_enum(self, e: EnumDefinition) -> None:
        g = self.graph
        enum_uri = self._enum_uri(e.name)
        g.add((enum_uri, RDF.type, OWL.Class))
        has_parent = False
        if e.is_a:
            self.graph.add((enum_uri, RDFS.subClassOf, self._enum_uri(e.is_a)))
            has_parent = True
        for mixin in sorted(e.mixins):
            parent = self._enum_uri(mixin)
            if self.mixins_as_expressions:
                parent = self._some_values_from(self._metaslot_uri("mixins"), parent)
            else:
                has_parent = True
            self.graph.add((enum_uri, RDFS.subClassOf, parent))
        if not has_parent and self.add_root_classes:
            self.graph.add((enum_uri, RDFS.subClassOf, URIRef(EnumDefinition.class_class_uri)))
        if self.metaclasses:
            g.add(
                (
                    enum_uri,
                    RDF.type,
                    URIRef(EnumDefinition.class_class_uri),
                )
            )
        pv_uris = []
        owl_types = []
        enum_owl_type = self._get_metatype(e, self.default_permissible_value_type)

        for pv in e.permissible_values.values():
            pv_owl_type = self._get_metatype(pv, enum_owl_type)
            owl_types.append(pv_owl_type)
            if pv_owl_type == RDFS.Literal:
                pv_node = Literal(pv.text)
                if pv.meaning:
                    logging.warning(f"Meaning on literal {pv.text} in {e.name} is ignored")
            else:
                pv_node = self._permissible_value_uri(pv, enum_uri, e)
            pv_uris.append(pv_node)
            g.add(
                (
                    enum_uri,
                    self.metamodel.namespaces[METAMODEL_NAMESPACE_NAME]["permissible_values"],
                    pv_node,
                )
            )
            if not isinstance(pv_node, Literal):
                g.add((pv_node, RDF.type, pv_owl_type))
                g.add((pv_node, RDFS.label, Literal(pv.text)))
                # TODO: make this configurable
                # self._add_element_properties(pv_uri, pv)
                if self.metaclasses:
                    g.add((pv_node, RDF.type, enum_uri))
                has_parent = False
                if pv.is_a:
                    self.graph.add((pv_node, RDFS.subClassOf, self._permissible_value_uri(pv.is_a, enum_uri, e)))
                    has_parent = True
                for mixin in sorted(pv.mixins):
                    parent = self._permissible_value_uri(mixin, enum_uri, e)
                    if self.mixins_as_expressions:
                        parent = self._some_values_from(self._metaslot_uri("mixins"), parent)
                    else:
                        has_parent = True
                    self.graph.add((enum_uri, RDFS.subClassOf, parent))
                if not has_parent and self.add_root_classes:
                    self.graph.add((pv_node, RDFS.subClassOf, URIRef(PermissibleValue.class_class_uri)))
        if all([pv is not None for pv in pv_uris]):
            all_is_class = all([owl_type == OWL.Class for owl_type in owl_types])
            all_is_individual = all([owl_type == OWL.NamedIndividual for owl_type in owl_types])
            all_is_literal = all([owl_type == RDFS.Literal for owl_type in owl_types])
            sub_pred = DCTERMS.isPartOf
            combo_pred = None
            if all_is_class or all_is_individual or all_is_literal:
                if all_is_class:
                    combo_pred = OWL.unionOf
                    # self._union_of(pv_uris, node=enum_uri)
                    sub_pred = RDFS.subClassOf
                elif all_is_individual:
                    combo_pred = OWL.oneOf
                    # self._object_one_of(pv_uris, node=enum_uri)
                    sub_pred = RDF.type
                elif all_is_literal:
                    combo_pred = OWL.oneOf
                    # self._object_one_of(pv_uris, node=enum_uri)
                    sub_pred = RDF.type
                if combo_pred:
                    self._boolean_expression(pv_uris, combo_pred, enum_uri, owl_types=set(owl_types))
            for pv_node in pv_uris:
                # this would normally be entailed, but we assert here so it is visible
                # without reasoning
                if not isinstance(pv_node, Literal):
                    g.add((pv_node, sub_pred, enum_uri))

    def _add_rule(self, subject: Union[URIRef, BNode], rule: ClassRule, cls: ClassDefinition):
        if not self.use_swrl:
            return
        logging.warning("SWRL support is experimental and incomplete")
        head = []
        body = []
        for pre in rule.preconditions:
            head.extend(self._add_rule_condition(subject, pre, cls))
        for post in rule.postconditions:
            body.extend(self._add_rule_condition(subject, post, cls))
        self._swrl_rule(subject, body, head)

    def _add_rule_condition(
        self,
        subject: Union[URIRef, BNode],
        condition: AnonymousClassExpression,
        cls: ClassDefinition,
    ) -> List[BNode]:
        for slot_name, expr in condition.slot_conditions.items():
            var = self._swrl_var(slot_name)
            if expr.maximum_value is not None:
                self.graph.add((var, SWRLB.lessThanOrEqual, Literal(expr.maximum_value)))

    def has_profile(self, profile: MetadataProfile, default=False) -> bool:
        """
        Determine if a metadata profile is active.

        :param profile: profile to check
        :param default: True if the configured profiles include the specified profile
        :return:
        """
        if default and not self.metadata_profile and not self.metadata_profiles:
            return True
        return profile in self.metadata_profiles or profile == self.metadata_profile

    def _get_owltypes(self, current: Set[OWL_TYPE], exprs: List[Union[BNode, URIRef]]) -> Set[OWL_TYPE]:
        """
        Gets the OWL types of specified expressions plus current owl types.

        :param current:
        :param exprs:
        :return:
        """
        owltypes = set()
        for x in exprs:
            x_owltypes = self.node_owltypes.get(x, None)
            if x_owltypes:
                owltypes.update(x_owltypes)
        owltypes.update(current)
        if len(owltypes) > 1:
            logging.warning(f"Multiple owl types {owltypes}")
            # if self.target_profile == OWLProfile.dl:
        return owltypes

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

    def _some_values_from(self, property: URIRef, filler: Union[URIRef, BNode]) -> BNode:
        if not property:
            raise ValueError(f"Property is required, filler: {filler}")
        if not filler:
            raise ValueError(f"Filler is required, property: {property}")
        node = BNode()
        self.graph.add((node, RDF.type, OWL.Restriction))
        self.graph.add((node, OWL.onProperty, property))
        self.graph.add((node, OWL.someValuesFrom, filler))
        return node

    def _has_value(self, property: URIRef, filler: Union[URIRef, BNode, Literal]) -> BNode:
        node = BNode()
        self.graph.add((node, RDF.type, OWL.Restriction))
        self.graph.add((node, OWL.onProperty, property))
        self.graph.add((node, OWL.hasValue, filler))
        return node

    @staticmethod
    def _swrl_var(var: str) -> URIRef:
        return URIRef(var)

    def _swrl_class_atom(self, cls_ref: Union[BNode, URIRef], var: str) -> BNode:
        node = BNode()
        self.graph.add((node, RDF.type, SWRL.ClassAtom))
        self.graph.add((node, SWRL.classPredicate, cls_ref))
        self.graph.add((node, SWRL.argument1, self._swrl_var(var)))
        return node

    def _swrl_abox_atom(self, pred_ref: Union[BNode, URIRef], arg1: str, arg2: str) -> BNode:
        node = BNode()
        self.graph.add((node, RDF.type, SWRL.IndividualPropertyAtom))
        self.graph.add((node, SWRL.classPredicate, pred_ref))
        self.graph.add((node, SWRL.argument1, self._swrl_var(arg1)))
        self.graph.add((node, SWRL.argument2, self._swrl_var(arg2)))
        return node

    def _swrl_rule(self, body, head) -> BNode:
        node = BNode()
        self.graph.add((node, RDF.type, SWRL.Imp))
        self.graph.add((node, SWRL.body, body))
        self.graph.add((node, SWRL.head, head))
        return node

    @staticmethod
    def _metaslot_uri(name: str) -> URIRef:
        return URIRef("https://w3id.org/linkml/" + name)

    def _complement_of_union_of(
        self, exprs: List[Union[BNode, URIRef]], owl_types: Set[OWL_TYPE] = None, **kwargs
    ) -> Optional[Union[BNode, URIRef]]:
        if not exprs:
            raise ValueError("Must pass at least one")
        neg_expr = BNode()
        if not owl_types:
            owl_types = self._get_owltypes(set(), exprs)
        complement_predicate = OWL.complementOf
        if len(owl_types) == 1:
            if RDFS.Literal in owl_types:
                self.graph.add((neg_expr, RDF.type, RDFS.Datatype))
                complement_predicate = OWL.datatypeComplementOf
        self.graph.add((neg_expr, complement_predicate, self._union_of(exprs)), **kwargs)

        return neg_expr

    def _intersection_of(self, exprs: List[Union[BNode, URIRef]], **kwargs) -> Optional[Union[BNode, URIRef]]:
        return self._boolean_expression(exprs, OWL.intersectionOf, **kwargs)

    def _union_of(self, exprs: List[Union[BNode, URIRef]], **kwargs) -> Optional[Union[BNode, URIRef]]:
        return self._boolean_expression(exprs, OWL.unionOf, **kwargs)

    def _object_one_of(self, exprs: List[Union[BNode, URIRef]], **kwargs) -> Optional[Union[BNode, URIRef]]:
        return self._boolean_expression(exprs, OWL.oneOf, **kwargs)

    def _exactly_one_of(self, exprs: List[Union[BNode, URIRef]]) -> Optional[Union[BNode, URIRef]]:
        if not exprs:
            raise ValueError("Must pass at least one")
        if len(exprs) == 1:
            return exprs[0]
        sub_exprs = []
        for i, x in enumerate(exprs):
            rest = exprs[0:i] + exprs[i + 1 :]
            neg_expr = self._complement_of_union_of(rest)
            sub_exprs.append(self._intersection_of([x, neg_expr]))
        return self._union_of(sub_exprs)

    def _datatype_restriction(self, datatype: URIRef, facets: List[Union[BNode, URIRef]]) -> BNode:
        node = BNode()
        graph = self.graph
        graph.add((node, RDF.type, RDFS.Datatype))
        graph.add((node, OWL.onDatatype, datatype))
        listnode = BNode()
        Collection(graph, listnode, facets)
        graph.add((node, OWL.withRestrictions, listnode))
        return node

    def _facet(self, typ: URIRef, val: Union[Literal, Any]):
        if not isinstance(val, Literal):
            val = Literal(val)
        node = BNode()
        self.graph.add((node, typ, val))
        return node

    def _boolean_expression(
        self,
        exprs: List[Union[BNode, URIRef]],
        predicate: URIRef,
        node: Optional[URIRef] = None,
        owl_types: Set[OWL_TYPE] = None,
    ) -> Optional[Union[BNode, URIRef]]:
        graph = self.graph
        if [x for x in exprs if x is None]:
            logging.warning(f"Null expr in: {exprs} for {predicate} {node}")
            exprs = [x for x in exprs if x is not None]
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
            if owl_types is None:
                owl_types = set()
            owl_types = owl_types.union(self._get_owltypes(set(), exprs))
            if len(owl_types) == 1:
                if RDFS.Literal in owl_types:
                    graph.add((node, RDF.type, RDFS.Datatype))
            return node

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

    @staticmethod
    def _mixin_grouping_class_uri():
        return URIRef(ClassDefinition.class_class_uri + "#Mixin")

    def _class_uri(self, cn: Union[str, ClassDefinitionName]) -> URIRef:
        c = self.schemaview.get_class(cn)
        return URIRef(self.schemaview.get_uri(c, expand=True, native=self.use_native_uris))

    def _enum_uri(self, en: Union[str, EnumDefinitionName]) -> URIRef:
        sv = self.schemaview
        e = sv.get_enum(en, strict=True)
        uri = e.enum_uri
        if not uri:
            uri = f"{sv.schema.default_prefix}:{camelcase(en)}"
        # TODO: allow control over URIs
        return URIRef(self.schemaview.expand_curie(uri))

    def _prop_uri(self, pn: Union[SlotDefinition, SlotDefinitionName]) -> URIRef:
        if isinstance(pn, SlotDefinition):
            p = pn
        else:
            p = self.schemaview.get_slot(pn, attributes=True)
        if not p:
            raise ValueError(f"No such slot or attribute: {pn}")
        try:
            return URIRef(self.schemaview.get_uri(p, expand=True, native=self.use_native_uris))
        except (KeyError, ValueError):
            # TODO: fix this upstream in schemaview
            default_prefix = self.schemaview.schema.default_prefix or ""
            return URIRef(self.schemaview.expand_curie(f"{default_prefix}:{underscore(p.name)}"))

    def _schema_uri(self, scn: Union[str, SchemaDefinitionName]) -> URIRef:
        if ":" in scn:
            return URIRef(self.schemaview.expand_curie(scn))
        else:
            default_prefix = self.schemaview.schema.default_prefix or ""
            return URIRef(self.schemaview.expand_curie(f"{default_prefix}:{scn}"))

    def _type_uri(self, tn: TypeDefinitionName, native: bool = None) -> URIRef:
        if native is None:
            # never use native unless type shadowing with objects is enabled
            native = self.type_objects
        if native:
            # UGLY HACK: Currently schemaview does not camelcase types
            e = self.schemaview.get_element(tn, imports=True)
            if e.from_schema is not None:
                schema = next(sc for sc in self.schemaview.schema_map.values() if sc.id == e.from_schema)
                pfx = schema.default_prefix
                if pfx == "linkml":
                    return URIRef(self.schemaview.expand_curie(f"{pfx}:{camelcase(tn)}"))
        t = self.schemaview.get_type(tn)
        expanded = self.schemaview.get_uri(t, expand=True, native=native)
        if expanded.startswith("xsd:"):
            # TODO: fix upstream in schemaview; default_curi_maps is different on windows
            return XSD[expanded[4:]]
        return URIRef(expanded)

    def _permissible_value_uri(
        self, pv: Union[str, PermissibleValue], enum_uri: str, enum_def: EnumDefinition = None
    ) -> URIRef:
        if isinstance(pv, str):
            pv_name = pv
            if enum_def is None:
                raise ValueError(f"Cannot find permissible value: {pv}, no enum definition provided")
            pvs = [pv for k, pv in enum_def.permissible_values.items() if k == pv_name]
            if len(pvs) != 1:
                raise ValueError(f"Cannot find permissible value: {pv_name}, got: {pvs}")
            pv = pvs[0]
        if pv.meaning:
            return URIRef(self.schemaview.expand_curie(pv.meaning))
        else:
            return URIRef(enum_uri + "#" + pv.text.replace(" ", "+"))

    def slot_owl_type(self, slot: SlotDefinition) -> URIRef:
        sv = self.schemaview
        if slot.implements:
            for t in ["owl:AnnotationProperty", "owl:ObjectProperty", "owl:DatatypeProperty"]:
                if t in slot.implements:
                    return OWL[t.replace("owl:", "")]
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
    "--add-root-classes/--no-add-root-classes",
    default=False,
    show_default=True,
    help="If true, include linkml metamodel classes as superclasses.",
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
@click.option(
    "--mixins-as-expressions/--no-mixins-as-expressions",
    default=False,
    show_default=True,
    help="If true, then mixins are represented as existential expressions",
)
@click.option(
    "--use-native-uris/--no-use-native-uris",
    default=True,
    show_default=True,
    help="Use model URIs rather than class/slot URIs",
)
@click.option(
    "--default-permissible-value-type",
    default=str(OWL.Class),
    show_default=True,
    help="Default OWL type for permissible values",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, metadata_profile: str, **kwargs):
    """Generate an OWL representation of a LinkML model

    Generate OWL using default parameters:

        gen-owl my_schema.yaml

    Note that in previous versions of this generator, the default was to use type objects and
    to include metaclasses. To restore this behavior:

        gen-owl --metaclasses --type-objects my_schema.yaml

    For more info, see: https://linkml.io/linkml/generators/owl
    """
    if metadata_profile is not None:
        metadata_profiles = [MetadataProfile(metadata_profile)]
    else:
        metadata_profiles = [MetadataProfile.linkml]
    gen = OwlSchemaGenerator(yamlfile, metadata_profiles=metadata_profiles, **kwargs)
    print(gen.serialize(**kwargs))


if __name__ == "__main__":
    cli()
