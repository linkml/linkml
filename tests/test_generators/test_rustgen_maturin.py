import os
import subprocess
from pathlib import Path

import pytest
from linkml_runtime.utils.introspection import package_schemaview

from linkml.generators.rustgen import RustGenerator

pytestmark = pytest.mark.rustgen


def _generate_rust_crate(schema_input, out_dir: Path) -> Path:
    """
    Generate a Rust crate with PyO3 bindings for the given schema input
    into the provided output directory and perform basic sanity checks.

    Returns the output directory.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    gen = RustGenerator(schema_input, mode="crate", pyo3=True, serde=True, output=str(out_dir))
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


def test_rustgen_personschema_maturin(input_path, temp_dir):
    """
    Generate a Rust crate from personinfo.yaml and try to build
    the Python bindings with maturin.
    """

    # Resolve schema and output directory
    schema_path = Path(input_path("personinfo.yaml"))
    out_dir = _generate_rust_crate(str(schema_path), Path(temp_dir) / "personinfo_rust")

    # Try to build a wheel via maturin. This may require network access
    # to fetch crates unless dependencies are cached.
    _build_rust_crate(out_dir)


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
