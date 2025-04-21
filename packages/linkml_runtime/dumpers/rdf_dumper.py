import json
from typing import Optional, Union
from pydantic import BaseModel

from hbreader import hbread
from rdflib import Graph


from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.context_utils import CONTEXTS_PARAM_TYPE, CONTEXT_TYPE
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.yamlutils import YAMLRoot


class RDFDumper(Dumper):
    def as_rdf_graph(self, element: Union[BaseModel, YAMLRoot], contexts: CONTEXTS_PARAM_TYPE, namespaces: CONTEXT_TYPE = None) -> Graph:
        """
        Convert element into an RDF graph guided by the context(s) in contexts
        :param element: element to represent in RDF
        :param contexts: JSON-LD context(s) in the form of:
            * file name
            * URL
            * JSON String
            * dict
            * JSON Object
            * A list containing elements of any type named above
        :param namespaces: A file name, URL, JSON String, dict or JSON object that includes the set of namespaces to
        be bound to the return graph.  If absent, contexts get used
        :return: rdflib Graph containing element
        """
        if contexts is None:
            raise Exception(f'Must pass in JSON-LD context via contexts parameter')
        if isinstance(contexts, list):
            inp_contexts = [json.loads(hbread(c)) for c in contexts]
        else:
            inp_contexts = json.loads(hbread(contexts))

        from linkml_runtime.dumpers import json_dumper
        jsonld_str = json_dumper.dumps(element)
        g = Graph().parse(data=jsonld_str, format='json-ld')
        #rdf_jsonld = expand()
        #g = rdflib_graph_from_pyld_jsonld(rdf_jsonld)

        if namespaces is not None:
            ns_source = json.loads(hbread(namespaces))
        else:
            ns_source = inp_contexts

        # TODO: make a utility out of this or add it to prefixcommons
        if ns_source and '@context' in ns_source:
            ns_contexts = ns_source['@context']
            if isinstance(ns_contexts, dict):
                ns_contexts = [ns_contexts]
            for ns_context in ns_contexts:
                if isinstance(ns_context, dict):
                    for pfx, ns in ns_context.items():
                        if isinstance(ns, dict):
                            if '@id' in ns and ns.get('@prefix', False):
                                ns = ns['@id']
                            else:
                                continue
                        if not pfx.startswith('@'):
                            g.bind(pfx, ns)

        return g

    def dump(self, element: Union[BaseModel, YAMLRoot], to_file: str, contexts: CONTEXTS_PARAM_TYPE = None, fmt: str = 'turtle') -> None:
        """
        Write element as rdf to to_file
        :param element: LinkML object to be emitted
        :param to_file: file to write to
        :param contexts: JSON-LD context(s) in the form of:
            * file name
            * URL
            * JSON String
            * dict
            * JSON Object
            * A list containing elements of any type named above
        :param fmt: RDF format
        """
        if isinstance(element, BaseModel):
            element = element.model_dump()
        super().dump(element, to_file, contexts=contexts, fmt=fmt)

    def dumps(self, element: Union[BaseModel, YAMLRoot], contexts: CONTEXTS_PARAM_TYPE = None, fmt: Optional[str] = 'turtle') -> str:
        """
        Convert element into an RDF graph guided by the context(s) in contexts
        :param element: element to represent in RDF
        :param contexts: JSON-LD context(s) in the form of a file or URL, a json string or a json obj
        :param fmt: rdf format
        :return: rdflib Graph containing element
        """
        if isinstance(element, BaseModel):
            element = element.model_dump()
        return self.as_rdf_graph(remove_empty_items(element, hide_protected_keys=True), contexts).\
            serialize(format=fmt)
