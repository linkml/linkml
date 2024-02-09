from importlib.metadata import version

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
    # TODO: also check for expanded dicts
    #  https://github.com/linkml/linkml/issues/1304
    with open(input_path("kitchen_sink_inst_01.yaml")) as stream:
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


@pytest.mark.parametrize(
    "range,multivalued,inlined,inlined_as_list,B_has_identifier,expected,notes",
    [
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
            "Optional[Dict[str, str]]",
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
    ],
)
def test_pydantic_inlining(range, multivalued, inlined, inlined_as_list, B_has_identifier, expected, notes):
    # Case = namedtuple("multivalued", "inlined", "inlined_as_list", "B_has_identities")
    expected_default_factories = {
        "Optional[List[str]]": "Field(default_factory=list)",
        "Optional[List[B]]": "Field(default_factory=list)",
        "Optional[Dict[str, B]]": "Field(default_factory=dict)",
        "Optional[Dict[str, str]]": "Field(default_factory=dict)",
    }

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
    assert f"a2b: {expected}" in slot_line, f"did not find expected {expected} in {slot_line}"
    if expected not in expected_default_factories:
        raise ValueError(f"unexpected default factory for {expected}")
    assert (
        expected_default_factories[expected] in slot_line
    ), f"did not find expected default factory {expected_default_factories[expected]}"


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


def test_pydantic_pattern(kitchen_sink_path, tmp_path, input_path):
    """Check if regex patterns are enforced. Only checks scalar case"""
    gen = PydanticGenerator(kitchen_sink_path, package=PACKAGE)
    code = gen.serialize()
    module = compile_python(code, PACKAGE)
    # scalar pattern enforcement
    p1 = module.Person(id="01", name="John Doe")
    assert p1.name == "John Doe"
    with pytest.raises(ValidationError):
        module.Person(id="01", name="x")


def test_pydantic_template_1666():
    """
    Regression test for https://github.com/linkml/linkml/issues/1666
    """
    bad_schema = """
name: BadSchema
id: BadSchema
imports:
- linkml:types
classes:
  BadClass:
    attributes:
      keys:
        name: keys
        range: string
      values:
        name: values
        range: integer
        ifabsent: int(1)
    """
    gen = PydanticGenerator(bad_schema, package=PACKAGE)
    code = gen.serialize()
    # test fails here if "is_string" check not applied
    # so the test is just that this completes successfully and
    # doesn't generate a field like
    # keys: Optional[str] = Field(<built-in method keys of dict object at 0x10f1f13c0>)
    mod = compile_python(code, PACKAGE)

    # and we check that we haven't lost defaults when they are set
    pydantic_major_version = int(version("pydantic").split(".")[0])
    if pydantic_major_version >= 2:
        assert mod.BadClass.model_fields["keys"].default is None
        assert mod.BadClass.model_fields["values"].default == 1
    else:
        assert mod.BadClass.__fields__["keys"].default is None
        assert mod.BadClass.__fields__["values"].default == 1


def test_pydantic_arrays():
    import numpy as np

    unit_test_schema = """
id: https://example.org/arrays
name: arrays-temperature-example
title: Array Temperature Example
description: |-
  Example LinkML schema to demonstrate a 3D DataArray of temperature values with labeled axes
license: MIT

prefixes:
  linkml: https://w3id.org/linkml/
  wgs84: http://www.w3.org/2003/01/geo/wgs84_pos#
  example: https://example.org/

default_prefix: example

imports:
  - linkml:types

classes:

  TemperatureDataset:
    tree_root: true
    implements:
      - linkml:DataArray
    attributes:
      name:
        identifier: true
        range: string
      latitude_in_deg:
        implements:
          - linkml:axis
        range: LatitudeSeries
        required: true
        annotations:
          axis_index: 0
      longitude_in_deg:
        implements:
          - linkml:axis
        range: LongitudeSeries
        required: true
        annotations:
          axis_index: 1
      time_in_d:
        implements:
          - linkml:axis
        range: DaySeries
        required: true
        annotations:
          axis_index: 2
      temperatures_in_K:
        implements:
          - linkml:array
        range: TemperatureMatrix
        required: true

  TemperatureMatrix:
    description: A 3D array of temperatures
    implements:
      - linkml:NDArray
      - linkml:RowOrderedArray
    attributes:
      values:
        range: float
        multivalued: true
        implements:
          - linkml:elements
        required: true
        unit:
          ucum_code: K
    annotations:
      dimensions: 3

  LatitudeSeries:
    description: A series whose values represent latitude
    implements:
      - linkml:NDArray
    attributes:
      values:
        range: float
        multivalued: true
        implements:
          - linkml:elements
        required: true
        unit:
          ucum_code: deg
    annotations:
      dimensions: 1

  LongitudeSeries:
    description: A series whose values represent longitude
    implements:
      - linkml:NDArray
    attributes:
      values:
        range: float
        multivalued: true
        implements:
          - linkml:elements
        required: true
        unit:
          ucum_code: deg
    annotations:
      dimensions: 1

  DaySeries:
    description: A series whose values represent the days since the start of the measurement period
    implements:
      - linkml:NDArray
    attributes:
      values:
        range: float
        multivalued: true
        implements:
          - linkml:elements
        required: true
        unit:
          ucum_code: d
    annotations:
      dimensions: 1
  """

    gen = PydanticGenerator(schema=unit_test_schema)

    code = gen.serialize()
    assert "import numpy as np" in code
    # assert code.count("values: np.ndarray = Field()") == 3
    # assert code.count("temperatures: np.ndarray = Field()") == 1

    mod = compile_python(code, PACKAGE)
    lat = mod.LatitudeSeries(values=np.array([1, 2, 3]))
    np.testing.assert_array_equal(lat.values, np.array([1, 2, 3]))
    lon = mod.LongitudeSeries(values=np.array([4, 5, 6]))
    np.testing.assert_array_equal(lon.values, np.array([4, 5, 6]))
    day = mod.DaySeries(values=np.array([7, 8, 9]))
    np.testing.assert_array_equal(day.values, np.array([7, 8, 9]))
    temperatures = mod.TemperatureMatrix(values=np.ones((3, 3, 3)))
    np.testing.assert_array_equal(temperatures.values, np.ones((3, 3, 3)))

    temperature_dataset = mod.TemperatureDataset(
        name="temperatures",
        latitude_in_deg=lat,
        longitude_in_deg=lon,
        time_in_d=day,
        temperatures_in_K=temperatures,
    )
    assert temperature_dataset.name == "temperatures"
    assert temperature_dataset.latitude_in_deg == lat
    assert temperature_dataset.longitude_in_deg == lon
    assert temperature_dataset.time_in_d == day
    assert temperature_dataset.temperatures_in_K == temperatures


def test_column_ordered_array_not_supported():
    unit_test_schema = """
id: https://example.org/arrays
name: arrays-example
prefixes:
  linkml: https://w3id.org/linkml/
  example: https://example.org/
  default_prefix: example
imports:
- linkml:types

classes:
  TemperatureMatrix:
    tree_root: true
    implements:
      - linkml:NDArray
      - linkml:ColumnOrderedArray
    attributes:
      temperatures:
        implements:
          - linkml:elements
        multivalued: true
        range: float
        required: true
        unit:
          ucum_code: K
    annotations:
      dimensions: 2
"""

    gen = PydanticGenerator(schema=unit_test_schema)
    with pytest.raises(NotImplementedError):
        gen.serialize()
