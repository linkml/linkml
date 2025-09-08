import os
import shutil
import subprocess
from pathlib import Path

import pytest
from linkml_runtime.utils.introspection import package_schemaview

from linkml.generators.rustgen import RustGenerator


@pytest.mark.rustgen
def test_rustgen_personschema_maturin(input_path, temp_dir):
    """
    Generate a Rust crate from personinfo.yaml and try to build
    the Python bindings with maturin. Skips if maturin/cargo are absent.
    """

    # Resolve schema and output directory
    schema_path = Path(input_path("personinfo.yaml"))
    out_dir = Path(temp_dir) / "personinfo_rust"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate the crate with pyO3 bindings enabled
    gen = RustGenerator(str(schema_path), mode="crate", pyo3=True, serde=True, output=str(out_dir))
    gen.serialize(force=True)

    # Basic sanity checks on generated project
    cargo_toml = out_dir / "Cargo.toml"
    pyproject_toml = out_dir / "pyproject.toml"
    assert cargo_toml.exists(), "Cargo.toml not generated"
    assert pyproject_toml.exists(), "pyproject.toml not generated"

    # Skip if maturin or cargo are not available
    if shutil.which("maturin") is None or shutil.which("cargo") is None:
        pytest.skip("maturin and/or cargo not installed; skipping build test")

    # Try to build a wheel via maturin. This may require network access
    # to fetch crates unless dependencies are cached.
    build_cmd = ["maturin", "build"]

    env = dict(**{k: v for k, v in dict(**os.environ).items()}) if "os" in globals() else None
    # Enable Rust backtraces for richer diagnostics
    if env is not None:
        env["RUST_BACKTRACE"] = "1"
    result = subprocess.run(build_cmd, cwd=out_dir, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        # Fallback: try cargo offline mode if cache is present
        offline_cmd = build_cmd + ["--offline"]
        offline_res = subprocess.run(offline_cmd, cwd=out_dir, capture_output=True, text=True, env=env)
        if offline_res.returncode != 0:
            pytest.fail(
                "maturin build failed. See output below for diagnostics.\n\n"
                "== Online attempt ==\n"
                f"cmd: {' '.join(build_cmd)}\n"
                f"exit: {result.returncode}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}\n\n"
                "== Offline attempt ==\n"
                f"cmd: {' '.join(offline_cmd)}\n"
                f"exit: {offline_res.returncode}\n"
                f"stdout:\n{offline_res.stdout}\n"
                f"stderr:\n{offline_res.stderr}\n"
            )

    # If build succeeded, confirm a wheel exists
    wheels_dir = out_dir / "target" / "wheels"
    assert wheels_dir.exists(), "maturin did not produce target/wheels"
    wheels = list(wheels_dir.glob("*.whl"))
    assert wheels, "no wheel produced by maturin"


@pytest.mark.rustgen
def test_rustgen_metamodel_maturin(temp_dir):
    """
    Generate a Rust crate from the LinkML metamodel (via package_schemaview)
    and build Python bindings with maturin. Skips if maturin/cargo are absent.

    This exercises enum PyO3 conversions and union handling used throughout
    the metamodel, mirroring common downstream usage.
    """

    # Resolve SchemaDefinition for the runtime metamodel
    metamodel_sv = package_schemaview("linkml_runtime.linkml_model.meta")
    out_dir = Path(temp_dir) / "metamodel_rust"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate the crate with pyO3 bindings enabled
    gen = RustGenerator(metamodel_sv.schema, mode="crate", pyo3=True, serde=True, output=str(out_dir))
    gen.serialize(force=True)

    cargo_toml = out_dir / "Cargo.toml"
    pyproject_toml = out_dir / "pyproject.toml"
    assert cargo_toml.exists(), "Cargo.toml not generated"
    assert pyproject_toml.exists(), "pyproject.toml not generated"

    # Skip if maturin or cargo are not available
    if shutil.which("maturin") is None or shutil.which("cargo") is None:
        pytest.skip("maturin and/or cargo not installed; skipping build test")

    build_cmd = ["maturin", "build"]
    env = dict(**{k: v for k, v in dict(**os.environ).items()}) if "os" in globals() else None
    if env is not None:
        env["RUST_BACKTRACE"] = "1"
    result = subprocess.run(build_cmd, cwd=out_dir, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        # Fallback: try cargo offline mode if cache is present
        offline_cmd = build_cmd + ["--offline"]
        offline_res = subprocess.run(offline_cmd, cwd=out_dir, capture_output=True, text=True, env=env)
        if offline_res.returncode != 0:
            pytest.fail(
                "maturin build failed for metamodel. See output below for diagnostics.\n\n"
                "== Online attempt ==\n"
                f"cmd: {' '.join(build_cmd)}\n"
                f"exit: {result.returncode}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}\n\n"
                "== Offline attempt ==\n"
                f"cmd: {' '.join(offline_cmd)}\n"
                f"exit: {offline_res.returncode}\n"
                f"stdout:\n{offline_res.stdout}\n"
                f"stderr:\n{offline_res.stderr}\n"
            )

    wheels_dir = out_dir / "target" / "wheels"
    assert wheels_dir.exists(), "maturin did not produce target/wheels for metamodel"
    wheels = list(wheels_dir.glob("*.whl"))
    assert wheels, "no wheel produced by maturin for metamodel"
