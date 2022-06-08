import logging
from abc import abstractmethod
from typing import Optional, Any, Dict

from rdflib import Graph, URIRef
from rdflib.term import Node, BNode, Literal
from rdflib.namespace import RDF


from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.schemaview import SchemaView, ElementName, PermissibleValue, PermissibleValueText
from linkml_runtime.utils.yamlutils import YAMLRoot


class RDFLibDumper(Dumper):
    """
    Dumps from elements (instances of a LinkML model) to an rdflib Graph

    Note: this should be used in place of rdf_loader for now

    This requires a SchemaView object

    """
    def as_rdf_graph(self, element: YAMLRoot, schemaview: SchemaView, prefix_map: Dict[str, str] = None) -> Graph:
        """
        Dumps from element to an rdflib Graph,
        following a schema

        :param element: element to represent in RDF
        :param schemaview:
        :param prefix_map:
        :return:
        """
        g = Graph()
        logging.debug(f'PREFIXMAP={prefix_map}')
        if prefix_map:
            for k, v in prefix_map.items():
                schemaview.namespaces()[k] = v
                g.namespace_manager.bind(k, URIRef(v))
            for prefix in schemaview.namespaces():
                g.bind(prefix, URIRef(schemaview.namespaces()[prefix]))
        else:
            for prefix in schemaview.namespaces():
                g.bind(prefix, URIRef(schemaview.namespaces()[prefix]))
        self.inject_triples(element, schemaview, g)
        return g

    def inject_triples(self, element: Any, schemaview: SchemaView, graph: Graph, target_type: ElementName = None) -> Node:
        """
        Inject triples from conversion of element into a Graph

        :param element: element to represent in RDF
        :param schemaview:
        :param graph:
        :param target_type:
        :return: root node as rdflib URIRef, BNode, or Literal
        """
        namespaces = schemaview.namespaces()
        slot_name_map = schemaview.slot_name_mappings()
        logging.debug(f'CONVERT: {element} // {type(element)} // {target_type}')
        if target_type in schemaview.all_enums():
            if isinstance(element, PermissibleValueText):
                e = schemaview.get_enum(target_type)
                element = e.permissible_values[element]
            else:
                element = element.code
            element: PermissibleValue
            if element.meaning is not None:
                return URIRef(schemaview.expand_curie(element.meaning))
            else:
                return Literal(element.text)
        if target_type in schemaview.all_types():
            t = schemaview.get_type(target_type)
            dt_uri = t.uri
            if dt_uri:
                if dt_uri == 'rdfs:Resource':
                    return URIRef(schemaview.expand_curie(element))
                elif dt_uri == 'xsd:string':
                    return Literal(element)
                else:
                    return Literal(element, datatype=namespaces.uri_for(dt_uri))
            else:
                logging.warning(f'No datatype specified for : {t.name}, using plain Literal')
                return Literal(element)
        element_vars = {k: v for k, v in vars(element).items() if not k.startswith('_')}
        if len(element_vars) == 0:
            return URIRef(schemaview.expand_curie(str(element)))
        element_type = type(element)
        cn = element_type.class_name
        id_slot = schemaview.get_identifier_slot(cn)
        if id_slot is not None:
            element_id = getattr(element, id_slot.name)
            logging.debug(f'ELEMENT_ID={element_id} // {id_slot.name}')
            element_uri = namespaces.uri_for(element_id)
        else:
            element_uri = BNode()
        type_added = False
        for k, v_or_list in element_vars.items():
            if isinstance(v_or_list, list):
                vs = v_or_list
            elif isinstance(v_or_list, dict):
                vs = v_or_list.values()
            else:
                vs = [v_or_list]
            for v in vs:
                if v is None:
                    continue
                if k in slot_name_map:
                    k = slot_name_map[k].name
                else:
                    logging.error(f'Slot {k} not in name map')
                slot = schemaview.induced_slot(k, cn)
                if not slot.identifier:
                    slot_uri = URIRef(schemaview.get_uri(slot, expand=True))
                    v_node = self.inject_triples(v, schemaview, graph, slot.range)
                    graph.add((element_uri, slot_uri, v_node))
                    if slot.designates_type:
                        type_added = True
        if not type_added:
            graph.add((element_uri, RDF.type, URIRef(schemaview.get_uri(cn, expand=True))))
        return element_uri

    def dump(self, element: YAMLRoot,
             to_file: str,
             schemaview: SchemaView = None,
             fmt: str = 'turtle', prefix_map: Dict[str, str] = None, **args) -> None:
        """
        Write element as rdf to to_file

        :param element: element to represent in RDF
        :param to_file:
        :param schemaview:
        :param fmt:
        :param prefix_map:
        :return:
        """
        super().dump(element, to_file, schemaview=schemaview, fmt=fmt, prefix_map=prefix_map)

    def dumps(self, element: YAMLRoot, schemaview: SchemaView = None,
              fmt: Optional[str] = 'turtle', prefix_map: Dict[str, str] = None) -> str:
        """
        Convert element into an RDF graph guided by the schema

        :param element:
        :param schemaview:
        :param fmt:
        :param prefix_map:
        :return: serialization of rdflib Graph containing element
        """
        return self.as_rdf_graph(element, schemaview, prefix_map=prefix_map).\
            serialize(format=fmt)

