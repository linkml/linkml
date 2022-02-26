from typing import Union, TextIO, Optional, Type, List

from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.context_utils import CONTEXTS_PARAM_TYPE
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import Graph

from linkml_runtime.loaders.requests_ssl_patch import no_ssl_verification

# TODO: figure out what mime types go here.  I think we can find the complete set in rdflib
RDF_MIME_TYPES = "application/x-turtle;q=0.9, application/rdf+n3;q=0.8, application/rdf+xml;q=0.5, text/plain;q=0.1"


class RDFLoader(Loader):

    def load_any(self, *args, **kwargs) -> Union[YAMLRoot, List[YAMLRoot]]:
        return self.load(*args, **kwargs)


    def load(self, source: Union[str, TextIO, Graph], target_class: Type[YAMLRoot], *, base_dir: Optional[str] = None,
             contexts: CONTEXTS_PARAM_TYPE = None, fmt: Optional[str] = 'turtle',
             metadata: Optional[FileInfo] = None) -> YAMLRoot:
        """
        Load the RDF in source into the python target_class structure
        :param source: RDF data source. Can be a URL, a file name, an RDF string, an open handle or an existing graph
        :param base_dir: Base directory that can be used if file name or URL.  This is copied into metadata if present
        :param target_class: LinkML class to load the RDF into
        :param contexts: JSON-LD context(s) to use to generate the JSON that will be loaded into target_class.  This is
        optional because, if source is in JSON-LD format, it is possible that the contexts are already there
        :param fmt: format of source if it isn't an existing Graph
        :param metadata: source information. Used by some loaders to record where information came from
        :return: Instance of target_class
        """

        def loader(data: Union[str, dict], _: FileInfo) -> Optional[dict]:
            """
            Process an RDF graph or a JSON-LD string.  We do this by using pyld_jsonld_from_rdflib_graph to
            emit a JSON-LD string and then process it with jsonld.frame.

            :param data: Graph or JSON-LD string
            :param _: Unused - part of signature for other implementations
            :return: Dictionary to load into the target class
            """
            # Where we sit -- we don't have the start string (and other info?) in the context, so we don't get a package
            # on the way out
            # Also - if we don't pop type below, we need to act accordingly
            if isinstance(data, str):
                if fmt != 'json-ld':
                    g = Graph()
                    g.parse(data=data, format=fmt)
                    jsonld_str = g.serialize(format='json-ld', indent=4)
                    data = json.loads(jsonld_str)
                    #data = pyld_jsonld_from_rdflib_graph(g)

            if not isinstance(data, dict):
                # TODO: Add a context processor to the source w/ CONTEXTS_PARAM_TYPE
                # TODO: figure out what to do base options below
                # TODO: determine whether jsonld.frame can handle something other than string input
                # TODO: see https://github.com/RDFLib/rdflib/issues/1727
                # frame = {'@context': contexts, '@type': f'{target_class.__name__}'}
                #data_as_dict = jsonld.frame(data, contexts)
                data_as_dict = data
            else:
                data_as_dict = data
            typ = data_as_dict.pop('@type', None)
            # TODO: remove this when we get the Biolinkml issue fixed
            if not typ:
                typ = data_as_dict.pop('type', None)
            if typ and typ != target_class.class_name:
                # TODO: connect this up with the logging facility or warning?
                print(f"Warning: input type mismatch. Expected: {target_class.__name__}, Actual: {typ}")
            return self.json_clean(data_as_dict)

        if not metadata:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir

        # If the input is a graph, convert it to JSON-LD
        if isinstance(source, Graph):
            source = pyld_jsonld_from_rdflib_graph(source)
            jsonld_str = source.serialize(format='json-ld', indent=4)
            source = json.loads(jsonld_str)
            fmt = 'json-ld'

        # While we may want to allow full SSL verification at some point, the general philosophy is that content forgery
        # is not going to be a serious problem.
        # TODO: Make the SSL option a settable parameter in the package itself
        with no_ssl_verification():
            return self.load_source(source, loader, target_class, accept_header=RDF_MIME_TYPES, metadata=metadata)
