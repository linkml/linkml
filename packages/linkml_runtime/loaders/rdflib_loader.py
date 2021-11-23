import logging
from copy import copy
from dataclasses import dataclass
from typing import Optional, Any, Dict, Type, Union, TextIO, List, Tuple, Set

from hbreader import FileInfo
from rdflib import Graph, URIRef
from rdflib.term import Node, BNode, Literal
from rdflib.namespace import RDF

from linkml_runtime import MappingError, DataNotFoundError
from linkml_runtime.linkml_model import ClassDefinitionName
from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView, SlotDefinition
from linkml_runtime.utils.yamlutils import YAMLRoot

VALID_SUBJECT = Union[URIRef, BNode]
ANYDICT = Dict[str, Any]

@dataclass
class Pointer:
    obj: str

class RDFLibLoader(Loader):
    """
    Loads objects from rdflib Graphs into the python target_class structure

    Note: this is a more complete replacement for rdf_loader
    """
    def from_rdf_graph(self, graph: Graph, schemaview: SchemaView, target_class: Type[YAMLRoot],
                       prefix_map: Dict[str, str] = None,
                       ignore_unmapped_predicates = False) -> List[YAMLRoot]:
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
        # data prefix map: supplements or overrides existing schema prefix map
        if prefix_map:
            for k, v in prefix_map.items():
                namespaces[k] = v
                graph.namespace_manager.bind(k, URIRef(v))
        # Step 1: Create stub root dicts
        target_class_uriref: URIRef = target_class.class_class_uri
        root_dicts: List[ANYDICT] = []
        root_subjects: List[VALID_SUBJECT] = list(graph.subjects(RDF.type, target_class_uriref))
        logging.debug(f'ROOTS = {root_subjects}')
        # Step 2: walk RDF graph starting from root subjects, constructing dict tree
        node_tuples_to_visit: List[Tuple[VALID_SUBJECT, ClassDefinitionName]]  ## nodes and their type still to visit
        node_tuples_to_visit = [(subject, target_class.class_name) for subject in root_subjects]
        uri_to_slot: Dict[str, SlotDefinition]  ## lookup table for RDF predicates -> slots
        uri_to_slot = {URIRef(schemaview.get_uri(s, expand=True)): s for s in schemaview.all_slots().values()}
        processed: Set[VALID_SUBJECT] = set()  ## track nodes already visited
        obj_map: Dict[VALID_SUBJECT, ANYDICT] = {}  ## map from an RDF node to its dict representation
        unmapped_predicates = set()
        while len(node_tuples_to_visit) > 0:
            subject, subject_class = node_tuples_to_visit.pop()
            processed.add(subject)
            dict_obj = self._get_id_dict(subject, schemaview, subject_class)
            if subject in root_subjects:
                root_dicts.append(dict_obj)
            obj_map[subject] = dict_obj
            # process all triples for this node
            for (_, p, o) in graph.triples((subject, None, None)):
                logging.debug(f' Processing triple {subject} {p} {o}, subject type = {subject_class}')
                if p == RDF.type:
                    logging.debug(f'Ignoring RDF.type for {subject} {o}, we automatically infer this')
                elif p not in uri_to_slot:
                    if ignore_unmapped_predicates:
                        unmapped_predicates.add(p)
                    else:
                        raise MappingError(f'No pred for {p} {type(p)}')
                else:
                    slot = schemaview.induced_slot(uri_to_slot[p].name, subject_class)
                    is_inlined = schemaview.is_inlined(slot)
                    slot_name = underscore(slot.name)
                    if isinstance(o, Literal):
                        v = o.value
                    else:
                        v = namespaces.curie_for(o)
                        if slot.range in schemaview.all_enums():
                            # if a PV has a meaning URI declared, map this
                            # back to a text representation
                            e = schemaview.get_enum(slot.range)
                            for pv in e.permissible_values.values():
                                if v == pv.meaning or str(o) == pv.meaning:
                                    v = pv.text
                                    break
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
                        # if o instantiates a class, add to list of nodes to be visited
                        if slot.range in schemaview.all_classes():
                            node_tuples_to_visit.append((o, ClassDefinitionName(slot.range)))
        if unmapped_predicates:
            logging.info(f'Unmapped predicated: {unmapped_predicates}')
        # Step 2: replace inline pointers with object dicts
        def repl(v):
            if isinstance(v, Pointer):
                v2 = obj_map[v.obj]
                if v2 is None:
                    raise Exception(f'No mapping for pointer {v}')
                return v2
            else:
                return v
        objs_to_visit: List[ANYDICT] = copy(root_dicts)
        while len(objs_to_visit) > 0:
            obj = objs_to_visit.pop()
            logging.debug(f'Replacing pointers for  {obj}')
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
            id_val = schemaview.namespaces().curie_for(node)
            if id_val == None:
                id_val = str(node)
            return {id_slot.name: id_val}
        else:
            if id_slot is not None:
                raise Exception(f'Unexpected blank node {node}, type {cn} expects {id_slot.name} identifier')
            return {}



    def load(self, source: Union[str, TextIO, Graph], target_class: Type[YAMLRoot], *,
             schemaview: SchemaView = None,
             prefix_map: Dict[str, str] = None,
             fmt: Optional[str] = 'turtle',
             metadata: Optional[FileInfo] = None,
             **kwargs) -> YAMLRoot:
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

    def loads(self, source: str, **kwargs) -> YAMLRoot:
        return self.load(source, **kwargs)


