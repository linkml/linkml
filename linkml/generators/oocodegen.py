import abc
import re
import unicodedata
from dataclasses import dataclass, field
from typing import List, Optional

from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              SchemaDefinition, SlotDefinition,
                                              TypeDefinition)
from linkml_runtime.utils.formatutils import camelcase, lcamelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml.utils.generator import Generator

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
    classes: List["OOClass"] = field(default_factory=lambda: [])
    imports: List[str] = field(default_factory=lambda: [])


@dataclass
class OOField:
    """
    A field belonging to an OO class that corresponds to a LinkML class slot
    """

    name: SAFE_NAME
    range: TYPE_EXPRESSION = None
    default_value: str = None
    annotations: List[ANNOTATION] = field(default_factory=lambda: [])
    source_slot: SlotDefinition = field(default_factory=lambda: [])


@dataclass
class OOClass:
    """
    An object-oriented class
    """

    # ObjectVars
    name: SAFE_NAME
    is_a: Optional[SAFE_NAME] = None
    abstract: Optional[bool] = None
    mixins: List[SAFE_NAME] = field(default_factory=lambda: [])
    fields: List[OOField] = field(default_factory=lambda: [])
    all_fields: List[OOField] = field(default_factory=lambda: [])
    annotations: List[ANNOTATION] = field(default_factory=lambda: [])
    package: PACKAGE = None
    source_class: ClassDefinition = None


@dataclass
class OOCodeGenerator(Generator):

    # ClassVars
    java_style = True
    visit_all_class_slots = False
    uses_schemaloader = False
    requires_metamodel = False

    template_file: str = None
    """Path to template"""

    package: PACKAGE = "example"

    def __post_init__(self):
        # TODO: consider moving up a level
        self.schemaview = SchemaView(self.schema)
        super().__post_init__()

    @abc.abstractmethod
    def serialize(self, directory: str) -> None:
        raise NotImplementedError("Not implemented.")

    def get_class_name(self, cn):
        return camelcase(cn)

    def get_slot_name(self, sn):
        if self.java_style:
            safe_sn = lcamelcase(sn)
        else:
            safe_sn = underscore(sn)
        return safe_sn

    def map_type(self, t: TypeDefinition) -> str:
        return t.base

    def make_multivalued(self, range: str) -> str:
        return f"List<{range}>"

    def replace_invalid_identifier_character(self, char: str) -> str:
        if char.isalpha() or char.isnumeric() or char == "_":
            return char
        else:
            return underscore(unicodedata.name(char))

    def generate_enum_label(self, value: str) -> str:
        label = underscore(value)
        if label.isidentifier():
            return label
        else:
            # add an underscore if the value starts with a digit
            label = re.sub("(?=^\d)", "number_", label)

            safe_label = ""
            for character in label:
                safe_label += self.replace_invalid_identifier_character(character)

            return safe_label

    def create_documents(self) -> List[OODocument]:
        """
        Currently hardcoded for java-style
        :return:
        """
        sv: SchemaView
        sv = self.schemaview
        docs = []
        for cn in sv.all_classes(imports=False):
            c = sv.get_class(cn)
            safe_cn = camelcase(cn)
            oodoc = OODocument(
                name=safe_cn, package=self.package, source_schema=sv.schema
            )
            docs.append(oodoc)
            ooclass = OOClass(
                name=safe_cn, package=self.package, fields=[], source_class=c
            )
            # currently hardcoded for java style, one class per doc
            oodoc.classes = [ooclass]
            if c.abstract:
                ooclass.abstract = c.abstract
            if c.is_a:
                ooclass.is_a = self.get_class_name(c.is_a)
                parent_slots = sv.class_slots(c.is_a)
            else:
                parent_slots = []
            for sn in sv.class_slots(cn):
                safe_sn = self.get_slot_name(sn)
                slot = sv.induced_slot(sn, cn)
                range = slot.range
                default_value = "null"

                if range is None:
                    # TODO: schemaview should infer this
                    range = sv.schema.default_range

                if range is None:
                    range = "string"

                if range in sv.all_classes():
                    range = self.get_class_name(range)
                    default_value = "null"
                elif range in sv.all_types():
                    t = sv.get_type(range)
                    range = self.map_type(t)
                    if range is None:  # If mapping fails,
                        range = self.map_type(sv.all_types().get("string"))
                elif range in sv.all_enums():
                    range = self.map_type(sv.all_types().get("string"))
                else:
                    raise Exception(f"Unknown range {range}")

                # Set default values for
                if range == "boolean":
                    default_value = "false"
                elif range == "integer":
                    default_value = "0"
                elif range == "String":
                    default_value = '""'

                if slot.multivalued:
                    range = self.make_multivalued(range)
                    default_value = "List.of()"
                oofield = OOField(
                    name=safe_sn,
                    source_slot=slot,
                    range=range,
                    default_value=default_value,
                )
                if sn not in parent_slots:
                    ooclass.fields.append(oofield)
                ooclass.all_fields.append(oofield)

        return docs
