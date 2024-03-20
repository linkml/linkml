"""
Generators translate between a SchemaDefinition and an alternative
representation such as JsonSchema
"""

from linkml.generators.javagen import JavaGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator
from linkml.generators.sqltablegen import SQLTableGenerator

__all__ = [
    "csvgen",
    "dotgen",
    "docgen",
    "golrgen",
    "graphqlgen",
    "javagen",
    "jsonldcontextgen",
    "jsonldgen",
    "jsonschemagen",
    "markdowngen",
    "namespacegen",
    "owlgen",
    "plantumlgen",
    "protogen",
    "pythongen",
    "pydanticgen",
    "rdfgen",
    "shexgen",
    "shaclgen",
    "sssomgen",
    "summarygen",
    "yamlgen",
    "yumlgen",
    "OwlSchemaGenerator",
    "PydanticGenerator",
    "PythonGenerator",
    "JavaGenerator",
    "ContextGenerator",
    "JSONLDGenerator",
    "JsonSchemaGenerator",
    "ShaclGenerator",
    "ShExGenerator",
    "SQLAlchemyGenerator",
    "SQLTableGenerator",
]

# TODO: deprecate usage of these
# GENERATOR_BASE = "0.9"

# PYTHON_GEN_VERSION = GENERATOR_BASE + ".0"
