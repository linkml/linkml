import re

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.yamlutils import YAMLRoot

from linkml.generators.pythongen import PythonGenerator
from linkml.utils.schema_builder import SchemaBuilder
from linkml.validators import JsonSchemaDataValidator

# reported in https://github.com/linkml/linkml/issues/349


def _safe_name(original_name: str, prefix: str = "x_") -> str:
    safe_name = re.sub("[^0-9a-z_A-Z]+", "_", original_name)
    c1 = safe_name[0]
    if "0" <= c1 <= "9":
        safe_name = underscore(f"{prefix}{safe_name}")
    return safe_name


def test_safe_name():
    cases = [
        ("a", "a"),
        ("A", "A"),
        ("1", "x_1"),
        ("1A", "x_1A"),
        ("five'", "five_"),
        ("5'", "x_5_"),
    ]
    for original, safe in cases:
        assert safe == _safe_name(original)


def test_reserved():
    slots = ["a", "1S", "a/b", "5'end"]
    # TODO: make classes safe
    # classes = ["c", "1C", "x-y"]
    classes = ["c"]
    for cn in classes:
        for sn in slots:
            sb = SchemaBuilder()
            sb.add_class(cn, [sn], tree_root=True)
            sb.add_defaults()
            schema = sb.schema
            _make_safe(schema)
            s = schema.slots[sn]
            k = s.alias if s.alias else s.name
            inst = {k: "test"}
            _test_jsonschema(schema, inst)
            _test_pythongen(schema, inst, cn, sn)


def _make_safe(schema: SchemaDefinition):
    for s in schema.slots.values():
        safe_name = _safe_name(s.alias) if s.alias else _safe_name(s.name)
        if safe_name != s.name:
            s.alias = safe_name


def _test_jsonschema(schema: SchemaDefinition, inst: YAMLRoot):
    validator = JsonSchemaDataValidator(schema=schema)
    errs = validator.validate_dict(inst)
    assert errs is None


def _test_pythongen(schema: SchemaDefinition, inst: YAMLRoot, cn: str, sn: str):
    gen_slots = False  # TODO
    pygen = PythonGenerator(schema, gen_slots=gen_slots)
    pygen.serialize()
    mod = pygen.compile_module()
    py_cls_name = camelcase(cn)
    py_cls = getattr(mod, py_cls_name)
    s = schema.slots[sn]
    k = s.alias if s.alias else s.name
    init_dict = {k: "test"}
    py_cls(**init_dict)
