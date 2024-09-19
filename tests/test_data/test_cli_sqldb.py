"""
Test the CLI commands in linkml.utils.sqlutils also known as `linkml sqldb` to the cli
"""

from click.testing import CliRunner

from linkml.utils.sqlutils import main as cli
from tests.utils.dict_comparator import compare_yaml


def test_sqldb_roundtrip(person, tmp_outputs):
    """
    Mimic the dump-load test in test_sqlite
    """
    runner = CliRunner()
    res_dump = runner.invoke(
        cli, ["dump", "-s", str(person["schema"]), "-D", str(tmp_outputs["db"]), str(person["data"])]
    )

    assert res_dump.exit_code == 0

    res_load = runner.invoke(
        cli, ["load", "-s", str(person["schema"]), "-D", str(tmp_outputs["db"]), "-o", str(tmp_outputs["data"])]
    )

    assert res_load.exit_code == 0

    assert compare_yaml(person["data"], tmp_outputs["data"]) == ""
