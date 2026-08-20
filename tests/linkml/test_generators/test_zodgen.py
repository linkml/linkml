from unittest.mock import patch

from click.testing import CliRunner

from linkml.generators.zodgen import ZodGenerator, cli
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.linkml_model.meta import AnonymousSlotExpression
from linkml_runtime.utils.schema_builder import SchemaBuilder


def test_zodgen(kitchen_sink_path):
    """Test that Zod schemas are generated from a kitchen sink schema."""
    # Generate the Zod schema as a string
    zod_schema = ZodGenerator(kitchen_sink_path)
    zod_schema_str = zod_schema.serialize()

    def assert_in(expected: str) -> None:
        # Remove spaces to do a flexible comparison
        assert expected.replace(" ", "") in zod_schema_str.replace(" ", "")

    # Check that the zod import is present
    assert 'import { z } from "zod";' in zod_schema_str
    # Check that an example schema for Organization is present
    assert "export const OrganizationSchema" in zod_schema_str
    # Check that a Person schema is generated
    assert_in("export const PersonSchema")
    # Class-valued slots are rendered as lazy getters to support recursive references
    assert_in("get has_familial_relationships() { return z.array(")
    # Check that a reference to a CodeSystem is generated correctly
    assert_in("get code_systems() { return z.array(")


def test_required_slots_zod():
    """Test that required and optional slots are generated correctly in Zod schemas."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    # Create a required slot and an optional slot
    id_slot = SlotDefinition(name="id", multivalued=False, range="string", required=True)
    description_slot = SlotDefinition(name="description", multivalued=False, range="string")
    sb.add_class("Person", slots=[id_slot, description_slot])
    schema = sb.schema

    # Generate Zod schema with type utilities (if relevant) and including induced slots
    zod_schema_str = ZodGenerator(schema, include_induced_slots=True).serialize()

    # The required field "id" should be mapped to a plain z.string()
    assert "id: z.string()" in zod_schema_str
    # The optional field "description" should be marked with .optional()
    assert "description: z.string().optional()" in zod_schema_str


def test_multivalued_string_zod():
    """Test that multivalued string slots are generated as z.array(z.string()) in Zod schemas."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    # Create two multivalued slots: one optional and one required
    aliases = SlotDefinition(name="aliases", multivalued=True, range="string")
    descriptions = SlotDefinition(name="descriptions", multivalued=True, range="string", required=True)
    sb.add_class("Person", slots=[aliases, descriptions])
    schema = sb.schema

    zod_schema_str = ZodGenerator(schema, include_induced_slots=True).serialize()

    # Optional multivalued field "aliases" should be wrapped in z.array(...) and be optional
    assert "aliases: z.array(z.string()).optional()" in zod_schema_str
    # Required multivalued field "descriptions" should be wrapped in z.array(z.string()) without .optional()
    assert "descriptions: z.array(z.string())" in zod_schema_str


def test_output_option_zod(kitchen_sink_path, tmp_path):
    """Test that Zod generator writes output to a file when the --output option is used."""
    zod_generator = ZodGenerator(kitchen_sink_path)
    output_file = tmp_path / "kitchen_sink_zod.ts"
    zod_generator.serialize(output=output_file)
    assert output_file.exists()


def test_cli_print_stdout_without_output_zod(kitchen_sink_path):
    """Test that the CLI prints to stdout when no output file is provided."""
    runner = CliRunner()
    with patch("builtins.print") as mock_print:
        result = runner.invoke(cli, [kitchen_sink_path])
        assert result.exit_code == 0
        mock_print.assert_called_once()


def test_cli_no_print_with_output_zod(kitchen_sink_path, tmp_path):
    """Test that the CLI does not print to stdout when an output file is specified."""
    runner = CliRunner()
    with patch("builtins.print") as mock_print:
        output_path = tmp_path / "kitchen_sink_zod.ts"
        result = runner.invoke(cli, [kitchen_sink_path, "--output", str(output_path)])
        assert result.exit_code == 0
        mock_print.assert_not_called()


def test_enums():
    enum_schema = """
id: unit_test
name: unit_test

prefixes:
  ex: https://example.org/
default_prefix: ex

enums:
  TestEnum:
    permissible_values:
      123:
      +:
      This & that, plus maybe a 🎩:
      Ohio:
classes:
  Dummy:
    attributes:
      test_value:
        range: TestEnum
"""

    gen = ZodGenerator(schema=enum_schema)
    output = gen.serialize()

    # Check if z.enum is generated correctly with sanitized keys
    assert "z.enum([" in output
    assert '"123"' in output
    assert '"+"' in output
    assert '"This & that, plus maybe a 🎩"' in output
    assert '"Ohio"' in output

    # Ensure the DummySchema uses the enum
    assert "test_value" in output
    assert "TestEnum" in output or "TestEnumSchema" in output


def test_inherited_slots_are_included():
    """Child classes must include slots induced through is_a inheritance and mixins."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("NamedThing", slots=[SlotDefinition(name="id", range="string", required=True)])
    sb.add_class("Aliased", slots=[SlotDefinition(name="alias", range="string")])
    sb.add_class(
        "Person",
        slots=[SlotDefinition(name="age", range="integer")],
        is_a="NamedThing",
        mixins=["Aliased"],
    )
    output = ZodGenerator(sb.schema).serialize()

    # The Person schema should contain its own slot plus inherited/mixed-in slots.
    person_block = output.split("export const PersonSchema")[1].split("export type Person")[0]
    assert "id:" in person_block
    assert "age:" in person_block
    assert "alias:" in person_block


def test_enum_range_reference():
    """A slot whose range is an enum must reference the generated enum schema, not z.string()."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
enums:
  StatusEnum:
    permissible_values:
      ACTIVE:
      INACTIVE:
classes:
  Record:
    attributes:
      status:
        range: StatusEnum
"""
    output = ZodGenerator(schema=schema).serialize()
    # No double "Enum" suffix, and the slot references the enum const rather than z.string().
    assert "export const StatusEnum = z.enum(" in output
    assert "status: StatusEnum" in output


def test_scalar_type_mapping():
    """Integer, float, boolean and datetime ranges map to precise Zod expressions."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Measurement",
        slots=[
            SlotDefinition(name="count", range="integer", required=True),
            SlotDefinition(name="ratio", range="float", required=True),
            SlotDefinition(name="ok", range="boolean", required=True),
            SlotDefinition(name="when", range="datetime", required=True),
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "count: z.number().int()" in output
    assert "ratio: z.number()" in output
    assert "ok: z.boolean()" in output
    assert "when: dateFromString" in output


def test_pattern_and_numeric_constraints():
    """pattern, minimum_value and maximum_value are rendered as Zod refinements."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Constrained",
        slots=[
            SlotDefinition(name="code", range="string", required=True, pattern="^[A-Z]+$"),
            SlotDefinition(name="score", range="integer", required=True, minimum_value=0, maximum_value=100),
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "code: z.string().regex(/^[A-Z]+$/)" in output
    assert "score: z.number().int().gte(0).lte(100)" in output


def test_array_cardinality_constraints():
    """minimum_cardinality and maximum_cardinality bound the generated z.array."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Bag",
        slots=[
            SlotDefinition(
                name="items",
                range="string",
                multivalued=True,
                required=True,
                minimum_cardinality=1,
                maximum_cardinality=5,
            )
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "items: z.array(z.string()).min(1).max(5)" in output


def test_non_identifier_slot_key_is_quoted():
    """Slot names that are not valid JS identifiers must be emitted as quoted object keys."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Weird", slots=[SlotDefinition(name="1st place", range="string")])
    output = ZodGenerator(sb.schema).serialize()
    # underscore() leaves a leading digit, which is not a valid identifier -> must be quoted.
    assert '"1st_place":' in output


def test_non_inlined_class_range_is_identifier_reference(kitchen_sink_path):
    """A non-inlined class-ranged slot is a reference (identifier string), not an embedded object."""
    output = ZodGenerator(kitchen_sink_path).serialize()
    # Company.ceo references a Person (which has an identifier) and is not inlined.
    assert "ceo: z.string()" in output
    # It must NOT be rendered as an embedded PersonSchema getter.
    assert "get ceo()" not in output


def test_inlined_as_list_is_array_of_schema(kitchen_sink_path):
    """An inlined_as_list multivalued class slot becomes an array of the target schema."""
    output = ZodGenerator(kitchen_sink_path).serialize()
    assert "get persons() { return z.array(PersonSchema)" in output


def test_inlined_dict_is_record():
    """A multivalued inlined (dict) slot keyed by identifier becomes a z.record."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Item",
        slots=[
            SlotDefinition(name="id", range="string", identifier=True),
            SlotDefinition(name="label", range="string"),
        ],
    )
    sb.add_class(
        "Container",
        slots=[SlotDefinition(name="items", range="Item", multivalued=True, inlined=True)],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "get items() { return z.record(z.string(), ItemSchema)" in output


def test_any_of_union():
    """any_of over scalar ranges becomes a z.union of the member expressions."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "U",
        slots=[
            SlotDefinition(
                name="value",
                any_of=[AnonymousSlotExpression(range="string"), AnonymousSlotExpression(range="integer")],
            )
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "value: z.union([z.string(), z.number().int()])" in output


def test_exactly_one_of_xor():
    """exactly_one_of is rendered as z.xor (Zod's exclusive union)."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "X",
        slots=[
            SlotDefinition(
                name="name",
                range="string",
                exactly_one_of=[
                    AnonymousSlotExpression(pattern="a"),
                    AnonymousSlotExpression(pattern="b"),
                ],
            )
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "name: z.xor([z.string().regex(/a/), z.string().regex(/b/)])" in output


def test_all_of_intersection():
    """all_of over member expressions is rendered as chained z.and intersections."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "A",
        slots=[
            SlotDefinition(
                name="code",
                range="string",
                all_of=[
                    AnonymousSlotExpression(pattern="^a"),
                    AnonymousSlotExpression(pattern="z$"),
                ],
            )
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "code: z.string().regex(/^a/).and(z.string().regex(/z$/))" in output


def test_none_of_refine():
    """none_of is rendered as a .refine that rejects values matching any member schema."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "N",
        slots=[
            SlotDefinition(
                name="color",
                range="string",
                none_of=[
                    AnonymousSlotExpression(equals_string="purple"),
                    AnonymousSlotExpression(equals_string="green"),
                ],
            )
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert ".refine((val) =>" in output
    assert 'z.literal("purple")' in output
    assert 'z.literal("green")' in output
    assert ".some((s) => s.safeParse(val).success)" in output


def test_ifabsent_defaults():
    """ifabsent directives are rendered as Zod .default(...) literals."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Defaults",
        slots=[
            SlotDefinition(name="s", range="string", ifabsent="string(hello)"),
            SlotDefinition(name="n", range="integer", ifabsent="int(7)"),
            SlotDefinition(name="b", range="boolean", ifabsent="true"),
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert 's: z.string().default("hello")' in output
    assert "n: z.number().int().default(7)" in output
    assert "b: z.boolean().default(true)" in output


def test_uri_type_maps_to_url():
    """A slot whose range is the builtin uri type maps to z.url()."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Resource", slots=[SlotDefinition(name="homepage", range="uri", required=True)])
    output = ZodGenerator(sb.schema).serialize()
    assert "homepage: z.url()" in output


def test_type_level_pattern_propagated():
    """A pattern declared on a custom type is applied wherever the type is used."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
types:
  ControlId:
    typeof: string
    pattern: "^CIS-[0-9]+$"
classes:
  Control:
    attributes:
      code:
        range: ControlId
        required: true
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "code: z.string().regex(/^CIS-[0-9]+$/)" in output


def test_type_level_numeric_bounds_propagated():
    """minimum_value / maximum_value declared on a custom numeric type are applied."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
types:
  Percent:
    typeof: integer
    minimum_value: 0
    maximum_value: 100
classes:
  Reading:
    attributes:
      pct:
        range: Percent
        required: true
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "pct: z.number().int().gte(0).lte(100)" in output


def test_meta_description_emitted():
    """Class and slot descriptions are emitted as .meta({ description }) for downstream tooling."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Person",
        slots=[SlotDefinition(name="name", range="string", required=True, description="The name of the person")],
        description="A human being",
    )
    output = ZodGenerator(sb.schema).serialize()
    assert '.meta({ id: "Person", description: "A human being" })' in output
    assert 'name: z.string().meta({ description: "The name of the person" })' in output


def test_meta_examples_and_unit():
    """Slot examples and unit of measure are surfaced in .meta(...)."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Measurement:
    attributes:
      height:
        range: float
        required: true
        unit:
          ucum_code: cm
        examples:
          - value: "170"
          - value: "180"
"""
    output = ZodGenerator(schema=schema).serialize()
    assert 'unit: "cm"' in output
    assert 'examples: ["170", "180"]' in output


def test_polymorphic_inlined_range_expands_to_union():
    """An inlined range on a class with concrete descendants expands to a z.union."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Shape:
    attributes:
      label:
        range: string
  Circle:
    is_a: Shape
  Square:
    is_a: Shape
  Canvas:
    attributes:
      shapes:
        range: Shape
        multivalued: true
        inlined_as_list: true
"""
    output = ZodGenerator(schema=schema).serialize()
    seg = output.split("get shapes()")[1].split(";")[0]
    assert "z.array(z.union([" in seg
    assert "ShapeSchema" in seg
    assert "CircleSchema" in seg
    assert "SquareSchema" in seg


def test_polymorphic_union_excludes_abstract_base():
    """An abstract base class is not itself a member of the polymorphic union."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Shape:
    abstract: true
    attributes:
      label:
        range: string
  Circle:
    is_a: Shape
  Square:
    is_a: Shape
  Canvas:
    attributes:
      shapes:
        range: Shape
        multivalued: true
        inlined_as_list: true
"""
    output = ZodGenerator(schema=schema).serialize()
    seg = output.split("get shapes()")[1].split(";")[0]
    assert "z.union([CircleSchema, SquareSchema])" in seg
    assert "ShapeSchema" not in seg


def test_class_union_of_renders_lazy_union():
    """A class-level union_of becomes a lazily-evaluated z.union of the member schemas."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Dog:
    attributes:
      bark:
        range: string
  Cat:
    attributes:
      meow:
        range: string
  Pet:
    union_of:
      - Dog
      - Cat
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "export const PetSchema = z.lazy(() => z.union([DogSchema, CatSchema]))" in output


def test_exact_cardinality_length():
    """exact_cardinality bounds a multivalued slot with .length(n)."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Point",
        slots=[SlotDefinition(name="coords", range="float", multivalued=True, required=True, exact_cardinality=3)],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "coords: z.array(z.number()).length(3)" in output


def test_strict_option_uses_strict_object():
    """The strict option emits z.strictObject instead of z.object."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Person", slots=[SlotDefinition(name="name", range="string", required=True)])
    output = ZodGenerator(sb.schema, strict=True).serialize()
    assert "z.strictObject({" in output
    assert "z.object({" not in output


def test_coerce_option_wraps_scalars():
    """The coerce option wraps scalar validators in z.coerce.*."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Measurement",
        slots=[
            SlotDefinition(name="count", range="integer", required=True),
            SlotDefinition(name="label", range="string", required=True),
        ],
    )
    output = ZodGenerator(sb.schema, coerce=True).serialize()
    assert "count: z.coerce.number().int()" in output
    assert "label: z.coerce.string()" in output


def test_coerce_preserves_numeric_constraints():
    """Coerced numeric scalars still receive minimum/maximum_value constraints."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Reading",
        slots=[SlotDefinition(name="score", range="integer", required=True, minimum_value=0, maximum_value=100)],
    )
    output = ZodGenerator(sb.schema, coerce=True).serialize()
    assert "score: z.coerce.number().int().gte(0).lte(100)" in output


def test_enum_value_meta():
    """Permissible-value descriptions and meanings are surfaced in enum .meta(values)."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
  PATO: http://purl.obolibrary.org/obo/PATO_
default_prefix: ex
imports:
  - linkml:types
enums:
  PersonStatus:
    permissible_values:
      ALIVE:
        description: the person is living
        meaning: PATO:0001421
      DEAD:
        description: the person is deceased
        meaning: PATO:0001422
classes:
  Person:
    attributes:
      status:
        range: PersonStatus
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "values: {" in output
    assert '"ALIVE": { description: "the person is living", meaning: "PATO:0001421" }' in output
    assert '"DEAD": { description: "the person is deceased", meaning: "PATO:0001422" }' in output


def test_readonly_slot():
    """A slot marked readonly gets a .readonly() modifier."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Record",
        slots=[SlotDefinition(name="id", range="string", required=True, readonly="server-assigned")],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "id: z.string().readonly()" in output


def test_dynamic_enum_falls_back_to_string():
    """A dynamic (reachable_from) enum with no static values falls back to z.string()."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
  obo: http://purl.obolibrary.org/obo/
default_prefix: ex
imports:
  - linkml:types
enums:
  NeuronTypeEnum:
    reachable_from:
      source_ontology: obo:cl
      source_nodes: [CL:0000540]
classes:
  Cell:
    attributes:
      kind:
        range: NeuronTypeEnum
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "export const NeuronTypeEnum = z.string()" in output
    assert "z.enum([])" not in output


def test_empty_enum_falls_back_to_string():
    """An enum declared with no permissible values falls back to z.string()."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
enums:
  EmptyEnum: {}
classes:
  C:
    attributes:
      v:
        range: EmptyEnum
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "export const EmptyEnum = z.string()" in output
    assert "z.enum([])" not in output


def test_uri_slot_with_pattern_keeps_regex():
    """A uri-ranged slot that also declares a pattern keeps both z.url() and .regex()."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Resource",
        slots=[SlotDefinition(name="homepage", range="uri", required=True, pattern="^https")],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert "homepage: z.url().regex(/^https/)" in output


def test_none_of_with_inlined_class_member_is_deferred():
    """A none_of member referencing an inlined class is rendered inside a lazy getter."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Inner:
    attributes:
      label:
        range: string
  Outer:
    attributes:
      thing:
        range: Inner
        inlined: true
        none_of:
          - range: Inner
"""
    output = ZodGenerator(schema=schema).serialize()
    # The slot must be emitted as a lazy getter so the referenced InnerSchema is deferred.
    assert "get thing()" in output
    assert ".refine((val) =>" in output


def test_any_class_maps_to_z_any():
    """A class with class_uri linkml:Any maps to z.any(), and slots ranged on it too."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/
default_prefix: ex
imports:
  - linkml:types
classes:
  AnyObject:
    class_uri: linkml:Any
  Holder:
    attributes:
      payload:
        range: AnyObject
        inlined: true
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "export const AnyObjectSchema = z.any()" in output
    # An Any-ranged slot is not a schema reference, so it is inlined (no lazy getter).
    assert "payload: z.any()" in output
    assert "get payload()" not in output


def test_array_exact_dimensions_nested():
    """A slot with array.exact_number_dimensions becomes nested z.array layers."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Grid:
    attributes:
      matrix:
        range: integer
        array:
          exact_number_dimensions: 2
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "matrix: z.array(z.array(z.number().int()))" in output


def test_array_dimensions_with_cardinality():
    """Explicit array dimensions carry per-axis cardinality bounds."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Vec:
    attributes:
      xyz:
        range: float
        array:
          dimensions:
            - alias: axis
              exact_cardinality: 3
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "xyz: z.array(z.number()).length(3)" in output


def test_class_rules_render_refine():
    """Class-level rules become a .refine enforcing 'preconditions imply postconditions'."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Address:
    attributes:
      country:
        range: string
      postal_code:
        range: string
    rules:
      - preconditions:
          slot_conditions:
            country:
              equals_string: USA
        postconditions:
          slot_conditions:
            postal_code:
              pattern: "[0-9]{5}"
"""
    output = ZodGenerator(schema=schema).serialize()
    assert ".refine((val) => {" in output
    assert 'z.literal("USA")' in output
    assert "z.string().regex(/[0-9]{5}/)" in output
    assert 'message: "rule violation", path: ["postal_code"]' in output


def test_equals_string_slot_is_literal():
    """A slot-level equals_string constraint becomes a z.literal."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("C", slots=[SlotDefinition(name="kind", equals_string="foo")])
    output = ZodGenerator(sb.schema).serialize()
    assert 'kind: z.literal("foo")' in output


def test_equals_string_in_slot_is_enum():
    """A slot-level equals_string_in constraint becomes a z.enum of the allowed values."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("C", slots=[SlotDefinition(name="kind", equals_string_in=["foo", "bar"])])
    output = ZodGenerator(sb.schema).serialize()
    assert 'kind: z.enum(["foo", "bar"])' in output


def test_equals_number_slot_is_literal():
    """A slot-level equals_number constraint becomes a numeric z.literal."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("C", slots=[SlotDefinition(name="answer", range="integer", equals_number=42)])
    output = ZodGenerator(sb.schema).serialize()
    assert "answer: z.literal(42)" in output


def test_type_designator_and_discriminated_union():
    """A type-designator slot becomes a per-class literal and drives z.discriminatedUnion."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
slots:
  shape_type:
    range: string
    designates_type: true
classes:
  Shape:
    abstract: true
    slots:
      - shape_type
  Circle:
    is_a: Shape
  Square:
    is_a: Shape
  Canvas:
    attributes:
      shapes:
        range: Shape
        multivalued: true
        inlined_as_list: true
"""
    output = ZodGenerator(schema=schema).serialize()
    # Each concrete class fixes its discriminator to a literal of its own name.
    assert 'shape_type: z.literal("Circle")' in output
    assert 'shape_type: z.literal("Square")' in output
    # The polymorphic range dispatches on the designator via a discriminated union.
    seg = output.split("get shapes()")[1].split(";")[0]
    assert 'z.discriminatedUnion("shape_type", [CircleSchema, SquareSchema])' in seg


def test_meta_id_emitted_for_unique_names():
    """Classes and enums with a unique name carry a meta id for stable JSON Schema $defs."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Person", slots=[SlotDefinition(name="name", range="string", required=True)])
    output = ZodGenerator(sb.schema).serialize()
    assert "export const PersonSchema = z.object({" in output
    assert '.meta({ id: "Person" })' in output


def test_ncname_maps_to_regex():
    """The builtin ncname type validates the NCName lexical form."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("C", slots=[SlotDefinition(name="local", range="ncname", required=True)])
    output = ZodGenerator(sb.schema).serialize()
    assert "local: z.string().regex(/^[A-Za-z_][A-Za-z0-9._-]*$/)" in output


def test_iso_dates_option():
    """--iso-dates validates dates as ISO strings and omits the dateFromString preprocessor."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Event",
        slots=[
            SlotDefinition(name="on_date", range="date", required=True),
            SlotDefinition(name="at_time", range="datetime", required=True),
        ],
    )
    output = ZodGenerator(sb.schema, iso_dates=True).serialize()
    assert "on_date: z.iso.date()" in output
    assert "at_time: z.iso.datetime()" in output
    assert "dateFromString" not in output


def test_iso_dates_default_is_iso_string():
    """Under --iso-dates a date ifabsent renders as an ISO string literal, not new Date()."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Event",
        slots=[SlotDefinition(name="on_date", range="date", ifabsent="date(2020-01-01)")],
    )
    output = ZodGenerator(sb.schema, iso_dates=True).serialize()
    assert 'on_date: z.iso.date().default("2020-01-01")' in output


def test_default_dates_use_date_object_without_iso():
    """Without --iso-dates, dates keep the Date-coercion behaviour."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Event", slots=[SlotDefinition(name="on_date", range="date", required=True)])
    output = ZodGenerator(sb.schema).serialize()
    assert "on_date: dateFromString" in output
    assert "const dateFromString" in output


def test_all_members_and_has_member():
    """all_members / has_member constraints append .refine checks to the array."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Bag",
        slots=[
            SlotDefinition(
                name="codes",
                range="string",
                multivalued=True,
                required=True,
                all_members=AnonymousSlotExpression(pattern="^[A-Z]"),
                has_member=AnonymousSlotExpression(equals_string="ROOT"),
            )
        ],
    )
    output = ZodGenerator(sb.schema).serialize()
    assert ".every((x) => (z.string().regex(/^[A-Z]/)).safeParse(x).success)" in output
    assert '.some((x) => (z.literal("ROOT")).safeParse(x).success)' in output


def test_brand_option_on_identifier_class():
    """--brand nominally brands classes that have an identifier slot."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Person",
        slots=[
            SlotDefinition(name="id", range="string", identifier=True),
            SlotDefinition(name="name", range="string"),
        ],
    )
    output = ZodGenerator(sb.schema, brand=True).serialize()
    assert '.brand("Person")' in output


def test_brand_option_skips_class_without_identifier():
    """--brand does not brand classes that lack an identifier slot."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Note", slots=[SlotDefinition(name="text", range="string")])
    output = ZodGenerator(sb.schema, brand=True).serialize()
    assert ".brand(" not in output


def test_zod_mini_import_and_wrappers():
    """--zod-mini emits the functional import and wrapper-style optionality."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Person",
        slots=[
            SlotDefinition(name="id", range="string", required=True),
            SlotDefinition(name="age", range="integer"),
        ],
    )
    output = ZodGenerator(sb.schema, zod_mini=True).serialize()
    assert 'import * as z from "zod/mini";' in output
    # optional slot is wrapped, not chained; integer uses the top-level z.int()
    assert "age: z.nullable(z.optional(z.int()))" in output
    # no Date preprocessor is emitted (mini has no z.preprocess)
    assert "dateFromString" not in output


def test_zod_mini_checks_and_meta():
    """--zod-mini collects constraints in .check(...) and attaches metadata via z.meta."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Rec",
        slots=[
            SlotDefinition(
                name="score",
                range="integer",
                required=True,
                minimum_value=0,
                maximum_value=100,
                description="a score",
            )
        ],
        description="a record",
    )
    output = ZodGenerator(sb.schema, zod_mini=True).serialize()
    assert 'score: z.int().check(z.gte(0), z.lte(100)).check(z.meta({ description: "a score" }))' in output
    assert '.check(z.meta({ id: "Rec", description: "a record" }))' in output


def test_zod_mini_default_and_dates():
    """--zod-mini uses z._default and ISO dates."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "E",
        slots=[
            SlotDefinition(name="kind", range="string", ifabsent="string(x)"),
            SlotDefinition(name="on_date", range="date", required=True),
        ],
    )
    output = ZodGenerator(sb.schema, zod_mini=True).serialize()
    assert 'kind: z._default(z.string(), "x")' in output
    assert "on_date: z.iso.date()" in output


def test_zod_mini_array_and_intersection():
    """--zod-mini uses .check length bounds and z.intersection for all_of."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "Bag",
        slots=[
            SlotDefinition(name="items", range="string", multivalued=True, required=True, minimum_cardinality=1),
            SlotDefinition(
                name="code",
                range="string",
                all_of=[
                    AnonymousSlotExpression(pattern="^a"),
                    AnonymousSlotExpression(pattern="z$"),
                ],
            ),
        ],
    )
    output = ZodGenerator(sb.schema, zod_mini=True).serialize()
    assert "items: z.array(z.string()).check(z.minLength(1))" in output
    assert "z.intersection(z.string().check(z.regex(/^a/)), z.string().check(z.regex(/z$/)))" in output


def test_zod_mini_annotates_only_recursive_getters():
    """In zod/mini, only reference getters in a cycle get the z.ZodMiniType annotation."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Leaf:
    attributes:
      v:
        range: string
  Node:
    attributes:
      child:
        range: Node
        inlined: true
      tag:
        range: Leaf
        inlined: true
"""
    output = ZodGenerator(schema=schema, zod_mini=True).serialize()
    # self-referential slot is annotated; the non-recursive Leaf reference is not.
    assert "get child(): z.ZodMiniType {" in output
    assert "get tag() {" in output


def test_zod_mini_coerce_integer_merges_checks():
    """--zod-mini --coerce integer enforces int and merges bounds into one .check(...)."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class(
        "M",
        slots=[SlotDefinition(name="n", range="integer", required=True, minimum_value=0, maximum_value=10)],
    )
    output = ZodGenerator(sb.schema, zod_mini=True, coerce=True).serialize()
    assert "n: z.coerce.number().check(z.int(), z.gte(0), z.lte(10))" in output


def test_mini_type_and_slot_constraints_single_check():
    """A custom-type constraint plus a slot constraint collapse into one .check(...) in mini."""
    schema = """
id: unit_test
name: unit_test
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
types:
  Bounded:
    typeof: integer
    minimum_value: 0
classes:
  C:
    attributes:
      n:
        range: Bounded
        maximum_value: 10
"""
    output = ZodGenerator(schema=schema, zod_mini=True).serialize()
    # type-level gte(0) and slot-level lte(10) in a single check call
    assert "z.int().check(z.gte(0), z.lte(10))" in output


def test_registry_emits_collection_and_metadata():
    """--registry emits a typed registry and registers each schema with its semantic metadata."""
    schema = """
id: https://example.org/r
name: r
prefixes:
  ex: https://example.org/
  schema: http://schema.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Person:
    class_uri: schema:Person
    exact_mappings: [schema:Person]
    in_subset: [core]
    attributes:
      name:
        range: string
enums:
  Status:
    permissible_values:
      ACTIVE:
"""
    output = ZodGenerator(schema=schema, registry="modelRegistry").serialize()
    assert "export interface LinkmlMeta {" in output
    assert "export const modelRegistry = z.registry<LinkmlMeta>();" in output
    assert 'modelRegistry.add(StatusEnum, { uri: "ex:Status" });' in output
    assert (
        'modelRegistry.add(PersonSchema, { uri: "schema:Person", '
        'exact_mappings: ["schema:Person"], in_subset: ["core"] });'
    ) in output


def test_no_registry_by_default():
    """Without --registry, no registry declaration or add calls are emitted."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Person", slots=[SlotDefinition(name="name", range="string")])
    output = ZodGenerator(sb.schema).serialize()
    assert "z.registry" not in output
    assert "LinkmlMeta" not in output
    assert ".add(" not in output


def test_registry_works_with_zod_mini():
    """The registry is emitted the same way when targeting zod/mini."""
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Person", slots=[SlotDefinition(name="name", range="string")])
    output = ZodGenerator(sb.schema, zod_mini=True, registry="reg").serialize()
    assert "export const reg = z.registry<LinkmlMeta>();" in output
    assert "reg.add(PersonSchema, {" in output


def test_zodgen_annotation_sets_behavior_flags():
    """A schema-level zod_strict annotation drives the strict behavior flag."""
    schema = """
id: https://example.org/a
name: a
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
annotations:
  zod_strict: true
classes:
  Person:
    attributes:
      name:
        range: string
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "z.strictObject({" in output
    assert "z.object({" not in output


def test_cli_flag_overrides_annotation():
    """An explicit constructor/CLI value overrides the schema annotation."""
    schema = """
id: https://example.org/a
name: a
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
annotations:
  zod_strict: true
classes:
  Person:
    attributes:
      name:
        range: string
"""
    output = ZodGenerator(schema=schema, strict=False).serialize()
    assert "z.object({" in output
    assert "z.strictObject({" not in output


def test_slot_zod_format_annotation():
    """A slot-level zod_format annotation selects a named Zod format validator."""
    schema = """
id: https://example.org/a
name: a
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Contact:
    attributes:
      email:
        range: string
        required: true
        annotations:
          zod_format: email
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "email: z.email()" in output


def test_slot_zod_type_annotation_verbatim():
    """A slot-level zod_type annotation is emitted verbatim as the base expression."""
    schema = """
id: https://example.org/a
name: a
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Widget:
    attributes:
      handle:
        range: string
        required: true
        annotations:
          zod_type: z.custom<Handle>()
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "handle: z.custom<Handle>()" in output


def test_slot_zod_format_works_in_zod_mini():
    """zod_format uses dialect-agnostic top-level validators, so it works in zod/mini too."""
    schema = """
id: https://example.org/a
name: a
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Contact:
    attributes:
      email:
        range: string
        annotations:
          zod_format: email
"""
    output = ZodGenerator(schema=schema, zod_mini=True).serialize()
    assert "email: z.nullable(z.optional(z.email()))" in output


def test_slot_zod_format_still_applies_pattern():
    """A pattern on a zod_format slot is applied on top of the format validator."""
    schema = """
id: https://example.org/a
name: a
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
classes:
  Contact:
    attributes:
      email:
        range: string
        required: true
        pattern: "@example.com$"
        annotations:
          zod_format: email
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "email: z.email().regex(/@example.com$/)" in output


def test_duplicate_type_and_slot_constraints_collapse():
    """A bound declared on both a type and its slot is emitted only once."""
    schema = """
id: https://example.org/a
name: a
prefixes:
  ex: https://example.org/
default_prefix: ex
imports:
  - linkml:types
types:
  Small:
    typeof: integer
    minimum_value: 0
classes:
  C:
    attributes:
      n:
        range: Small
        required: true
        minimum_value: 0
"""
    output = ZodGenerator(schema=schema).serialize()
    assert "n: z.number().int().gte(0)" in output
    assert ".gte(0).gte(0)" not in output
