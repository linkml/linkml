import json
from typing import TextIO

from hbreader import FileInfo
from pydantic import BaseModel
from rdflib import Graph

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.loaders.requests_ssl_patch import no_ssl_verification
from linkml_runtime.utils.context_utils import CONTEXTS_PARAM_TYPE
from linkml_runtime.utils.yamlutils import YAMLRoot

# TODO: figure out what mime types go here.  I think we can find the complete set in rdflib
RDF_MIME_TYPES = "application/x-turtle;q=0.9, application/rdf+n3;q=0.8, application/rdf+xml;q=0.5, text/plain;q=0.1"


def _rdf_type_values(typ: str | list[str] | None) -> list[str]:
    """Normalize a JSON-LD @type value (string, list, missing, or explicit null) into a list."""
    if isinstance(typ, str):
        return [typ]
    return list(typ) if typ else []


def _target_class_type_tokens(target_class: type) -> set[str]:
    """Identifiers that may appear in a JSON-LD node's @type for target_class.

    Covers both generated YAMLRoot dataclasses (class_name/class_class_uri) and pydantic
    BaseModel classes (linkml_meta['class_uri']), which have different metadata.
    """
    # Python class name is always present, and only identifier for BaseModel with no
    # LinkML-generated metadata attached. Collect all identifiers ('tokens') into a
    # set of strings to compare against the @type value(s) in the JSON-LD node
    tokens = {target_class.__name__}
    # YAMLRoot dataclasses (pythongen): the LinkML class name and its class URI.
    class_name = getattr(target_class, "class_name", None)
    if class_name:
        tokens.add(class_name)
    class_class_uri = getattr(target_class, "class_class_uri", None)
    if class_class_uri:
        tokens.add(str(class_class_uri))
    # Pydantic BaseModel classes: class_name/class_class_uri don't exist here, but
    # class URI lives in linkml_meta mapping, if metadata generation included it.
    linkml_meta = getattr(target_class, "linkml_meta", None)
    if linkml_meta is not None and "class_uri" in linkml_meta:
        tokens.add(str(linkml_meta["class_uri"]))
    return tokens


class RDFLoader(Loader):
    def load_any(self, *args, **kwargs) -> BaseModel | YAMLRoot | list[BaseModel] | list[YAMLRoot]:
        return self.load(*args, **kwargs)

    def load(
        self,
        source: str | TextIO | Graph,
        target_class: type[BaseModel | YAMLRoot],
        *,
        base_dir: str | None = None,
        contexts: CONTEXTS_PARAM_TYPE = None,
        fmt: str | None = "turtle",
        metadata: FileInfo | None = None,
    ) -> BaseModel | YAMLRoot:
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

        target_class_tokens = _target_class_type_tokens(target_class)

        def loader(data: str | dict, _: FileInfo) -> dict | None:
            """
            Process an RDF string or dict into a target-class-shaped dict.

            :param data: RDF/JSON-LD string or already-parsed dict
            :param _: Unused - part of signature for other implementations
            :return: Dictionary to load into the target class
            """
            if isinstance(data, str):
                if fmt != "json-ld":
                    g = Graph()
                    g.parse(data=data, format=fmt)
                    data = json.loads(g.serialize(format="json-ld", indent=4))
                else:
                    data = json.loads(data)

            if isinstance(data, list):
                # rdflib JSON-LD serialization produces a graph array (list of nodes).
                # Find the node whose @type matches the target class URI.
                # TODO: replace with jsonld.frame(data, {'@context': contexts, '@type': class_uri})
                #   using pyld directly (https://github.com/digitalbazaar/pyld/issues/149) is fixed,
                #   confirmed by unit test added to https://github.com/digitalbazaar/pyld/pull/228,
                #   so nested @id framing now works. rdflib itself still lacks native framing support
                #   (https://github.com/RDFLib/rdflib/issues/1727) but pyld works.

                # Fallback: locate the node by @type without framing (for now)
                matching = [
                    d
                    for d in data
                    if isinstance(d, dict) and not target_class_tokens.isdisjoint(_rdf_type_values(d.get("@type")))
                ]
                data_as_dict = matching[0] if matching else next((d for d in data if isinstance(d, dict)), {})
            elif isinstance(data, dict):
                data_as_dict = data
            else:
                data_as_dict = {}
            typ = data_as_dict.pop("@type", None)
            # TODO: remove this when we get the Biolinkml issue fixed
            if not typ:
                typ = data_as_dict.pop("type", None)
            # typ may be a URI, a CURIE, or a list, so compare against every known
            # identifier for target_class.
            if typ and target_class_tokens.isdisjoint(_rdf_type_values(typ)):
                # TODO: connect this up with the logging facility or warning?
                print(f"Warning: input type mismatch. Expected: {target_class.__name__}, Actual: {typ}")
            return self.json_clean(data_as_dict)

        if not metadata:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir

        # If the input is a graph, convert it to JSON-LD string for load_source
        if isinstance(source, Graph):
            source = source.serialize(format="json-ld", indent=4)
            fmt = "json-ld"

        # While we may want to allow full SSL verification at some point, the general philosophy is that content forgery
        # is not going to be a serious problem.
        # TODO: Make the SSL option a settable parameter in the package itself
        with no_ssl_verification():
            return self.load_source(source, loader, target_class, accept_header=RDF_MIME_TYPES, metadata=metadata)
