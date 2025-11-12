# Auto generated from kitchen_sink.yaml by namespacegen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: kitchen_sink
#
# id: https://w3id.org/linkml/tests/kitchen_sink
# description: Kitchen Sink Schema This schema does not do anything useful. It exists to test all features of
#              linkml. This particular text field exists to demonstrate markdown within a text field: Lists: * a *
#              b * c And links, e.g to [Person](Person.md)
# license: https://creativecommons.org/publicdomain/zero/1.0/

from collections import defaultdict
from typing import Iterable, Dict, Tuple

from linkml_runtime.utils.curienamespace import CurieNamespace

GENE = 'gene'
DISEASE = 'disease'
CHEMICAL_SUBSTANCE = 'chemical substance'

SYMBOL = 'Approved_Symbol'


class IdentifierResolverException(RuntimeError):
    pass


class BiolinkNameSpace:
    """
    Map of BioLink Model registered URI Namespaces
    """

    _namespaces = [
        CurieNamespace('A', 'http://example.org/activities/'),
        CurieNamespace('BFO', 'http://purl.obolibrary.org/obo/BFO_'),
        CurieNamespace('CODE', 'http://example.org/code/'),
        CurieNamespace('P', 'http://example.org/person/'),
        CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_'),
        CurieNamespace('ROR', 'http://example.org/ror/'),
        CurieNamespace('biolink', 'https://w3id.org/biolink/'),
        CurieNamespace('bizcodes', 'https://example.org/bizcodes/'),
        CurieNamespace('core', 'https://w3id.org/linkml/tests/core/'),
        CurieNamespace('dce', 'http://purl.org/dc/elements/1.1/'),
        CurieNamespace('ks', 'https://w3id.org/linkml/tests/kitchen_sink/'),
        CurieNamespace('lego', 'http://geneontology.org/lego/'),
        CurieNamespace('linkml', 'https://w3id.org/linkml/'),
        CurieNamespace('pav', 'http://purl.org/pav/'),
        CurieNamespace('prov', 'http://www.w3.org/ns/prov#'),
        CurieNamespace('schema', 'http://schema.org/'),
        CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#'),
        CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#'),
    ]

    # class level dictionaries

    _prefix_map: Dict[str, CurieNamespace] = {}

    @classmethod
    def _get_prefix_map(cls):
        if not cls._prefix_map:
            for ns in cls._namespaces:
                # index by upper case for uniformity of search
                cls._prefix_map[ns.prefix.upper()] = ns
        return cls._prefix_map

    @classmethod
    def parse_curie(cls, curie: str) -> Tuple[CurieNamespace, str]:
        """
        Parse a candidate CURIE
        :param curie: candidate curie string
        :return: CURIE namespace and object_id
        """
        found = CurieNamespace("", ""), curie  # default value if not a CURIE or unknown XMLNS prefix
        if ':' in curie:
            part = curie.split(":")
            # Normalize retrieval with upper case of prefix for lookup
            prefix = part[0].upper()
            if prefix in cls._get_prefix_map():
                found = cls._prefix_map[prefix], part[1]
        return found

    @classmethod
    def parse_uri(cls, uri: str) -> Tuple[CurieNamespace,  str]:
        """
        Parse a candidate URI
        :param uri: candidate URI string
        :return: namespace and object_id
        """
        found = CurieNamespace("", ""), uri   # default value returned if unknown URI namespace

        # TODO: is there a more efficient lookup scheme here than a linear search of namespaces?
        for ns in cls._namespaces:
            base_uri = str(ns)
            if uri.startswith(base_uri):
                # simple minded deletion of base_uri to give the object_id
                object_id = uri.replace(base_uri, "")
                found = ns, object_id
                break
        return found

    @classmethod
    def parse_identifier(cls,  identifier: str) -> Tuple[CurieNamespace,  str]:

        # trivial case of a null identifier?
        if not identifier:
            return CurieNamespace("", ""), ""

        # check if this is a candidate URI...
        if identifier.lower().startswith("http"):
            # guess that perhaps it is, so try to parse it
            return cls.parse_uri(identifier)

        else:  # attempt to parse as a CURIE
            return cls.parse_curie(identifier)


def object_id(identifier, keep_version=False) -> str:
    """
    Returns the core object_id of a CURIE, with or without the version suffix.
    Note:  not designed to be used with a URI (will give an invalid outcome)
    :param identifier: candidate CURIE identifier for processing
    :param keep_version: True if the version string suffix is to be retained in the identifier
    :return:
    """
    # trivial case: null input value?
    if not identifier:
        return identifier

    if ':' in identifier:
        identifier = identifier.split(":")[1]

    if not keep_version and '.' in identifier:
        identifier = identifier.split(".")[0]

    return identifier


def fix_curies(identifiers, prefix=''):
    """
    Applies the specified XMLNS prefix to (an) identifier(s) known
    to be "raw" IDs as keys in a dictionary or elements in a list (or a simple string)
    :param identifiers:
    :param prefix:
    :return:
    """
    if not prefix:
        # return identifiers without modification
        # Caller may already consider them in curie format
        return identifiers

    if isinstance(identifiers, dict):
        curie_dict = defaultdict(dict)
        for key in identifiers.keys():
            curie_dict[prefix + ':' + object_id(key, keep_version=True)] = identifiers[key]
        return curie_dict

    # identifiers assumed to be just a single object identifier
    elif isinstance(identifiers, str):
        # single string to convert
        return prefix + ':' + object_id(identifiers, keep_version=True)

    elif isinstance(identifiers, Iterable):
        return [prefix + ':' + object_id(x, keep_version=True) for x in identifiers]

    else:
        raise RuntimeError("fix_curie() is not sure how to fix an instance of data type '", type(identifiers))


def curie(identifier) -> str:
    # Ignore enpty strings
    if not identifier:
        return ""
    else:
        namespace: CurieNamespace
        identifier_object_id: str
        namespace, identifier_object_id = BiolinkNameSpace.parse_identifier(identifier)
        return namespace.curie(identifier_object_id)

