import json
import logging
import os
from collections import UserDict
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

import click
from linkml_runtime.linkml_model.meta import (AnonymousClassExpression,
                                              AnonymousSlotExpression,
                                              ClassDefinition, EnumDefinition,
                                              PermissibleValue,
                                              PermissibleValueText,
                                              SlotDefinition, ClassDefinitionName,
                                              metamodel_version)
from linkml_runtime.utils.formatutils import be, camelcase, underscore

from linkml._version import __version__
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

class JsonSchema(UserDict):

    OPTIONAL_IDENTIFIER_SUFFIX = "__identifier_optional"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lax_forward_refs = {}

    def add_def(self, name: str, subschema: "JsonSchema") -> None:
        canonical_name = camelcase(name)

        if '$defs' not in self:
            self['$defs'] = {}

        if 'title' not in subschema:
            subschema['title'] = canonical_name

        self['$defs'][canonical_name] = subschema

        if canonical_name in self._lax_forward_refs:
            identifier_name = self._lax_forward_refs.pop(canonical_name)
            self.add_lax_def(canonical_name, identifier_name)

    def add_lax_def(self, name: str, identifier_name: str) -> None:
        # JSON-Schema does not have inheritance,
        # so we duplicate slots from inherited parents and mixins
        # Maps e.g. Person --> Person__identifier_optional
        # for use when Person is a range of an inlined-as-dict slot
        canonical_name = camelcase(name)

        if "$defs" not in self or canonical_name not in self["$defs"]:
            self._lax_forward_refs[canonical_name] = identifier_name
        else:
            lax_cls = deepcopy(self["$defs"][canonical_name])
            lax_cls['required'].remove(identifier_name)
            self["$defs"][canonical_name + self.OPTIONAL_IDENTIFIER_SUFFIX] = lax_cls

    def add_property(self, name: str, subschema: "JsonSchema", required: bool = False) -> None:
        canonical_name = underscore(name)
        
        if 'properties' not in self:
            self['properties'] = {}
        
        self['properties'][canonical_name] = subschema

        if required:
            if 'required' not in self:
                self['required'] = []
            
            self['required'].append(canonical_name)

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.data, default=lambda d: d.data, **kwargs)

    @classmethod
    def ref_for(cls, class_name: Union[str, List[str]], identifier_optional: bool = False):
        def _ref(class_name):
            return { 
                "$ref": f"#/$defs/{camelcase(class_name)}{cls.OPTIONAL_IDENTIFIER_SUFFIX if identifier_optional else ''}"
            }
        if isinstance(class_name, list):
            return {
                "oneOf": [_ref(name) for name in class_name]
            }
        else:
            return _ref(class_name)

    @classmethod
    def array_of(cls, subschema: "JsonSchema") -> "JsonSchema":
        schema = {
            "type": "array",
            "items": subschema
        }

        return JsonSchema(schema)


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
    generatorversion = "0.0.3"
    valid_formats = ["json"]
    uses_schemaloader = False

    #@deprecated("Use top_class")
    topClass: Optional[str] = None

    not_closed: Optional[bool] = field(default_factory=lambda: True)
    """If not closed, then an open-ended set of attributes can be instantiated for any object"""

    indent: int = 4

    inline: bool = False
    top_class: Optional[ClassDefinitionName] = None  ## JSON object is one instance of this
    """Class instantiated by the root node of the document tree"""

    include_range_class_descendants: bool = field(default_factory=lambda: False)

    top_level_schema: JsonSchema = None

    def __post_init__(self):
        if self.topClass:
            logging.warning(f"topClass is deprecated - use top_class")
            self.top_class = self.topClass

        super().__post_init__()

    def start_schema(self, inline: bool = False) -> JsonSchema:
        self.inline = inline

        self.top_level_schema = JsonSchema({
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": self.schema.id,
            "metamodel_version": metamodel_version,
            "version": self.schema.version if self.schema.version else None,
            "title": self.schema.name,
            "type": "object",
            "additionalProperties": self.not_closed,
        })

    def handle_class(self, cls: ClassDefinition) -> None:
        if cls.mixin or cls.abstract:
            return
        
        additional_properties = False
        if self.is_class_unconstrained(cls):
            additional_properties = True
        
        class_subschema = JsonSchema({
            "type": "object",
            "additionalProperties": additional_properties,
            "description": be(cls.description),
        })

        for slot_definition in self.schemaview.class_induced_slots(cls.name):
            self.handle_class_slot(
                subschema=class_subschema,
                cls=cls,
                slot=slot_definition
            )

        rule_subschemas = []
        for rule in cls.rules:
            subschema = JsonSchema()

            open_world = rule.open_world
            if open_world is None:
                open_world = False

            if_subschema = self.get_subschema_for_anonymous_class(rule.preconditions, properties_required=True)
            if if_subschema:
                subschema["if"] = if_subschema
            
            then_subschema = self.get_subschema_for_anonymous_class(rule.postconditions, properties_required=not open_world)
            if then_subschema:
                subschema["then"] = then_subschema

            # same as required requirements as postconditions?
            else_subschema = self.get_subschema_for_anonymous_class(rule.elseconditions, properties_required=not open_world)
            if else_subschema:
                subschema["else"] = else_subschema

            rule_subschemas.append(subschema)

            if rule.bidirectional:
                inverse_subschema = JsonSchema()

                if then_subschema:
                    inverse_subschema["if"] = then_subschema
                
                if if_subschema:
                    inverse_subschema["then"] = if_subschema

                rule_subschemas.append(inverse_subschema)

        if len(rule_subschemas) == 1:
            self.top_level_schema.update(rule_subschemas[0])
        elif len(rule_subschemas) > 1:
            self.top_level_schema["allOf"] = rule_subschemas

        self.top_level_schema.add_def(cls.name, class_subschema)


    def get_subschema_for_anonymous_class(self, cls: AnonymousClassExpression, properties_required: bool = False) -> Union[None, JsonSchema]:
        if not cls:
            return None

        subschema = JsonSchema()
        for slot in cls.slot_conditions.values():
            prop = self.get_subschema_for_slot(slot, omit_type=True)
            subschema.add_property(self.aliased_slot_name(slot), prop, properties_required)

        if cls.any_of is not None and len(cls.any_of) > 0:
            subschema["anyOf"] = [self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.any_of]

        if cls.all_of is not None and len(cls.all_of) > 0:
            subschema["allOf"] = [self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.all_of]

        if cls.exactly_one_of is not None and len(cls.exactly_one_of) > 0:
            subschema["oneOf"] = [self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.exactly_one_of]

        if cls.none_of is not None and len(cls.none_of) > 0:
            subschema["not"] = {
                "anyOf": [self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.any_of]
            }

        return subschema


    def handle_enum(self, enum: EnumDefinition) -> None:
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

        enum_schema = JsonSchema({
            "type": "string",
            "enum": permissible_values_texts,
            "description": be(enum.description),
        })
        self.top_level_schema.add_def(enum.name, enum_schema)

    def get_type_info_for_slot_subschema(self, slot: AnonymousSlotExpression, slot_is_inlined: bool) -> Tuple[str, str, Union[str, List[str]]]:
        typ = None  # JSON Schema type (https://json-schema.org/understanding-json-schema/reference/type.html)
        reference = None  # Reference to a JSON schema entity (https://json-schema.org/understanding-json-schema/structuring.html#ref)
        fmt = None  # JSON Schema format (https://json-schema.org/understanding-json-schema/reference/string.html#format)

        if slot.range in self.schemaview.all_types().keys():
            schema_type = self.schemaview.induced_type(slot.range)
            (typ, fmt) = json_schema_types.get(schema_type.base.lower(), ("string", None))
        elif slot.range in self.schemaview.all_enums().keys():
            reference = slot.range
        elif slot_is_inlined and slot.range in self.schemaview.all_classes().keys():
            descendants = [desc for desc in self.schemaview.class_descendants(slot.range) 
                if not self.schemaview.get_class(desc).abstract]
            if descendants and self.include_range_class_descendants:
                reference = descendants
            else:
                reference = slot.range
        else:
            typ = "string"

        return (typ, fmt, reference)

    def get_subschema_for_slot(self, slot: SlotDefinition, omit_type: bool = False) -> JsonSchema:
        slot_has_range_union = slot.any_of is not None and len(slot.any_of) > 0 and all(s.range is not None for s in slot.any_of)
        if omit_type:
            prop = JsonSchema()
        else:
            slot_is_inlined = self.schemaview.is_inlined(slot)

            if slot_has_range_union:
                items = []
                for sub_slot in slot.any_of:
                    typ, fmt, reference = self.get_type_info_for_slot_subschema(sub_slot, slot_is_inlined)
                    if reference is not None:
                        item = JsonSchema.ref_for(reference)
                    elif fmt is None:
                        item = JsonSchema({"type": typ})
                    else:
                        item = JsonSchema({"type": typ, "format": fmt})
                    items.append(item)
                subschema = JsonSchema({
                    "anyOf": items
                })
                if slot.multivalued:
                    prop = JsonSchema.array_of(subschema)
                else:
                    prop = subschema
            else:
                typ, fmt, reference = self.get_type_info_for_slot_subschema(slot, slot_is_inlined)
                if slot_is_inlined:
                    # If inline we have to include redefined slots
                    if slot.multivalued:
                        range_id_slot = self.schemaview.get_identifier_slot(slot.range, use_key=True)
                        if range_id_slot is not None and not slot.inlined_as_list:
                            prop = JsonSchema({
                                "type": "object",
                                "additionalProperties": JsonSchema.ref_for(reference, identifier_optional=True)
                            })
                            self.top_level_schema.add_lax_def(reference, self.aliased_slot_name(range_id_slot))
                        else:
                            prop = JsonSchema.array_of(JsonSchema.ref_for(reference))
                    else:
                        prop = JsonSchema.ref_for(reference)
                else:
                    if slot.multivalued:
                        if reference is not None:
                            prop = JsonSchema.array_of(JsonSchema.ref_for(reference))
                        elif fmt is None:
                            prop = JsonSchema.array_of(JsonSchema({"type": typ}))
                        else:
                            prop = JsonSchema.array_of(JsonSchema({"type": typ, "format": fmt}))
                    else:
                        if reference is not None:
                            prop = JsonSchema.ref_for(reference)
                        elif fmt is None:
                            prop = JsonSchema({"type": typ})
                        else:
                            prop = JsonSchema({"type": typ, "format": fmt})

        if slot.description:
            prop['description'] = slot.description

        if slot.pattern:
            # See https://github.com/linkml/linkml/issues/193
            prop['pattern'] = slot.pattern

        if slot.minimum_value is not None:
            prop['minimum'] = slot.minimum_value

        if slot.maximum_value is not None:
            prop['maximum'] = slot.maximum_value

        if slot.equals_string is not None:
            prop['const'] = slot.equals_string

        if slot.equals_number is not None:
            prop['const'] = slot.equals_number

        if slot.minimum_cardinality is not None:
            if prop['type'] == 'array':
                prop['minItems'] = slot.minimum_cardinality
            elif prop['type'] == 'object':
                prop['minProperties'] = slot.minimum_cardinality

        if slot.maximum_cardinality is not None:
            if prop['type'] == 'array':
                prop['maxItems'] = slot.maximum_cardinality
            elif prop['type'] == 'object':
                prop['maxProperties'] = slot.maximum_cardinality

        if slot.any_of is not None and len(slot.any_of) > 0:
            if not slot_has_range_union:
                prop['anyOf'] = [self.get_subschema_for_slot(s, omit_type=True) for s in slot.any_of]

        if slot.all_of is not None and len(slot.all_of) > 0:
            prop['allOf'] = [self.get_subschema_for_slot(s, omit_type=True) for s in slot.all_of]

        if slot.exactly_one_of is not None and len(slot.exactly_one_of) > 0:
            prop['oneOf'] = [self.get_subschema_for_slot(s, omit_type=True) for s in slot.exactly_one_of]

        if slot.none_of is not None and len(slot.none_of) > 0:
            prop['not'] = {
                'anyOf': [self.get_subschema_for_slot(s, omit_type=True) for s in slot.none_of]
            }

        return prop


    def handle_class_slot(self, subschema: JsonSchema, cls: ClassDefinition, slot: SlotDefinition) -> None:
        class_id_slot = self.schemaview.get_identifier_slot(cls.name, use_key=True)
        slot_is_required = slot.required or slot == class_id_slot

        aliased_slot_name = self.aliased_slot_name(slot)
        prop = self.get_subschema_for_slot(slot)
        subschema.add_property(aliased_slot_name, prop, slot_is_required)

        if (
            self.top_class is not None and camelcase(self.top_class) == camelcase(cls.name)
        ) or (self.top_class is None and cls.tree_root):
            self.top_level_schema.add_property(aliased_slot_name, prop, slot_is_required)

    def serialize(self, **kwargs) -> str:
        self.start_schema()
        for enum_definition in self.schemaview.all_enums().values():
            self.handle_enum(enum_definition)

        for class_definition in self.schemaview.all_classes().values():
            self.handle_class(class_definition)

        return self.top_level_schema.to_json(sort_keys=True, indent=self.indent if self.indent > 0 else None)


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
@click.option(
    "--indent",
    default=4,
    show_default=True,
    help="""
If this is a positive number the resulting JSON will be pretty-printed with that indent level. Set to 0 to
disable pretty-printing and return the most compact JSON representation
"""
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate JSON Schema representation of a LinkML model"""
    print(JsonSchemaGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
