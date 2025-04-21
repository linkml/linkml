from dataclasses import dataclass
from typing import Optional, Any
from re import Pattern

from rdflib import URIRef


@dataclass
class Slot:
    """ Runtime slot definition """
    uri: URIRef
    name: str
    curie: Optional[str]
    model_uri: URIRef

    domain: Optional[type]
    range: Any
    mappings: Optional[list[URIRef]] = None
    pattern: Optional[Pattern] = None
