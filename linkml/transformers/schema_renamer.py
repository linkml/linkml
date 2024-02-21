from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Type

import click
from jsonasobj2 import as_dict
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import (
    ClassDefinition,
    ClassDefinitionName,
    ElementName,
    EnumDefinition,
    EnumDefinitionName,
    SchemaDefinition,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
    TypeDefinitionName,
)
from linkml_runtime.utils.formatutils import camelcase, lcamelcase, underscore
from linkml_runtime.utils.schema_as_dict import schema_as_yaml_dump
from linkml_runtime.utils.yamlutils import YAMLRoot

ref_map = {
    ClassDefinitionName: ClassDefinition,
    SlotDefinitionName: SlotDefinition,
    EnumDefinitionName: EnumDefinition,
    TypeDefinitionName: TypeDefinition,
}


@dataclass
class SchemaRenamer:
    """
    Renames schema elements
    """

    rename_function_map: Dict[Type, Callable] = field(default_factory=lambda: {})
    schema: SchemaDefinition = None

    def rename_elements(self, schema: SchemaDefinition) -> SchemaDefinition:
        """
        Rename all elements in the schema using rename_function_map

        :param schema:
        :return:
        """
        schema = SchemaDefinition(**as_dict(schema))
        self.schema = schema
        return self._rename(schema)

    def _rename(self, element: Any, parent_key: ElementName = None) -> Any:
        """
        Renames an individual element plus its children

        Does not modify in place: creates a new element
        :param element:
        :return:
        """
        typ = type(element)
        if element is None:
            return None
        elif isinstance(element, ElementName):
            # element is a *Reference* to a Class, Slot, or other schema element
            if typ == ElementName:
                # cast generic element names, e.g. for ranges
                if element in self.schema.classes:
                    typ = ClassDefinitionName
                elif element in self.schema.enums:
                    typ = EnumDefinitionName
                elif element in self.schema.types:
                    typ = TypeDefinitionName
            typ_deref = ref_map.get(typ, None)
            if typ_deref in self.rename_function_map:
                return typ(self.rename_function_map[typ_deref](element))
            else:
                return element
        elif isinstance(element, dict):
            # element is a dict; keys may be rewired
            new_element = {}
            for k, v in element.items():
                v2 = self._rename(v, k)
                typ = type(v2)
                new_k = k
                if typ in self.rename_function_map:
                    new_k = v2.name
                new_element[new_k] = v2
            return new_element
        elif isinstance(element, list):
            return [self._rename(e) for e in element]
        elif isinstance(element, YAMLRoot):
            # element is a Class, Slot, or other schema element
            new_element = deepcopy(element)
            if typ in self.rename_function_map:
                new_element.name = self.rename_function_map[typ](element.name)
            for k, v in vars(new_element).items():
                setattr(new_element, k, self._rename(v))
            return new_element
        else:
            try:
                element_vars = {k: v for k, v in vars(element).items() if not k.startswith("_")}
                if len(element_vars) == 0:
                    return element
                else:
                    new_element = deepcopy(element)
                    for k, v in vars(new_element).items():
                        setattr(new_element, k, self._rename(v))
                    return new_element
            except TypeError:
                return element


@click.command()
@click.option("-o", "--output", help="path to output schema")
@click.option("-C", "--class-names", help="function for class names")
@click.option("-S", "--slot-names", help="function for slot names")
@click.argument("schema")
def main(schema, output, class_names, slot_names):
    sv = SchemaView(schema)

    def n2f(n: str) -> Callable:
        if n.startswith("camel"):
            return camelcase
        elif n.startswith("lcamel") or n.startswith("lowerpascal"):
            return lcamelcase
        elif n.startswith("snake") or n.startswith("under"):
            return underscore
        elif n.startswith("upper"):
            return lambda x: x.upper()
        elif n.startswith("lower"):
            return lambda x: x.lower()
        else:
            raise NotImplementedError(f"Function: {n}")

    rename_map = {}
    if class_names:
        rename_map[ClassDefinition] = n2f(class_names)
    if slot_names:
        rename_map[SlotDefinition] = n2f(slot_names)
    if not rename_map.keys():
        raise ValueError("No transformations specified")
    renamer = SchemaRenamer(rename_function_map=rename_map)
    rschema = renamer.rename_elements(sv.schema)
    ystr = schema_as_yaml_dump(rschema)
    if output:
        with open(output, "w", encoding="UTF-8") as stream:
            stream.write(ystr)
    else:
        print(ystr)


if __name__ == "__main__":
    main()
