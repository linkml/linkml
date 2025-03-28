from typing import Callable

import pytest
from linkml_runtime.dumpers import json_dumper, rdf_dumper, yaml_dumper
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_issue_368(input_path, snapshot, tmp_path):
    """Make sure that types are generated as part of the output"""
    output = PythonGenerator(input_path("issue_368_imports.yaml"), mergeimports=False).serialize()
    assert output == snapshot("issue_368_imports.py")

    python = PythonGenerator(input_path("issue_368.yaml"), mergeimports=False).serialize()
    py_snapshot = snapshot("issue_368.py")
    assert python == py_snapshot

    has_imports = False
    for line in python.split("\n"):
        if line.startswith("from . issue_368_imports"):
            imps = line.replace("from . issue_368_imports import ", "").split(", ")
            assert "SampleEnum" in imps
            assert "ParentClass" in imps
            has_imports = True
    assert has_imports
    module = compile_python(str(py_snapshot.path))

    enum_inst = module.SampleEnum("pva")  # EnumInstanceImpl
    example = module.SampleClass(slot_1="pva")
    assert hasattr(example, "slot_1")
    assert example.slot_1.code.text == enum_inst.code.text
    assert str(example.slot_1) == "pva"

    def dump_and_load(dumper: Callable, sfx: str) -> None:
        fname = str(tmp_path / f"issue_368_1.{sfx}")
        dumper(example, fname)

    dump_and_load(json_dumper.dump, "json")
    dump_and_load(yaml_dumper.dump, "yaml")

    context = ContextGenerator(input_path("issue_368.yaml"), emit_metadata=False).serialize()
    assert context == snapshot("issue_368.context.jsonld")

    dump_and_load(
        lambda obj, fname: rdf_dumper.dump(obj, fname, context),
        "ttl",
    )
