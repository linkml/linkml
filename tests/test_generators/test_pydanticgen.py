import pytest
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.utils.schema_builder import SchemaBuilder

PACKAGE = "kitchen_sink"


def test_pydantic(kitchen_sink_path, tmp_path, input_path):
    """Generate pydantic classes"""
    gen = PydanticGenerator(kitchen_sink_path, package=PACKAGE)
    code = gen.serialize()
    # TODO: lowering the bar for the pydantic test until list to dict normalization is supported
    #  https://github.com/linkml/linkml/issues/1304
    with open(input_path("kitchen_sink_normalized_inst_01.yaml")) as stream:
        dataset_dict = yaml.safe_load(stream)

    module = compile_python(code, PACKAGE)
    # NOTE: generated pydantic doesn't yet do validation
    e1 = module.EmploymentEvent(is_current=True)
    p1 = module.Person(id="x", has_employment_history=[e1])
    assert p1.id == "x"
    assert p1.name is None
    json = {"id": "P1", "has_employment_history": [{"is_current": True}]}
    module.Person(**json)
    module.Person(**dataset_dict["persons"][0])
    ds1 = module.Dataset(**dataset_dict)
    assert len(ds1.persons) == 2


def test_compile_pydantic(kitchen_sink_path):
    """Generate and compile pydantic classes"""
    gen = PydanticGenerator(kitchen_sink_path, package=PACKAGE)
    code = gen.serialize()
    mod = compile_python(code, PACKAGE)
    p = mod.Person(id="P:1")
    assert p.id == "P:1"
    with pytest.raises(ValidationError):
        mod.Person(no_such_field="x")
    with pytest.raises(ValidationError):
        mod.Person(age_in_years="x")


def test_pydantic_enums():
    unit_test_schema = """
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
"""

    sv = SchemaView(unit_test_schema)
    gen = PydanticGenerator(schema=unit_test_schema)
    enums = gen.generate_enums(sv.all_enums())
    assert enums
    enum = enums["TestEnum"]
    assert enum
    assert enum["values"]["number_123"]["value"] == "123"
    assert enum["values"]["PLUS_SIGN"]["value"] == "+"
    assert enum["values"]["This_AMPERSAND_that_plus_maybe_a_TOP_HAT"]["value"] == "This & that, plus maybe a 🎩"
    assert enum["values"]["Ohio"]["value"] == "Ohio"


def test_pydantic_any_of():
    # TODO: convert to SchemaBuilder and parameterize?
    schema_str = """
id: test_schema
name: test_info
description: just testing
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/

imports:
  - https://w3id.org/linkml/types

classes:
  A:
    slots:
      - id
  B:
    slots:
      - id
  C:
    slots:
      - id
      - inlined_things
      - inlined_as_list_things
      - not_inlined_things
slots:
  id:
    identifier: true
  inlined_things:
    inlined: true
    multivalued: true
    any_of:
      - range: A
      - range: B
  inlined_as_list_things:
    inlined_as_list: true
    multivalued: true
    any_of:
      - range: A
      - range: B
  not_inlined_things:
    multivalued: true
    any_of:
      - range: A
      - range: B
        """
    gen = PydanticGenerator(schema_str, package=PACKAGE)
    code = gen.serialize()
    lines = code.splitlines()
    ix = lines.index("class C(ConfiguredBaseModel):")
    assert lines[ix + 3] == "    inlined_things: Optional[Dict[str, Union[A, B]]] = Field(default_factory=dict)"
    assert lines[ix + 4] == "    inlined_as_list_things: Optional[List[Union[A, B]]] = Field(default_factory=list)"
    assert lines[ix + 5] == "    not_inlined_things: Optional[List[str]] = Field(default_factory=list)"


def test_pydantic_inlining():
    # Case = namedtuple("multivalued", "inlined", "inlined_as_list", "B_has_identities")
    expected_default_factories = {
        "Optional[List[str]]": "Field(default_factory=list)",
        "Optional[List[B]]": "Field(default_factory=list)",
        "Optional[Dict[str, B]]": "Field(default_factory=dict)",
    }
    cases = [
        # block 1: primitives are NEVER inlined
        (
            "T",
            True,
            False,
            False,
            True,
            "Optional[List[str]]",
            "primitives are never inlined",
        ),
        # attempting to inline a type
        # TBD: does the spec actively forbid this
        (
            "T",
            True,
            True,
            True,
            True,
            "Optional[List[str]]",
            "primitives are never inlined, even if requested",
        ),
        # block 2: referenced element is a class
        (
            "B",
            True,
            False,
            False,
            False,
            "Optional[List[B]]",
            "references to classes without identifiers ALWAYS inlined as list",
        ),
        (
            "B",
            True,
            True,
            False,
            False,
            "Optional[List[B]]",
            "references to classes without identifiers ALWAYS inlined as list",
        ),
        (
            "B",
            True,
            True,
            True,
            False,
            "Optional[List[B]]",
            "references to classes without identifiers ALWAYS inlined as list",
        ),
        (
            "B",
            True,
            True,
            False,
            True,
            "Optional[Dict[str, B]]",
            "references to class with identifier inlined ONLY ON REQUEST, with dict as default",
        ),
        # TODO: fix the next two
        (
            "B",
            True,
            True,
            True,
            True,
            "Optional[List[B]]",
            "references to class with identifier inlined as list ONLY ON REQUEST",
        ),
        ("B", True, False, False, True, "Optional[List[str]]", ""),
    ]
    for (
        range,
        multivalued,
        inlined,
        inlined_as_list,
        B_has_identifier,
        expected,
        notes,
    ) in cases:
        sb = SchemaBuilder("test")
        sb.add_type("T", typeof="string")
        a2b = SlotDefinition(
            "a2b",
            range=range,
            multivalued=multivalued,
            inlined=inlined,
            inlined_as_list=inlined_as_list,
        )
        sb.add_class("A", slots=[a2b])
        b_id = SlotDefinition("id", identifier=B_has_identifier)
        sb.add_class("B", slots=[b_id, "name"])
        sb.add_defaults()
        schema = sb.schema
        schema_str = yaml_dumper.dumps(schema)
        gen = PydanticGenerator(schema_str, package=PACKAGE)
        code = gen.serialize()
        lines = code.splitlines()
        ix = lines.index("class A(ConfiguredBaseModel):")
        assert ix > 0
        # assume a single blank line separating
        slot_line = lines[ix + 2]
        assert f"a2b: {expected}" in slot_line
        if expected not in expected_default_factories:
            raise ValueError(f"unexpected default factory for {expected}")
        assert expected_default_factories[expected] in slot_line


def test_ifabsent():
    schema_str = """
id: id
name: test_info
description: just testing

prefixes:
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/

imports:
  - https://w3id.org/linkml/types

classes:
  Test:
    description: just a test
    attributes:
      attr1:
        range: integer
        ifabsent: int(10)
      attr2:
        range: string
        ifabsent: string(hello world)
      attr3:
        range: boolean
        ifabsent: True
      attr4:
        range: float
        ifabsent: float(1.0)
      attr5:
        range: date
        ifabsent: date(2020-01-01)
      attr6:
        range: datetime
        ifabsent: datetime(2020-01-01T00:00:00Z)
        """

    gen = PydanticGenerator(schema_str)
    code = gen.serialize()
    lines = code.splitlines()
    ix = lines.index("class Test(ConfiguredBaseModel):")
    integer_slot_line = lines[ix + 4].strip()
    assert integer_slot_line == "attr1: Optional[int] = Field(10)"
    string_slot_line = lines[ix + 5].strip()
    assert string_slot_line == 'attr2: Optional[str] = Field("hello world")'
    boolean_slot_line = lines[ix + 6].strip()
    assert boolean_slot_line == "attr3: Optional[bool] = Field(True)"
    float_slot_line = lines[ix + 7].strip()
    assert float_slot_line == "attr4: Optional[float] = Field(1.0)"
    date_slot_line = lines[ix + 8].strip()
    assert date_slot_line == "attr5: Optional[date] = Field(datetime.date(2020, 01, 01))"
    datetime_slot_line = lines[ix + 9].strip()
    assert datetime_slot_line == "attr6: Optional[datetime ] = Field(datetime.datetime(2020, 01, 01, 00, 00, 00))"


def test_multiline_module(input_path):
    """
    Ensure that multi-line enum descriptions and enums containing
    reserved characters are handled correctly
    """
    gen = PydanticGenerator(str(input_path("kitchen_sink_mlm.yaml")), package=PACKAGE)

    assert gen.schema.enums["EmploymentEventType"].description == "\n".join(
        [
            "codes for different kinds of employment",
            "or HR related events",
            '"""',
            "print('Deleting your stuff!!')",
            '"""',
            "HR is pretty dull",
            'but they get "annoyed if [they]',
            'are not included"',
            "",
        ]
    )

    assert 'INTERNAL "REORGANIZATION"' in gen.schema.enums["EmploymentEventType"].permissible_values
