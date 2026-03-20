"""Generate OpenAPI 3"""

import json
import os
from dataclasses import dataclass

import click
import yaml

from linkml._version import __version__
from linkml.generators.common.lifecycle import LifecycleMixin
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.generator import Generator, shared_arguments


@dataclass
class OpenApiGenerator(Generator, LifecycleMixin):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["openapi3"]
    file_extension = "yaml"
    uses_schemaloader = False

    def _find_referenced_classes(self) -> set[str]:
        """Return a list with all the classes referenced by the endpoints"""
        result = set()
        for endp_spec in self._template["paths"].values():
            for req_spec in endp_spec.values():
                if "requestBody" in req_spec and "content" in req_spec["requestBody"]:
                    for content_spec in req_spec["requestBody"]["content"].values():
                        if "$ref" in content_spec["schema"]:
                            class_name = content_spec["schema"]["$ref"].removeprefix("#/components/schemas/")
                            result.add(class_name)
                if "responses" in req_spec:
                    for response in req_spec["responses"].values():
                        if "content" in response:
                            for content_spec in response["content"].values():
                                if "$ref" in content_spec["schema"]:
                                    class_name = content_spec["schema"]["$ref"].removeprefix("#/components/schemas/")
                                    result.add(class_name)
        return result

    def _fix_openapi_spec(self, element, keys_to_remove):
        """
        When using the JSON schemas of the classes in the OpenAPI specification document,
        following things need to be fixed:
        - some keys need to be removed
        - references need to be changed from "$defs" to "components/schemas"
        """
        new_element = None
        if isinstance(element, dict):
            new_element = {}
            for key, value in element.items():
                if key not in keys_to_remove:
                    if key == "const":
                        new_element["enum"] = [value]
                    elif key == "type" and isinstance(value, list):
                        new_element["anyOf"] = [{"type": item} for item in value if item != "null"]
                    else:
                        if isinstance(value, dict) or isinstance(value, list):
                            value = self._fix_openapi_spec(value, keys_to_remove)
                        elif isinstance(value, str) and value.startswith("#/$defs/"):
                            value = value.replace("$defs", "components/schemas")
                        new_element[key] = value
        elif isinstance(element, list):
            new_element = []
            for item in element:
                if isinstance(item, dict) or isinstance(item, list):
                    item = self._fix_openapi_spec(item, keys_to_remove)
                elif isinstance(item, str) and item.startswith("#/$defs/"):
                    item = item.replace("#/$defs/", "#/components/schemas/")
                new_element.append(item)
        return new_element

    def _find_references(self, element, referenced_classes):
        if isinstance(element, dict):
            if "$ref" in element:
                referenced_classes.add(element["$ref"].replace("#/$defs/", ""))
            for value in element.values():
                self._find_references(value, referenced_classes)
        elif isinstance(element, list):
            for item in element:
                self._find_references(item, referenced_classes)

    def _sanitize_schemas(self, class_schemas, endpoint_referenced_classes):
        referenced_classes = endpoint_referenced_classes.copy()
        for class_schema in class_schemas.values():
            self._find_references(class_schema, referenced_classes)
        while set(class_schemas.keys()).difference(referenced_classes):
            class_schema_names = list(class_schemas.keys())
            for class_name in class_schema_names:
                if class_name not in referenced_classes:
                    del class_schemas[class_name]
            referenced_classes = endpoint_referenced_classes.copy()
            for class_schema in class_schemas.values():
                self._find_references(class_schema, referenced_classes)
        return class_schemas

    def serialize(self, template_file: str = "", **kwargs) -> str:
        self._template = yaml.safe_load(open(template_file))
        referenced_classes = self._find_referenced_classes()
        self._template["components"]["schemas"] = {}
        class_schemas = {}
        for class_name in referenced_classes:
            json_schema = JsonSchemaGenerator(self.schema, include_null=False, top_class=class_name).generate()
            json_schema_classes = json.loads(json_schema.to_json())["$defs"]
            class_schemas = class_schemas | json_schema_classes
        class_schemas = self._sanitize_schemas(class_schemas, referenced_classes)
        class_schemas = self._fix_openapi_spec(
            class_schemas,
            ["description", "title"],
        )
        self._template["components"]["schemas"] = class_schemas
        return yaml.dump(self._template, sort_keys=False)


@shared_arguments(OpenApiGenerator)
@click.command(name="openapi")
@click.option(
    "--template",
    "-t",
    help="OpenAPI template - includes the header, the endpoints and the securityschemes",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, template, **args):
    """Generate an OpenAPI 3 spec with resources modelled with LinkML"""
    print(OpenApiGenerator(yamlfile, **args).serialize(template_file=template, **args), end="")


if __name__ == "__main__":
    cli()
