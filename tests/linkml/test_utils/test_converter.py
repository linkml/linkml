import json

import pytest
from click.testing import CliRunner
from rdflib import Graph

from linkml.utils.converter import cli


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner(mix_stderr=False)


def test_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    out = result.stdout
    assert "INPUT" in out


P1_EXPECTED = {
    "full_name": "first1 last1",
    "is_juvenile": True,
    "age_in_years": 10,
    "age_in_months": 120,
    "age_category": "juvenile",
}

P2_EXPECTED = {
    "full_name": "first2 last2",
    "age_in_years": 20,
    "age_in_months": 240,
    "age_category": "adult",
}


def check_output(json_out):
    with open(json_out) as file:
        obj = json.load(file)
        persons = obj["persons"]
        for p, exptc in [(persons["P:1"], P1_EXPECTED), (persons["P:2"], P2_EXPECTED)]:
            for attr in exptc.keys():
                assert p[attr] == exptc[attr]

        assert "is_juvenile" not in persons["P:2"]


def test_infer(input_path, cli_runner, tmp_path):
    """
    Tests using the --infer option to add missing values
    """
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    result = cli_runner.invoke(cli, ["--infer", "-s", schema, data_in, "-o", json_out])
    assert result.exit_code == 0
    check_output(json_out)


@pytest.mark.xfail(reason="Bug 2723: missing intermediate checks")
def test_convert(input_path, cli_runner, tmp_path):
    """
    Tests using the --infer option to add missing values, and also roundtripping
    through yaml->json->yaml->rdf->json
    """
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    json_out = tmp_path / "data_example.out.json"
    yaml_out = tmp_path / "data_example.out.yaml"
    rdf_out = tmp_path / "data_example.out.ttl"
    result = cli_runner.invoke(cli, ["--infer", "-s", schema, data_in, "-o", json_out])
    assert result.exit_code == 0
    result = cli_runner.invoke(cli, ["-s", schema, json_out, "-t", "yaml", "-o", yaml_out])
    assert result.exit_code == 0
    result = cli_runner.invoke(cli, ["-s", schema, yaml_out, "-t", "rdf", "-o", rdf_out])
    assert result.exit_code == 0
    result = cli_runner.invoke(cli, ["-s", schema, rdf_out, "-t", "json", "-o", json_out])
    assert result.exit_code == 0
    check_output(json_out)


def test_prefix_file(input_path, cli_runner, tmp_path):
    schema = input_path("schema_with_inference.yaml")
    data_in = input_path("data_example.yaml")
    rdf_out = tmp_path / "data_example.out.ttl"
    prefix_file = input_path("data_example_prefix_map.yaml")
    result = cli_runner.invoke(
        cli, ["-s", schema, data_in, "-t", "rdf", "-o", rdf_out, "--prefix-file", prefix_file], catch_exceptions=True
    )
    assert result.exit_code == 0
    rdf_graph = Graph()
    rdf_graph.parse(rdf_out, format="turtle")
    namespaces = {str(prefix): str(namespace) for prefix, namespace in rdf_graph.namespaces()}
    assert "P" in namespaces
    assert namespaces["P"] == "http://www.example.com/personinfo/"


def test_version(cli_runner):
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.stdout
