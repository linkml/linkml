from pathlib import Path
from typing import Optional

import pytest
from click.testing import CliRunner

from linkml.generators.pythongen import cli
from linkml_runtime.utils.compile_python import compile_python
from tests.conftest import KITCHEN_SINK_PATH, Snapshot

pytestmark = pytest.mark.pythongen


def gen_and_comp_python(
    schema: Path,
    snapshot: Snapshot,
    addl_args: Optional[list[str]] = None,
    python_base: Optional[str] = None,
) -> None:
    """Generate yaml_file into python_file and compare it against master_file"""
    arglist = [str(schema), "--no-metadata"] + (addl_args if addl_args else [])

    runner = CliRunner()
    result = runner.invoke(cli, arglist)
    assert result.exit_code == 0
    assert result.output == snapshot

    # Make sure the python is valid
    compile_python(result.output, "test")


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate python classes to represent a LinkML model" in result.output


def test_metamodel(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, [KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot("genpython/meta.py")


def test_multi_id(input_path, snapshot):
    """Test the multi-identifier error"""
    gen_and_comp_python(input_path("multi_id.yaml"), snapshot("genpython/multi_id.py"))


def test_timepoint(input_path, snapshot):
    """Test an issue with the biolink-model timepoint rendering"""
    gen_and_comp_python(input_path("timepoint.yaml"), snapshot("genpython/timepoint.py"))


def test_type_inheritance(input_path, snapshot):
    """Make sure that typeof's get represented correctly"""
    gen_and_comp_python(input_path("testtypes.yaml"), snapshot("genpython/testtypes.py"))


def test_inherited_identifiers(input_path, snapshot):
    gen_and_comp_python(input_path("inheritedid.yaml"), snapshot("genpython/inheritedid.py"))


def test_ordering(input_path, snapshot):
    gen_and_comp_python(input_path("ordering.yaml"), snapshot("genpython/ordering.py"))


def test_default_namespace(input_path, snapshot):
    """Test that curie_for replaces '@default' with a blank"""
    gen_and_comp_python(input_path("default_namespace.yaml"), snapshot("genpython/default_namespace.py"))


def test_gen_classvars_slots(input_path, snapshot):
    gen_and_comp_python(
        input_path("inheritedid.yaml"), snapshot("genpython/inheritedid_ncvs.py"), ["--no-classvars", "--no-slots"]
    )


@pytest.mark.parametrize("flag", ["metadata", "no-metadata"])
def test_metadata_flag(flag: str) -> None:
    """Test that metadata is only generated, when flag active"""
    runner = CliRunner()
    result = runner.invoke(cli, [f"--{flag}", KITCHEN_SINK_PATH])
    assert result.exit_code == 0

    lines = result.output.splitlines()
    matched_lines = [
        True
        for line in lines
        if line.startswith("# Auto generated from ")
        or line.startswith("# Generation date: ")
        or line.startswith("# Schema: ")
    ]
    if flag == "metadata":
        assert matched_lines
    else:
        assert not matched_lines


def test_head_deprecated():
    'Test that expected deprecation warning appears when using "--head"'
    runner = CliRunner(mix_stderr=False)
    with pytest.warns() as record:
        result = runner.invoke(cli, ["--head", KITCHEN_SINK_PATH])
    deprecation_shown = False
    for warning in record:
        if warning.category is DeprecationWarning and str(warning.message).startswith("[metadata-flag] DEPRECATED"):
            deprecation_shown = True
    assert result.exit_code == 0
    assert deprecation_shown
