import importlib
import inspect
import re
import typing
from contextlib import nullcontext as does_not_raise
from dataclasses import dataclass
from importlib.metadata import version
from importlib.util import find_spec
from pathlib import Path
from types import GeneratorType, ModuleType
from typing import ClassVar, Dict, Iterable, List, Literal, Optional, Type, Union

import numpy as np
import pytest
import yaml
from jinja2 import DictLoader, Environment, Template
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import ClassDefinition, Definition, SchemaDefinition, SlotDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import camelcase, remove_empty_items, underscore
from linkml_runtime.utils.schemaview import load_schema_wrap
from pydantic import BaseModel, ValidationError

from linkml.generators import pydanticgen as pydanticgen_root
from linkml.generators.common.lifecycle import TClass, TSlot
from linkml.generators.pydanticgen import (
    MetadataMode,
    PydanticGenerator,
    array,
    build,
    pydanticgen,
    template,
)
from linkml.generators.pydanticgen.array import AnyShapeArray, ArrayRepresentation, ArrayValidator
from linkml.generators.pydanticgen.template import (
    ConditionalImport,
    Import,
    Imports,
    ObjectImport,
    PydanticAttribute,
    PydanticClass,
    PydanticModule,
    PydanticTemplateModel,
    PydanticValidator,
)
from linkml.utils.exceptions import ValidationError as ArrayValidationError
from linkml.utils.schema_builder import SchemaBuilder

from .conftest import MyInjectedClass

PACKAGE = "kitchen_sink"
pytestmark = pytest.mark.pydanticgen


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


def test_pydantic_enum_titles():
    unit_test_schema = """
id: unit_test
name: unit_test

prefixes:
  ex: https://example.org/
default_prefix: ex

enums:
  TestEnum:
    permissible_values:
      value1:
        title: label1
      value2:
        title: label2
      value3:
    """
    sv = SchemaView(unit_test_schema)
    gen = PydanticGenerator(schema=unit_test_schema)
    enums = gen.generate_enums(sv.all_enums())
    assert enums
    enum = enums["TestEnum"]
    assert enum
    assert enum["values"]["label1"]["value"] == "value1"
    assert enum["values"]["label2"]["value"] == "value2"
    assert enum["values"]["value3"]["value"] == "value3"


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
  - linkml:types

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
    assert "inlined_things: Optional[Dict[str, Union[A, B]]] = Field(None" in code
    assert "inlined_as_list_things: Optional[List[Union[A, B]]] = Field(None" in code
    assert "not_inlined_things: Optional[List[str]] = Field(None" in code


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
            "Optional[Dict[str, Union[str, B]]]",
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
        "Optional[List[str]]": "Field(None",
        "Optional[List[B]]": "Field(None",
        "Optional[Dict[str, B]]": "Field(None",
        "Optional[Dict[str, str]]": "Field(None",
        "Optional[Dict[str, Union[str, B]]]": "Field(None",
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

    assert f"a2b: {expected}" in code, f"did not find expected {expected} in {code}"
    if expected not in expected_default_factories:
        raise ValueError(f"unexpected default factory for {expected}")
    assert (
        expected_default_factories[expected] in code
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
  - linkml:types

classes:
  Test_Class:
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
    assert "attr1: Optional[int] = Field(10" in code
    assert 'attr2: Optional[str] = Field("hello world"' in code
    assert "attr3: Optional[bool] = Field(True" in code
    assert "attr4: Optional[float] = Field(1.0" in code
    assert "attr5: Optional[date] = Field(date(2020, 1, 1)" in code
    assert "attr6: Optional[datetime ] = Field(datetime(2020, 1, 1, 0, 0, 0)" in code


def test_equals_string():
    equals_string = "THIS_IS_THE_ONLY_VALUE"
    another_string = "ANY OTHER STRING"
    schema_str = f"""
id: test_schema
name: test_info
imports:
  - linkml:types
classes:
  A:
    attributes:
      my_slot:
        range: string
        equals_string: {equals_string}
        required: true
"""
    gen = PydanticGenerator(schema_str, package=PACKAGE)
    rendered = gen.render()
    code = gen.serialize(rendered_module=rendered)
    mod = compile_python(code)

    assert equals_string != another_string

    # our annotation should be a literal
    annotation = mod.A.model_fields["my_slot"].annotation
    assert annotation.__origin__ is Literal
    assert annotation.__args__ == (equals_string,)

    # can instantiate with the ONE STRING WE ALLOW
    _ = mod.A(my_slot=equals_string)

    # but any other string should fail
    with pytest.raises(ValidationError):
        _ = mod.A(my_slot=another_string)


def test_equals_string_in():
    equals_string_in = ["THIS_IS_THE_ONLY_VALUE", "THAT WAS A LIE", "THERE ARE MULTIPLE"]
    another_string_in = ["ANY OTHER STRING THOUGH", "STRICTLY NOT ALLOWED", "WE ARE SERIOUS"]
    schema_str = f"""
id: test_schema
name: test_info
imports:
  - linkml:types
classes:
  A:
    attributes:
      my_slot:
        range: string
        equals_string_in: [{", ".join(equals_string_in)}]
        required: true
"""
    gen = PydanticGenerator(schema_str, package=PACKAGE)
    rendered = gen.render()
    code = gen.serialize(rendered_module=rendered)
    mod = compile_python(code)

    assert not any([a_string in equals_string_in for a_string in another_string_in])

    # our annotation should be a literal
    annotation = mod.A.model_fields["my_slot"].annotation
    assert annotation.__origin__ is Literal
    assert annotation.__args__ == tuple(equals_string_in)

    # can instantiate with the ONE STRING WE ALLOW
    for a_string in equals_string_in:
        _ = mod.A(my_slot=a_string)

    # but any other string should fail
    for a_string in another_string_in:
        with pytest.raises(ValidationError):
            _ = mod.A(my_slot=a_string)


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


@pytest.mark.skip("this format of arrays is not yet implemented in the metamodel??")
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


@pytest.mark.parametrize(
    "value, required, minimium_cardinality, maximum_cardinality, exact_cardinality, valid",
    (
        (
            None,
            False,
            None,
            None,
            None,
            True,
        ),  # if it is not required and the passed in value is None, it should be valid
        (None, False, 1, None, None, True),
        (None, False, None, 1, None, True),
        (None, False, None, None, 1, True),
        (None, True, None, None, None, False),  # if it is required, None should not be valid
        (None, True, 1, None, None, False),
        (None, True, None, 1, None, False),
        (None, True, None, None, 1, False),
        ([], False, None, None, None, True),  # empty arrays should be treated like regular array values nevertheless
        ([], False, 1, None, None, False),
        ([], False, None, 1, None, True),
        ([], False, None, None, 1, False),
        ([], True, None, None, None, True),
        ([], True, 1, None, None, False),
        ([], True, None, None, 2, False),
        ([], True, 0, None, None, True),
        ([], True, None, 0, None, True),
        ([1, 2, 3], False, None, None, None, True),  # typical case, not required
        ([1, 2, 3], False, 1, None, None, True),
        ([1, 2, 3], False, 3, None, None, True),
        ([1, 2, 3], False, 4, None, None, False),
        ([1, 2, 3], False, None, 1, None, False),
        ([1, 2, 3], False, None, 3, None, True),
        ([1, 2, 3], False, None, 4, None, True),
        ([1, 2, 3], False, None, None, 2, False),
        ([1, 2, 3], False, None, None, 3, True),
        ([1, 2, 3], False, 1, 3, None, True),
        ([1, 2, 3], False, 1, 2, None, False),
        ([5] * 11, False, None, 10, None, False),
        ([1, 2, 3], True, None, None, None, True),  # typical case, required
        ([1, 2, 3], True, 1, None, None, True),
        ([1, 2, 3], True, 3, None, None, True),
        ([1, 2, 3], True, 4, None, None, False),
        ([1, 2, 3], True, None, 1, None, False),
        ([1, 2, 3], True, None, 3, None, True),
        ([1, 2, 3], True, None, 4, None, True),
        ([1, 2, 3], True, None, None, 2, False),
        ([1, 2, 3], True, None, None, 3, True),
        ([1, 2, 3], True, 1, 3, None, True),
        ([1, 2, 3], True, 1, 2, None, False),
        ([5] * 11, True, None, 10, None, False),
        ([1, 2, 3], True, 3, 3, 3, True),
    ),
)
def test_pydantic_cardinality(value, required, minimium_cardinality, maximum_cardinality, exact_cardinality, valid):
    """
    Ensure that the cardinality constraints for list length are correctly applied
    to the generated pydantic model, using SchemaBuilder.
    """
    schema_builder = SchemaBuilder("cardinality_test")
    schema_builder.add_class(
        "CardinalityArray",
        slots=[
            SlotDefinition(
                "cardinality_array",
                range="float",
                multivalued=True,
                required=required,
                minimum_cardinality=minimium_cardinality,
                maximum_cardinality=maximum_cardinality,
                exact_cardinality=exact_cardinality,
            )
        ],
    )
    schema_builder.add_defaults()

    gen = PydanticGenerator(schema=schema_builder.schema)
    code = gen.serialize()

    mod = compile_python(code)
    cls = mod.CardinalityArray
    field = cls.model_fields["cardinality_array"]

    assert field.is_required() == required
    assert field.annotation == List[float] if required else Optional[List[float]]

    # filter down the metadata to only min_length and max_length entries
    min_length = [entry.min_length for entry in field.metadata if getattr(entry, "min_length", None) is not None]
    max_length = [entry.max_length for entry in field.metadata if getattr(entry, "max_length", None) is not None]

    if exact_cardinality:
        assert len(min_length) == 1
        assert len(max_length) == 1
        assert exact_cardinality == min_length[0]
        assert exact_cardinality == max_length[0]
    if minimium_cardinality:
        assert len(min_length) == 1
        assert minimium_cardinality == min_length[0]
    if maximum_cardinality:
        assert len(max_length) == 1
        assert maximum_cardinality == max_length[0]

    if valid:
        cls(cardinality_array=value)
    else:
        with pytest.raises(ValidationError):
            cls(cardinality_array=value)


def test_pydantic_cardinality_plain():
    """
    Ensure that the cardinality constraints for list length are correctly applied to
    the generated pydantic model, from plaintext schema.
    """
    unit_test_schema = """
id: https://example.org/arrays
name: arrays-cardinality-example
title: Array Cardinality Example
description: |-
    Example LinkML schema to test array cardinality
license: MIT
default_prefix: example
imports:
    - linkml:types
classes:
    CardinalityArray:
        description: A class with arrays of different cardinality constraints
        attributes:
            minimum_cardinality_array:
                range: float
                multivalued: true
                required: true
                minimum_cardinality: 1
            maximum_cardinality_array:
                range: float
                multivalued: true
                maximum_cardinality: 10
            exact_cardinality_array:
                range: float
                multivalued: true
                exact_cardinality: 5
            min_max_cardinality_array:
                range: float
                multivalued: true
                minimum_cardinality: 0
                maximum_cardinality: 8
"""

    gen = PydanticGenerator(schema=unit_test_schema)
    code = gen.serialize()

    mod = compile_python(code)
    assert mod.CardinalityArray.model_fields["minimum_cardinality_array"].annotation == List[float]
    assert mod.CardinalityArray.model_fields["minimum_cardinality_array"].metadata[0].min_length == 1
    assert mod.CardinalityArray.model_fields["maximum_cardinality_array"].metadata[0].max_length == 10
    assert mod.CardinalityArray.model_fields["exact_cardinality_array"].metadata[0].min_length == 5
    assert mod.CardinalityArray.model_fields["exact_cardinality_array"].metadata[1].max_length == 5
    assert mod.CardinalityArray.model_fields["min_max_cardinality_array"].metadata[0].min_length == 0
    assert mod.CardinalityArray.model_fields["min_max_cardinality_array"].metadata[1].max_length == 8


@pytest.mark.skip("this format of arrays is not yet implemented in the metamodel??")
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


@pytest.mark.parametrize(
    "imports,expected",
    [
        (
            [
                Import(
                    module="typing",
                    objects=[ObjectImport(name="Dict"), ObjectImport(name="List"), ObjectImport(name="Union")],
                )
            ],
            (("Dict", Dict), ("List", List), ("Union", Union)),
        ),
        ([Import(module="typing")], (("typing", typing),)),
        (
            [
                Import(
                    module="types",
                    objects=[
                        ObjectImport(name="ModuleType", alias="RenamedA"),
                        ObjectImport(name="GeneratorType", alias="RenamedB"),
                    ],
                )
            ],
            (("RenamedA", ModuleType), ("RenamedB", GeneratorType)),
        ),
        ([Import(module="typing", alias="tp")], (("tp", typing),)),
    ],
)
def test_inject_imports(kitchen_sink_path, tmp_path, input_path, imports, expected):
    gen = PydanticGenerator(kitchen_sink_path, package=PACKAGE, imports=imports)
    code = gen.serialize()
    module = compile_python(code, PACKAGE)
    for condition in expected:
        assert hasattr(module, condition[0])
        assert getattr(module, condition[0]) is condition[1]


_StringClass = (
    """class MyInjectedClass:\n    field: str = 'field'\n    def __init__(self):\n        self.apple = 'banana'"""
)


@pytest.mark.parametrize(
    "inject,expected", ((MyInjectedClass, inspect.getsource(MyInjectedClass)), (_StringClass, _StringClass))
)
def test_inject_classes(kitchen_sink_path, tmp_path, input_path, inject, expected):
    gen = PydanticGenerator(
        kitchen_sink_path,
        package=PACKAGE,
        injected_classes=[inject],
    )
    code = gen.serialize()
    module = compile_python(code, PACKAGE)
    assert hasattr(module, "MyInjectedClass")
    # can't do inspect on the compiled module since it doesn't have a file
    assert expected in code


@pytest.mark.parametrize(
    "inject,name,type,default,description",
    (
        (
            'object_id: Optional[str] = Field(None, description="Unique UUID for each object")',
            "object_id",
            Optional[str],
            None,
            "Unique UUID for each object",
        ),
    ),
)
def test_inject_field(kitchen_sink_path, tmp_path, input_path, inject, name, type, default, description):
    gen = PydanticGenerator(kitchen_sink_path, package=PACKAGE, injected_fields=[inject])
    code = gen.serialize()
    module = compile_python(code, PACKAGE)

    base = getattr(module, "ConfiguredBaseModel")

    assert name in base.model_fields
    field = base.model_fields[name]
    assert field.annotation == type
    assert field.default == default
    assert field.description == description


# --------------------------------------------------
# pydanticgen template module tests
# --------------------------------------------------


@pytest.fixture
def sample_class() -> PydanticClass:
    # no pattern makes no validators
    attr_1 = PydanticAttribute(name="attr_1", range="Union[str,int]", required=True)
    attr_2 = PydanticAttribute(name="attr_2", range="List[float]")
    cls = PydanticClass(name="Sample", attributes={"attr_1": attr_1, "attr_2": attr_2})
    return cls


def test_attribute_field():
    """
    PydanticAttribute field should be able to autocompute ``field``
    """
    attr = PydanticAttribute(name="attr")
    assert attr.model_dump()["field"] == "None"

    predefined = "List[Union[str,int]]"
    attr = PydanticAttribute(name="attr", predefined=predefined)
    assert attr.model_dump()["field"] == predefined

    for item in ("required", "identifier", "key"):
        attr = PydanticAttribute(name="attr", **{item: True})
        assert attr.model_dump()["field"] == "..."


def test_class_validators():
    """
    PydanticClass should create validators from attributes that have `patterns`
    """
    # no attributes means no attributes!
    no_attrs = PydanticClass(name="no_attrs")
    assert no_attrs.validators is None

    # no pattern makes no validators
    no_validator = PydanticAttribute(name="no_validator", annotations={"python_range": {"value": "str"}})
    no_valid_class = PydanticClass(name="no_validator_class", attributes={"no_validator": no_validator})
    assert not no_valid_class.validators

    # a pattern makes a validator!
    validator = PydanticAttribute(
        name="validator", annotations={"python_range": {"value": "str"}}, pattern="word.*other"
    )
    valid_class = PydanticClass(name="valid_class", attributes={"validator": validator})
    assert valid_class.validators["validator"] == PydanticValidator(**validator.model_dump())

    # Adding a validator after object instantiation should still result in a generated validator
    no_valid_class.attributes["validator"] = validator
    assert "def pattern_validator" in no_valid_class.render()


def test_import_merge():
    import_a = Import(module="module_a")
    import_b = Import(module="module_b")
    import_cond_a = ConditionalImport(module="module_a", condition="1 == 1", alternative=Import(module="module_b"))
    import_cond_b = ConditionalImport(module="module_a", condition="2 == 2", alternative=Import(module="module_c"))
    import_a_alias = Import(module="module_a", alias="alias_a")
    import_a_objects = Import(module="module_a", objects=[ObjectImport(name="object_1"), ObjectImport(name="object_2")])
    import_a_objects_2 = Import(module="module_a", objects=[ObjectImport(name="object_3")])
    import_a_objects_combined = Import(
        module="module_a",
        objects=[ObjectImport(name="object_1"), ObjectImport(name="object_2"), ObjectImport(name="object_3")],
    )
    import_a_objects_alias = Import(module="module_a", objects=[ObjectImport(name="object_2", alias="alias_2")])

    # orthogonal merges just return both
    assert import_a.merge(import_b) == [import_a, import_b]

    # adding conditionals or mixed conditionals returns both
    assert import_cond_a.merge(import_cond_b) == [import_cond_a, import_cond_b]
    assert import_a.merge(import_cond_a) == [import_a, import_cond_a]

    # merging an alias returns the other if it updates the alias
    assert import_a.merge(import_a_alias) == [import_a_alias]

    # merging module and objects keeps both
    assert import_a.merge(import_a_objects) == [import_a, import_a_objects]

    # merging orthogonal objects adds
    assert import_a_objects.merge(import_a_objects_2) == [import_a_objects_combined]

    # merging objects with aliases updates to the new alias
    alias_merged = import_a_objects.merge(import_a_objects_alias)
    assert len(alias_merged) == 1
    assert len(alias_merged[0].objects) == 2
    assert alias_merged[0].objects[0].name == "object_1"
    assert alias_merged[0].objects[0].alias is None
    assert alias_merged[0].objects[1].name == "object_2"
    assert alias_merged[0].objects[1].alias == "alias_2"


def test_imports_add():
    """
    Only tests additional functionality different than :meth:`.Import.merge`
    """
    import_a = Import(module="module_a")
    import_b = Import(module="module_b")
    import_cond_a = ConditionalImport(module="module_a", condition="1 == 1", alternative=Import(module="module_b"))
    import_cond_b = ConditionalImport(module="module_a", condition="2 == 2", alternative=Import(module="module_c"))

    imports = Imports(render_sorted=False) + import_a

    imports_1 = imports + import_b
    assert len(imports_1) == len(imports) + 1
    assert imports_1[1] == import_b

    # dedupe here too
    imports_2 = imports_1 + import_b
    assert len(imports_2) == len(imports_1)

    imports_3 = imports_2 + import_cond_a
    imports_4 = imports_3 + import_cond_b
    assert len(imports_4) == len(imports_3) + 1
    assert imports_4[-1] == import_cond_b

    # adding to the end means removing from the front
    imports_5 = imports_4 + import_a
    assert len(imports_5) == len(imports_4)
    assert imports_5[-1] == import_a
    assert imports_5[0] != import_a
    rendered = imports_5.render()
    assert (
        rendered
        == """import module_b
if 1 == 1:
    import module_a
else:
    import module_b

if 2 == 2:
    import module_a
else:
    import module_c

import module_a
"""
    )


def test_imports_dunder():
    """
    The dunder methods in Imports should do what they're supposed to
    """
    import_a = Import(module="module_a")
    import_b = Import(module="module_b")
    imports = Imports() + import_a + import_b

    assert len(imports) == 2
    assert [i for i in imports] == [import_a, import_b]
    assert imports[1] == import_b


def test_imports_future():
    """
    __future__ imports should always be imported first
    """
    import_a = Import(module="module_a")
    import_b = Import(module="module_b")
    import_c = ConditionalImport(
        module="module_c",
        alias="module_c_alias",
        objects=[ObjectImport(name="module_c_obj")],
        condition="1 == 1",
        alternative=Import(module="module_d", objects=[ObjectImport(name="module_d_obj", alias="module_c_obj")]),
    )
    future = Import(module="__future__", objects=[ObjectImport(name="annotations")])

    imports = Imports() + import_a + import_b + import_c + future
    assert imports.imports[0] == future
    assert not any([i.module == "__future__" for i in imports.imports[1:]])
    # the rest of the order should be unchanged
    assert imports.imports[1] == import_a
    assert imports.imports[2] == import_b
    assert imports.imports[3] == import_c

    # this should also work if we add two imports objects together - they should be merged down to one statement
    # we DONT currently handle merging when `Imports` is instantiated, it's intended to be used iteratively
    # but when we add two imports together, the first should iterate over the second term
    future_2 = Import(module="__future__", objects=[ObjectImport(name="unicode_literals")])
    future_3 = Import(module="__future__", objects=[ObjectImport(name="generator_stop")])
    imports_2 = Imports(imports=[future_2, future_3])
    # Declaring as a list should merge
    assert imports_2.imports == [
        Import(
            module="__future__", objects=[ObjectImport(name="unicode_literals"), ObjectImport(name="generator_stop")]
        )
    ]

    imports += imports_2
    # now we should have merged and collapsed the future imports to a single expression at the top
    assert imports.imports[0].module == "__future__"
    assert imports.imports[0].objects == [
        ObjectImport(name="annotations"),
        ObjectImport(name="unicode_literals"),
        ObjectImport(name="generator_stop"),
    ]
    assert not any([i.module == "__future__" for i in imports.imports[1:]])


def test_imports_getitem():
    """
    Can get an import from Imports with an integer index or the name of a module
    """
    import_a = Import(module="module_a.submodule")
    import_b = Import(module="module_b")
    import_a_objects = Import(module="module_a", objects=[ObjectImport(name="object_1"), ObjectImport(name="object_2")])
    imports = Imports(imports=[import_a, import_b, import_a_objects])

    assert imports[1] == import_b
    with pytest.raises(IndexError):
        _ = imports[3]

    assert imports["module_a.submodule"] == import_a
    with pytest.raises(KeyError):
        _ = imports["fake_module"]

    with pytest.raises(TypeError):
        _ = imports[(1, 2)]


def test_imports_contains():
    """
    Can test whetheran Imports contains another Import or Imports
    """
    import_a = Import(module="module_a.submodule")
    import_b = Import(module="module_b")
    import_c = Import(module="module_c", alias="WhackyNamedModule")
    import_a_objects = Import(
        module="module_a",
        objects=[ObjectImport(name="object_1"), ObjectImport(name="object_2"), ObjectImport(name="object_3")],
    )
    import_d_objects = Import(module="module_d", objects=[ObjectImport(name="object_1", alias="WhackyObjectName")])
    all_imports = [import_a, import_b, import_c, import_a_objects, import_d_objects]
    imports = Imports(imports=all_imports)

    # everything we added should be in there
    for an_import in all_imports:
        assert an_import in imports

    # a subset of objects
    import_a_subset = Import(module="module_a", objects=[ObjectImport(name="object_1"), ObjectImport(name="object_3")])
    assert import_a_subset in imports

    # Imports and lists of imports succeed too
    sub_imports = [import_a, import_d_objects]
    sub_imports_subset = [import_b, import_a_subset]
    assert sub_imports in imports
    assert sub_imports_subset in imports
    assert Imports(imports=sub_imports) in imports
    assert Imports(imports=sub_imports_subset) in imports

    # failures ------
    # Alias mismatches fail
    assert Import(module="module_c") not in imports
    assert Import(module="module_d", alias="WhackyNamedModule") not in imports
    assert Import(module="module_d", alias="WhackyObjectName") not in imports
    assert Import(module="module_d", objects=[ObjectImport(name="object_1")]) not in imports
    assert Import(module="module_d", objects=[ObjectImport(name="object_2", alias="WhackyObjectName")]) not in imports
    assert Import(module="module_a", objects=[ObjectImport(name="object_1", alias="WhackyObjectName")]) not in imports

    # supersets fail
    superset_a = Import(
        module="module_a",
        objects=[
            ObjectImport(name="object_1"),
            ObjectImport(name="object_2"),
            ObjectImport(name="object_3"),
            ObjectImport(name="object_4"),
        ],
    )
    assert superset_a not in imports
    assert [import_a, superset_a] not in imports
    assert Imports(imports=[import_a, superset_a]) not in imports
    import_e = Import(module="module_e")
    assert import_e not in imports
    module_superset = [import_e, import_b]
    assert module_superset not in imports
    assert Imports(imports=module_superset) not in imports

    # module/class import mismatches fail
    assert Import(module="module_a") not in imports

    with pytest.raises(TypeError):
        _ = "a string!?!?" in imports


def test_import_sort():
    """
    Import.sort should sort its objects alphabetically and according to capitalization
    """
    an_import = Import(
        module="module_a",
        objects=[
            ObjectImport(name="A"),
            ObjectImport(name="C"),
            ObjectImport(name="a"),
            ObjectImport(name="B", alias="Z"),
        ],
    )

    an_import.sort()
    obj_names = [o.name for o in an_import.objects]
    assert obj_names == ["A", "B", "C", "a"]


@pytest.mark.parametrize(
    "module,group",
    (
        ("__future__", "future"),
        ("typing", "stdlib"),
        ("numpy", "thirdparty"),
        (".mymodule", "local"),
    ),
)
def test_import_group(module, group):
    """Import.group should correctly identify import group"""
    assert Import(module=module).group == group


def test_imports_sort():
    """
    Imports.sort should sort like isort
    """
    imports = Imports(
        imports=[
            # ConditionalImports come last
            ConditionalImport(module="aaa", condition="True", alternative=Import(module="bbb")),
            # local modules come after thirdparty
            Import(module=".mymodule"),
            # thirdparty come after stdlib
            Import(module="numpy"),
            # __future__ always comes first
            Import(module="__future__", objects=[ObjectImport(name="print")]),
            Import(module="typing", objects=[ObjectImport(name="List")]),
            # objects should be sorted within an Import
            Import(module="datetime", objects=[ObjectImport(name="time"), ObjectImport(name="datetime")]),
            # imports without objects come first within a group
            Import(module="sys"),
            Import(module="enum"),
        ]
    )
    imports.sort()
    module_order = [i.module for i in imports.imports]
    assert module_order == ["__future__", "enum", "sys", "datetime", "typing", "numpy", ".mymodule", "aaa"]
    assert [o.name for o in imports["datetime"].objects] == ["datetime", "time"]


def test_imports_groups_rendering(kitchen_sink_path):
    """
    When rendering, python import groups should be rendered by newline-delimited groups
    """
    gen = PydanticGenerator(
        kitchen_sink_path, imports=[Import(module=".mymodule"), Import(module="numpy")], sort_imports=True
    )
    rendered = gen.render()
    rendered_imports = rendered.python_imports.render()
    # yes line break between builtins and thirdparty
    assert re.search(r"\)\n\nimport numpy", rendered_imports)
    # no line break between builtins
    assert re.search("import re\nimport sys", rendered_imports)


def test_template_models_templates():
    """
    All template models should have templates!
    """
    for model in PydanticTemplateModel.__subclasses__():
        assert hasattr(model, "template")
        assert isinstance(model.template, str)
        env = model.environment()
        template = env.get_template(model.template)
        assert isinstance(template, Template)


def test_default_environment():
    """
    Check that the default environment has the configuration for our templates
    """
    env = PydanticTemplateModel.environment()
    assert env.trim_blocks
    assert env.lstrip_blocks


def test_template_pass_environment(sample_class):
    """
    It should be possible to override default templates by passing an environment
    """
    templates = {
        "class.py.jinja": """{{ name }}
{%- for attr in attributes.values() %}
{{ attr }}
{%- endfor -%}""",
        "attribute.py.jinja": """attr: {{ name }}
range: {{ range }}""",
    }
    env = Environment(loader=DictLoader(templates))
    rendered = sample_class.render(env)
    assert (
        rendered
        == """Sample
attr: attr_1
range: Union[str,int]
attr: attr_2
range: List[float]"""
    )


def test_template_render():
    """
    Template should recursively render templatemodels to strings, preserving
    their structure as lists or dicts
    """

    class PlainModel(BaseModel):
        plain_field: str = "plain_field"
        second: int = 1

    class InnerTemplate(PydanticTemplateModel):
        template: ClassVar[str] = "inner.jinja"
        value: Union[int, str] = 1

    class TestTemplate(PydanticTemplateModel):
        template: ClassVar[str] = "test.jinja"
        a_list: List[InnerTemplate] = [InnerTemplate(value=1), InnerTemplate(value=2)]
        a_dict: Dict[str, InnerTemplate] = {"one": InnerTemplate(value="one"), "two": InnerTemplate(value="two")}
        a_value: int = 1
        plain_model: PlainModel = PlainModel()
        recursive: Optional["TestTemplate"] = None

    templates = {
        "inner.jinja": """inner_value: {{ value }}""",
        "test.jinja": """a_list: {{ a_list }}
a_dict: {{ a_dict }}
a_value: {{ a_value }}
plain_model: {{ plain_model }}
recursive:
{{ recursive }}""",
    }
    env = Environment(loader=DictLoader(templates))

    inner = TestTemplate()
    test = TestTemplate(recursive=inner)
    rendered = test.render(env)
    assert (
        rendered
        == """a_list: ['inner_value: 1', 'inner_value: 2']
a_dict: {'one': 'inner_value: one', 'two': 'inner_value: two'}
a_value: 1
plain_model: {'plain_field': 'plain_field', 'second': 1}
recursive:
a_list: ['inner_value: 1', 'inner_value: 2']
a_dict: {'one': 'inner_value: one', 'two': 'inner_value: two'}
a_value: 1
plain_model: {'plain_field': 'plain_field', 'second': 1}
recursive:
None"""
    )


# --------------------------------------------------
# Pydanticgen arrays generators and objects
# --------------------------------------------------


def test_arrays_anyshape():
    """
    Test anyshape class itself
    """

    class MyModel(BaseModel):
        array: AnyShapeArray[int]

    arr = np.ones((2, 4, 5, 3, 2), dtype=int)
    _ = MyModel(array=arr.tolist())

    with pytest.raises(ValidationError):
        arr = np.random.random((2, 5, 3))
        _ = MyModel(array=arr.tolist())


# --------------------------------------------------
# Test array generation from schema
# --------------------------------------------------


@pytest.fixture(scope="module")
def array_anyshape(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "any_shape.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_bounded(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "bounded_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_parameterized(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "parameterized_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_complex(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "complex_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_error_complex_dimensions(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "error_complex_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_error_complex_unbounded(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "error_complex_unbounded.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_validator_errors(input_path) -> ClassDefinition:
    schema_file = str(Path(input_path("arrays")) / "validator_errors.yaml")
    schema = load_schema_wrap(schema_file)
    return schema.classes["ErrorRiddenClass"]


@dataclass
class TestCase:
    __test__ = False
    type: Literal["pass", "fail"]
    array: np.ndarray

    @property
    def expectation(self):
        if self.type == "pass":
            return does_not_raise()
        else:
            return pytest.raises(ValidationError)


@pytest.mark.parametrize(
    "case",
    [TestCase(type="pass", array=np.zeros((3, 4, 5, 6), dtype=dt)) for dt in (int, float, str)]
    + [TestCase(type="fail", array=a) for a in (4, 3.0, "three")],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_anyshape(case, representation, array_anyshape):
    """
    Any array shape, any dtype!
    """
    if ArrayRepresentation.LIST in representation and isinstance(case.array, np.ndarray):
        case.array = case.array.tolist()
    if ArrayRepresentation.NUMPYDANTIC in representation and case.type == "fail":
        pytest.skip("numpydantic coerces scalars rather than failing validation")

    generated = PydanticGenerator(array_anyshape, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "AnyType")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 3, 4), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 3, 4), dtype=float)),
        TestCase(type="fail", array=np.zeros((2, 3, 4), dtype=str)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_anyshape_typed(case, representation, array_anyshape):
    """
    Same as above, except dtype mismatches should cause a failure
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_anyshape, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "Typed")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 3, 4), dtype=int)),
        TestCase(type="pass", array=np.zeros((6, 3, 1, 4), dtype=int)),
        TestCase(type="pass", array=np.zeros((2, 3), dtype=int)),
        TestCase(type="fail", array=np.zeros((2,), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 3, 4), dtype=str)),
        TestCase(type="fail", array=np.zeros((2,), dtype=str)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_bounded_min(case, representation, array_bounded):
    """
    Any integer array with greater than 2 dimensions.
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_bounded, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "MinDimensions")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 3, 4), dtype=int)),
        TestCase(type="pass", array=np.zeros((2, 6, 7, 2, 3), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 6, 7, 2, 3, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 3, 4), dtype=str)),
        TestCase(type="fail", array=np.zeros((2, 6, 7, 2, 3, 6), dtype=str)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_bounded_max(case, representation, array_bounded):
    """
    Any integer array with less or equal dimensions than 5
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_bounded, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "MaxDimensions")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 3, 4), dtype=int)),
        TestCase(type="pass", array=np.zeros((6, 3, 1, 4), dtype=int)),
        TestCase(type="pass", array=np.zeros((2, 3), dtype=int)),
        TestCase(type="fail", array=np.zeros((2,), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 3, 4), dtype=str)),
        TestCase(type="fail", array=np.zeros((2,), dtype=str)),
        TestCase(type="pass", array=np.zeros((2, 6, 7, 2, 3), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 6, 7, 2, 3, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 6, 7, 2, 3, 6), dtype=str)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_bounded_range(case, representation, array_bounded):
    """
    Any integer array equal to or between 2 and 5 dimensions
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_bounded, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "RangeDimensions")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 3, 4), dtype=int)),
        TestCase(type="pass", array=np.zeros((6, 3, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 3, 4), dtype=str)),
        TestCase(type="fail", array=np.zeros((2, 3), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 3, 4, 5), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 2), dtype=str)),
        TestCase(type="fail", array=np.zeros((2, 3, 4, 5), dtype=str)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_bounded_exact(case, representation, array_bounded):
    """
    Any integer array with exactly 3 dimensions
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_bounded, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ExactDimensions")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 5, 4, 6), dtype=int)),
        TestCase(type="pass", array=np.zeros((3, 5, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((1, 5, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((6, 5, 4), dtype=int)),
        TestCase(type="fail", array=np.zeros((6, 5, 4, 6, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((3, 5, 4, 6), dtype=str)),
        # FIXME: Add a float testcase back in here when https://github.com/linkml/linkml/issues/1955 is resolved
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_parameterized_min(case, representation, array_parameterized):
    """
    Any 4 dimensional integer array, the first dimension is equal to or greater than cardinality 2
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_parameterized, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ParameterizedArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 5, 4, 6), dtype=int)),
        TestCase(type="pass", array=np.zeros((2, 4, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 6, 4, 6), dtype=int)),
        # this is the same field, so dtype failures only need to be tested in one case
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_parameterized_max(case, representation, array_parameterized):
    """
    Any 4 dimensional integer array, the second dimension is equal to or less than cardinality 5
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_parameterized, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ParameterizedArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 5, 2, 6), dtype=int)),
        TestCase(type="pass", array=np.zeros((2, 5, 5, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 5, 1, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 5, 6, 6), dtype=int)),
        # this is the same field, so dtype failures only need to be tested in one case
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_parameterized_range(case, representation, array_parameterized):
    """
    Any 4 dimensional integer array, the third dimension has a cardinality between 2 and 5, inclusive
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_parameterized, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ParameterizedArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((2, 5, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 5, 4, 4), dtype=int)),
        TestCase(type="fail", array=np.zeros((2, 5, 4, 7), dtype=int)),
        # this is the same field, so dtype failures only need to be tested in one case
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_parameterized_exact(case, representation, array_parameterized):
    """
    Any 4 dimensional integer array, the fourch dimension has a cardinality of exactly 6
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_parameterized, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ParameterizedArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 7, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((6, 2, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 1, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 1, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 6, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 5), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 7), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6), dtype=str)),
        TestCase(type="fail", array=np.zeros((5, 2, 4), dtype=int)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_complex_any(case, representation, array_complex):
    """
    An array with at least four dimensions,
    - the first of which has a maximum cardinality of 5, and
    - the second of which has a minimum cardinality of 2
    - the third of which has a cardinality between 2 and 5, inclusive, and
    - the fourth of which has an exact cardinality of 6
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_complex, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ComplexAnyShapeArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 7, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6, 7, 1, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((6, 2, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 1, 4, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 1, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 6, 6), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 5), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 7), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6), dtype=str)),
        TestCase(type="fail", array=np.zeros((5, 2, 4), dtype=int)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_complex_max(case, representation, array_complex):
    """
    An array with at most, or equal to 6 dimensions,
    - the first of which has a maximum cardinality of 5, and
    - the second of which has a minimum cardinality of 2
    - the third of which has a cardinality between 2 and 5, inclusive, and
    - the fourth of which has an exact cardinality of 6
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_complex, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ComplexMaxShapeArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 7), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 7, 1, 1), dtype=int)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_complex_min(case, representation, array_complex):
    """
    An array with at least 5 dimensions (with the rest of the usual requirements for complex shape test)
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_complex, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ComplexMinShapeArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 1), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 1, 1), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 1, 1, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6, 1, 1, 1, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((6, 2, 4, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 1, 4, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 1, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 6, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 5, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 7, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6, 1), dtype=str)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_complex_range(case, representation, array_complex):
    """
    An array with between 5 and 7 dimensions, inclusive,
    - the first of which has a maximum cardinality of 5, and
    - the second of which has a minimum cardinality of 2
    - the third of which has a cardinality between 2 and 5, inclusive, and
    - the fourth of which has an exact cardinality of 6
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_complex, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ComplexRangeShapeArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "case",
    [
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6, 1), dtype=int)),
        TestCase(type="pass", array=np.zeros((5, 2, 4, 6, 1, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6, 1, 1, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((6, 2, 4, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 1, 4, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 1, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 6, 6, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 5, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 7, 1), dtype=int)),
        TestCase(type="fail", array=np.zeros((5, 2, 4, 6, 1), dtype=str)),
    ],
)
@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_complex_exact(case, representation, array_complex):
    """
    An array with exactly 6 dimensions,
    - the first of which has a maximum cardinality of 5, and
    - the second of which has a minimum cardinality of 2
    - the third of which has a cardinality between 2 and 5, inclusive, and
    - the fourth of which has an exact cardinality of 6
    """
    if ArrayRepresentation.LIST in representation:
        case.array = case.array.tolist()

    generated = PydanticGenerator(array_complex, array_representations=representation).serialize()
    mod = compile_python(generated)
    cls = getattr(mod, "ComplexExactShapeArray")
    with case.expectation:
        cls(array=case.array)


@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_bounded_implicit_exact(representation, array_bounded):
    """
    The representation of an bounded array with min and max dimensions that are equal should be the same as
    setting an exact dimensionality.
    """

    generated = PydanticGenerator(array_bounded, array_representations=representation, metadata_mode=None).render()
    explicit = generated.classes["ExactDimensions"].attributes["array"]
    implicit = generated.classes["ImplicitExact"].attributes["array"]
    assert explicit.render() == implicit.render()


@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_complex_implicit_exact(representation, array_complex):
    """
    The representation of an complex array with min and max dimensions that are equal should be the same as
    setting an exact dimensionality.
    """

    generated = PydanticGenerator(array_complex, array_representations=representation, metadata_mode=None).render()
    explicit = generated.classes["ComplexExactShapeArray"].attributes["array"]
    implicit = generated.classes["ComplexImplicitExactShapeArray"].attributes["array"]
    assert explicit.render() == implicit.render()


@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_complex_noop_exact(representation, array_complex, array_parameterized):
    """
    When the exact number of dimensions is equal to the number of parameterized dimensions,
    the representation should be equivalent to if it hadn't been specified
    """

    generated_complex = PydanticGenerator(
        array_complex, array_representations=representation, metadata_mode=None
    ).render()
    generated_parameterized = PydanticGenerator(
        array_parameterized, array_representations=representation, metadata_mode=None
    ).render()
    complex = generated_complex.classes["ComplexNoOpExactShapeArray"].attributes["array"]
    parameterized = generated_parameterized.classes["ParameterizedArray"].attributes["array"]
    assert complex.render() == parameterized.render()


@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_error_complex_exact_shape(representation, array_error_complex_dimensions):
    """
    When we try and make a complex array where the exact number of dimensions are lower than the parameterized
    dimensions, we should throw an error
    """

    with pytest.raises(ValueError, match=".*must be greater than the parameterized dimensions.*"):
        _ = PydanticGenerator(array_error_complex_dimensions, array_representations=representation).serialize()


@pytest.mark.parametrize(
    "representation",
    [[ArrayRepresentation.LIST], pytest.param([ArrayRepresentation.NUMPYDANTIC], marks=pytest.mark.pydantic_npd)],
)
def test_generate_array_error_complex_unbounded_shape(representation, array_error_complex_unbounded):
    """
    When we specify a minimum number of dimensions without a max (or setting max to False) in a complex array,
    we should throw an error - min without a max is undefined behavior, to set unbounded we need the max to be
    explicitly false.
    """

    with pytest.raises(ValueError, match=".*Cannot specify a minimum_number_dimensions while maximum is None.*"):
        _ = PydanticGenerator(array_error_complex_unbounded, array_representations=representation).serialize()


@pytest.mark.parametrize(
    "method",
    [
        "array_exact_dimensions",
        "array_consistent_n_dimensions",
        "array_dimensions_ordinal",
        "array_explicitly_unbounded",
    ],
)
def test_array_validator(method, array_validator_errors):
    """Array-level validator method testing for ArrayValidator"""
    array_expr = array_validator_errors.attributes[method].array

    # global validation should always error
    with pytest.raises(ArrayValidationError):
        ArrayValidator.validate(array_expr)

    # should have a matching method, which should be the one that specifically raises
    assert hasattr(ArrayValidator, method)

    # it should be static, so we can just call it independently
    with pytest.raises(ArrayValidationError):
        getattr(ArrayValidator, method)(array_expr)


@pytest.mark.parametrize("method", ["dimension_exact_cardinality", "dimension_ordinal"])
def test_dimension_validator(method, array_validator_errors):
    """Dimension-level validator method testing for ArrayValidator"""
    dimension_array_expr = array_validator_errors.attributes["dimension_errors"].array

    with pytest.raises(ArrayValidationError):
        ArrayValidator.validate(dimension_array_expr)

    dimension = [d for d in dimension_array_expr.dimensions if d.alias == method][0]
    with pytest.raises(ArrayValidationError):
        getattr(ArrayValidator, method)(dimension)


# --------------------------------------------------
# Black formatting
# --------------------------------------------------


def _has_black() -> bool:
    return find_spec("black") is not None


@pytest.mark.xfail(not _has_black(), reason="black is not installed!")
def test_template_black(array_complex):
    """
    When black is installed, we should format template models with black :)
    """
    generated = PydanticGenerator(
        array_complex, array_representations=[ArrayRepresentation.LIST], metadata_mode=None
    ).render()
    array_repr = generated.classes["ComplexRangeShapeArray"].attributes["array"].render(black=True)
    assert (
        array_repr
        == """array: Optional[
    conlist(
        max_length=5,
        item_type=conlist(
            min_length=2,
            item_type=conlist(
                min_length=2,
                max_length=5,
                item_type=conlist(
                    min_length=6, max_length=6, item_type=Union[List[int], List[List[int]], List[List[List[int]]]]
                ),
            ),
        ),
    )
] = Field(None)
"""
    )


def test_template_noblack(array_complex, mock_black_import):
    """
    When we don't have black, we should still be able to render templates normally

    .. note::

        keep this test last in the module because it messed up the objects we have imported previously :)

    """

    # ensure our mock worked
    with pytest.raises(ImportError):
        import black  # noqa F401

    importlib.reload(template)
    importlib.reload(build)
    importlib.reload(array)
    importlib.reload(pydanticgen)
    importlib.reload(pydanticgen_root)
    from linkml.generators.pydanticgen import PydanticGenerator
    from linkml.generators.pydanticgen.array import ArrayRepresentation

    generated = PydanticGenerator(
        array_complex, array_representations=[ArrayRepresentation.LIST], metadata_mode=None
    ).render()
    array_repr = generated.classes["ComplexRangeShapeArray"].attributes["array"].render(black=False)

    assert (
        array_repr
        == "array: Optional[conlist(max_length=5, item_type=conlist(min_length=2, item_type=conlist(min_length=2, max_length=5, item_type=conlist(min_length=6, max_length=6, item_type=Union[List[int], List[List[int]], List[List[List[int]]]]))))] = Field(None)"  # noqa: E501
    )

    # trying to render with black when we don't have it should raise a ValueError
    with pytest.raises(ValueError):
        _ = generated.classes["ComplexRangeShapeArray"].attributes["array"].render(black=True)


# --------------------------------------------------
# Metadata inclusion
# --------------------------------------------------


def _test_meta(linkml_meta, definition: Definition, model: Type[PydanticTemplateModel], mode: str):
    def_clean = remove_empty_items(definition)
    for k, v in def_clean.items():
        if mode == "auto":
            if k in model.exclude_from_meta():
                assert k not in linkml_meta
            else:
                assert k in linkml_meta
        elif mode == "full":
            assert k in linkml_meta
        elif mode == "except_children":
            # basically nothing that has a template model
            if k in ("slots", "classes", "enums", "attributes"):
                assert k not in linkml_meta
            else:
                assert k in linkml_meta
        elif mode == "None":
            assert linkml_meta is None or k not in linkml_meta
        else:
            raise ValueError(f"Don't know how to test this metadata mode: {mode}")


@pytest.mark.parametrize("mode", MetadataMode)
def test_linkml_meta(kitchen_sink_path, tmp_path, input_path, mode):
    """
    Pydanticgen can inject missing linkml metadata from schema definitions
    with several different modes :)
    """
    schema = SchemaView(kitchen_sink_path)

    gen = PydanticGenerator(kitchen_sink_path, package=PACKAGE, metadata_mode=mode)
    code = gen.serialize()
    module = compile_python(code, PACKAGE)
    _test_meta(module.linkml_meta, schema.schema, PydanticModule, mode)

    for cls_name, cls_def in schema.all_classes().items():
        if cls_def["class_uri"] == "linkml:Any":
            continue
        cls = getattr(module, camelcase(cls_name))  # type: Type[BaseModel]
        if mode == MetadataMode.NONE:
            assert not hasattr(cls, "linkml_meta")
        else:
            _test_meta(cls.linkml_meta, cls_def, PydanticClass, mode)

        for slot_def in schema.class_induced_slots(cls_name):
            extra = cls.model_fields[underscore(slot_def.name)].json_schema_extra
            if mode == MetadataMode.NONE:
                assert extra is None or "linkml_meta" not in extra
            else:
                _test_meta(extra["linkml_meta"], slot_def, PydanticAttribute, mode)


# --------------------------------------------------
# Split generation
# --------------------------------------------------


@pytest.mark.pydanticgen_split
def test_generate_split(input_path):
    """
    Schemas can be generated such that they import from imported schemas in different modules rather than
    having all models present in a single module
    """
    schema = input_path("split/main.yaml")
    generator = PydanticGenerator(schema, split=True)
    rendered = generator.render()
    imports = Imports(imports=rendered.python_imports)

    should_have = [
        Import(
            module=".schema_1",
            objects=[ObjectImport(name="S1"), ObjectImport(name="S1Any"), ObjectImport(name="S1Mixin")],
        ),
        Import(module=".schema_2", objects=[ObjectImport(name="S2"), ObjectImport(name="S2Any")]),
    ]
    shouldnt_have = [
        Import(module=".schema_3"),
        Import(module=".schema_3", objects=[ObjectImport(name="S3")]),
        Import(module=".schema_1", objects=[ObjectImport(name="S1Unused")]),
        Import(module=".schema_2", objects=[ObjectImport(name="S2Unused")]),
    ]

    for an_import in should_have:
        assert an_import in imports
    for an_import in shouldnt_have:
        assert an_import not in imports

    # imported classes should not be defined
    # (we do string tests here bc we can't import/execute this module since its imports
    # won't be present)
    for cls_name in ("S1", "S1Any", "S2", "S2Any"):
        assert cls_name not in rendered.classes

    # inheritance should be respected
    assert "S1" in rendered.classes["S1Inheritance"].bases
    assert "S1Mixin" in rendered.classes["S1HasMixin"].bases


@pytest.mark.pydanticgen_split
def test_generate_split_full(input_path):
    """
    When the split mode is full, we should get all imports regardless of whether or not
    they are used.

    Basic functionality is tested above, so this just checks for the presence of the
    unused classes
    """
    schema = input_path("split/main.yaml")
    generator = PydanticGenerator(schema, split=True, split_mode=pydanticgen.SplitMode.FULL)
    rendered = generator.render()
    imports = Imports(imports=rendered.python_imports)

    # all imported modules should be present
    should_have = [
        Import(
            module=".schema_1",
            objects=[
                ObjectImport(name="S1"),
                ObjectImport(name="S1Any"),
                ObjectImport(name="S1Mixin"),
                ObjectImport(name="S1Unused"),
            ],
        ),
        Import(
            module=".schema_2",
            objects=[ObjectImport(name="S2"), ObjectImport(name="S2Any"), ObjectImport(name="S2Unused")],
        ),
        Import(module=".schema_3", objects=[ObjectImport(name="S3")]),
    ]
    for an_import in should_have:
        assert an_import in imports

    # All imported modules and classes should not be generated
    for cls_name in (
        "S1",
        "S1Any",
        "S1Unused",
        "S1Mixin",
        "S2",
        "S2Any",
        "S2Unused",
        "S3",
    ):
        assert cls_name not in rendered.classes


@pytest.mark.pydanticgen_split
def test_generate_split_pattern(input_path):
    """
    I can customize the module part of the import to use attributes from the imported schema
    """
    context_val = {"context_val": "A_CONTEXT_VALUE"}
    custom_pattern = "...{{ schema.name }}.{{ schema.annotations.custom.value }}.{{ context_val }}"
    schema = input_path("split/main.yaml")
    generator = PydanticGenerator(schema, split=True, split_pattern=custom_pattern, split_context=context_val)
    rendered = generator.render()
    imports = Imports(imports=rendered.python_imports)

    should_have = [
        Import(
            module="...schema_1.additional_metadata.a_context_value",
            objects=[
                ObjectImport(name="S1"),
                ObjectImport(name="S1Any"),
                ObjectImport(name="S1Mixin"),
            ],
        ),
        Import(
            module="...schema_2.different_metadata.a_context_value",
            objects=[ObjectImport(name="S2"), ObjectImport(name="S2Any")],
        ),
    ]
    shouldnt_have = [
        Import(module=".schema_3"),
        Import(module=".schema_3", objects=[ObjectImport(name="S3")]),
        Import(module=".schema_1", objects=[ObjectImport(name="S1Unused")]),
        Import(module=".schema_2", objects=[ObjectImport(name="S2Unused")]),
        Import(
            module=".schema_1",
            objects=[ObjectImport(name="S1"), ObjectImport(name="S1Any"), ObjectImport(name="S1Mixin")],
        ),
        Import(module=".schema_2", objects=[ObjectImport(name="S2"), ObjectImport(name="S2Any")]),
    ]

    for an_import in should_have:
        assert an_import in imports, "Missed a necessary import when generating from a pattern"
    for an_import in shouldnt_have:
        assert an_import not in imports, (
            "Got one of the imports with the default template " "instead of the supplied pattern"
        )


@pytest.mark.pydanticgen_split
def test_generate_split_directory(input_path, tmp_path):
    schema = input_path("split/main.yaml")
    pattern = "..{{ schema.version | replace('.', '_') }}.{{ schema.name }}"
    output_file = tmp_path / "test_module" / "v1_2_3" / "main.py"
    result = PydanticGenerator.generate_split(schema, output_file, split_pattern=pattern)

    # should be possible to import the main module
    # (this checks that relative imports resolve correctly!)
    main = [r for r in result if r.main][0]
    imported_spec = importlib.util.spec_from_file_location("test_module.v1_2_3.main", main.path)
    _ = importlib.util.module_from_spec(imported_spec)

    # all expected files should exist in the places we expect them to be
    pkg_path = tmp_path / "test_module"
    all_paths = [
        pkg_path / "__init__.py",
        pkg_path / "v0_1_2" / "__init__.py",
        pkg_path / "v0_1_2" / "schema_1.py",
        pkg_path / "v1_2_3" / "__init__.py",
        pkg_path / "v1_2_3" / "main.py",
        pkg_path / "v2_3_4" / "__init__.py",
        pkg_path / "v2_3_4" / "schema_2.py",
    ]
    for path in all_paths:
        assert path.exists()

    # we didn't generate __init__.py files outside the topmost common directory
    assert not (tmp_path / "__init__.py").exists()


@pytest.mark.parametrize(
    "test,expected", [("Schema 1", "schema_1"), ("SchemaOneTwo", "schema_one_two"), ("Schema! One", "schema__one")]
)
@pytest.mark.pydanticgen_split
def test_snake_case_regex(test, expected):
    assert re.sub(PydanticGenerator.SNAKE_CASE, "_", test).lower() == expected


# --------------------------------------------------
# Lifecycle methods
# --------------------------------------------------


def test_lifecycle_classes(kitchen_sink_path):
    """We can modify the generation process by subclassing lifecycle hooks"""

    class TestPydanticGenerator(PydanticGenerator):
        def before_generate_classes(self, cls: Iterable[ClassDefinition], sv: SchemaView) -> Iterable[ClassDefinition]:
            all_classes = sv.all_classes()
            assert len(cls) == len(all_classes) - 1

            for a_cls in cls:
                assert a_cls.name in all_classes

            # delete a class and make sure we don't get it in the output
            assert cls[0].name == "activity"
            del cls[0]
            return cls

        def after_generate_classes(self, cls: Iterable[TClass], sv: SchemaView) -> Iterable[TClass]:
            for a_cls in cls:
                a_cls.cls.attributes["test"] = PydanticAttribute(name="test", range="str")
            return cls

        def before_generate_class(self, cls: ClassDefinition, sv: SchemaView) -> ClassDefinition:
            # change all the descriptions, idk
            cls.description = "TEST MODIFYING CLASSES"
            return cls

        def after_generate_class(self, cls: TClass, sv: SchemaView) -> TClass:
            cls.imports = Imports(imports=[Import(module="csv")])
            return cls

    generator = TestPydanticGenerator(kitchen_sink_path)
    rendered = generator.render()
    assert "activity" not in rendered.classes
    for cls in rendered.classes.values():
        assert cls.description == "TEST MODIFYING CLASSES"
        assert "test" in cls.attributes
    assert "csv" in [i.module for i in rendered.python_imports]


def test_lifecycle_slots(kitchen_sink_path):
    """We can modify the generation process by subclassing lifecycle hooks"""

    class TestPydanticGenerator(PydanticGenerator):
        def before_generate_slots(self, slot: Iterable[SlotDefinition], sv: SchemaView) -> Iterable[SlotDefinition]:
            # make a new slot that's the number of slots for some reason
            slot.append(SlotDefinition(name="number_of_slots", range="integer", ifabsent=f"integer({len(slot)})"))
            return slot

        def after_generate_slots(self, slot: Iterable[TSlot], sv: SchemaView) -> Iterable[TSlot]:
            for a_slot in slot:
                a_slot.attribute.meta["extra_meta_field"] = True
            return slot

        def before_generate_slot(self, slot: SlotDefinition, sv: SchemaView) -> SlotDefinition:
            slot.description = "TEST MODIFYING SLOTS"
            return slot

        def after_generate_slot(self, slot: TSlot, sv: SchemaView) -> TSlot:
            # make em all required
            slot.attribute.required = True
            return slot

    generator = TestPydanticGenerator(kitchen_sink_path)
    rendered = generator.render()

    for cls in rendered.classes.values():
        assert "number_of_slots" in cls.attributes
        for attr in cls.attributes.values():
            assert attr.description == "TEST MODIFYING SLOTS"
            assert attr.required
            assert attr.meta["extra_meta_field"]


def test_crappy_stdlib_set_removed():
    """
    After support for <3.10 is dropped, remove the dang stdlib list stub

    since this is just a tidiness test rather than a correctness test,
    wrap the whole thing in a try and self-contain its imports
    """
    try:
        from importlib.metadata import metadata

        from packaging.specifiers import SpecifierSet
        from packaging.version import Version

        linkml_meta = metadata("linkml")
        req_python = SpecifierSet(linkml_meta.json["requires_python"])
        assert req_python.contains(
            Version("3.9")
        ), "REMOVE _some_stdlib_module_names from the bottom of pydanticgen/template.py, "
        "and then REMOVE THIS TEST!"
    except Exception:
        pass
