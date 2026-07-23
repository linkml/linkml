import json
import keyword
import re
from types import ModuleType, SimpleNamespace

import pytest
from jsonasobj2 import as_json

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.loaders import json_loader
from linkml_runtime.utils.compile_python import compile_python

pytestmark = pytest.mark.pythongen


def make_python(infile) -> ModuleType:
    pstr = str(PythonGenerator(infile, mergeimports=True).serialize())
    kitchen_module = compile_python(pstr)
    return kitchen_module


def test_pythongen(kitchen_sink_path):
    """python"""
    kitchen_module = make_python(kitchen_sink_path)
    c = kitchen_module.Company("ROR:1")
    assert str(c) == "Company({'id': 'ROR:1'})"
    h = kitchen_module.EmploymentEvent(employed_at=c.id)
    assert str(h) == "EmploymentEvent({'employed_at': 'ROR:1'})"
    p = kitchen_module.Person("P:1", has_employment_history=[h])
    assert p.id == "P:1"
    assert p.has_employment_history[0] is not None
    assert p.has_employment_history[0].employed_at == c.id

    # Inline lists work:
    p2dict = {
        "id": "P:2",
        "addresses": [{"street": "1 foo street", "city": "foo city"}],
    }
    json_loader.loads(p2dict, kitchen_module.Person)

    # however, inline in a non-list context does not
    p2dict = {"id": "P:2", "has_birth_event": {"started_at_time": "1981-01-01"}}
    json_loader.loads(p2dict, kitchen_module.Person)
    assert str(p) == "Person({'id': 'P:1', 'has_employment_history': [EmploymentEvent({'employed_at': 'ROR:1'})]})"

    f = kitchen_module.FamilialRelationship(related_to="me", type="SIBLING_OF", cordialness="heartfelt")
    assert (
        str(f)
        == """FamilialRelationship({
  'related_to': 'me',
  'type': 'SIBLING_OF',
  'cordialness': CordialnessEnum(text='heartfelt', description='warm and hearty friendliness')
})"""
    )

    diagnosis = kitchen_module.DiagnosisConcept(id="CODE:D0001", name="headache")
    event = kitchen_module.MedicalEvent(in_location="GEO:1234", diagnosis=diagnosis)
    assert (
        str(event)
        == """MedicalEvent({
  'in_location': 'GEO:1234',
  'diagnosis': DiagnosisConcept({'id': 'CODE:D0001', 'name': 'headache'})
})"""
    )


def test_multiline_stuff(input_path):
    multi_line_module = make_python(input_path("kitchen_sink_mlm.yaml"))

    assert (
        multi_line_module.EmploymentEventType.PROMOTION.description
        == 'This refers to some sort of promotion event.")\n\n\nimport os\n'
        "print('DELETING ALL YOUR STUFF. HA HA HA.')"
    )


def test_enum_permissiblevalue_ifabsent(input_path):
    # this would fail if generated python code is not compilable
    ksm = make_python(input_path("kitchen_sink_ifabsent.yaml"))
    # ensure that the right permissible value is taken if other value absent
    ifabsent_obj = ksm.IfAbsent()
    assert isinstance(ifabsent_obj.ifabsent_not_literal, ksm.CordialnessEnum)
    assert ifabsent_obj.ifabsent_not_literal.code == ksm.CordialnessEnum.heartfelt


def test_enum_ifabsent_default_applied():
    """When a slot has ifabsent pointing to an enum value, instantiating the class
    without supplying that slot should give back a proper enum instance, not a string.

    Regression test for https://github.com/linkml/linkml/issues/2380
    """
    schema = """
id: https://examples.org/issue2380
name: issue2380

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://examples.org/issue2380/

default_prefix: ex
default_range: string

imports:
  - linkml:types

classes:
  Person:
    attributes:
      name:
      age_category:
        range: AgeEnum
        ifabsent: AgeEnum(infant)

enums:
  AgeEnum:
    permissible_values:
      infant:
      juvenile:
      adult:
"""
    module = make_python(schema)

    # Instantiate with only `name` — age_category should default to AgeEnum.infant
    # example from https://github.com/linkml/linkml/issues/2382#issuecomment-2437523856
    person = module.Person(name="John Doe")
    assert isinstance(person.age_category, module.AgeEnum), (
        f"Expected AgeEnum instance, got {type(person.age_category)}"
    )
    assert person.age_category.code == module.AgeEnum.infant

    # Explicitly supplying a value should override the default
    person2 = module.Person(name="Jane Doe", age_category=module.AgeEnum.adult)
    assert isinstance(person2.age_category, module.AgeEnum)
    assert person2.age_category.code == module.AgeEnum.adult


def test_enum_ifabsent_snake_case_name():
    """Enum ifabsent with a snake_case enum name should use the camelcased Python class name.

    Regression test for https://github.com/linkml/linkml/pull/3308#discussion_r2106197183
    When an enum's schema name is snake_case (e.g. 'cordiality_level'), pythongen must
    use the camelcased class name (e.g. 'CordialityLevel') in the generated __post_init__
    constructor call, not the raw schema name.
    """
    yaml = """
id: https://example.org/test_snake_case_enum_ifabsent
name: test_snake_case_enum_ifabsent
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types
default_prefix: ex
default_range: string

enums:
  cordiality_level:
    permissible_values:
      heartfelt:
      hateful:
      indifferent:

classes:
  Greeting:
    attributes:
      mood:
        range: cordiality_level
        ifabsent: cordiality_level(heartfelt)
"""
    module = make_python(yaml)
    greeting = module.Greeting()
    assert isinstance(greeting.mood, module.CordialityLevel)
    assert greeting.mood.code == module.CordialityLevel.heartfelt


def test_issue_121_imported_type_is_emitted_once(input_path):
    """Imported LinkML types should remain available in generated Python."""
    python = PythonGenerator(input_path("issue_121.yaml")).serialize()

    type_import_lines = [
        line for line in python.splitlines() if line.startswith("from linkml_runtime.linkml_model.types ")
    ]
    assert type_import_lines == ["from linkml_runtime.linkml_model.types import String"]

    module = compile_python(python)

    biosample = module.Biosample(depth="test")
    assert biosample.depth == "test"
    assert json.loads(as_json(biosample)) == {"depth": "test"}

    imported = module.ImportedClass()
    assert json.loads(as_json(imported)) == {}


def test_head():
    """Validate the head/nohead parameter"""
    yaml = """id: "https://w3id.org/biolink/metamodel"
description: Metamodel for biolink schema
license: https://creativecommons.org/publicdomain/zero/1.0/
version: 0.4.0
default_range: string
prefixes:
    xsd: http://www.w3.org/2001/XMLSchema#
types:
   string:
      base: str
      uri: xsd:string"""

    output = PythonGenerator(
        yaml,
        format="py",
        metadata=True,
        source_file_date="August 10, 2020",
        source_file_size=173,
    ).serialize()
    assert output.startswith(f"# Auto generated from None by pythongen.py version: {PythonGenerator.generatorversion}")

    output = PythonGenerator(yaml, format="py", metadata=False).serialize()
    assert output.startswith("# id: https://w3id.org/biolink/metamodel")


def test_repr(kitchen_sink_path):
    """
    Be default, don't create __repr__ for dataclasses, but do if requested!
    """
    parentclass = """
class ParentClass:
    def __repr__(self):
        return "overridden"

    def __post_init__(self, *args, **kwargs):
        pass
"""

    pstr = str(PythonGenerator(kitchen_sink_path).serialize())
    pstr = parentclass + pstr
    pstr = re.sub(r"\(YAMLRoot\)", "(ParentClass)", pstr)
    kitchen_module = compile_python(pstr)

    # if a dataclass has `repr=False`, it shouldn't override the parent class's
    friend = kitchen_module.Friend(name="bestie")
    assert repr(friend) == "overridden"

    # but we should be able to make pythongenerator do `repr=True`, where the dataclasses _do_ override
    pstr = str(PythonGenerator(kitchen_sink_path, dataclass_repr=True).serialize())
    pstr = parentclass + pstr
    pstr = re.sub(r"\(YAMLRoot\)", "(ParentClass)", pstr)
    kitchen_module = compile_python(pstr)
    friend = kitchen_module.Friend(name="bestie")
    assert repr(friend) != "overridden"


def test_keyword_named_slots_and_attributes(input_path):
    """
    Slots and attributes whose name is a Python reserved keyword must be emitted
    with trailing underscore (PEP 8 trailing-underscore convention) everywhere
    they appear as a Python identifier: in the ``slots`` registry, in dataclass
    fields, and in ``__post_init__`` self-references. The generated module must
    also be valid Python.
    """
    output = PythonGenerator(input_path("unmasked_python_keywords_example.yaml"), mergeimports=False).serialize()

    # PythonGenerator calls underscore() on slot names before checking iskeyword().
    # underscore() lowercases the name, so only already-lowercase keywords (e.g. 'and',
    # 'from') remain keywords after transformation and receive the trailing-underscore.
    # Capitalised keywords ('False', 'None', 'True') become 'false', 'none', 'true'
    # after underscore(), so are no longer keywords and are not mangled.
    for kw in keyword.kwlist:
        if kw.islower():
            # Check slots registry
            assert f"slots.{kw}_" in output, f"Expected 'slots.{kw}_' in slots registry but got no match"
            # Check dataclass fields (both inline attributes and slot references)
            assert f"{kw}_:" in output, f"Expected dataclass field '{kw}_:' in generated output but got no match"

    # The generated module must be valid Python (catches dataclass fields,
    # __post_init__ self-refs, and CurieNamespace attribute access).
    compile(output, "<generated>", "exec")


def test_permissible_values():
    """
    Test that permissible values are generated correctly
    """
    yaml = """id: http://example.org/test
description: Test schema for permissible values
prefixes:
  example: http://example.org/
enums:
  TestEnum:
    permissible_values:
      - BASIC:
      - ADVANCED:
          description: This is an advanced option
          title: Advanced Option
          meaning: "example:advanced"
"""

    py_module = make_python(yaml)
    assert py_module.TestEnum.BASIC.text == "BASIC"
    assert py_module.TestEnum.BASIC.description is None
    assert py_module.TestEnum.BASIC.title is None
    assert py_module.TestEnum.BASIC.meaning is None

    assert py_module.TestEnum.ADVANCED.text == "ADVANCED"
    assert py_module.TestEnum.ADVANCED.description == "This is an advanced option"
    assert py_module.TestEnum.ADVANCED.title == "Advanced Option"
    assert py_module.TestEnum.ADVANCED.meaning == "http://example.org/advanced"


def test_derived_class_as_key_range_ordering():
    """Test that class reference types are ordered correctly when a key slot's range
    is a derived class that inherits its identifier from a parent.

    Regression test for https://github.com/linkml/linkml/issues/2600

    The bug: when the class containing the key slot (Annotation) appeared before
    the range class's parent (Thing) in the schema dict, gen_references() would
    emit AnnotationAnnotationTag(AnnotationTagPid) before AnnotationTagPid(ThingPid),
    causing a NameError on import.
    """
    # Annotation intentionally listed BEFORE Thing to trigger the ordering bug
    yaml = """
id: https://example.org/issue2600
name: issue2600
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/issue2600/
imports:
  - linkml:types
default_range: string

classes:
  Annotation:
    slots:
      - annotation_tag
      - annotation_value
    slot_usage:
      annotation_tag:
        key: true
  Thing:
    slots:
      - pid
    slot_usage:
      pid:
        identifier: true
  AnnotationTag:
    is_a: Thing

slots:
  pid:
    range: uriorcurie
  annotation_tag:
    range: AnnotationTag
  annotation_value:
    range: string
"""
    gen = PythonGenerator(yaml)
    output = gen.serialize()

    # The generated code must be compilable — the original bug was a NameError
    # from forward-referencing an undefined class
    module = compile_python(str(output))
    assert hasattr(module, "Annotation")
    assert hasattr(module, "Thing")
    assert hasattr(module, "AnnotationTag")

    # Verify the class reference ordering: each parent must appear before its child
    ref_classes = re.findall(r"^class (\w+)\((\w+)\):\n\tpass", str(output), re.MULTILINE)
    positions = {name: i for i, (name, _parent) in enumerate(ref_classes)}
    for name, parent in ref_classes:
        if parent in positions:
            assert positions[parent] < positions[name], (
                f"Class reference {name}({parent}) appears before its parent {parent} is defined"
            )


def test_sort_classes_unresolved_parent_raises_value_error():
    """Unresolved parent references should fail with a clear ValueError."""
    classes = [ClassDefinition(name="Child", is_a="MissingParent")]
    with pytest.raises(ValueError, match="Cyclic or unresolved class inheritance"):
        PythonGenerator._sort_classes(classes)


def test_gen_references_cycle_safety_raises_value_error(monkeypatch):
    """Wrapper inheritance cycles should raise ValueError instead of recursing forever."""
    generator = PythonGenerator.__new__(PythonGenerator)
    class_a = ClassDefinition(name="a", is_a="b")
    class_b = ClassDefinition(name="b", is_a="a")
    generator.schema = SimpleNamespace(
        classes={"a": class_a, "b": class_b},
        slots={"id": SlotDefinition(name="id", identifier=True, range="string")},
        enums={},
    )

    monkeypatch.setattr(generator, "_sort_classes", lambda _classes: [class_a, class_b])
    monkeypatch.setattr(generator, "primary_keys_for", lambda _cls: ["id"])
    monkeypatch.setattr(generator, "aliased_slot_name", lambda slot_name: slot_name)
    monkeypatch.setattr(generator, "class_identifier", lambda _cls_or_name: "id")
    monkeypatch.setattr(
        generator,
        "class_identifier_path",
        lambda cls_or_name, _force_non_key: ["AId"] if cls_or_name == "a" else ["BId"],
    )
    monkeypatch.setattr(generator, "slot_range_path", lambda _slot: ["str"])

    with pytest.raises(ValueError, match="Cyclic wrapper inheritance"):
        generator.gen_references()


# ---------------------------------------------------------------------------
# Regression tests for enum-ranged identifier slots.
#
# Tests for correct ordering and emission of class-reference wrappers for enum-rooted identifiers:
# Ensures wrappers are defined after their referenced enum classes, compile without NameError,
# and maintain correct dependency order in generated Python code.
# ---------------------------------------------------------------------------


_ENUM_ID_SCHEMA = """
id: https://example.org/enum_id
name: enum_id
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/enum_id/
default_prefix: ex
default_range: string
imports:
  - linkml:types

enums:
  FIXDatatypeName:
    permissible_values:
      INT:
      STRING:

classes:
  FIXDatatype:
    attributes:
      datatype_name:
        range: FIXDatatypeName
        identifier: true
        required: true
"""


_ENUM_ID_SCHEMA_NAME_COLLISION = """
id: https://example.org/bug_collision
name: bug_collision
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/bug_collision/
default_prefix: ex
default_range: string
imports:
  - linkml:types

enums:
  ColorName:
    permissible_values:
      RED:
      GREEN:
      BLUE:

classes:
  Color:
    attributes:
      name:
        range: ColorName
        identifier: true
        required: true
"""


_ENUM_ID_SCHEMA_SUBCLASS = """
id: https://example.org/enum_id_sub
name: enum_id_sub
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/enum_id_sub/
default_prefix: ex
default_range: string
imports:
  - linkml:types

enums:
  FIXDatatypeName:
    permissible_values:
      INT:
      STRING:

classes:
  FIXDatatype:
    attributes:
      datatype_name:
        range: FIXDatatypeName
        identifier: true
        required: true
  IntDatatype:
    is_a: FIXDatatype
"""


def _ref_class_positions(output: str) -> dict[str, int]:
    """Return a mapping from wrapper class name to line number in ``output``."""
    positions: dict[str, int] = {}
    for lineno, line in enumerate(output.splitlines(), start=1):
        match = re.match(r"^class (\w+)\((\w+)\):\s*$", line)
        if match:
            positions[match.group(1)] = lineno
    return positions


def test_enum_ranged_identifier_imports():
    """Wrapper for an enum-ranged identifier must compile and import cleanly.

    Regression test for the ``NameError: name 'FIXDatatypeName' is not defined``
    raised by generated modules when an identifier slot ranged over an enum.
    """
    output = str(PythonGenerator(_ENUM_ID_SCHEMA).serialize())

    # Must compile and expose both the enum and its wrapper.
    module = compile_python(output)
    assert hasattr(module, "FIXDatatypeName")
    assert hasattr(module, "FIXDatatypeDatatypeName")
    assert issubclass(module.FIXDatatypeDatatypeName, module.FIXDatatypeName)
    # The enum's permissible values must still resolve through the wrapper's MRO.
    assert module.FIXDatatypeName.INT.text == "INT"


def test_enum_ranged_identifier_wrapper_after_enum():
    """The wrapper class must be emitted after the enum it inherits from."""
    output = str(PythonGenerator(_ENUM_ID_SCHEMA).serialize())

    positions = _ref_class_positions(output)
    # Find the enum class declaration line.
    enum_match = re.search(r"^class FIXDatatypeName\(EnumDefinitionImpl\):", output, re.MULTILINE)
    assert enum_match is not None, "enum class declaration not found"
    enum_lineno = output[: enum_match.start()].count("\n") + 1

    assert "FIXDatatypeDatatypeName" in positions, "wrapper class not emitted"
    assert positions["FIXDatatypeDatatypeName"] > enum_lineno, (
        "wrapper class must appear after the enum it inherits from"
    )


def test_enum_ranged_identifier_name_collision():
    """Wrapper whose name collides with the enum it inherits from must still import.

    When ``class Color`` declares identifier ``name`` ranged on enum ``ColorName``,
    the wrapper name (``Color`` + ``Name`` = ``ColorName``) collides with the enum
    name. The generated code must still be valid Python.
    """
    output = str(PythonGenerator(_ENUM_ID_SCHEMA_NAME_COLLISION).serialize())

    module = compile_python(output)
    # Module-level ``ColorName`` is rebound by the wrapper subclass; verify it is
    # still a subclass of the original enum and exposes its permissible values.
    assert hasattr(module, "ColorName")
    assert module.ColorName.RED.text == "RED"


def test_enum_ranged_identifier_subclass_chain_ordering():
    """An ``is_a`` chain whose identifier is enum-rooted must emit wrappers in order.

    ``IntDatatype is_a FIXDatatype`` inherits the enum-ranged identifier, so
    its wrapper ``IntDatatypeDatatypeName`` extends ``FIXDatatypeDatatypeName``,
    which extends ``FIXDatatypeName``. All three must be defined in dependency
    order, after the enum.
    """
    output = str(PythonGenerator(_ENUM_ID_SCHEMA_SUBCLASS).serialize())

    module = compile_python(output)
    assert issubclass(module.FIXDatatypeDatatypeName, module.FIXDatatypeName)
    assert issubclass(module.IntDatatypeDatatypeName, module.FIXDatatypeDatatypeName)

    positions = _ref_class_positions(output)
    enum_match = re.search(r"^class FIXDatatypeName\(EnumDefinitionImpl\):", output, re.MULTILINE)
    enum_lineno = output[: enum_match.start()].count("\n") + 1

    assert enum_lineno < positions["FIXDatatypeDatatypeName"] < positions["IntDatatypeDatatypeName"]


def test_non_enum_identifier_wrapper_emitted_before_enums():
    """String-ranged identifier wrappers must still be emitted in the pre-enum section.

    Guards against regression where deferring enum-rooted wrappers accidentally
    deferred all wrappers.
    """
    yaml = """
id: https://example.org/mixed
name: mixed
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/mixed/
default_prefix: ex
default_range: string
imports:
  - linkml:types

enums:
  ColorEnum:
    permissible_values:
      RED:

classes:
  Thing:
    attributes:
      pid:
        identifier: true
        required: true
      color:
        range: ColorEnum
"""
    output = str(PythonGenerator(yaml).serialize())

    positions = _ref_class_positions(output)
    enum_match = re.search(r"^class ColorEnum\(EnumDefinitionImpl\):", output, re.MULTILINE)
    enum_lineno = output[: enum_match.start()].count("\n") + 1

    # ``ThingPid`` is a string-ranged identifier — must appear BEFORE the enum.
    assert "ThingPid" in positions
    assert positions["ThingPid"] < enum_lineno
