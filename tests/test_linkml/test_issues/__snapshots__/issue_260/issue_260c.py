# Auto generated from issue_260c.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: issue_260c
#
# id: http://example.org/tests/issue_260c
# description: Another small file to be imported
# license:

from typing import ClassVar

from linkml_runtime.utils.curienamespace import CurieNamespace
from rdflib import URIRef

from .issue_260b import C260b

metamodel_version = "1.7.0"
version = None

# Namespaces
DEFAULT_ = CurieNamespace("", "http://example.org/tests/issue_260c/")


# Types

# Class references


class C260c(C260b):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef(
        "http://example.org/tests/issue_260c/C260c"
    )
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "C260c"
    class_model_uri: ClassVar[URIRef] = URIRef(
        "http://example.org/tests/issue_260c/C260c"
    )


# Enumerations


# Slots
class slots:
    pass
