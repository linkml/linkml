from dataclasses import dataclass
from re import Pattern
from typing import Any

from rdflib import URIRef


@dataclass
class Slot:
    """Runtime slot definition"""

    uri: URIRef
    name: str
    curie: str | None
    model_uri: URIRef

    domain: type | None
    range: Any
    mappings: list[URIRef] | None = None
    pattern: Pattern | None = None
