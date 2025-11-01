# Auto generated from issue_107.yaml by pythongen.py version: 0.0.1
# Generation date: 2000-01-01T00:00:00
# Schema: schema
#
# id: https://issue_test/107/schema
# description:
# license:


from linkml_runtime.utils.curienamespace import CurieNamespace
from rdflib import URIRef

metamodel_version = "1.7.0"
version = None

# Namespaces
ICD_9 = CurieNamespace("ICD-9", "http://test.org/prefix/ICD9")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = CurieNamespace("", "https://issue_test/107/schema/")


# Types
class String(str):
    """A character string"""

    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "string"
    type_model_uri = URIRef("https://issue_test/107/schema/String")


# Class references


# Enumerations


# Slots
class slots:
    pass
