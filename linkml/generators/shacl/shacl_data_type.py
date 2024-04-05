from enum import Enum

from rdflib import URIRef


class DataType:
    linkml_type: str
    uri_ref: URIRef


class ShaclDataType(DataType, Enum):
    STRING = ("string", URIRef("http://www.w3.org/2001/XMLSchema#string"))
    BOOLEAN = ("boolean", URIRef("http://www.w3.org/2001/XMLSchema#boolean"))
    DURATION = ("duration", URIRef("http://www.w3.org/2001/XMLSchema#duration"))
    DATETIME = ("datetime", URIRef("http://www.w3.org/2001/XMLSchema#dateTime"))
    DATE = ("date", URIRef("http://www.w3.org/2001/XMLSchema#date"))
    TIME = ("time", URIRef("http://www.w3.org/2001/XMLSchema#time"))
    DECIMAL = ("decimal", URIRef("http://www.w3.org/2001/XMLSchema#decimal"))
    INTEGER = ("integer", URIRef("http://www.w3.org/2001/XMLSchema#integer"))
    FLOAT = ("float", URIRef("http://www.w3.org/2001/XMLSchema#float"))
    DOUBLE = ("double", URIRef("http://www.w3.org/2001/XMLSchema#double"))
    URI = ("uri", URIRef("http://www.w3.org/2001/XMLSchema#anyURI"))
    CURI = ("curi", URIRef("http://www.w3.org/2001/XMLSchema#string"))
    NCNAME = ("ncname", URIRef("http://www.w3.org/2001/XMLSchema#string"))
    OBJECT_IDENTIFIER = ("objectidentifier", URIRef("http://www.w3.org/ns/shex#iri"))
    NODE_IDENTIFIER = ("nodeidentifier", URIRef("http://www.w3.org/ns/shex#nonLiteral"))
    JSON_POINTER = ("jsonpointer", URIRef("http://www.w3.org/2001/XMLSchema#string"))
    JSON_PATH = ("jsonpath", URIRef("http://www.w3.org/2001/XMLSchema#string"))
    SPARQL_PATH = ("sparqlpath", URIRef("http://www.w3.org/2001/XMLSchema#string"))

    def __new__(cls, linkml_type, uri_ref):
        obj = object.__new__(cls)
        obj.linkml_type = linkml_type
        obj.uri_ref = uri_ref

        return obj

    def __init__(self, linkml_type, uri_ref):
        self.linkml_type = linkml_type
        self.uri_ref = uri_ref
