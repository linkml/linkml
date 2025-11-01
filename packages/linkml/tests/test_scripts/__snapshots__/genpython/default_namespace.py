# Auto generated from default_namespace.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: namespace
#
# id: http://example.org/tests/namespace
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

from dataclasses import dataclass
from typing import Any, ClassVar, Optional

from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef

metamodel_version = "1.7.0"
version = None

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
TEST = CurieNamespace("test", "http://example.org/test/")
DEFAULT_ = CurieNamespace("", "http://example.org/tests/namespace/")


# Types

# Class references


@dataclass(repr=False)
class C1(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/namespace/C1")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "c1"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/tests/namespace/C1")

    s1: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.s1 is not None and not isinstance(self.s1, str):
            self.s1 = str(self.s1)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.s1 = Slot(
    uri=DEFAULT_.s1, name="s1", curie=DEFAULT_.curie("s1"), model_uri=DEFAULT_.s1, domain=None, range=Optional[str]
)
