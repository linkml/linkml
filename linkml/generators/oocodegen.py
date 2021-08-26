import keyword
import os
import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Union, TextIO, Callable, Dict, Iterator, Set
import logging

import click
from linkml_runtime.linkml_model import linkml_files
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import URIRef

import linkml
from linkml.generators import JAVA_GEN_VERSION
from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinition, ClassDefinition, ClassDefinitionName, \
    SlotDefinitionName, DefinitionName, Element, TypeDefinition, Definition, EnumDefinition, PermissibleValue
from linkml_runtime.utils.formatutils import camelcase, underscore, be, wrapped_annotation, split_line, sfx, lcamelcase
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.ifabsent_functions import ifabsent_value_declaration, ifabsent_postinit_declaration, \
    default_curie_or_uri
from linkml_runtime.utils.metamodelcore import builtinnames


SAFE_NAME = str
TYPE_EXPRESSION = str
ANNOTATION = str
PACKAGE = str

@dataclass
class OODocument:
    """
    A collection of one or more OO classes
    """
    name: SAFE_NAME
    package: PACKAGE = None
    source_schema: SchemaDefinition = None
    classes: List["OOClass"] = None


@dataclass
class OOField:
    """
    A field belonging to an OO class that corresponds to a LinkML class slot
    """
    name: SAFE_NAME
    range: TYPE_EXPRESSION
    annotations: List[ANNOTATION] = None
    source_slot: SlotDefinition = None

@dataclass
class OOClass:
    """
    An object-oriented class
    """
    name: SAFE_NAME
    is_a: Optional[SAFE_NAME] = None
    mixins: List[SAFE_NAME] = None
    fields: List[OOField] = None
    annotations: List[ANNOTATION] = None
    package: PACKAGE = None
    source_class: ClassDefinition = None

class OOCodeGenerator(Generator):
    package: PACKAGE = "example"
    java_style = True

    def get_class_name(self, cn):
        return camelcase(cn)

    def get_slot_name(self, sn):
        if self.java_style:
            safe_sn = lcamelcase(sn)
        else:
            safe_sn = underscore(sn)

    def create_documents(self):
        """
        Currently hardcoded for java-style
        :return:
        """
        sv: SchemaView
        sv = self.schemaview
        docs = []
        for cn in sv.all_class(imports=False):
            c = sv.get_class(c)
            safe_cn = camelcase(cn)
            oodoc = OODocument(name=safe_cn, package=self.package, source_schema=sv.schema)
            docs.append(oodoc)
            ooclass = OOClass(name=safe_cn, package=self.package, fields=[], source_class=c)
            if c.is_a:
                ooclass.is_a = self.get_class_name(c.is_a)
                parent_slots = sv.class_slots(c.is_a)
            else:
                parent_slots = []
            for sn in sv.class_slots(cn):
                if sn in parent_slots:
                    # TODO: overrides
                    continue
                safe_sn = self.get_slot_name(sn)
                slot = sv.induced_slot(sn, cn)
                oofield = OOField(name=safe_sn, source_slot=slot)
                ooclass.fields.append(oofield)
        return docs








