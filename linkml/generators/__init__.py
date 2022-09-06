"""
Generators translate between a SchemaDefinition and an alternative
representation such as JsonSchema
"""
# Generator version numbers
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
    "protogen",
    "pythongen",
    "rdfgen",
    "shexgen",
    "sssomgen",
    "summarygen",
    "yamlgen",
    "yumlgen",
    "PYTHON_GEN_VERSION",
]
GENERATOR_BASE = "0.9"

PYTHON_GEN_VERSION = GENERATOR_BASE + ".0"
JAVA_GEN_VERSION = GENERATOR_BASE + ".0"
