import logging
from pathlib import Path

import pytest
from graphql import build_schema, parse, validate_schema

from linkml.generators.graphqlgen import GraphqlGenerator

logger = logging.getLogger(__name__)

PERSON = """
type Person implements HasAliases
  {
    id: String!
    name: String
    hasEmploymentHistory: [EmploymentEvent]
    hasFamilialRelationships: [FamilialRelationship]
    hasMedicalHistory: [MedicalEvent]
    ageInYears: Int
    addresses: [Address]
    hasBirthEvent: BirthEvent
    speciesName: String
    stomachCount: Int
    isLiving: LifeStatusEnum
    aliases: [String]
  }
"""

MEDICALEVENT = """
type MedicalEvent
  {
    startedAtTime: String
    endedAtTime: String
    isCurrent: Boolean
    metadata: AnyObject
    inLocation: Place
    diagnosis: DiagnosisConcept
    procedure: ProcedureConcept
  }
"""

FAMILIALRELATIONSHIP = """
type FamilialRelationship
  {
    startedAtTime: String
    endedAtTime: String
    cordialness: CordialnessEnum
    type: FamilialRelationshipType!
    relatedTo: Person!
  }
"""

DATASET = """
type Dataset
  {
    metadata: AnyObject
    persons: [Person]
    companies: [Company]
    activities: [Activity]
    codeSystems: [CodeSystem]
  }
"""

FAMILIALRELATIONSHIPTYPE = """
enum FamilialRelationshipType
  {
    SIBLING_OF
    PARENT_OF
    CHILD_OF
  }
"""


@pytest.mark.parametrize(
    "input_class,expected",
    [
        # check that expected GraphQL schema blocks are present
        ("Person", PERSON),
        ("Dataset", DATASET),
        ("MedicalEvent", MEDICALEVENT),
        ("FamilialRelationship", FAMILIALRELATIONSHIP),
        ("FamilialRelationshipType", FAMILIALRELATIONSHIPTYPE),
    ],
)
def test_serialize_selected(input_class, expected, kitchen_sink_path):
    """Test serialization of select GraphQL schema from schema."""
    generator = GraphqlGenerator(kitchen_sink_path)
    graphql = generator.serialize(classes=[input_class])

    # check that the expected blocks are present
    assert expected in graphql


def test_snapshot(kitchen_sink_path, snapshot):
    generator = GraphqlGenerator(kitchen_sink_path)
    generated = generator.serialize()
    assert generated == snapshot("kitchen_sink.graphql")


def test_graphql_validity(kitchen_sink_path):
    generator = GraphqlGenerator(kitchen_sink_path)
    generated = generator.serialize()
    logger.info("\nGenerated GraphQL schema:")
    logger.info("vvvvvv Start GraphQL vvvvvv")
    logger.info(generated)
    logger.info("^^^^^^^ End GraphQL ^^^^^^^")
    try:
        parse(generated)
    except Exception as ex:
        pytest.fail(
            "Generated GraphQL appears to be wrong, it cannot be parsed!\n"
            + "vvvvvv Start Error Message vvvvvv\n"
            + f"{str(ex)}\n"
            + "^^^^^^^ End Error Message ^^^^^^^"
        )


EMPTY_CLASS_SCHEMA = """
id: https://example.org/empty
name: empty
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/empty/
default_prefix: ex
default_range: string
imports: [linkml:types]
classes:
  Marker:
    description: A class that carries no slot.
  AbstractMarker:
    abstract: true
    description: An abstract class that carries no slot.
  Holder:
    attributes:
      marker: {range: Marker}
"""

CUSTOM_TYPE_SCHEMA = """
id: https://example.org/types
name: types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/types/
default_prefix: ex
default_range: string
imports: [linkml:types]
types:
  city code:
    typeof: string
  unused code:
    typeof: string
  int:
    typeof: string
classes:
  Place:
    attributes:
      code: {range: city code}
      ranking: {range: int}
"""

MIXIN_SCHEMA = """
id: https://example.org/mixin
name: mixin
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mixin/
default_prefix: ex
default_range: string
imports: [linkml:types]
classes:
  BareMixin:
    mixin: true
    description: A mixin that carries no slot.
  RichMixin:
    mixin: true
    attributes:
      tag: {}
  Consumer:
    mixins: [BareMixin, RichMixin]
    attributes:
      name: {}
"""

NESTED_MIXIN_SCHEMA = """
id: https://example.org/nested
name: nested
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/nested/
default_prefix: ex
default_range: string
imports: [linkml:types]
classes:
  Base:
    mixin: true
    attributes:
      a: {}
  Nested:
    mixin: true
    mixins: [Base]
    attributes:
      b: {}
  Consumer:
    mixins: [Nested]
    attributes:
      c: {}
"""

ANY_SCHEMA = """
id: https://example.org/any
name: any
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/any/
default_prefix: ex
default_range: string
imports: [linkml:types]
classes:
  any object:
    class_uri: linkml:Any
  Holder:
    attributes:
      payload: {range: any object}
"""

# The class of the name that ANY_SCHEMA declares to be "linkml:Any" is an ordinary one here.
PLAIN_SAME_NAME_SCHEMA = """
id: https://example.org/plain
name: plain
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/plain/
default_prefix: ex
default_range: string
imports: [linkml:types]
classes:
  any object:
    attributes:
      label: {}
"""

# LinkML holds its types, classes and enumerations apart, so one name may stand in several
# of them; GraphQL carries every type in one namespace.
COLLIDING_NAME_SCHEMA = """
id: https://example.org/collide
name: collide
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/collide/
default_prefix: ex
default_range: string
imports: [linkml:types]
types:
  person:
    typeof: string
  colour:
    typeof: string
enums:
  Colour:
    permissible_values:
      red:
classes:
  Person:
    attributes:
      name: {}
  Holder:
    attributes:
      who: {range: Person}
      reference: {range: person}
      shade: {range: colour}
"""

DYNAMIC_ENUM_SCHEMA = """
id: https://example.org/dynamic
name: dynamic
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/dynamic/
default_prefix: ex
default_range: string
imports: [linkml:types]
enums:
  VehicleKind:
    reachable_from:
      source_ontology: obo:vehicle
      source_nodes: [VEHICLE:1]
classes:
  Car:
    attributes:
      kind: {range: VehicleKind}
"""


def generate(tmp_path: Path, schema_text: str, name: str = "schema.yaml") -> str:
    """Write a schema and return the GraphQL document generated from it."""
    schema = tmp_path / name
    schema.write_text(schema_text, encoding="utf-8")
    return GraphqlGenerator(str(schema)).serialize()


def schema_errors(generated: str) -> list[str]:
    """Return what the GraphQL type system rejects in a document, bar the missing query root.

    ``build_schema`` raises when the document does not parse. The generator names no root
    operation type, which a schema has to provide (GraphQL spec, October 2021, section
    3.3.1); that gap is left aside here so the remaining rules can be checked.
    """
    errors = validate_schema(build_schema(generated))
    return [str(error) for error in errors if "Query root type must be provided" not in str(error)]


@pytest.mark.parametrize(
    "schema_text",
    [
        pytest.param(EMPTY_CLASS_SCHEMA, id="class-without-a-slot"),
        pytest.param(CUSTOM_TYPE_SCHEMA, id="type-of-the-schema-itself"),
        pytest.param(MIXIN_SCHEMA, id="two-mixins"),
        pytest.param(NESTED_MIXIN_SCHEMA, id="mixin-of-a-mixin"),
        pytest.param(ANY_SCHEMA, id="any-class"),
        pytest.param(COLLIDING_NAME_SCHEMA, id="type-sharing-a-name"),
        pytest.param(DYNAMIC_ENUM_SCHEMA, id="enum-without-permissible-values"),
    ],
)
def test_the_generated_document_is_a_valid_schema(tmp_path, schema_text):
    """Every generated document parses and satisfies the GraphQL type system."""
    assert schema_errors(generate(tmp_path, schema_text)) == []


def test_a_class_without_a_slot_still_defines_a_field(tmp_path):
    """An object type and an interface each define at least one field.

    GraphQL spec, October 2021, sections 3.6 and 3.7. A LinkML class may carry no slot,
    and an empty body does not parse.
    """
    generated = generate(tmp_path, EMPTY_CLASS_SCHEMA)
    assert "type Marker\n  {\n    _placeholder: Boolean\n  }" in generated
    assert "interface AbstractMarker\n  {\n    _placeholder: Boolean\n  }" in generated
    # A class with a slot of its own is left alone.
    assert "_placeholder" not in generated.split("type Holder")[1].split("}")[0]


def test_an_implementation_repeats_the_field_of_a_fieldless_interface(tmp_path):
    """An object type defines every field of the interfaces it implements.

    GraphQL spec, October 2021, section 3.6. The placeholder an interface needs is
    therefore part of the implementing type as well.
    """
    generated = generate(tmp_path, MIXIN_SCHEMA)
    assert "interface BareMixin\n  {\n    _placeholder: Boolean\n  }" in generated
    consumer = generated.split("type Consumer")[1].split("}")[0]
    assert "_placeholder: Boolean" in consumer


def test_interfaces_are_separated_by_an_ampersand(tmp_path):
    """``implements`` separates interfaces with "&"; a comma does not parse.

    GraphQL spec, October 2021, section 3.6, ImplementsInterfaces.
    """
    generated = generate(tmp_path, MIXIN_SCHEMA)
    assert "type Consumer implements BareMixin & RichMixin" in generated


def test_a_mixin_of_a_mixin_is_an_interface_and_is_implemented_along(tmp_path):
    """A mixin stays an interface when it is mixed into another, and is declared by its users.

    An interface may implement an interface, and a type declares the interfaces that the
    interfaces it implements declare in turn (GraphQL spec, October 2021, sections 3.6
    and 3.7).
    """
    generated = generate(tmp_path, NESTED_MIXIN_SCHEMA)
    assert "interface Nested implements Base" in generated
    assert "type Consumer implements Nested & Base" in generated


def test_a_type_of_the_schema_itself_is_declared_as_a_custom_scalar(tmp_path):
    """A document defines every type it names, and a custom scalar carries one GraphQL lacks.

    GraphQL spec, October 2021, section 3.5, Custom Scalars.
    """
    generated = generate(tmp_path, CUSTOM_TYPE_SCHEMA)
    assert "code: CityCode" in generated
    assert "scalar CityCode" in generated


def test_a_type_no_slot_names_is_not_declared(tmp_path):
    """Only the types a field names are declared, so an unused one stays out of the document."""
    generated = generate(tmp_path, CUSTOM_TYPE_SCHEMA)
    assert "scalar CityCode" in generated
    assert "scalar UnusedCode" not in generated


def test_a_type_named_after_a_built_in_scalar_is_not_redeclared(tmp_path):
    """A built-in scalar is defined by every service, so the document does not repeat it.

    GraphQL spec, October 2021, section 3.5. The type ``int`` of the schema collapses onto
    the built-in ``Int`` rather than being declared, which is the behaviour of record; the
    type it is declared with is lost in the process.
    """
    generated = generate(tmp_path, CUSTOM_TYPE_SCHEMA)
    assert "ranking: Int" in generated
    assert "scalar Int" not in generated


def test_a_type_sharing_a_name_with_a_class_or_an_enum_is_not_declared_twice(tmp_path, caplog):
    """Every type of a schema shares one namespace, in which a name is unique.

    GraphQL spec, October 2021, section 3.3. A LinkML type whose name lands on that of a
    class or of an enumeration is therefore left undeclared rather than repeated, which
    would make the document unloadable.
    """
    with caplog.at_level(logging.WARNING):
        generated = generate(tmp_path, COLLIDING_NAME_SCHEMA)
    assert "type Person" in generated
    assert "scalar Person" not in generated
    assert "enum Colour" in generated
    assert "scalar Colour" not in generated
    assert "Person" in caplog.text
    assert "Colour" in caplog.text


def test_an_enum_without_permissible_values_is_declared_as_a_scalar(tmp_path):
    """An enum type defines one or more values, so an enumeration short of them is a scalar.

    GraphQL spec, October 2021, section 3.9. The values of an enumeration reached from an
    ontology are not known at generation time; leaving it out altogether left the fields
    naming it pointing at a type the document never declared.
    """
    generated = generate(tmp_path, DYNAMIC_ENUM_SCHEMA)
    assert "kind: VehicleKind" in generated
    assert "scalar VehicleKind" in generated
    assert "enum VehicleKind" not in generated


def test_an_any_class_is_declared_under_the_name_its_fields_use(tmp_path):
    """A class standing for ``linkml:Any`` is a scalar named as the fields naming it are."""
    generated = generate(tmp_path, ANY_SCHEMA)
    assert "scalar AnyObject" in generated
    assert "payload: AnyObject" in generated


def test_one_generator_does_not_see_the_any_class_of_another(tmp_path):
    """The names a run collects stay with it.

    Held on the class, the name of a ``linkml:Any`` class outlived its generator, and the
    class of that name in the next schema was closed as if it were a scalar.
    """
    generate(tmp_path, ANY_SCHEMA, name="any.yaml")
    generated = generate(tmp_path, PLAIN_SAME_NAME_SCHEMA, name="plain.yaml")
    parse(generated)
    assert "type AnyObject\n  {\n    label: String\n  }" in generated
