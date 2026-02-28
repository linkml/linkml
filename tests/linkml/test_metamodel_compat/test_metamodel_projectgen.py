import py_compile

import pytest

from linkml.generators.projectgen import ProjectConfiguration, ProjectGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.schemaview import SchemaView


@pytest.mark.slow
def test_metamodel_projectgen(metamodel_path, tmp_path):
    def check_contains(v: str, folder: str, local_path: str):
        with open(tmp_path / folder / local_path, encoding="UTF-8") as stream:
            assert v in stream.read()

    """Generate whole project from metamodel.

    Note: Some generators are excluded due to known limitations with the metamodel:
    - shacl: doesn't support special ifabsent functions (e.g., default_range)
    - excel: metamodel has no tree_root classes, creating empty workbook
    """
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.generator_args["owl"] = {"metaclasses": False, "type_objects": False}
    config.excludes = ["shacl", "excel"]
    gen = ProjectGenerator()
    gen.generate(metamodel_path, config)
    # Validate key outputs contain expected content
    check_contains("CREATE TABLE", "sqlschema", "meta.sql")
    check_contains("linkml:SchemaDefinition a owl:Class", "owl", "meta.owl.ttl")
    check_contains('"$defs"', "jsonschema", "meta.schema.json")


@pytest.mark.slow
def test_metamodel_python_compiles(metamodel_path, tmp_path):
    """Verify that generated Python code compiles without syntax errors."""
    config = ProjectConfiguration()
    config.directory = tmp_path
    config.generator_args["owl"] = {"metaclasses": False, "type_objects": False}
    config.excludes = ["excel"]
    gen = ProjectGenerator()
    gen.generate(metamodel_path, config)
    python_file = tmp_path / "meta.py"
    assert python_file.exists(), "Python file not generated"
    # py_compile.compile raises py_compile.PyCompileError if there are syntax errors
    py_compile.compile(str(python_file), doraise=True)


@pytest.mark.slow
def test_bundled_schema_loads(bundled_schema_path):
    """Verify that each bundled schema can be loaded by SchemaView."""
    sv = SchemaView(bundled_schema_path)
    assert sv.schema is not None
    assert sv.schema.name


@pytest.mark.slow
def test_bundled_schema_python_generates(bundled_schema_path, tmp_path):
    """Verify that each bundled schema can generate compilable Python."""
    gen = PythonGenerator(bundled_schema_path)
    output = gen.serialize()
    assert output
    out_file = tmp_path / "output.py"
    out_file.write_text(output)
    py_compile.compile(str(out_file), doraise=True)
