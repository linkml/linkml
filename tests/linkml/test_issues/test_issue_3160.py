"""Test that inlined_as_list slots without identifiers emit _normalize_inlined_as_list.

Issue #3160: pythongen skips _normalize_inlined for inlined_as_list slots
when the range class has no identifier but does have a required field.
This meant dict-form YAML input was not handled correctly.
"""

from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

LIST_DATA = """
items:
  - name: item1
    value: v1
  - name: item2
    value: v2
"""

DICT_DATA = """
items:
  item1:
    value: v1
  item2:
    value: v2
"""

# --- Inline schemas for edge cases ---

# inlined_as_list, no identifier, no required fields at all
NO_REQUIRED_SCHEMA = """
id: https://w3id.org/linkml/tests/issue_3160_no_req
name: issue_3160_no_req
prefixes:
  linkml: https://w3id.org/linkml/
default_prefix: https://w3id.org/linkml/tests/
imports:
  - linkml:types
classes:
  Container:
    slots:
      - items
  Item:
    slots:
      - name
      - value
slots:
  name:
    range: string
  value:
    range: string
  items:
    multivalued: true
    range: Item
    inlined: true
    inlined_as_list: true
"""

# inlined_as_list, no identifier, only required field has a class range
CLASS_RANGE_REQUIRED_SCHEMA = """
id: https://w3id.org/linkml/tests/issue_3160_class_range
name: issue_3160_class_range
prefixes:
  linkml: https://w3id.org/linkml/
default_prefix: https://w3id.org/linkml/tests/
imports:
  - linkml:types
classes:
  Container:
    slots:
      - items
  Item:
    slots:
      - info
      - value
  Info:
    slots:
      - label
slots:
  info:
    required: true
    range: Info
  label:
    range: string
  value:
    range: string
  items:
    multivalued: true
    range: Item
    inlined: true
    inlined_as_list: true
"""


def _compile(schema_source):
    """Compile a schema (file path or string) to a Python module."""
    gen = PythonGenerator(schema_source)
    return compile_python(gen.serialize())


# --- Core fix: inlined_as_list with simple required field ---


def test_normalize_inlined_as_list_emitted(input_path):
    """The generated __post_init__ should call _normalize_inlined_as_list, not a naive comprehension."""
    gen = PythonGenerator(input_path("issue_3160.yaml"))
    pystr = gen.serialize()
    assert "_normalize_inlined_as_list" in pystr, (
        "Expected _normalize_inlined_as_list call in generated code for "
        "inlined_as_list slot with no identifier but a required field"
    )


def test_list_form_input(input_path):
    """List-form YAML input loads correctly."""
    module = _compile(input_path("issue_3160.yaml"))
    obj = yaml_loader.loads(LIST_DATA, target_class=module.Container)
    assert len(obj.items) == 2
    assert obj.items[0].name == "item1"
    assert obj.items[0].value == "v1"
    assert obj.items[1].name == "item2"
    assert obj.items[1].value == "v2"


def test_dict_form_input(input_path):
    """Dict-form YAML input (keyed by the required field) loads correctly."""
    module = _compile(input_path("issue_3160.yaml"))
    obj = yaml_loader.loads(DICT_DATA, target_class=module.Container)
    assert len(obj.items) == 2
    names = {item.name for item in obj.items}
    assert names == {"item1", "item2"}
    values = {item.value for item in obj.items}
    assert values == {"v1", "v2"}


def test_duplicate_key_values_allowed(input_path):
    """With keyed=False, duplicate values in the key field are allowed."""
    module = _compile(input_path("issue_3160.yaml"))
    data = """
items:
  - name: same_name
    value: v1
  - name: same_name
    value: v2
"""
    obj = yaml_loader.loads(data, target_class=module.Container)
    assert len(obj.items) == 2
    assert all(item.name == "same_name" for item in obj.items)
    assert {item.value for item in obj.items} == {"v1", "v2"}


# --- Edge case: no required fields at all -> naive comprehension fallback ---


def test_no_required_fields_falls_back():
    """When no required field exists, pythongen should not emit _normalize_inlined_as_list."""
    gen = PythonGenerator(NO_REQUIRED_SCHEMA)
    pystr = gen.serialize()
    assert "_normalize_inlined_as_list" not in pystr
    assert "_normalize_inlined_as_dict" not in pystr


def test_no_required_fields_list_input_works():
    """List-form input still works via the naive comprehension fallback."""
    module = _compile(NO_REQUIRED_SCHEMA)
    data = """
items:
  - name: a
    value: x
  - name: b
    value: y
"""
    obj = yaml_loader.loads(data, target_class=module.Container)
    assert len(obj.items) == 2
    assert obj.items[0].name == "a"


# --- Edge case: only required field has class range -> naive comprehension fallback ---


def test_class_range_required_field_falls_back():
    """When the only required field has a class range, it should not be used as key."""
    gen = PythonGenerator(CLASS_RANGE_REQUIRED_SCHEMA)
    pystr = gen.serialize()
    assert "_normalize_inlined_as_list" not in pystr
    assert "_normalize_inlined_as_dict" not in pystr


def test_class_range_required_field_list_input_works():
    """List-form input works when falling back to naive comprehension for class-range keys."""
    module = _compile(CLASS_RANGE_REQUIRED_SCHEMA)
    data = """
items:
  - info:
      label: info1
    value: x
  - info:
      label: info2
    value: y
"""
    obj = yaml_loader.loads(data, target_class=module.Container)
    assert len(obj.items) == 2
    assert obj.items[0].info.label == "info1"
    assert obj.items[1].info.label == "info2"
