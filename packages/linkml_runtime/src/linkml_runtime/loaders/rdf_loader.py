import json
from typing import Any, TextIO

from hbreader import FileInfo, hbread
from jsonasobj2 import JsonObj, as_json
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


def _target_class_uri(target_class: type) -> str | None:
    """Best-known absolute URI for target_class, for use as a JSON-LD frame @type.

    YAMLRoot dataclasses (pythongen) expose this as class_class_uri. Pydantic BaseModel
    classes (pydanticgen) don't have that attribute; their class URI, if generated, lives in
    the linkml_meta mapping instead.
    """
    class_class_uri = getattr(target_class, "class_class_uri", None)
    if class_class_uri:
        return str(class_class_uri)
    linkml_meta = getattr(target_class, "linkml_meta", None)
    if linkml_meta is not None and "class_uri" in linkml_meta:
        return str(linkml_meta["class_uri"])
    return None


def _target_class_type_tokens(target_class: type) -> set[str]:
    """Identifiers that may appear in a JSON-LD node's @type for target_class.

    Covers both generated YAMLRoot dataclasses (class_name/class_class_uri) and pydantic
    BaseModel classes (linkml_meta['class_uri']), which have different metadata.
    """
    # Python class name is always present, and only identifier for BaseModel with no
    # LinkML-generated metadata attached. Collect all identifiers ('tokens') into a
    # set of strings to compare against the @type value(s) in the JSON-LD node
    tokens = {target_class.__name__}
    class_name = getattr(target_class, "class_name", None)
    if class_name:
        tokens.add(class_name)
    # Framing compacts @type against the context, so a CURIE ("termci:Package")
    # is just as likely to come back as the full URI - collect both forms.
    class_class_curie = getattr(target_class, "class_class_curie", None)
    if class_class_curie:
        tokens.add(str(class_class_curie))
    class_uri = _target_class_uri(target_class)
    if class_uri:
        tokens.add(class_uri)
    return tokens


def _resolve_frame_context(contexts: CONTEXTS_PARAM_TYPE, base_dir: str | None = None) -> Any:
    """Load `contexts` (filenames, URLs, JSON text, or already-parsed dicts/JsonObj) into
    inline JSON-LD @context content, so jsonld.frame() doesn't need a document loader to
    resolve them (e.g. over the network) at framing time.

    pyld inspects context content with isinstance(..., dict), so JsonObj inputs are converted
    to plain dicts rather than passed through as-is.
    """
    if contexts is None:
        return None
    resolved = []
    for item in contexts if isinstance(contexts, list) else [contexts]:
        if isinstance(item, str):
            item = json.loads(hbread(item, base_path=base_dir))
        elif isinstance(item, JsonObj):
            item = json.loads(as_json(item))
        # Accept either a whole context document or a bare @context body
        resolved.append(item["@context"] if isinstance(item, dict) and "@context" in item else item)
    if not resolved:
        return None
    return resolved[0] if len(resolved) == 1 else resolved


def _frame_graph_node(
    data: list,
    contexts: CONTEXTS_PARAM_TYPE,
    base_dir: str | None,
    target_class_uri: str | None,
    target_class_tokens: set[str],
) -> dict:
    """Extract the target_class node from a JSON-LD graph array (rdflib's JSON-LD
    serialization produces a flat array of nodes rather than a single framed object).

    Real JSON-LD framing (pyld) both selects the node matching target_class and compacts its
    properties per the context - e.g. turning "http://www.w3.org/ns/shacl#prefix" into
    "prefix" - which naive @type matching alone cannot do. Framing needs a context and a class
    URI, so fall back to locating a node by @type without compaction when either is missing
    (e.g. the source JSON-LD is already in the target class's shape), or when framing matched
    no node at all.
    """
    if target_class_uri is not None:
        # Resolved here rather than up front so an absent/unreachable context only matters
        # when framing is actually attempted
        frame_context = _resolve_frame_context(contexts, base_dir)
        if frame_context is not None:
            # Imported lazily: pyld (and its lxml dependency) is only needed to frame, which
            # requires a context, so importing linkml_runtime.loaders does not pay for it
            from pyld import jsonld

            framed = jsonld.frame(data, {"@context": frame_context, "@type": target_class_uri})
            framed.pop("@context", None)
            if "@graph" in framed:
                # pyld wraps results in @graph when the frame matches other than one node
                graph = framed.pop("@graph")
                framed = graph[0] if graph else {}
            if framed:
                return framed

    matching = [
        d for d in data if isinstance(d, dict) and not target_class_tokens.isdisjoint(_rdf_type_values(d.get("@type")))
    ]
    return matching[0] if matching else next((d for d in data if isinstance(d, dict)), {})


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

        if not metadata:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir

        target_class_tokens = _target_class_type_tokens(target_class)
        target_class_frame_uri = _target_class_uri(target_class)
        # Captured now because reading the source rewrites metadata.base_path to the source's
        # own location, which is not where a relative `contexts` location is anchored
        context_base = metadata.base_path

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
                data_as_dict = _frame_graph_node(
                    data, contexts, context_base, target_class_frame_uri, target_class_tokens
                )
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

        # If the input is a graph, convert it to JSON-LD string for load_source
        if isinstance(source, Graph):
            source = source.serialize(format="json-ld", indent=4)
            fmt = "json-ld"

        # While we may want to allow full SSL verification at some point, the general philosophy is that content forgery
        # is not going to be a serious problem.
        # TODO: Make the SSL option a settable parameter in the package itself
        with no_ssl_verification():
            return self.load_source(source, loader, target_class, accept_header=RDF_MIME_TYPES, metadata=metadata)
