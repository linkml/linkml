import logging
import urllib
from copy import copy
from dataclasses import dataclass
from typing import Optional, Any, Union, TextIO

from curies import Converter
from hbreader import FileInfo
from rdflib import Graph, URIRef
from rdflib.term import BNode, Literal
from rdflib.namespace import RDF

from linkml_runtime import MappingError, DataNotFoundError
from linkml_runtime.linkml_model import ClassDefinitionName, TypeDefinition, EnumDefinition, ClassDefinition
from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView, SlotDefinition
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel

logger = logging.getLogger(__name__)


VALID_SUBJECT = Union[URIRef, BNode]
ANYDICT = dict[str, Any]

@dataclass
class Pointer:
    obj: str

class RDFLibLoader(Loader):
    """
    Loads objects from rdflib Graphs into the python target_class structure

    Note: this is a more complete replacement for rdf_loader
    """
    def from_rdf_graph(
        self, graph: Graph,
        schemaview: SchemaView,
        target_class: type[Union[BaseModel, YAMLRoot]],
        prefix_map: Union[dict[str, str], Converter, None] = None,
        cast_literals: bool = True,
        allow_unprocessed_triples: bool = True,
        ignore_unmapped_predicates: bool = False,
    ) -> list[Union[BaseModel, YAMLRoot]]:
        """
        Loads objects from graph into lists of the python target_class structure,
        recursively walking RDF graph from instances of target_class.

        :param graph: rdflib Graph that holds instances of target_class
        :param schemaview: schema to which graph conforms
        :param target_class: class which root nodes should instantiate
        :param prefix_map: additional prefix mappings for data objects
        :param ignore_unmapped_predicates: if True then a predicate that has no mapping to a slot does not raise an error
        :return: all instances of target class type
        """
        namespaces = schemaview.namespaces()
        uri_to_class_map = {}
        for cn, c in schemaview.all_classes().items():
            uri = schemaview.get_uri(c, expand=True)
            if uri in uri_to_class_map:
                c2 = uri_to_class_map[uri]
                if c2.name in schemaview.class_ancestors(cn):
                    continue
                else:
                    logger.error(f'Inconsistent URI to class map: {uri} -> {c2.name}, {c.name}')
            uri_to_class_map[uri] = c
        # data prefix map: supplements or overrides existing schema prefix map
        if isinstance(prefix_map, Converter):
            # TODO replace with `prefix_map = prefix_map.bimap` after making minimum requirement on python 3.8
            prefix_map = {record.prefix: record.uri_prefix for record in prefix_map.records}
        if prefix_map:
            for k, v in prefix_map.items():
                namespaces[k] = v
                graph.namespace_manager.bind(k, URIRef(v))
        # Step 1: Create stub root dict-objects
        target_class_uriref: URIRef = target_class.class_class_uri
        root_dicts: list[ANYDICT] = []
        root_subjects: list[VALID_SUBJECT] = list(graph.subjects(RDF.type, target_class_uriref))
        logger.debug(f'ROOTS = {root_subjects}')
        # Step 2: walk RDF graph starting from root subjects, constructing dict tree
        node_tuples_to_visit: list[tuple[VALID_SUBJECT, ClassDefinitionName]]  ## nodes and their type still to visit
        node_tuples_to_visit = [(subject, target_class.class_name) for subject in root_subjects]
        uri_to_slot: dict[str, SlotDefinition]  ## lookup table for RDF predicates -> slots
        uri_to_slot = {URIRef(schemaview.get_uri(s, expand=True)): s for s in schemaview.all_slots().values()}
        processed: set[VALID_SUBJECT] = set()  ## track nodes already visited, or already scheduled
        for n, _ in node_tuples_to_visit:
            processed.add(n)
        obj_map: dict[VALID_SUBJECT, ANYDICT] = {}  ## map from an RDF node to its dict representation
        unmapped_predicates = set()
        processed_triples: set[tuple] = set()
        while len(node_tuples_to_visit) > 0:
            subject, subject_class = node_tuples_to_visit.pop()
            processed.add(subject)
            dict_obj = self._get_id_dict(subject, schemaview, subject_class)
            if subject in root_subjects:
                root_dicts.append(dict_obj)
            obj_map[subject] = dict_obj
            type_designator_slot = schemaview.get_type_designator_slot(subject_class)
            if type_designator_slot:
                td_iri = schemaview.get_uri(type_designator_slot, expand=True)
                type_vals = list(graph.objects(subject, URIRef(td_iri)))
                if len(type_vals) > 0:
                    type_classes = [uri_to_class_map[str(x)] for x in type_vals]
                    if len(type_classes) > 1:
                        raise ValueError(f'Ambiguous types for {subject} == {type_classes}')
                    logger.info(f'Replacing {subject_class} with {type_classes}')
                    subject_class = type_classes[0].name
            # process all triples for this node
            for (_, p, o) in graph.triples((subject, None, None)):
                processed_triples.add((subject,p,o))
                logger.debug(f' Processing triple {subject} {p} {o}, subject type = {subject_class}')
                if p == RDF.type:
                    logger.debug(f'Ignoring RDF.type for {subject} {o}, we automatically infer this from {subject_class}')
                elif p not in uri_to_slot:
                    if ignore_unmapped_predicates:
                        unmapped_predicates.add(p)
                    else:
                        raise MappingError(f'No pred for {p} {type(p)}')
                else:
                    slot = schemaview.induced_slot(uri_to_slot[p].name, subject_class)
                    range_applicable_elements = schemaview.slot_applicable_range_elements(slot)
                    is_inlined = schemaview.is_inlined(slot)
                    slot_name = underscore(slot.name)
                    if isinstance(o, Literal):
                        if EnumDefinition.class_name in range_applicable_elements:
                            logger.debug(f'Assuming no meaning assigned for value {o} for Enum {slot.range}')
                        elif TypeDefinition.class_name not in range_applicable_elements:
                            raise ValueError(f'Cannot map Literal {o} to a slot {slot.name} whose range {slot.range} is not a type;')
                        v = o.value
                    elif isinstance(o, BNode):
                        if not is_inlined:
                            logger.error(f'blank nodes should be inlined; {slot_name}={o} in {subject}')
                        v = Pointer(o)
                    else:
                        if ClassDefinition.class_name in range_applicable_elements:
                            if slot.range in schemaview.all_classes():
                                id_slot = schemaview.get_identifier_slot(slot.range)
                                v = self._uri_to_id(o, id_slot, schemaview)
                            else:
                                v = namespaces.curie_for(o)
                            if v is None:
                                logger.debug(f'No CURIE for {p}={o} in {subject} [{subject_class}]')
                                v = str(o)
                        elif EnumDefinition.class_name in range_applicable_elements:
                            range_union_elements = schemaview.slot_range_as_union(slot)
                            enum_names = [e for e in range_union_elements if e in schemaview.all_enums()]
                            # if a PV has a meaning URI declared, map this
                            # back to a text representation
                            v = namespaces.curie_for(o)
                            for enum_name in enum_names:
                                e = schemaview.get_enum(enum_name)
                                for pv in e.permissible_values.values():
                                    if v == pv.meaning or str(o) == pv.meaning:
                                        v = pv.text
                                        break
                        elif TypeDefinition.class_name in range_applicable_elements:
                            if cast_literals:
                                v = namespaces.curie_for(o)
                                if v is None:
                                    v = str(o)
                                logger.debug(f'Casting {o} to string')
                            else:
                                raise ValueError(f'Expected literal value ({range_applicable_elements}) for {slot_name}={o}')
                        if is_inlined:
                            # the object of the triple may not yet be processed;
                            # we store a pointer to o, and then replace this later
                            v = Pointer(o)
                    if slot.multivalued:
                        if slot_name not in dict_obj:
                            dict_obj[slot_name] = []
                        dict_obj[slot_name].append(v)
                    else:
                        dict_obj[slot_name] = v
                    if o not in processed:
                        # if o instantiates a class, add to list of nodes to be visited.
                        # force type based on range constraint
                        if slot.range in schemaview.all_classes():
                            node_tuples_to_visit.append((o, ClassDefinitionName(slot.range)))
        if unmapped_predicates:
            logger.info(f'Unmapped predicated: {unmapped_predicates}')
        unprocessed_triples = set(graph.triples((None, None, None))) - processed_triples
        logger.info(f'Triple processed = {len(processed_triples)}, unprocessed = {len(unprocessed_triples)}')
        if len(unprocessed_triples) > 0:
            if not allow_unprocessed_triples:
                for t in unprocessed_triples:
                    logger.warning(f'  Unprocessed: {t}')
                raise ValueError(f'Unprocessed triples: {len(unprocessed_triples)}')
        # Step 2: replace inline pointers with object dicts
        def repl(v):
            if isinstance(v, Pointer):
                v2 = obj_map[v.obj]
                if v2 is None:
                    raise Exception(f'No mapping for pointer {v}')
                return v2
            else:
                return v
        objs_to_visit: list[ANYDICT] = copy(root_dicts)
        while len(objs_to_visit) > 0:
            obj = objs_to_visit.pop()
            logger.debug(f'Replacing pointers for  {obj}')
            for k, v in obj.items():
                if v is None:
                    continue
                if isinstance(v, list):
                    v = [repl(v1) for v1 in v if v1 is not None]
                    for v1 in v:
                        if isinstance(v1, dict):
                            objs_to_visit.append(v1)
                else:
                    v = repl(v)
                    if isinstance(v, dict):
                        objs_to_visit.append(v)
                obj[k] = v
        # Final step: translate dicts into instances of target_class
        return [target_class(**x) for x in root_dicts]

    def _get_id_dict(self, node: VALID_SUBJECT, schemaview: SchemaView, cn: ClassDefinitionName) -> ANYDICT:
        id_slot = schemaview.get_identifier_slot(cn)
        if not isinstance(node, BNode):
            id_val = self._uri_to_id(node, id_slot, schemaview)
            #id_val = schemaview.namespaces().curie_for(node)
            if id_val == None:
                id_val = str(node)
            return {id_slot.name: id_val}
        else:
            if id_slot is not None:
                raise Exception(f'Unexpected blank node {node}, type {cn} expects {id_slot.name} identifier')
            return {}

    def _uri_to_id(self, node: VALID_SUBJECT, id_slot: SlotDefinition, schemaview: SchemaView) -> str:
        if schemaview.is_slot_percent_encoded(id_slot):
            return urllib.parse.unquote(node).replace(schemaview.namespaces()._base, "")
        else:
            return schemaview.namespaces().curie_for(node)


    def load(
        self,
        source: Union[str, TextIO, Graph],
        target_class: type[Union[BaseModel, YAMLRoot]], *,
        schemaview: SchemaView = None,
        prefix_map: Union[dict[str, str], Converter, None] = None,
        fmt: Optional[str] = 'turtle',
        metadata: Optional[FileInfo] = None,
        **kwargs,
    ) -> Union[BaseModel, YAMLRoot]:
        """
        Load the RDF in source into the python target_class structure

        The assumption of all loaders is that the source contains exactly one instance of the
        target class. To load from graphs with multiple instances, use from_rdf_graph

        :param source: RDF data source. Can be a file name, an open handle or an existing graph
        :param target_class: LinkML class to load the RDF into
        :param schemaview: view over schema to guide instantiation
        :param prefix_map: map of prefixes used in data
        :param fmt: format of source if it isn't an existing Graph
        :param metadata: source information. Used by some loaders to record where information came from
        :param kwargs: additional arguments passed to from_rdf_graph
        :return: Instance of target_class
        """
        if isinstance(source, Graph):
            g = source
        else:
            g = Graph()
            if '\n' in source:
                g.parse(data=source, format=fmt)
            else:
                g.parse(source, format=fmt)
        objs = self.from_rdf_graph(g, schemaview=schemaview, target_class=target_class, prefix_map=prefix_map, **kwargs)
        if len(objs) != 1:
            raise DataNotFoundError(f'Got {len(objs)} of type {target_class} from source, expected exactly 1')
        return objs[0]

    def loads(self, source: str, **kwargs) -> Union[BaseModel, YAMLRoot]:
        return self.load(source, **kwargs)

    def load_any(self, source: str, **kwargs) -> Union[BaseModel, YAMLRoot, list[BaseModel], list[YAMLRoot]]:
        return self.load(source, **kwargs)


