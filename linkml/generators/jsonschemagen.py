import os
from typing import Union, TextIO, Optional, Dict, Tuple

import click
from jsonasobj2 import JsonObj, as_json
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition, EnumDefinition, PermissibleValue, PermissibleValueText
from linkml_runtime.utils.formatutils import camelcase, be, underscore

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

class JsonSchemaGenerator(Generator):
    """
    Generates JSONSchema documents from a LinkML SchemaDefinition


    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = ["json"]
    visit_all_class_slots = True

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], top_class: Optional[str] = None, **kwargs) -> None:
        """
        Instantiation

        :param schema:
        :param top_class: root class for JSONSchema generation
        :param kwargs:
        """
        super().__init__(schema, **kwargs)
        self.schemaobj: JsonObj = None
        self.clsobj: JsonObj = None
        self.inline = False
        self.topCls = top_class  ## JSON object is one instance of this
        self.entryProperties = {}
        # JSON-Schema does not have inheritance,
        # so we duplicate slots from inherited parents and mixins
        self.visit_all_slots = True

    def visit_schema(self, inline: bool = False, not_closed=True, **kwargs) -> None:    
        self.inline = inline
        self.schemaobj = JsonObj(title=self.schema.name,
                                 type="object",
                                 properties={},
                                 additionalProperties=not_closed)
        for p, c in self.entryProperties.items():
            self.schemaobj['properties'][p] = {
                'type': "array",
                'items': {'$ref': f"#/$defs/{camelcase(c)}"}}
        self.schemaobj['$schema'] = "http://json-schema.org/draft-07/schema#"
        self.schemaobj['$id'] = self.schema.id
        self.schemaobj['$defs'] = JsonObj()

    def end_schema(self, **_) -> None:
        print(as_json(self.schemaobj, sort_keys=True))

    def visit_class(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract:
            return False
        self.clsobj = JsonObj(title=camelcase(cls.name),
                              type='object',
                              properties=JsonObj(),
                              required=[],
                              additionalProperties=False,
                              description=be(cls.description))
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        self.schemaobj['$defs'][camelcase(cls.name)] = self.clsobj

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
            raise ValueError(f'Invalid permissible value in enum {enum}: {pv}')

        permissible_values_texts = list(map(extract_permissible_text, enum.permissible_values or []))

        self.schemaobj['$defs'][camelcase(enum.name)] = JsonObj(
            title=camelcase(enum.name),
            type='string',
            enum=permissible_values_texts,
            description=be(enum.description))


    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        typ = None          # JSON Schema type (https://json-schema.org/understanding-json-schema/reference/type.html)
        reference = None    # Reference to a JSON schema entity (https://json-schema.org/understanding-json-schema/structuring.html#ref)
        fmt = None          # JSON Schema format (https://json-schema.org/understanding-json-schema/reference/string.html#format)
        if slot.range in self.schema.types:
            (typ, fmt) = json_schema_types.get(self.schema.types[slot.range].base.lower(), ("string", None))
        elif slot.range in self.schema.enums:
            reference = f"#/$defs/{camelcase(slot.range)}"
            typ = 'object'
        elif slot.range in self.schema.classes and slot.inlined:
            reference = f"#/$defs/{camelcase(slot.range)}"
            typ = 'object'
        else:
            typ = "string"

        if slot.inlined:
            # If inline we have to include redefined slots
            ref = JsonObj()
            ref['$ref'] = reference
            if slot.multivalued:
                prop = JsonObj(type="array", items=ref)
            else:
                prop = ref
        else:
            if slot.multivalued:
                if reference is not None:
                    prop = JsonObj(type="array", items={'$ref': reference})
                elif fmt is None:
                    prop = JsonObj(type="array", items={'type': typ})
                else:
                    prop = JsonObj(type="array", items={'type': typ, 'format': fmt})
            else:
                if reference is not None:
                    prop = JsonObj({'$ref': reference})
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
        self.clsobj.properties[underscore(aliased_slot_name)] = prop
        if self.topCls is not None and camelcase(self.topCls) == camelcase(cls.name) or \
                self.topCls is None and cls.tree_root:
            self.schemaobj.properties[underscore(aliased_slot_name)] = prop


@shared_arguments(JsonSchemaGenerator)
@click.command()
@click.option("-i", "--inline", is_flag=True, help="""
Generate references to types rather than inlining them.
Note that declaring a slot as inlined: true will always inline the class
""")
@click.option("-t", "--top-class", help="""
Top level class; slots of this class will become top level properties in the json-schema
""")
@click.option("--not-closed/--closed", default=True, help="""
Set additionalProperties=False if closed otherwise true if not closed at the global level
""")
def cli(yamlfile, **kwargs):
    """ Generate JSON Schema representation of a LinkML model """
    print(JsonSchemaGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == '__main__':
    cli()
