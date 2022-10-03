import logging
import os
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

import click
from jsonasobj2 import JsonObj, as_json
from linkml_runtime.linkml_model.meta import (ClassDefinition, EnumDefinition,
                                              PermissibleValue,
                                              PermissibleValueText,
                                              SchemaDefinition, SlotDefinition, ClassDefinitionName)
from linkml_runtime.utils.formatutils import be, camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml.utils.generator import Generator, shared_arguments

# Map from underlying python data type to json equivalent
# Note: The underlying types are a union of any built-in python datatype + any type defined in
#       linkml-runtime/utils/metamodelcore.py
# Note the keys are all lower case
json_schema_types: Dict[str, Tuple[str, Optional[str]]] = {
    "int": ("integer", None),
    "integer": ("integer", None),
    "bool": ("boolean", None),
    "boolean": ("boolean", None),
    "float": ("number", None),
    "double": ("number", None),
    "decimal": ("number", None),
    "xsddate": ("string", "date"),
    "xsddatetime": ("string", "date-time"),
    "xsdtime": ("string", "time"),
}

WITH_OPTIONAL_IDENTIFIER_SUFFIX = "__identifier_optional"


@dataclass
class JsonSchemaGenerator(Generator):
    """
    Generates JSONSchema documents from a LinkML SchemaDefinition

    - Each linkml class generates a schema
    - inheritance hierarchies are rolled-down from ancestors
    - Composition not yet implemented
    - Enumerations treated as strings
    - Foreign key references are treated as semantics-free strings
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = ["json"]
    visit_all_class_slots = True
    visit_all_slots = True
    uses_schemaloader = True
    #requires_metamodel = False

    #@deprecated("Use top_class")
    topClass: Optional[str] = None

    not_closed: Optional[bool] = field(default_factory=lambda: True)
    """If not closed, then an open-ended set of attributes can be instantiated for any object"""

    schemaobj: JsonObj = None
    clsobj: JsonObj = None
    inline: bool = False
    top_class: Optional[ClassDefinitionName] = None  ## JSON object is one instance of this
    """Class instantiated by the root node of the document tree"""

    entryProperties: dict = field(default_factory=lambda: {})
    include_range_class_descendants: bool = field(default_factory=lambda: False)

    # JSON-Schema does not have inheritance,
    # so we duplicate slots from inherited parents and mixins
    # Maps e.g. Person --> Person__identifier_optional
    # for use when Person is a range of an inlined-as-dict slot
    optional_identifier_class_map: Dict[str, Tuple[str, str]] = field(default_factory=lambda: {})

    def __post_init__(self):
        if self.topClass:
            logging.warning(f"topCls is deprecated - use top_class")
            self.top_class = self.topClass
        # TODO: consider moving up a level
        self.schemaview = SchemaView(self.schema)
        super().__post_init__()

    def visit_schema(self, inline: bool = False, **kwargs) -> None:
        self.inline = inline
        #logging.error(f"NC: {self.not_closed}")
        self.schemaobj = JsonObj(
            title=self.schema.name,
            type="object",
            metamodel_version=self.schema.metamodel_version,
            version=self.schema.version if self.schema.version else None,
            properties={},
            additionalProperties=self.not_closed,
        )
        for p, c in self.entryProperties.items():
            self.schemaobj["properties"][p] = {
                "type": "array",
                "items": {"$ref": f"#/$defs/{camelcase(c)}"},
            }
        self.schemaobj["$schema"] = "http://json-schema.org/draft-07/schema#"
        self.schemaobj["$id"] = self.schema.id
        self.schemaobj["$defs"] = JsonObj()
        self.schemaobj["required"] = []

    def end_schema(self, **_) -> None:
        # create more lax version of every class that is used as an inlined dict reference;
        # in this version, the primary key/identifier is optional, since it is used as the key of the dict
        for cls_name, (
            id_slot,
            cls_name_lax,
        ) in self.optional_identifier_class_map.items():
            lax_cls = deepcopy(self.schemaobj["$defs"][cls_name])
            lax_cls.required.remove(id_slot)
            self.schemaobj["$defs"][cls_name_lax] = lax_cls
        print(as_json(self.schemaobj, sort_keys=True))

    def visit_class(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract:
            return False
        additional_properties = False
        if self.is_class_unconstrained(cls):
            additional_properties = True
        self.clsobj = JsonObj(
            title=camelcase(cls.name),
            type="object",
            properties=JsonObj(),
            required=[],
            additionalProperties=additional_properties,
            description=be(cls.description),
        )
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        self.schemaobj["$defs"][camelcase(cls.name)] = self.clsobj

    def visit_enum(self, enum: EnumDefinition) -> bool:
        # TODO: this only works with explicitly permitted values. It will need to be extended to
        # support other pv_formula

        def extract_permissible_text(pv):
            if type(pv) is str:
                return pv
            if type(pv) is PermissibleValue:
                return pv.text.code
            if type(pv) is PermissibleValueText:
                return pv
            raise ValueError(f"Invalid permissible value in enum {enum}: {pv}")

        permissible_values_texts = list(
            map(extract_permissible_text, enum.permissible_values or [])
        )

        self.schemaobj["$defs"][camelcase(enum.name)] = JsonObj(
            title=camelcase(enum.name),
            type="string",
            enum=permissible_values_texts,
            description=be(enum.description),
        )

    def get_ref_for_descendants(self, descendants: List):
        ref_list = []
        for descendant in descendants:
            descendant_class = self.schema.classes[descendant]
            if descendant_class.abstract:
                continue
            descendant_ref = JsonObj()
            descendant_ref_obj = camelcase(descendant)
            descendant_ref["$ref"] = f"#/$defs/{descendant_ref_obj}"
            ref_list.append(descendant_ref)
        return ref_list

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ) -> None:
        typ = None  # JSON Schema type (https://json-schema.org/understanding-json-schema/reference/type.html)
        reference = None  # Reference to a JSON schema entity (https://json-schema.org/understanding-json-schema/structuring.html#ref)
        fmt = None  # JSON Schema format (https://json-schema.org/understanding-json-schema/reference/string.html#format)
        reference_obj = None
        descendants = None
        if slot.range in self.schema.types:
            (typ, fmt) = json_schema_types.get(
                self.schema.types[slot.range].base.lower(), ("string", None)
            )
        elif slot.range in self.schema.enums:
            reference_obj = camelcase(slot.range)
            reference = f"#/$defs/{reference_obj}"
            typ = "object"
        elif slot.range in self.schema.classes and slot.inlined:
            reference_obj = camelcase(slot.range)
            descendants = self.schemaview.class_descendants(slot.range)
            reference = f"#/$defs/{reference_obj}"
            typ = "object"
        else:
            typ = "string"
        if slot.inlined:
            range_cls = self.schema.classes[slot.range]
            id_slot = None
            for sn in range_cls.slots:
                s = self.schema.slots[sn]
                # TODO: extension_tag should be declared as a key in extensions.yaml in metamodel
                if (
                    s.identifier
                    or s.key
                    or (
                        s.alias == "tag"
                        and (range_cls == "extension" or range_cls == "annotation")
                    )
                ):
                    id_slot = s
                    break
            # If inline we have to include redefined slots
            ref = JsonObj()
            ref["$ref"] = reference
            if slot.multivalued:
                if id_slot is not None and not slot.inlined_as_list:
                    prop = JsonObj(
                        additionalProperties={
                            "$ref": f"{reference}{WITH_OPTIONAL_IDENTIFIER_SUFFIX}"
                        }
                    )
                    if id_slot.alias is not None:
                        id_slot_name = id_slot.alias
                    else:
                        id_slot_name = id_slot.name
                    self.optional_identifier_class_map[reference_obj] = (
                        id_slot_name,
                        f"{reference_obj}{WITH_OPTIONAL_IDENTIFIER_SUFFIX}",
                    )
                else:
                    if descendants and self.include_range_class_descendants:
                        items = JsonObj()
                        ref_list = self.get_ref_for_descendants(descendants)
                        items["oneOf"] = ref_list
                        prop = JsonObj(type="array", items=items)
                    else:
                        prop = JsonObj(type="array", items=ref)
            else:
                if descendants and self.include_range_class_descendants:
                    prop = JsonObj()
                    ref_list = self.get_ref_for_descendants(descendants)
                    prop["oneOf"] = ref_list
                else:
                    prop = ref
        else:
            if slot.multivalued:
                if reference is not None:
                    prop = JsonObj(type="array", items={"$ref": reference})
                elif fmt is None:
                    prop = JsonObj(type="array", items={"type": typ})
                else:
                    prop = JsonObj(type="array", items={"type": typ, "format": fmt})
            else:
                if reference is not None:
                    prop = JsonObj({"$ref": reference})
                elif fmt is None:
                    prop = JsonObj(type=typ)
                else:
                    prop = JsonObj(type=typ, format=fmt)

        if slot.description:
            prop.description = slot.description
        if slot.required:
            self.clsobj.required.append(underscore(aliased_slot_name))
        if slot.pattern:
            # See https://github.com/linkml/linkml/issues/193
            prop.pattern = slot.pattern
        if slot.minimum_value is not None:
            prop.minimum = slot.minimum_value
        if slot.maximum_value is not None:
            prop.maximum = slot.maximum_value
        if slot.equals_string is not None:
            prop.const = slot.equals_string
        if slot.equals_number is not None:
            prop.const = slot.equals_number
        self.clsobj.properties[underscore(aliased_slot_name)] = prop
        if (
            self.top_class is not None and camelcase(self.top_class) == camelcase(cls.name)
        ) or (self.top_class is None and cls.tree_root):
            self.schemaobj.properties[underscore(aliased_slot_name)] = prop

            if slot.required:
                self.schemaobj.required.append(underscore(aliased_slot_name))


@shared_arguments(JsonSchemaGenerator)
@click.command()
@click.option(
    "-i",
    "--inline",
    is_flag=True,
    help="""
Generate references to types rather than inlining them.
Note that declaring a slot as inlined: true will always inline the class
""",
)
@click.option(
    "-t",
    "--top-class",
    help="""
Top level class; slots of this class will become top level properties in the json-schema
""",
)
@click.option(
    "--not-closed/--closed",
    default=True,
    show_default=True,
    help="""
Set additionalProperties=False if closed otherwise true if not closed at the global level
""",
)
@click.option(
    "--include-range-class-descendants/--no-range-class-descendants",
    default=False,
    show_default=False,
    help="""
When handling range constraints, include all descendants of the range class instead of just the range class
""",
)
def cli(yamlfile, **kwargs):
    """Generate JSON Schema representation of a LinkML model"""
    print(JsonSchemaGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
