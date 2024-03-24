import inspect
import typing
from importlib.metadata import version
from types import GeneratorType, ModuleType
from typing import ClassVar, Dict, List, Optional, Union, get_args, get_origin

import pytest
import yaml
from jinja2 import DictLoader, Environment, Template
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.compile_python import compile_python
from pydantic import BaseModel, ValidationError
from pydantic.version import VERSION as PYDANTIC_VERSION

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pydanticgen.template import (
    ConditionalImport,
    Import,
    Imports,
    ObjectImport,
    PydanticAttribute,
    PydanticClass,
    PydanticValidator,
    TemplateModel,
)
from linkml.utils.schema_builder import SchemaBuilder

from .conftest import MyInjectedClass

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
    lines = code.splitlines()
    ix = lines.index("class C(ConfiguredBaseModel):")
    assert lines[ix + 2] == "    inlined_things: Optional[Dict[str, Union[A, B]]] = Field(default_factory=dict)"
    assert lines[ix + 3] == "    inlined_as_list_things: Optional[List[Union[A, B]]] = Field(default_factory=list)"
    assert lines[ix + 4] == "    not_inlined_things: Optional[List[str]] = Field(default_factory=list)"


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
    slot_line = lines[ix + 1]
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
  - linkml:types

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
    assert date_slot_line == "attr5: Optional[date] = Field(date(2020, 1, 1))"
    datetime_slot_line = lines[ix + 9].strip()
    assert datetime_slot_line == "attr6: Optional[datetime ] = Field(datetime(2020, 1, 1, 0, 0, 0))"


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


@pytest.mark.skip("Labeled arrays not implemented")
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


@pytest.mark.skip("labeled arrays not implemented")
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

    if int(PYDANTIC_VERSION.split(".")[0]) >= 2:
        assert name in base.model_fields
        field = base.model_fields[name]
        assert field.annotation == type
        assert field.default == default
        assert field.description == description
    else:
        assert name in base.__fields__
        field = base.__fields__[name]
        # pydantic <2 mangles annotations so can't do direct annotation comparison
        assert not field.required
        if get_origin(type):
            assert field.type_ is get_args(type)[0]
        else:
            assert field.type_ is type
        assert field.field_info.description == description


# --------------------------------------------------
# pydanticgen template module tests
# --------------------------------------------------


@pytest.fixture
def sample_class() -> PydanticClass:
    # no pattern makes no validators
    attr_1 = PydanticAttribute(name="attr_1", annotations={"python_range": {"value": "Union[str,int]"}}, required=True)
    attr_2 = PydanticAttribute(name="attr_2", annotations={"python_range": {"value": "List[float]"}})
    cls = PydanticClass(name="Sample", attributes={"attr_1": attr_1, "attr_2": attr_2})
    return cls


@pytest.mark.parametrize(
    "mode,expected",
    [["python", {"pydantic_ver": int(PYDANTIC_VERSION[0])}], ["json", f'{{"pydantic_ver": {PYDANTIC_VERSION[0]}}}']],
)
def test_template_model_dump(mode: str, expected):
    if mode == "json" and int(PYDANTIC_VERSION[0]) >= 2:
        return
    assert TemplateModel().model_dump(mode=mode) == expected


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

    imports = Imports() + import_a

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


def test_template_models_templates():
    """
    All template models should have templates!
    """
    for model in TemplateModel.__subclasses__():
        assert hasattr(model, "template")
        assert isinstance(model.template, str)
        env = model.environment()
        template = env.get_template(model.template)
        assert isinstance(template, Template)


def test_default_environment():
    """
    Check that the default environment has the configuration for our templates
    """
    env = TemplateModel.environment()
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
range: {{ annotations.python_range.value }}""",
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

    class InnerTemplate(TemplateModel):
        template: ClassVar[str] = "inner.jinja"
        value: Union[int, str] = 1

    class TestTemplate(TemplateModel):
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
