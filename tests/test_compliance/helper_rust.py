import os
import pytest
import sys
import zipfile
import importlib
import subprocess
from pathlib import Path
import logging

#
# Rust build methods copied from test_rustgen.py as an example
# should go in i.e. a validator plugin
#

logger = logging.getLogger(__name__)


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
            except PermissionError:
                p.rmdir()
        extract_dir.rmdir()
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(wheel_path) as zf:
        zf.extractall(extract_dir)

    sys.path.insert(0, str(extract_dir))
    try:
        mod = importlib.import_module(module_name)
    finally:
        if sys.path and sys.path[0] == str(extract_dir):
            sys.path.pop(0)
    return mod

def check_data_rustgen(schema, output, out_dir, target_class, object_to_validate, expected_behavior, valid):
    # logger.info((schema, output, target_class, object_to_validate, expected_behavior, valid))

    logger.info(f"SCHEMA NAME: {schema['name']}")

    try:
        _build_rust_crate(out_dir, context="metamodel")
        mod = _import_built_wheel(out_dir, module_name=schema['name'])
        assert mod is not None

        Clz = getattr(mod, target_class)
        instance = Clz(**object_to_validate)

        # needs a better check here
        for k, v in object_to_validate.items():
            expected = v
            actual = getattr(instance, k)
            logger.info(f"Validating slot {k}: {expected} == {actual}?")
            assert expected == actual
            logger.info("ok")
    except Exception as e:
        if valid:
            raise AssertionError(f"Exception on valid object: {e}")