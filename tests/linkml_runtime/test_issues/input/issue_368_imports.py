# Auto generated from issue_368_imports.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-26 14:21
# Schema: mixs
#
# id: https://microbiomedata/schema/mixs
# description:
# license:

import dataclasses
from typing import ClassVar
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue

from linkml_runtime.utils.yamlutils import YAMLRoot
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace


metamodel_version = "1.7.0"

# Namespaces
DEFAULT_ = CurieNamespace('', 'https://microbiomedata/schema/mixs/')


# Types

# Class references



class ParentClass(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/mixs/ParentClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "parent_class"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/mixs/ParentClass")


# Enumerations
class SampleEnum(EnumDefinitionImpl):

    pva = PermissibleValue(text="pva",
                             description="PVA description")
    pvb = PermissibleValue(text="pvb",
                             description="PVB description")

    _defn = EnumDefinition(
        name="SampleEnum",
    )

# Slots
class slots:
    pass

