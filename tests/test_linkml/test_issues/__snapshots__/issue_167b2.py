# Auto generated from issue_167b.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: annotations_test
#
# id: http://example.org/tests/issue167b
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

from typing import ClassVar

from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef


metamodel_version = "1.7.0"
version = None

# Namespaces
EX = CurieNamespace("ex", "http://example.org/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
DEFAULT_ = EX


# Types

# Class references


class MyClass(YAMLRoot):
    """
    Annotations as tag value pairs. Note that altLabel is defined in the default namespace, not in the SKOS namespace
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["MyClass"]
    class_class_curie: ClassVar[str] = "ex:MyClass"
    class_name: ClassVar[str] = "my class"
    class_model_uri: ClassVar[URIRef] = EX.MyClass


class MyClass2(YAMLRoot):
    """
    -> This form of annotations is a tag/value format, which allows annotations to be annotated. Note, however, that
    the annotation source is NOT a CURIE, rather just a string.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["MyClass2"]
    class_class_curie: ClassVar[str] = "ex:MyClass2"
    class_name: ClassVar[str] = "my class 2"
    class_model_uri: ClassVar[URIRef] = EX.MyClass2


# Enumerations


# Slots
class slots:
    pass
