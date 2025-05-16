import json
import logging
import os
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Optional, Union

import click
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousSlotExpression,
    ClassDefinition,
    ClassDefinitionName,
    EnumDefinition,
    PermissibleValue,
    PermissibleValueText,
    PresenceEnum,
    SlotDefinition,
    metamodel_version,
)
from linkml_runtime.utils.formatutils import be, camelcase, underscore

from linkml._version import __version__
from linkml.generators.common import build
from linkml.generators.common.lifecycle import LifecycleMixin
from linkml.generators.common.type_designators import get_type_designator_value
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.helpers import get_range_associated_slots

logger = logging.getLogger(__name__)

# Map from underlying python data type to json equivalent
# Note: The underlying types are a union of any built-in python datatype + any type defined in
#       linkml-runtime/utils/metamodelcore.py
# Note the keys are all lower case
json_schema_types: dict[str, tuple[str, Optional[str]]] = {
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


class JsonSchema(dict):
    OPTIONAL_IDENTIFIER_SUFFIX = "__identifier_optional"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lax_forward_refs = {}

    def add_def(self, name: str, subschema: "JsonSchema") -> None:
        canonical_name = camelcase(name)

        if "$defs" not in self:
            self["$defs"] = {}

        if "title" not in subschema:
            subschema["title"] = canonical_name

        self["$defs"][canonical_name] = subschema

        if canonical_name in self._lax_forward_refs:
            identifier_name = self._lax_forward_refs.pop(canonical_name)
            self.add_lax_def(canonical_name, identifier_name)

    def add_lax_def(self, names: Union[str, list[str]], identifier_name: str) -> None:
        # JSON-Schema does not have inheritance,
        # so we duplicate slots from inherited parents and mixins
        # Maps e.g. Person --> Person__identifier_optional
        # for use when Person is a range of an inlined-as-dict slot
        if isinstance(names, str):
            names = [names]

        for name in names:
            canonical_name = camelcase(name)

            if "$defs" not in self or canonical_name not in self["$defs"]:
                self._lax_forward_refs[canonical_name] = identifier_name
            else:
                lax_cls = deepcopy(self["$defs"][canonical_name])
                lax_cls["required"].remove(identifier_name)
                self["$defs"][canonical_name + self.OPTIONAL_IDENTIFIER_SUFFIX] = lax_cls

    def add_property(
        self, name: str, subschema: "JsonSchema", *, value_required: bool = False, value_disallowed: bool = False
    ) -> None:
        canonical_name = underscore(name)

        if "properties" not in self:
            self["properties"] = {}

        self["properties"][canonical_name] = subschema

        if value_required:
            if "required" not in self:
                self["required"] = []

            self["required"].append(canonical_name)

        # JSON Schema does not have a very natural way to express that a property cannot be present.
        # The apparent best way to do it is to use:
        # {
        #   properties: {
        #     foo: ...
        #   },
        #   not: {
        #     required: ['foo']
        #   }
        # }
        # The {required: [foo]} subschema evaluates to true if the foo property is present with any
        # value. Wrapping that in a `not` keyword inverts that condition.
        if value_disallowed:
            if "not" not in self:
                self["not"] = {}
            if "required" not in self["not"]:
                self["not"]["required"] = []

            self["not"]["required"].append(canonical_name)

    def add_keyword(self, keyword: str, value: Any):
        if value is None:
            return

        self[keyword] = value

    @property
    def is_array(self):
        typ = self.get("type", False)
        if isinstance(typ, str):
            return typ == "array"
        elif isinstance(typ, list):
            return "array" in typ
        else:
            return False

    @property
    def is_object(self):
        return self.get("type") == "object"

    def to_json(self, **kwargs) -> str:
        return json.dumps(self, **kwargs)

    @classmethod
    def ref_for(cls, class_name: Union[str, list[str]], identifier_optional: bool = False, required: bool = True):
        def _ref(class_name):
            def_name = camelcase(class_name)
            def_suffix = cls.OPTIONAL_IDENTIFIER_SUFFIX if identifier_optional else ""
            return JsonSchema({"$ref": f"#/$defs/{def_name}{def_suffix}"})

        if isinstance(class_name, list):
            if len(class_name) == 1:
                ref = _ref(class_name[0])
            else:
                ref = JsonSchema({"anyOf": [_ref(name) for name in class_name]})
        else:
            ref = _ref(class_name)

        if not required:
            if "anyOf" in ref:
                ref["anyOf"].append({"type": "null"})
            else:
                ref = JsonSchema({"anyOf": [ref, {"type": "null"}]})
        return ref

    @classmethod
    def array_of(cls, subschema: "JsonSchema", required: bool = True) -> "JsonSchema":
        if required:
            typ = "array"
        else:
            typ = ["array", "null"]

        schema = {"type": typ, "items": subschema}

        return JsonSchema(schema)


class SchemaResult(build.SchemaResult):
    """Top-level result of building a json schema"""

    schema_: JsonSchema


class EnumResult(build.EnumResult):
    """A single built enum"""

    schema_: JsonSchema


class ClassResult(build.ClassResult):
    """A single built class"""

    schema_: JsonSchema


class SlotResult(build.SlotResult):
    """A slot within the context of a class"""

    schema_: JsonSchema


@dataclass
class JsonSchemaGenerator(Generator, LifecycleMixin):
    """
    Generates JSONSchema documents from a LinkML SchemaDefinition

    - Each linkml class generates a schema
    - inheritance hierarchies are rolled-down from ancestors
    - Composition not yet implemented
    - Enumerations treated as strings
    - Foreign key references are treated as semantics-free strings

    This generator implements the following :class:`.LifecycleMixin` methods:

    * :meth:`.LifecycleMixin.before_generate_schema`
    * :meth:`.LifecycleMixin.after_generate_schema`
    * :meth:`.LifecycleMixin.before_generate_classes`
    * :meth:`.LifecycleMixin.before_generate_enums`
    * :meth:`.LifecycleMixin.before_generate_class_slots`
    * :meth:`.LifecycleMixin.before_generate_class`
    * :meth:`.LifecycleMixin.after_generate_class`
    * :meth:`.LifecycleMixin.before_generate_class_slot`
    * :meth:`.LifecycleMixin.after_generate_class_slot`
    * :meth:`.LifecycleMixin.before_generate_enum`
    * :meth:`.LifecycleMixin.after_generate_enum`

    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.3"
    valid_formats = ["json"]
    uses_schemaloader = False
    file_extension = "schema.json"
    materialize_patterns: bool = False

    # @deprecated("Use top_class")
    topClass: Optional[str] = None

    not_closed: Optional[bool] = True
    """If not closed, then an open-ended set of attributes can be instantiated for any object"""

    indent: int = 4

    inline: bool = False

    top_class: Optional[Union[ClassDefinitionName, str]] = None  # JSON object is one instance of this
    """Class instantiated by the root node of the document tree"""

    include_range_class_descendants: bool = False
    """If set, use an open world assumption and allow the range of a slot to be any descendant of the declared range.
    Note that if the range of a slot has a type designator, descendants will always be included.
    """

    title_from: str = "name"
    """The slot from which to populate JSONSchema title annotation."""

    top_level_schema: JsonSchema = None

    include_null: bool = True
    """Whether to include a "null" type in optional slots"""

    def __post_init__(self):
        if self.topClass:
            logger.warning("topClass is deprecated - use top_class")
            self.top_class = self.topClass

        super().__post_init__()

        if self.top_class:
            if self.schemaview.get_class(self.top_class) is None:
                logger.warning(f"No class in schema named {self.top_class}")

    def start_schema(self, inline: bool = False):
        self.inline = inline

        self.top_level_schema = JsonSchema(
            {
                "$schema": "https://json-schema.org/draft/2019-09/schema",
                "$id": self.schema.id,
                "metamodel_version": metamodel_version,
                "version": self.schema.version if self.schema.version else None,
                "title": self.schema.title if self.title_from == "title" and self.schema.title else self.schema.name,
                "type": "object",
                "additionalProperties": self.not_closed,
            }
        )

    def handle_class(self, cls: ClassDefinition) -> None:
        cls = self.before_generate_class(cls, self.schemaview)

        if cls.mixin or cls.abstract:
            return

        subschema_type = "object"
        additional_properties = False
        if self.is_class_unconstrained(cls):
            subschema_type = ["null", "boolean", "object", "number", "string"]
            additional_properties = True

        class_subschema = JsonSchema(
            {
                "type": subschema_type,
                "additionalProperties": additional_properties,
                "description": be(cls.description),
            }
        )
        if self.title_from == "title" and cls.title:
            class_subschema["title"] = cls.title

        class_slots = self.before_generate_class_slots(
            self.schemaview.class_induced_slots(cls.name), cls, self.schemaview
        )
        for slot_definition in class_slots:
            self.handle_class_slot(subschema=class_subschema, cls=cls, slot=slot_definition)

        rule_subschemas = []
        for ancestor_class_name in self.schemaview.class_ancestors(cls.name):
            ancestor_class = self.schemaview.get_class(ancestor_class_name)
            for rule in ancestor_class.rules:
                subschema = JsonSchema()

                open_world = rule.open_world
                if open_world is None:
                    open_world = False

                if_subschema = self.get_subschema_for_anonymous_class(rule.preconditions, properties_required=True)
                if if_subschema:
                    subschema["if"] = if_subschema

                then_subschema = self.get_subschema_for_anonymous_class(
                    rule.postconditions, properties_required=not open_world
                )
                if then_subschema:
                    subschema["then"] = then_subschema

                # same as required requirements as postconditions?
                else_subschema = self.get_subschema_for_anonymous_class(
                    rule.elseconditions, properties_required=not open_world
                )
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
            class_subschema.update(rule_subschemas[0])
        elif len(rule_subschemas) > 1:
            if "allOf" not in class_subschema:
                class_subschema["allOf"] = []
            class_subschema["allOf"].extend(rule_subschemas)

        class_subschema = self.after_generate_class(
            ClassResult.model_construct(schema_=class_subschema, source=cls), self.schemaview
        ).schema_

        self.top_level_schema.add_def(cls.name, class_subschema)

        if (self.top_class is not None and camelcase(self.top_class) == camelcase(cls.name)) or (
            self.top_class is None and cls.tree_root
        ):
            for key, value in class_subschema.items():
                # check this first to ensure we don't overwrite things like additionalProperties
                # or description on the root. But we do want to copy over properties, required,
                # if, then, etc.
                if key not in self.top_level_schema:
                    self.top_level_schema[key] = value

    def get_subschema_for_anonymous_class(
        self, cls: AnonymousClassExpression, properties_required: bool = False
    ) -> Union[None, JsonSchema]:
        if not cls:
            return None

        subschema = JsonSchema()
        for slot in cls.slot_conditions.values():
            prop = self.get_subschema_for_slot(slot, omit_type=True, include_null=False)
            value_required = False
            value_disallowed = False
            if slot.value_presence:
                if slot.value_presence == PresenceEnum(PresenceEnum.PRESENT):
                    value_required = True
                elif slot.value_presence == PresenceEnum(PresenceEnum.ABSENT):
                    value_disallowed = True
            elif slot.required is not None:
                value_required = slot.required
            else:
                value_required = properties_required
            subschema.add_property(
                self.aliased_slot_name(slot), prop, value_required=value_required, value_disallowed=value_disallowed
            )

        if cls.any_of is not None and len(cls.any_of) > 0:
            subschema["anyOf"] = [self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.any_of]

        if cls.all_of is not None and len(cls.all_of) > 0:
            subschema["allOf"] = [self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.all_of]

        if cls.exactly_one_of is not None and len(cls.exactly_one_of) > 0:
            subschema["oneOf"] = [
                self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.exactly_one_of
            ]

        if cls.none_of is not None and len(cls.none_of) > 0:
            subschema["not"] = {
                "anyOf": [self.get_subschema_for_anonymous_class(c, properties_required) for c in cls.any_of]
            }

        return subschema

    def handle_enum(self, enum: EnumDefinition) -> None:
        # TODO: this only works with explicitly permitted values. It will need to be extended to
        # support other pv_formula
        enum = self.before_generate_enum(enum, self.schemaview)

        def extract_permissible_text(pv):
            if isinstance(pv, str):
                return pv
            if isinstance(pv, PermissibleValue):
                return pv.text.code
            if isinstance(pv, PermissibleValueText):
                return pv
            raise ValueError(f"Invalid permissible value in enum {enum}: {pv}")

        permissible_values_texts = list(map(extract_permissible_text, enum.permissible_values or []))

        enum_schema = JsonSchema(
            {
                "type": "string",
                "description": be(enum.description),
            }
        )
        if self.title_from == "title" and enum.title:
            enum_schema["title"] = enum.title

        if permissible_values_texts:
            enum_schema["enum"] = permissible_values_texts

        enum_schema = self.after_generate_enum(
            EnumResult.model_construct(schema_=enum_schema, source=enum), self.schemaview
        ).schema_
        self.top_level_schema.add_def(enum.name, enum_schema)

    def get_type_info_for_slot_subschema(
        self, slot: Union[SlotDefinition, AnonymousSlotExpression]
    ) -> tuple[str, str, Union[str, list[str]]]:
        # JSON Schema type (https://json-schema.org/understanding-json-schema/reference/type.html)
        typ = None
        # Reference to a JSON schema entity (https://json-schema.org/understanding-json-schema/structuring.html#ref)
        reference = None
        # JSON Schema format (https://json-schema.org/understanding-json-schema/reference/string.html#format)
        fmt = None

        slot_is_inlined = self.schemaview.is_inlined(slot)
        if slot.range in self.schemaview.all_types().keys():
            schema_type = self.schemaview.induced_type(slot.range)
            (typ, fmt) = json_schema_types.get(schema_type.base.lower(), ("string", None))
        elif slot.range in self.schemaview.all_enums().keys():
            reference = slot.range
        elif slot.range in self.schemaview.all_classes().keys():
            if slot_is_inlined:
                descendants = [
                    desc
                    for desc in self.schemaview.class_descendants(slot.range)
                    if not self.schemaview.get_class(desc).abstract
                ]
                # Always include class descendants if the range class has a type designator
                include_range_class_descendants = (
                    self.include_range_class_descendants
                    or self.schemaview.get_type_designator_slot(slot.range) is not None
                )
                if descendants and include_range_class_descendants:
                    reference = descendants
                else:
                    reference = slot.range
            else:
                id_slot = self.schemaview.get_identifier_slot(slot.range)
                return self.get_type_info_for_slot_subschema(id_slot)

        return (typ, fmt, reference)

    def get_value_constraints_for_slot(self, slot: Union[SlotDefinition, AnonymousSlotExpression, None]) -> JsonSchema:
        if slot is None:
            return JsonSchema()

        constraints = JsonSchema()
        if slot.range in self.schemaview.all_types().keys():
            # types take lower priority
            schema_type = self.schemaview.induced_type(slot.range)
            constraints.add_keyword("pattern", schema_type.pattern)
            constraints.add_keyword("minimum", schema_type.minimum_value)
            constraints.add_keyword("maximum", schema_type.maximum_value)
            constraints.add_keyword("const", schema_type.equals_string)
            constraints.add_keyword("const", schema_type.equals_number)
        constraints.add_keyword("pattern", slot.pattern)
        constraints.add_keyword("minimum", slot.minimum_value)
        constraints.add_keyword("maximum", slot.maximum_value)
        constraints.add_keyword("const", slot.equals_string)
        constraints.add_keyword("const", slot.equals_number)
        if slot.equals_string_in:
            constraints.add_keyword("enum", slot.equals_string_in)
        return constraints

    def get_subschema_for_slot(
        self, slot: Union[SlotDefinition, AnonymousSlotExpression], omit_type: bool = False, include_null: bool = True
    ) -> JsonSchema:
        """
        Args:
            include_null: Include ``type: null`` when generating ranges that are not required
        """
        prop = JsonSchema()
        if isinstance(slot, SlotDefinition) and slot.array:
            # TODO: this is currently too lax, in that it will validate ANY array.
            # see https://github.com/linkml/linkml/issues/2188
            prop = JsonSchema(
                {
                    "type": ["null", "boolean", "object", "number", "string", "array"],
                    "additionalProperties": True,
                }
            )
            return JsonSchema.array_of(prop, required=slot.required)
        slot_is_multivalued = "multivalued" in slot and slot.multivalued
        slot_is_inlined = self.schemaview.is_inlined(slot)
        slot_is_boolean = any([slot.any_of, slot.all_of, slot.exactly_one_of, slot.none_of])
        if not omit_type:
            typ, fmt, reference = self.get_type_info_for_slot_subschema(slot)
            if slot_is_inlined:
                # If inline we have to include redefined slots
                if slot_is_multivalued:
                    (
                        range_id_slot,
                        range_simple_dict_value_slot,
                        range_required_slots,
                    ) = get_range_associated_slots(self.schemaview, slot.range)
                    # if the range class has an ID and the slot is not inlined as a list, then we need to consider
                    # various inlined as dict formats
                    if range_id_slot is not None and not slot.inlined_as_list:
                        # At a minimum, the inlined dict can have keys (additionalProps) that are IDs
                        # and the values are the range class but possibly omitting the ID.
                        additionalProps = [JsonSchema.ref_for(reference, identifier_optional=True)]

                        # If the range can be collected as a simple dict, then we can also accept the value
                        # of that simple dict directly.
                        if range_simple_dict_value_slot is not None:
                            additionalProps.append(
                                self.get_subschema_for_slot(range_simple_dict_value_slot, include_null=False)
                            )

                        # If the range has no required slots, then null is acceptable
                        if len(range_required_slots) == 0:
                            additionalProps.append(JsonSchema({"type": "null"}))

                        # If through the above logic we identified multiple acceptable forms, then wrap them
                        # in an "anyOf", otherwise just take the only acceptable form
                        if len(additionalProps) == 1:
                            additionalProps = additionalProps[0]
                        else:
                            additionalProps = JsonSchema({"anyOf": additionalProps})
                        if slot.required or not include_null:
                            typ = "object"
                        else:
                            typ = ["object", "null"]
                        prop = JsonSchema({"type": typ, "additionalProperties": additionalProps})
                        self.top_level_schema.add_lax_def(reference, self.aliased_slot_name(range_id_slot))
                    else:
                        prop = JsonSchema.array_of(JsonSchema.ref_for(reference), required=slot.required)
                else:
                    prop = JsonSchema.ref_for(reference, required=slot.required or not include_null)

            else:
                if reference is not None:
                    prop = JsonSchema.ref_for(reference)
                elif typ and fmt is None:
                    prop = JsonSchema({"type": typ})
                elif typ:
                    prop = JsonSchema({"type": typ, "format": fmt})

                if slot_is_multivalued:
                    prop = JsonSchema.array_of(prop, required=slot.required)
                else:
                    # handle optionals - bools like any_of, etc. below as they call this method recursively
                    if not slot.required and not slot_is_boolean and include_null:
                        if "type" in prop:
                            prop["type"] = [prop["type"], "null"]

        prop.add_keyword("description", slot.description)
        if self.title_from == "title" and slot.title:
            prop.add_keyword("title", slot.title)

        own_constraints = self.get_value_constraints_for_slot(slot)

        if prop.is_array:
            all_element_constraints = self.get_value_constraints_for_slot(slot.all_members)
            any_element_constraints = self.get_value_constraints_for_slot(slot.has_member)
            prop.add_keyword("minItems", slot.minimum_cardinality)
            prop.add_keyword("maxItems", slot.maximum_cardinality)
            prop["items"].update(own_constraints)
            prop["items"].update(all_element_constraints)
            if any_element_constraints:
                prop["contains"] = any_element_constraints
        else:
            prop.update(own_constraints)

        if prop.is_object:
            prop.add_keyword("minProperties", slot.minimum_cardinality)
            prop.add_keyword("maxProperties", slot.maximum_cardinality)

        bool_subschema = JsonSchema()
        if slot.any_of is not None and len(slot.any_of) > 0:
            bool_subschema["anyOf"] = [self.get_subschema_for_slot(s, include_null=False) for s in slot.any_of]
            if not slot.required and not prop.is_array and include_null:
                bool_subschema["anyOf"].append({"type": "null"})

        if slot.all_of is not None and len(slot.all_of) > 0:
            bool_subschema["allOf"] = [self.get_subschema_for_slot(s, include_null=False) for s in slot.all_of]

        if slot.exactly_one_of is not None and len(slot.exactly_one_of) > 0:
            bool_subschema["oneOf"] = [self.get_subschema_for_slot(s, include_null=False) for s in slot.exactly_one_of]

        if slot.none_of is not None and len(slot.none_of) > 0:
            bool_subschema["not"] = {
                "anyOf": [self.get_subschema_for_slot(s, include_null=False) for s in slot.none_of]
            }

        if bool_subschema:
            if prop.is_array:
                if "items" not in prop:
                    prop["items"] = {}
                if slot.required or not include_null:
                    prop["type"] = "array"
                else:
                    prop["type"] = ["array", "null"]
                prop["items"].update(bool_subschema)
            else:
                prop.update(bool_subschema)

        return prop

    def handle_class_slot(self, subschema: JsonSchema, cls: ClassDefinition, slot: SlotDefinition) -> None:
        slot = self.before_generate_class_slot(slot, cls, self.schemaview)
        class_id_slot = self.schemaview.get_identifier_slot(cls.name, use_key=True)
        value_required = (
            slot.required or slot == class_id_slot or slot.value_presence == PresenceEnum(PresenceEnum.PRESENT)
        )
        value_disallowed = slot.value_presence == PresenceEnum(PresenceEnum.ABSENT)

        aliased_slot_name = self.aliased_slot_name(slot)
        prop = self.get_subschema_for_slot(slot, include_null=self.include_null)
        prop = self.after_generate_class_slot(
            SlotResult.model_construct(schema_=prop, source=slot), cls, self.schemaview
        ).schema_
        subschema.add_property(
            aliased_slot_name, prop, value_required=value_required, value_disallowed=value_disallowed
        )

        if slot.designates_type:
            type_value = get_type_designator_value(self.schemaview, slot, cls)
            prop["enum"] = [type_value]

    def generate(self) -> JsonSchema:
        self.schema = self.before_generate_schema(self.schema, self.schemaview)
        self.start_schema()

        all_enums = self.before_generate_enums(self.schemaview.all_enums().values(), self.schemaview)
        for enum_definition in all_enums:
            self.handle_enum(enum_definition)

        all_classes = self.before_generate_classes(self.schemaview.all_classes().values(), self.schemaview)
        for class_definition in all_classes:
            self.handle_class(class_definition)

        self.top_level_schema = self.after_generate_schema(
            SchemaResult.model_construct(schema_=self.top_level_schema, source=self.schema), self.schemaview
        ).schema_
        return self.top_level_schema

    def serialize(self, **kwargs) -> str:
        if self.materialize_patterns:
            logger.info("Materializing patterns in the schema before serialization")
            self.schemaview.materialize_patterns()

        return self.generate().to_json(sort_keys=True, indent=self.indent if self.indent > 0 else None)


@shared_arguments(JsonSchemaGenerator)
@click.command(name="json-schema")
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
""",
)
@click.option(
    "--title-from",
    type=click.Choice(["name", "title"], case_sensitive=False),
    default="name",
    help="""
Specify from which slot are JSON Schema 'title' annotations generated.
""",
)
@click.option(
    "-d",
    "--include",
    help="""
Include LinkML Schema outside of imports mechanism.  Helpful in including deprecated classes and slots in a separate
YAML, and including it when necessary but not by default (e.g. in documentation or for backwards compatibility)
""",
)
@click.option(
    "--materialize-patterns/--no-materialize-patterns",
    default=True,  # Default set to True
    show_default=True,
    help="If set, patterns will be materialized in the generated JSON Schema.",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate JSON Schema representation of a LinkML model"""
    print(JsonSchemaGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
