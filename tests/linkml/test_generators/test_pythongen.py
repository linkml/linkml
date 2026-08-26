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


def test_structured_patterns_are_resolved_without_modifying_schema(input_path) -> None:
    """Generate regular patterns from structured patterns without modifying the schema."""
    generator = PythonGenerator(input_path("pattern-example.yaml"))
    height_slot = generator.schemaview.get_slot("height")

    assert height_slot.pattern is None

    output = generator.serialize()
    materialized_pattern = r"pattern=re.compile(r'^(?:\d+[\.\d+] (centimeter|meter|inch))$')"
    assert materialized_pattern in output
    assert height_slot.pattern is None


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
# any_of / exactly_one_of range-union support (issue #1813)
# ---------------------------------------------------------------------------
#
# Prior to this fix, pythongen ignored `any_of` entirely: a slot's Python type
# annotation was derived solely from `slot.range`, and no `__post_init__`
# coercion logic existed to decide which candidate class/type a raw value
# should become. See https://github.com/linkml/linkml/issues/1813,
# https://github.com/linkml/linkml/issues/1521, and
# https://github.com/linkml/linkml/issues/1483.

_ANY_OF_SCHEMA = """id: https://example.org/any-of-test
name: any-of-test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  D:
    attributes:
      s2:
        range: string
  C:
    attributes:
      s1:
        range: Any
        any_of:
          - range: D
          - range: integer
"""


def test_any_of_union_annotation():
    """The generated annotation should be a real Union of the any_of branches,
    not the single generic type slot.range alone would produce."""
    code = PythonGenerator(_ANY_OF_SCHEMA).serialize()
    assert "s1: Optional[Union[dict, D, int]]" in code


def test_any_of_coercion_picks_matching_candidate():
    """A raw dict shaped for D becomes a D instance; a raw int stays an int."""
    py_module = make_python(_ANY_OF_SCHEMA)
    c = py_module.C(s1={"s2": "hello"})
    assert isinstance(c.s1, py_module.D)
    assert c.s1.s2 == "hello"

    c2 = py_module.C(s1=1)
    assert isinstance(c2.s1, int)
    assert not isinstance(c2.s1, bool)


def test_any_of_first_declared_candidate_wins_on_ambiguity():
    """When a value could structurally satisfy more than one candidate, the
    first one declared in any_of wins -- a deterministic, documented tie-break,
    not an attempt to guess the 'best' match."""
    schema = """id: https://example.org/any-of-tiebreak
name: any-of-tiebreak
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  P:
    attributes:
      a:
        range: string
  Q:
    attributes:
      a:
        range: string
      b:
        range: string
  Top:
    attributes:
      thing:
        range: Any
        any_of:
          - range: P
          - range: Q
"""
    py_module = make_python(schema)
    # {"a": "x"} satisfies both P and Q's (both optional) fields; P is declared first.
    t = py_module.Top(thing={"a": "x"})
    assert isinstance(t.thing, py_module.P)


def test_any_of_rdf_export_regression_1521():
    """Regression test for the originally-reported symptom of issue #1521: a slot
    coerced via any_of into an identifier-less embedded class used to stay an
    untyped JsonObj at runtime, and exporting it to RDF crashed with
    `ValueError: Class JsonObj not found in schema`. The compliance suite's
    test_slot_any_of case runs with exclude_rdf=True, so nothing else in the suite
    exercises this path."""
    schema = """id: https://example.org/any-of-rdf
name: any-of-rdf
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
default_range: string
imports:
  - linkml:types

classes:
  Any:
    class_uri: linkml:Any
  Dataset:
    attributes:
      title:
        range: string
  Catalogue:
    attributes:
      label:
        range: string
  Container:
    attributes:
      cid:
        identifier: true
      item:
        range: Any
        any_of:
          - range: Dataset
          - range: Catalogue
"""
    py_module = make_python(schema)
    c = py_module.Container(cid="ex:C1", item={"title": "T"})
    assert isinstance(c.item, py_module.Dataset)

    from linkml_runtime import SchemaView
    from linkml_runtime.dumpers import rdflib_dumper

    rdf = rdflib_dumper.dumps(c, schemaview=SchemaView(schema))
    assert "ex:Dataset" in rdf


def test_any_of_raises_value_error_when_no_candidate_fits():
    py_module = make_python(_ANY_OF_SCHEMA)
    with pytest.raises(ValueError, match="None of the candidate types"):
        py_module.C(s1="abc")


def test_any_of_with_any_type_and_default_range():
    """Reproduces the use_any_type=True, use_default_range=True combination from
    tests/linkml/test_compliance/test_boolean_slot_compliance.py::test_slot_any_of:
    any_of must take priority over both the explicit `range: Any` and the
    schema's default_range, not collapse to either."""
    schema = """id: https://example.org/any-of-default-range
name: any-of-default-range
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  Any:
    class_uri: linkml:Any
  D:
    attributes:
      s2:
        range: string
  C:
    attributes:
      s1:
        range: Any
        any_of:
          - range: D
          - range: integer
"""
    py_module = make_python(schema)
    c = py_module.C(s1={"s2": "hi"})
    assert isinstance(c.s1, py_module.D)
    c2 = py_module.C(s1=1)
    assert isinstance(c2.s1, int)
    with pytest.raises(ValueError, match="None of the candidate types"):
        py_module.C(s1="abc")


def test_any_of_boolean_branch_compiles_and_coerces():
    """Regression test: an any_of branch ranged over `boolean` must both compile
    (no NameError/missing import for whatever runtime type the branch resolves
    to) and correctly coerce a bool value. Mirrors the LinkML metamodel's own
    `ArrayExpression.maximum_number_dimensions` slot shape
    (`range: Anything, any_of: [integer, boolean]`)."""
    schema = """id: https://example.org/any-of-boolean
name: any-of-boolean
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  C:
    attributes:
      s1:
        range: Any
        any_of:
          - range: integer
          - range: boolean
"""
    py_module = make_python(schema)
    c = py_module.C(s1=True)
    assert c.s1 is True
    c2 = py_module.C(s1=5)
    assert c2.s1 == 5


def test_any_of_forward_reference_quotes_annotation():
    """A branch class declared AFTER the slot's containing class, with no
    identifier slot, must be quoted in the annotation (forward reference) and
    still compile without NameError."""
    schema = """id: https://example.org/any-of-forward-ref
name: any-of-forward-ref
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  C:
    attributes:
      s1:
        range: Any
        any_of:
          - range: D
          - range: integer
  D:
    attributes:
      s2:
        range: string
"""
    code = PythonGenerator(schema).serialize()
    assert '"D"' in code
    py_module = make_python(schema)
    c = py_module.C(s1={"s2": "hi"})
    assert isinstance(c.s1, py_module.D)


def test_any_of_multivalued_unchanged():
    """Documents current scope: multivalued any_of slots are intentionally left
    untouched by this fix (a separate, larger follow-up). This test pins
    today's output so a future change to multivalued any_of support gets a
    clear, intentional test failure to update, rather than silently changing
    behavior."""
    schema = """id: https://example.org/any-of-multivalued
name: any-of-multivalued
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  D:
    attributes:
      s2:
        range: string
  C:
    attributes:
      s1:
        range: Any
        multivalued: true
        any_of:
          - range: D
          - range: integer
"""
    code = PythonGenerator(schema).serialize()
    assert "s1: Optional[Union[Union[dict, Any], list[Union[dict, Any]]]] = empty_list()" in code
    class_c_start = code.index("class C(")
    class_c_end = code.index("\nclass ", class_c_start + 1)
    class_c = code[class_c_start:class_c_end]
    assert "__post_init__" not in class_c


# --- Nested / recursive any_of -----------------------------------------------


def test_any_of_nested_candidate_resolves_bottom_up():
    """A slot whose any_of candidate class itself has its own any_of slot must
    resolve correctly: constructing the outer candidate requires its nested
    field to resolve first, via ordinary Python call-stack + exception
    propagation -- no explicit recursive algorithm is needed."""
    schema = """id: https://example.org/any-of-nested
name: any-of-nested
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  X:
    attributes:
      a:
        range: string
        required: true
  Y:
    attributes:
      b:
        range: string
        required: true
  Inner:
    attributes:
      target:
        range: Any
        any_of:
          - range: X
          - range: Y
  Top:
    attributes:
      thing:
        range: Any
        any_of:
          - range: Inner
"""
    py_module = make_python(schema)
    t = py_module.Top(thing={"target": {"a": "hi"}})
    assert isinstance(t.thing, py_module.Inner)
    assert isinstance(t.thing.target, py_module.X)


def test_any_of_deep_disambiguation_by_nested_shape():
    """Two outer candidate classes that are structurally identical at their own
    level, distinguishable only by what their respective nested any_of
    accepts, must still resolve correctly -- because attempting to construct
    a candidate *is* looking inside its nested fields."""
    schema = """id: https://example.org/any-of-deep-disambiguation
name: any-of-deep-disambiguation
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  LeafA:
    attributes:
      value_a:
        range: string
        required: true
  LeafB:
    attributes:
      value_b:
        range: string
        required: true
  P:
    attributes:
      target:
        range: Any
        any_of:
          - range: LeafA
  Q:
    attributes:
      target:
        range: Any
        any_of:
          - range: LeafB
  Root:
    attributes:
      thing:
        range: Any
        any_of:
          - range: P
          - range: Q
"""
    py_module = make_python(schema)
    r1 = py_module.Root(thing={"target": {"value_a": "x"}})
    assert isinstance(r1.thing, py_module.P)
    assert isinstance(r1.thing.target, py_module.LeafA)

    r2 = py_module.Root(thing={"target": {"value_b": "y"}})
    assert isinstance(r2.thing, py_module.Q)
    assert isinstance(r2.thing.target, py_module.LeafB)


def test_any_of_self_referential_tree():
    """A modest-depth self-referential (tree-shaped) schema resolves correctly.
    This does not attempt to test or guard against pathologically deep
    (hundreds of levels) recursion hitting Python's own RecursionError -- that
    is a pre-existing characteristic of LinkML's recursive object construction
    in general, not something introduced by or specific to this fix."""
    schema = """id: https://example.org/any-of-tree
name: any-of-tree
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  Leaf:
    attributes:
      value:
        range: string
        required: true
  Node:
    attributes:
      child:
        range: Any
        any_of:
          - range: Leaf
          - range: Node
"""
    py_module = make_python(schema)
    depth = 25
    data = {"value": "bottom"}
    for _ in range(depth):
        data = {"child": data}
    root = py_module.Node(**data)
    measured = 0
    node = root
    while isinstance(node, py_module.Node):
        node = node.child
        measured += 1
    assert measured == depth
    assert node.value == "bottom"


# --- exactly_one_of type-union support ---------------------------------------

_EXACTLY_ONE_OF_SCHEMA = """id: https://example.org/exactly-one-of-test
name: exactly-one-of-test
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_range: string

classes:
  Any:
    class_uri: linkml:Any
  X:
    attributes:
      a:
        range: string
        required: true
  Y:
    attributes:
      b:
        range: string
        required: true
  Z:
    attributes:
      a:
        range: string
        required: true
  Top:
    attributes:
      thing:
        range: Any
        exactly_one_of:
          - range: X
          - range: Y
          - range: Z
"""


def test_exactly_one_of_union_annotation():
    code = PythonGenerator(_EXACTLY_ONE_OF_SCHEMA).serialize()
    assert "thing: Optional[Union[dict, X, Y, Z]]" in code


def test_exactly_one_of_single_match_succeeds():
    py_module = make_python(_EXACTLY_ONE_OF_SCHEMA)
    t = py_module.Top(thing={"b": "hi"})
    assert isinstance(t.thing, py_module.Y)


def test_exactly_one_of_zero_matches_raises():
    py_module = make_python(_EXACTLY_ONE_OF_SCHEMA)
    with pytest.raises(ValueError, match="None of the candidate types"):
        py_module.Top(thing={"c": "x"})


def test_exactly_one_of_ambiguous_matches_raises_distinct_message():
    """X and Z both have a required field named 'a', so a value with only
    that field matches both -- a genuine exactly_one_of violation, which must
    be reported distinctly from the "no candidate fits" case."""
    py_module = make_python(_EXACTLY_ONE_OF_SCHEMA)
    with pytest.raises(ValueError, match="ambiguously matches"):
        py_module.Top(thing={"a": "hi"})
