import builtins
import datetime
import re
from dataclasses import field
from decimal import Decimal
from typing import Union, Optional, Tuple
from urllib.parse import urlparse

from ShExJSG.ShExJ import IRIREF, PN_PREFIX
from rdflib import Literal, BNode, URIRef
from rdflib.namespace import is_ncname
from rdflib.term import Identifier as rdflib_Identifier

from linkml_runtime.utils.namespaces import Namespaces
from linkml_runtime.utils.strictness import is_strict

# Reference Decimal to make sure it stays in the imports
_z = Decimal(1)

# ===========================
# Fields for use in dataclass
# ===========================
from linkml_runtime.utils.yamlutils import TypedNode


def empty_list():
    """ Return a field with a list factory """
    return field(default_factory=list)


def empty_dict():
    """ Return a field with a dictionary factory """
    return field(default_factory=dict)


def addl_args():
    rval = field(default_factory=dict)
    rval.name = '**args'
    return rval


def empty_set():
    """" Return a field with a set factory """
    return field(default_factory=set)


def bnode():
    """ Return a field with a BNode factory """
    return field(default_factory=lambda: BNode().n3())


# List of builtins for mangling names
builtinnames = dir(builtins)


class NCName(str):
    """ Wrapper for NCName class """
    def __init__(self, v: str) -> None:
        if is_strict() and not self.is_valid(v):
            raise ValueError(f"{TypedNode.yaml_loc(v)}{v}: Not a valid NCName")
        self.nsm: Optional[Namespaces] = None
        super().__init__()

    @classmethod
    def is_valid(cls, v: str) -> bool:
        return is_ncname(v) if v else True      # Empty is default name


class Identifier(str, TypedNode):
    """ A datatype that can be a URI, CURIE or a BNode """
    def __init__(self, v: Union[str, URIRef, BNode, "URIorCURIE", "Identifier"]) -> None:
        v = str(v) if not isinstance(v, str) else v
        if is_strict() and not self.is_valid(v):
            raise ValueError(f"{v}: is not a valid Identifier")
        TypedNode.__init__(self, v)

    @classmethod
    def is_valid(cls, v: Union[str, URIRef, BNode, "URIorCURIE", "Identifier"]) -> bool:
        if v is None:
            return False
        if v.startswith('_:'):
            pfx, ln = v.split(':')
            return len(ln) == 1 and bool(Curie.term_name.match(ln))
        else:
            return URIorCURIE.is_valid(v)

    def as_identifier(self, nsm: Optional[Namespaces]) -> Optional[rdflib_Identifier]:
        if self.startswith('_:'):
            return BNode(self)
        elif URIorCURIE.is_absolute(self):
            return URIRef(self)
        elif nsm:
            return URIorCURIE(self).as_uri(nsm)
        return None


class URIorCURIE(Identifier):
    """ A datatype that can either be a URI or a CURIE """
    def __init__(self, v: Union[str, URIRef, "Curie", "URIorCURIE"]) -> None:
        if is_strict() and not URIorCURIE.is_valid(v):
            raise ValueError(f"{v} is not a valid URI or CURIE")
        super().__init__(v)

    @classmethod
    def is_valid(cls, v: Union[str, URIRef, "Curie", "URIorCURIE"]) -> bool:
        if not isinstance(v, (str, URIRef, Curie, URIorCURIE)):
            return False
        v = str(v)
        if ':' in v and '://' not in v:
            return URIorCURIE.is_curie(v)
        else:
            return URI.is_valid(v)

    @staticmethod
    def is_absolute(v: str) -> bool:
        return bool(urlparse(v).netloc)

    @staticmethod
    def is_curie(v: str, nsm: Optional[Namespaces] = None) -> bool:
        if ':' in v and '://' not in v:
            ns, ln = v.split(':', 1)
            return len(ns) == 0 or (NCName.is_valid(ns) and
                                    (nsm is None or any(ns == nsns for nsns, _ in nsm.namespaces())))
        return False

    def as_uri(self, nsm: Namespaces) -> Optional[URIRef]:
        if self.is_absolute(self):
            return URIRef(self)
        return Curie(self).as_uri(nsm)


class URI(URIorCURIE):
    """ A relative absolute URI
    """
    def __init__(self, v: str) -> None:
        if is_strict() and not URI.is_valid(v):
            raise ValueError(f"{v}: is not a valid URI")
        super().__init__(v)

    @classmethod
    def is_valid(cls, v: str) -> bool:
        return v is not None and not URIorCURIE.is_curie(v) and isinstance(v, IRIREF)


class Curie(URIorCURIE):

    """ Wrapper for an element that MUST be represented as a CURIE """
    def __init__(self, v: str) -> None:
        if is_strict() and not self.is_valid(v):
            raise ValueError(f"{v} is not a valid CURIE")
        super().__init__(v)

    # TODO: see whether we can leverage the rdflib RDFA termorcurie package
    term_name = re.compile("^[A-Za-z]([A-Za-z0-9._-]|/)*$")

    @classmethod
    def ns_ln(cls, v: str) -> Optional[Tuple[str, str]]:
        # See if this is indeed a valid CURIE, ie, it can be split by a colon
        curie_split = v.split(':', 1)
        if len(curie_split) == 1:
            # there is no ':' character in the string, ie, it is not a valid CURIE
            return None
        else:
            prefix = curie_split[0].lower()
            if not NCName.is_valid(prefix):
                return None
            reference = curie_split[1]
            if not cls.term_name.match(reference):
                return None
        return prefix, reference

    @classmethod
    def is_valid(cls, v: str) -> bool:
        pnln = cls.ns_ln(v)
        return pnln is not None and (not pnln[0] or isinstance(pnln[0], PN_PREFIX))

    # This code was extracted from the termorcurie package of the rdfa
    def as_uri(self, nsm: Namespaces) -> Optional[URIRef]:
        """ Return the URI for the CURIE if a mapping is available, otherwise return None """
        try:
            return nsm.uri_for(self)
        except ValueError:
            pass
        return None


class Bool:
    """ Wrapper for boolean datatype """
    bool_true = re.compile(r'([Tt]rue)|(1)$')
    bool_false = re.compile(r'([Ff]alse)|(0)$')

    def __new__(cls, v: Union[str, bool, "Bool"]) -> bool:
        if isinstance(v, bool):
            return v
        if cls.bool_true.match(str(v)):
            return True
        if cls.bool_false.match(str(v)):
            return False
        if is_strict():
            raise ValueError(f"{v}: Must be a boolean value")
        return bool(v)

    @classmethod
    def is_valid(cls, v: str) -> bool:
        """ Determine whether the string v is a valid instance of bool """
        return isinstance(v, bool) or cls.bool_true.match(str(v)) or cls.bool_false.match(str(v))


class XSDTime(str, TypedNode):
    """ Wrapper for time datatype """
    def __new__(cls, value: Union[str, datetime.time, datetime.datetime, Literal]) -> str:
        if is_strict() and not cls.is_valid(value):
            raise ValueError(f"{value} is not a valid time")
        if isinstance(value, Literal):
            value = value.value
        try:
            if not isinstance(value, datetime.time):
                value = datetime.time.fromisoformat(value)
            return datetime.time.fromisoformat(str(value)).isoformat()
        except TypeError as e:
            pass
        except ValueError as e:
            pass
        if not is_strict():
            return str(value)
        raise e

    @classmethod
    def is_valid(cls, value: Union[str, datetime.time, datetime.datetime, Literal]) -> bool:
        if isinstance(value, Literal):
            value = value.value
        if isinstance(value, (datetime.time, datetime.datetime)):
            value = value.isoformat()
        try:
            datetime.time.fromisoformat(str(value))
        except ValueError:
            return False
        return True


class XSDDate(str, TypedNode):
    """ Wrapper for date datatype """
    def __new__(cls, value: Union[str, datetime.date, Literal]) -> str:
        if is_strict() and not cls.is_valid(value):
            raise ValueError(f"{value} is not a valid date")
        if isinstance(value, Literal):
            value = value.value
        try:
            if not isinstance(value, datetime.date):
                value = datetime.date.fromisoformat(str(value))
            return value.isoformat()
        except TypeError as e:
            pass
        except ValueError as e:
            pass
        if not is_strict():
            return str(value)
        raise e

    @classmethod
    def is_valid(cls, value: Union[str, datetime.date, Literal]) -> bool:
        if isinstance(value, Literal):
            value = value.value
        if isinstance(value, datetime.date):
            value = value.isoformat()
        try:
            datetime.date.fromisoformat(str(value))
        except ValueError:
            return False
        return True


class XSDDateTime(str, TypedNode):
    """ Wrapper for date time dataclass """
    def __new__(cls, value: Union[str, datetime.datetime, Literal]) -> str:
        if is_strict() and not cls.is_valid(value):
            raise ValueError(f"{value} is not a valid datetime")
        if isinstance(value, Literal):
            value = value.value
        try:
            if not isinstance(value, datetime.datetime):
                value = datetime.datetime.fromisoformat(value)      # Note that this handles non 'T' format as well
            return value.isoformat()
        except TypeError as e:
            pass
        except ValueError as e:
            pass
        if not is_strict():
            return str(value)
        raise e

    @classmethod
    def is_valid(cls, value: Union[str, datetime.datetime, Literal]) -> bool:
        if isinstance(value, Literal):
            value = value.value
        if isinstance(value, datetime.datetime):
            value = value.isoformat()
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            return False
        return True


class NodeIdentifier(Identifier):
    """ A RDFLib Identifier that represents a URI, CURIE or BNode in a model """

    def __new__(cls, v: Union[str, URIRef, URIorCURIE, "NodeIdentifier", BNode]) -> "NodeIdentifier":
        if hasattr(v, 'id'):        # Allows passing instances of identified objects
            v = v.id
        if isinstance(v, NodeIdentifier):
            if is_strict() and not issubclass(type(v), cls):
                raise ValueError(f"Invalid identifier type for {cls.__name__}: {v} ({type(v).__name__})")
            else:
                return super().__new__(cls, v)
        elif type(v) in (str, URIRef, URIorCURIE, BNode) or not is_strict():
            return super().__new__(cls, str(v))
        else:
            raise ValueError(f"Unknown identifier for {cls.__name__}: {v}")

    def __post_init__(self):
        pass


class ElementIdentifier(NodeIdentifier):
    """ A URIorCURIE that represents an element in a model """

    def __new__(cls, v: Union[str, URIRef, URIorCURIE, NodeIdentifier, "ElementIdentifier"]) -> "ElementIdentifier":
        if hasattr(v, 'id'):        # Allows passing instances of identified objects
            v = v.id
        if is_strict() and (type(v) is BNode or str(v).startswith('_:')):
            raise ValueError(f"Invalid identifier type for {cls.__name__}: {v} ({type(v).__name__})")
        return super().__new__(cls, v)

    def __post_init__(self):
        pass
