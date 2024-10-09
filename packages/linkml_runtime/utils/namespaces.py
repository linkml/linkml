import logging
from typing import Any, Optional, Union

from prefixcommons import curie_util
from rdflib import Namespace, URIRef, Graph, BNode
from rdflib.namespace import is_ncname
from requests.structures import CaseInsensitiveDict
from prefixmaps.io.parser import load_context

from linkml_runtime.utils.yamlutils import TypedNode
from linkml_runtime.utils.uri_validator import validate_uri

META_NS = "meta"
META_URI = "https://w3id.org/linkml/meta"
BIOCONTEXT_CONTEXTS = [
    "biocaddie-context",
    "commons_context",
    "globi_context",
    "go_context",
    "go_obo_context",
    "idot_context",
    "idot_nr_context",
    "minerva_context",
    "monarch_context",
    "obo_context",
    "ro_vocab_context",
    "semweb_context",
    "semweb_vocab_context"
]
PREFIXMAPS_CONTEXTS = [
    "bioportal",
    "bioregistry",
    "bioregistry.upper",
    "go",
    "linked_data",
    "merged",
    "merged.oak",
    "obo",
    "prefixcc"
]


class Namespaces(CaseInsensitiveDict):
    """ Namespace manager.  Functions as both a dictionary and a python
     namespace.

     Supports:  namespaces.NS [= uri]
                namespaces[NS] [= uri]
                namespaces._default [= uri]    # namespace for ':'
                namespaces._base [= uri]       # namespace for @base

     Functions: namespaces.curie_for(uri) --> curie
                namespaces.prefix_for(uri_or_curie) --> NCName
                namespaces.add_prefixmap(map name)
     """
    _default_key = '@default'
    _base_key = '@base'

    # BNODE management -- when the namespace is '_', we map the ln via _bnodes to a new bnode
    _bnodes = {}                    # BNode to BNode map
    _empty_bnode = BNode()          # Node for '_:'

    def __init__(self, g: Optional[Graph] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if g is not None:
            self.from_graph(g)

    def __setitem__(self, key, value):
        if key == '_':
            if not value:
                if self._empty_bnode not in self._bnodes:
                    self._bnodes[self._empty_bnode] = BNode()
            elif value in self._bnodes:
                raise ValueError(f"BNode {value} is already mapped to {self[self._bnodes[value]]}")
            else:
                target_bnode = BNode()
                self._bnodes[value] = target_bnode
                super().__setitem__(value, target_bnode)
        elif is_ncname(key):
            v = Namespace(str(value))
            if key in self and self[key] != v:
                logger = logging.getLogger('linkml_runtime.Namespaces')
                logger.warning(f"{key} namespace is already mapped to {self[key]} - Overriding with mapping to {v}")

            super().__setitem__(key, v)
        else:
            raise ValueError(f"Invalid NCName: {key}")

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key: str, value):
        if key.startswith('_') and len(key) > 1:
            super().__setattr__(key, value)
        else:
            self[key] = value

    def _cased_key(self, key: str) -> str:
        # Return the case sensitive key for key if in the namespace else just the key itself
        return self._store.get(key.lower(), (key,))[0] if key else key

    @property
    def _default(self) -> Optional[URIRef]:
        return self.get(self._default_key, None)

    @_default.setter
    def _default(self, item: Any) -> None:
        v = Namespace(str(item))
        if self._default is not None:
            if self._default != v:
                raise ValueError(f"Default value is already set to {self._default}")
        else:
            super().__setitem__(self._default_key, v)

    @_default.deleter
    def _default(self) -> None:
        super().__delitem__(self._default_key)

    @property
    def _base(self) -> Optional[URIRef]:
        return self.get(self._base_key, None)

    @_base.setter
    def _base(self, item: Any) -> None:
        v = Namespace(str(item))
        if self._base is not None:
            if self._base != v:
                raise ValueError(f"Base value is already set to {self._base}")
        else:
            super().__setitem__(self._base_key, v)

    @_base.deleter
    def _base(self) -> None:
        super().__delitem__(self._base_key)

    def curie_for(self, uri: Any, default_ok: bool = True, pythonform: bool = False) -> Optional[str]:
        """
        Return the most appropriate CURIE for URI.  The first longest matching prefix used, if any.  If no CURIE is
        present, None is returned.

        Please see https://www.w3.org/TR/curie/ for more details about CURIEs.

        @param uri: URI to create the CURIE for
        @param default_ok: True means the default prefix is ok. Otherwise, we have to have a real prefix
        @param pythonform: True means take the python/rdflib uppercase format
        """
        if not validate_uri(uri):
            raise ValueError(f"{TypedNode.yaml_loc(uri)}Not a valid URI: {uri}")

        if pythonform:
            default_ok = False
        match: tuple[str, Optional[Namespace]] = ('', None)     # match string / prefix
        uri_string = str(uri)

        # Find the longest match for the URI, self.items() is a list of (prefix/namespace, uri base prefix) tuples
        for namespace, uri_base in self.items():
            uri_base_string = str(uri_base)
            # uri_string is passed into this method as the full URI to be converted to a CURIE
            if uri_string.startswith(uri_base_string):
                # default key and base key are `@default` `@base` respectively
                # at this point match[0] is '', match[1] is None
                if len(uri_base_string) > len(match[0]) and \
                        (default_ok or namespace not in (Namespaces._default_key, Namespaces._base_key)):
                    match = (uri_base_string, namespace)

        # check if length of uri_base_string is > 0, now after basically assigning it to be the URI base string
        # that matches the start of the URI coming into the method
        if len(match[0]):
            if pythonform:
                # uppercase the namespace
                namespace = match[1].upper()
                # match[0] is the URI base string, so we remove that from the incoming URI
                leftover_uri = uri_string.replace((match[0]), '')
                if not leftover_uri:
                    return f"URIRef(str({namespace}))"
                # why?
                # elif leftover_uri.isidentifier():
                #    return f"{namespace}.{leftover_uri}"
                else:
                    return f'{namespace}["{leftover_uri}"]'
            else:
                if match[1] == Namespaces._default_key:
                    return uri_string.replace(match[0], ':')
                elif match[1] == Namespaces._base_key:
                    return uri_string.replace(match[0], '')
                else:
                    return uri_string.replace(match[0], match[1] + ':')
        return None

    def prefix_for(self, uri_or_curie: Any, case_shift: bool = True) -> Optional[str]:
        return self.prefix_suffix(uri_or_curie, case_shift)[0]

    def prefix_suffix(self, uri_or_curie: Any, case_shift: bool = True) -> tuple[Optional[str], Optional[str]]:
        uri_or_curie = str(uri_or_curie)
        if '://' in uri_or_curie:
            uri_or_curie = self.curie_for(uri_or_curie)
            if not uri_or_curie:
                return None, None
        if ':' in uri_or_curie:
            pfx, sfx = uri_or_curie.split(':')
        else:
            pfx, sfx = uri_or_curie, ''
        return self._cased_key(pfx) if case_shift else pfx, sfx

    def uri_for(self, uri_or_curie: Any) -> URIRef:
        """
        Map a curie or URI into a full URIRef.

        :param uri_or_curie: "NCNAME ':' suffix" or plain URI
        :return: Corresponding URI
        """
        uri_or_curie_str = str(uri_or_curie)
        if '://' in uri_or_curie_str:
            return URIRef(uri_or_curie_str)
        if ':\\' in uri_or_curie_str:  # Windows drive letters
            return URIRef(uri_or_curie_str)
        if ':' in uri_or_curie_str:
            prefix, local = str(uri_or_curie_str).split(':', 1)
            if not prefix:
                prefix = self._default_key
            elif not is_ncname(prefix):
                raise ValueError(f"{TypedNode.yaml_loc(uri_or_curie)}Not a valid CURIE: {uri_or_curie_str}")
        else:
            prefix, local = self._base_key, uri_or_curie_str

        if prefix not in self:
            raise ValueError(f"{TypedNode.yaml_loc(uri_or_curie)}Unknown CURIE prefix: {prefix}")
        return URIRef(self.join(self[prefix], local))

    def uri_or_curie_for(self, prefix: Union[str, URIRef], suffix: str) -> str:
        """ Return a CURIE for prefix/suffix if possible, else a URI """
        if isinstance(prefix, URIRef) or ':/' in str(prefix):
            prefix_as_uri = str(prefix)
            for k, v in self.items():
                if not k.startswith('@') and prefix_as_uri == str(v):
                    return k + ':' + suffix
            return self.join(str(prefix), suffix)
        elif prefix not in self:
            raise ValueError(f"Unrecognized prefix: {prefix}")
        else:
            return prefix + ':' + suffix

    def load_graph(self, g: Graph) -> Graph:
        """ Transfer all of the known namespaces into G """
        for k, v in self.items():
            if not k.startswith('_') and not k.startswith('@'):
                g.bind(k, URIRef(v))
        return g

    def from_graph(self, g: Graph) -> "Namespaces":
        """ Transfer al bindings from G """
        for ns, name in g.namespaces():
            if ns:
                self[ns] = name
            else:
                self._default = name
        return self

    @staticmethod
    def join(prefix: str, suffix: str) -> str:
        return prefix + suffix

    @staticmethod
    def sfx(uri: str) -> str:
        """
        Add a separator to a uri if none exists.

        Note: This should only be used with module id's -- it is not uncommon to use partial prefixes,
        e.g. PREFIX bfo: http://purl.obolibrary.org/obo/BFO_
        :param uri: uri to be suffixed
        :return: URI with suffix
        """
        return str(uri) + ('' if uri.endswith(('/', '#')) else '/')

    def add_prefixmap(self, map_name: str, include_defaults: bool = True) -> None:
        """
        Add a prefixcommons map or the merged map from prefixmaps repo.

        Only prefixes that have not been previously defined are added.

        :param map_name: prefixcommons map name
        :param include_defaults: if True, take defaults from the map.
        :return:
        """

        if map_name in BIOCONTEXT_CONTEXTS:
            prefix_map = curie_util.read_biocontext(map_name)
        elif map_name in PREFIXMAPS_CONTEXTS:
            context = load_context(map_name)
            prefix_map = context.as_dict()
        else:
            raise ValueError(f"Unknown prefix map: {map_name}")

        for k, v in prefix_map.items():
            if not k:
                if include_defaults and not self._default:
                    self._default = v
            elif k not in self:
                if is_ncname(k):
                    self[k] = v
                else:
                    # logging.getLogger('Namespaces').info(f"biocontext map {map_name} has illegal prefix: {k}")
                    pass


def base_namespace(nsm: Namespaces) -> Optional[str]:
    return nsm._base


def default_namespace(nsm: Namespaces) -> Optional[str]:
    return nsm._default
