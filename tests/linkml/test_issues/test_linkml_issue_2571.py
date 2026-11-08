"""String defaults must survive parsing and code generation without truncation."""

import pytest
from rdflib import SH, XSD, Graph, Literal

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime.linkml_model import SchemaDefinition


@pytest.fixture(
    params=[
        ('string("J/(kg K)")', "J/(kg K)"),
        ("string(J/(kg K))", "J/(kg K)"),
        ("string('ln(...)')", "ln(...)"),
        ('string("hello(you)")', "hello(you)"),
        ('string("outer(inner(x)) + y")', "outer(inner(x)) + y"),
        ('string("a)b(c")', "a)b(c"),
        ('string("it\'s (fine)")', "it's (fine)"),
        ("string('a \"quoted\" (unit)')", 'a "quoted" (unit)'),
        ('"hello(you)"', "hello(you)"),
        ("J/(kg K)", "J/(kg K)"),
        ('string("  x(y)  ")', "  x(y)  "),
        ('string("first (line)\nsecond line")', "first (line)\nsecond line"),
        (r'string("C:\new\(units)")', r"C:\new\(units)"),
        ("string(plain)", "plain"),
    ]
)
def string_default(request: pytest.FixtureRequest) -> tuple[SchemaDefinition, str]:
    """Build a schema using both constructor syntax and existing bare defaults."""
    expression, expected = request.param
    schema = SchemaDefinition(
        id="https://example.org/defaults",
        name="defaults",
        prefixes={"ex": "https://example.org/defaults/", "linkml": "https://w3id.org/linkml/"},
        imports=["linkml:types"],
        default_prefix="ex",
        default_range="string",
        classes={"Measurement": {"attributes": {"units": {"ifabsent": expression}}}},
    )
    return schema, expected


@pytest.mark.parametrize("generator", [PythonGenerator, PydanticGenerator])
def test_generated_string_default(
    string_default: tuple[SchemaDefinition, str], generator: type[PythonGenerator] | type[PydanticGenerator]
) -> None:
    """Execute the generated models and check default and explicit values."""
    schema, expected = string_default
    module = generator(schema).compile_module()
    assert module.Measurement().units == expected
    assert module.Measurement(units="provided").units == "provided"


def test_shacl_string_default(string_default: tuple[SchemaDefinition, str]) -> None:
    """Round-trip the generated RDF so quoting is checked by the Turtle parser."""
    schema, expected = string_default
    graph = Graph().parse(data=ShaclGenerator(schema).serialize(), format="turtle")
    defaults = list(graph.objects(None, SH.defaultValue))
    assert len(defaults) == 1
    assert defaults[0].eq(Literal(expected, datatype=XSD.string))
