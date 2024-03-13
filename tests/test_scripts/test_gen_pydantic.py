from pathlib import Path

from click.testing import CliRunner

from linkml.generators.pydanticgen import cli
from ..conftest import KITCHEN_SINK_PATH


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
