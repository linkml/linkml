import ast
import importlib
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Optional

import pytest
from linkml_runtime.utils.introspection import package_schemaview

from linkml.generators.rustgen import RustGenerator

pytestmark = [
    pytest.mark.rustgen,
]


def _generate_rust_crate(schema_input, out_dir: Path, *, handwritten_lib: bool = False) -> Path:
    """
    Generate a Rust crate with PyO3 bindings for the given schema input
    into the provided output directory and perform basic sanity checks.

    Returns the output directory.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    gen = RustGenerator(
        schema_input,
        mode="crate",
        pyo3=True,
        serde=True,
        output=str(out_dir),
        handwritten_lib=handwritten_lib,
    )
    gen.serialize(force=True)

    cargo_toml = out_dir / "Cargo.toml"
    pyproject_toml = out_dir / "pyproject.toml"
    assert cargo_toml.exists(), "Cargo.toml not generated"
    assert pyproject_toml.exists(), "pyproject.toml not generated"
    return out_dir


def _build_rust_crate(out_dir: Path, context: str = "") -> list[Path]:
    """
    Build the Rust crate at out_dir using maturin and assert a wheel is produced.
    Returns list of produced wheel paths.
    """
    build_cmd = ["maturin", "build"]
    env = os.environ.copy()
    env["RUST_BACKTRACE"] = "1"
    result = subprocess.run(build_cmd, cwd=out_dir, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        prefix = f" for {context}" if context else ""
        pytest.fail(
            f"maturin build failed{prefix}. See output below for diagnostics.\n\n"
            f"cmd: {' '.join(build_cmd)}\n"
            f"exit: {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}\n"
        )

    wheels_dir = out_dir / "target" / "wheels"
    assert wheels_dir.exists(), f"maturin did not produce target/wheels{(' for ' + context) if context else ''}"
    wheels = list(wheels_dir.glob("*.whl"))
    assert wheels, f"no wheel produced by maturin{(' for ' + context) if context else ''}"
    return wheels


def _run_stubgen_binary(out_dir: Path, extra_args: Optional[list[str]] = None, context: str = "") -> None:
    """Run the generated stub_gen binary to (re)generate or validate PyO3 stubs."""

    cmd = ["cargo", "run", "--bin", "stub_gen", "--features", "stubgen"]
    if extra_args:
        cmd.append("--")
        cmd.extend(extra_args)

    env = os.environ.copy()
    env["RUST_BACKTRACE"] = "1"
    result = subprocess.run(cmd, cwd=out_dir, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        prefix = f" for {context}" if context else ""
        pytest.fail(
            f"cargo run stub_gen failed{prefix}. See output below for diagnostics.\n\n"
            f"cmd: {' '.join(cmd)}\n"
            f"exit: {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}\n"
        )


def _import_built_wheel(out_dir: Path, module_name: str):
    """
    Add the built wheel to sys.path and import its top-level module.
    Returns the imported module.
    """

    wheels_dir = out_dir / "target" / "wheels"
    wheels = sorted(wheels_dir.glob("*.whl"), key=lambda p: p.stat().st_mtime, reverse=True)
    assert wheels, "no wheel produced by maturin"
    wheel_path = wheels[0]

    # Binary extensions cannot be imported directly from a zip file.
    # Extract the wheel to a temp dir and import from there.
    extract_dir = out_dir / ".wheel_extract"
    if extract_dir.exists():
        # Clean previous extraction to avoid stale artifacts
        for p in sorted(extract_dir.rglob("*"), reverse=True):
            try:
                p.unlink()
            except IsADirectoryError:
                p.rmdir()
        extract_dir.rmdir()
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(wheel_path) as zf:
        zf.extractall(extract_dir)

    sys.path.insert(0, str(extract_dir))
    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
        mod = importlib.import_module(module_name)
    finally:
        if sys.path and sys.path[0] == str(extract_dir):
            sys.path.pop(0)
    return mod


def test_rustgen_personschema_maturin(temp_dir):
    """
    Generate a Rust crate from personinfo.yaml and try to build
    the Python bindings with maturin.
    """

    # Resolve schema and output directory
    schema_path = Path(__file__).resolve().parents[2] / "examples" / "PersonSchema" / "personinfo.yaml"
    assert schema_path.exists(), f"Schema not found at {schema_path}"
    out_dir = _generate_rust_crate(str(schema_path), Path(temp_dir) / "personinfo_rust")

    # Try to build a wheel via maturin. This may require network access
    # to fetch crates unless dependencies are cached.
    _build_rust_crate(out_dir)
    # Try importing the generated wheel/module and sanity-check a class
    mod = _import_built_wheel(out_dir, module_name="personinfo")
    assert hasattr(mod, "Person"), "Expected class 'Person' not found in module"

    person_data = {
        "id": "1",
        "name": "P. One",
        "description": "Person One",
        "depicted_by": "http://example.org/image_one.jpg",
        "primary_email": "one@example.org",
        "birth_date": "1900-01-01",
        "age_in_years": 125,
        "gender": "cisgender man",  # matches GenderType enum value
        "current_address": {
            "street": "1 Maple Street",
            "city": "Springfield, AZ",
            "postal_code": "12345",
        },  # compliance tests will have a dict here.
        "telephone": "800-555-1111",
        "has_employment_history": None,
        "has_familial_relationships": None,
        "has_interpersonal_relationships": None,
        "has_medical_history": None,
        "has_news_events": None,
        "aliases": None,
    }

    person = mod.Person(**person_data)
    assert person.name == "P. One"


def test_rustgen_personschema_stubgen(temp_dir):
    """Run the generated stub_gen binary and sanity-check emitted stub files."""

    schema_path = Path(__file__).resolve().parents[2] / "examples" / "PersonSchema" / "personinfo.yaml"
    assert schema_path.exists(), f"Schema not found at {schema_path}"
    out_dir = _generate_rust_crate(str(schema_path), Path(temp_dir) / "personinfo_stubgen")

    _run_stubgen_binary(out_dir, context="personschema stub generation")

    stub_files = list(out_dir.rglob("*.pyi"))
    assert stub_files, "stub_gen did not materialize any .pyi files under target/"

    class_signature_found = False
    for stub_file in stub_files:
        text = stub_file.read_text(encoding="utf-8")
        try:
            ast.parse(text)
        except SyntaxError as exc:  # pragma: no cover - executed only on failure
            pytest.fail(f"Generated stub {stub_file} contains invalid Python syntax: {exc}")
        if "class Person" in text:
            class_signature_found = True

    assert class_signature_found, "Generated stubs do not contain expected 'class Person' definition"

    _run_stubgen_binary(out_dir, extra_args=["--check"], context="personschema stub check")

    handwritten_dir = _generate_rust_crate(
        str(schema_path), Path(temp_dir) / "personinfo_handwritten", handwritten_lib=True
    )
    shim_path = handwritten_dir / "src" / "lib.rs"
    generated_mod = handwritten_dir / "src" / "generated" / "mod.rs"
    assert shim_path.exists(), "handwritten shim lib.rs not generated"
    assert generated_mod.exists(), "generated module not created under src/generated"
    shim_text = shim_path.read_text(encoding="utf-8")
    assert "load_yaml_container" in shim_text
    assert "#[pyfunction" in shim_text


def test_rustgen_metamodel_maturin(temp_dir):
    """
    Generate a Rust crate from the LinkML metamodel (via package_schemaview)
    and build Python bindings with maturin.

    This exercises enum PyO3 conversions and union handling used throughout
    the metamodel, mirroring common downstream usage.
    """

    # Resolve SchemaDefinition for the runtime metamodel
    metamodel_sv = package_schemaview("linkml_runtime.linkml_model.meta")
    out_dir = _generate_rust_crate(metamodel_sv.schema, Path(temp_dir) / "metamodel_rust")

    _build_rust_crate(out_dir, context="metamodel")
    # Try importing the generated wheel/module and sanity-check a metamodel class
    mod = _import_built_wheel(out_dir, module_name=metamodel_sv.schema.name)
    assert hasattr(mod, "ClassDefinition"), "Expected class 'ClassDefinition' not found in metamodel module"

    # Verify Anything/AnyValue is accessible from Python via a field
    # Extension.value in the metamodel has range AnyValue.
    assert hasattr(mod, "Extension"), "Expected class 'Extension' not found in metamodel module"
    # Create an Extension with a simple string value. If Anything conversions work,
    # Python should see a native str for .value.
    # Constructor uses positional args only with current PyO3 generator
    ext = mod.Extension("test:tag", "hello-any", None)
    assert isinstance(ext.extension_value, str)
    assert ext.extension_value == "hello-any"


def test_rustgen_file_mode_generation(temp_dir):
    schema_path = Path(__file__).resolve().parents[2] / "examples" / "PersonSchema" / "personinfo.yaml"
    out_file = Path(temp_dir) / "personinfo.rs"
    gen = RustGenerator(
        str(schema_path),
        mode="file",
        pyo3=True,
        serde=True,
        output=str(out_file),
    )
    gen.serialize(force=True)

    assert out_file.exists(), "file mode did not create the expected .rs file"
    contents = out_file.read_text(encoding="utf-8")
    assert "define_stub_info_gatherer!(stub_info);" in contents
    assert "#[pymodule]" in contents
    assert "pub fn register_pymodule" not in contents
