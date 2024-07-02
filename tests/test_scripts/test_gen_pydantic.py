from pathlib import Path

from click.testing import CliRunner
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pydanticgen import cli


def test_template_dir(input_path):
    """Override templates from a template directory"""
    pydantic_dir = input_path("pydantic")
    args = [str(Path(pydantic_dir) / "simple.yaml"), "--template-dir", str(pydantic_dir)]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert (
        """Sample
attr: attr_1
range: Optional[Union[int, str]]
attr: attr_2
range: Optional[List[float]]"""
        in result.stdout
    )


def test_pydantic_metadata_mode(input_path):
    """
    Should be possible to change metadata modes from the CLI

    Note that this does not test the functionality of including metadata, just
    the ability to specify from the CLI
    """
    pydantic_dir = input_path("pydantic")
    args = [str(Path(pydantic_dir) / "simple.yaml"), "--meta", "None"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    mod = compile_python(result.stdout)
    assert mod.linkml_meta is None

    args = [str(Path(pydantic_dir) / "simple.yaml"), "--meta", "auto"]

    runner = CliRunner()
    result = runner.invoke(cli, args)
    mod = compile_python(result.stdout)
    assert mod.linkml_meta["id"] == "simple"
