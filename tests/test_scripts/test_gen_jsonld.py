import json

import pytest
from click.testing import CliRunner
from rdflib import Graph, URIRef

from linkml import METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator, cli

from ..conftest import KITCHEN_SINK_PATH


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "Generate JSONLD file from LinkML schema" in result.output


@pytest.mark.parametrize(
    "arguments,snapshot_file",
    [
        ([], "meta.jsonld"),
        (["-f", "jsonld"], "meta.jsonld"),
        (["-f", "json"], "meta.json"),
    ],
)
def test_metamodel_valid_calls(arguments, snapshot_file, snapshot):
    """Test generation of meta.yaml JSON"""

    # This path is not actually used by the generator other than being injected into the final
    # output. We use a mock relative path here so that snapshots don't fail due to comparing
    # absolute paths
    mock_context_path = "file:./context.jsonld"

    runner = CliRunner()
    result = runner.invoke(cli, arguments + ["--context", mock_context_path, KITCHEN_SINK_PATH])
    assert result.exit_code == 0
    assert result.output == snapshot(f"genjsonld/{snapshot_file}")


def test_metamodel_invalid_calls():
    runner = CliRunner()
    result = runner.invoke(cli, ["-f", "xsv", KITCHEN_SINK_PATH], standalone_mode=False)
    assert result.exit_code == 1
    assert "xsv" in str(result.exception)


def test_simple_uris(input_path, snapshot):
    """Test a simple schema that needs both LinkML AND Specific prefixes"""
    # Generate all of the required contexts
    output = ContextGenerator(input_path("includes/simple_types.yaml"), emit_metadata=False).serialize()
    assert output == snapshot("genjsonld/includes/simple_types.context.jsonld")

    output = ContextGenerator(input_path("simple_slots.yaml"), emit_metadata=False).serialize()
    assert output == snapshot("genjsonld/simple_slots.context.jsonld")

    output = ContextGenerator(input_path("simple_uri_test.yaml"), emit_metadata=False).serialize()
    assert output == snapshot("genjsonld/simple_uri_test.context.jsonld")

    runner = CliRunner()
    result = runner.invoke(cli, [str(input_path("simple_uri_test.yaml"))])
    assert result.exit_code == 0
    assert result.output == snapshot("genjsonld/simple_uri_test.jsonld")


def check_size(
    g: Graph,
    g2: Graph,
    root: URIRef,
    expected_classes: int,
    expected_slots: int,
    expected_types: int,
    expected_subsets: int,
    expected_enums: int,
    model: str,
) -> None:
    """
    Check
    :param g:
    :param g2:
    :param root:
    :param expected_classes:
    :param expected_slots:
    :param expected_types:
    :param expected_subsets:
    :param expected_enums:
    :param model:
    :return:
    """
    for graph in [g, g2]:
        n_classes = len(list(graph.objects(root, METAMODEL_NAMESPACE.classes)))
        n_slots = len(list(graph.objects(root, METAMODEL_NAMESPACE.slots)))
        n_types = len(list(graph.objects(root, METAMODEL_NAMESPACE.types)))
        n_subsets = len(list(graph.objects(root, METAMODEL_NAMESPACE.subsets)))
        n_enums = len(list(graph.objects(root, METAMODEL_NAMESPACE.enums)))
        assert expected_classes == n_classes, f"Expected {expected_classes} classes in {model}"
        assert expected_slots == n_slots, f"Expected {expected_slots} slots in {model}"
        assert expected_types == n_types, f"Expected {expected_types} types in {model}"
        assert expected_subsets == n_subsets, f"Expected {expected_subsets} subsets in {model}"
        assert expected_enums == n_enums, f"Expected {expected_enums} enums in {model}"


@pytest.mark.skip(reason="This test is too fragile, needs updated when metamodel changes")
def test_meta_output(tmp_path_factory):
    """Generate a context AND a jsonld for the metamodel and make sure it parses as RDF"""
    tmp_path = tmp_path_factory.mktemp("meta")
    tmp_jsonld_path = str(tmp_path / "metajson.jsonld")
    tmp_rdf_path = str(tmp_path / "metardf.ttl")
    tmp_meta_context_path = str(tmp_path / "metacontext.jsonld")

    # Generate an image of the metamodel
    gen = ContextGenerator(KITCHEN_SINK_PATH)

    base = gen.namespaces[gen.schema.default_prefix]
    if str(base)[-1] not in "/#":
        base += "/"
    schema = base + "meta"

    # Generate context
    with open(tmp_meta_context_path, "w") as tfile:
        tfile.write(gen.serialize())

    # Generate JSON
    with open(tmp_jsonld_path, "w") as tfile:
        tfile.write(
            JSONLDGenerator(
                KITCHEN_SINK_PATH,
                format=JSONLDGenerator.valid_formats[0],
            ).serialize(context=tmp_meta_context_path)
        )

    # Convert JSON to TTL
    g = Graph()
    g.load(tmp_jsonld_path, format="json-ld")
    g.serialize(tmp_rdf_path, format="ttl")
    g.bind("meta", METAMODEL_NAMESPACE)
    new_ttl = g.serialize(format="turtle")

    # Make sure that the generated TTL matches the JSON-LD (probably not really needed, as this is more of a test
    # of rdflib than our tooling but it doesn't hurt
    new_g = Graph()
    new_g.parse(data=new_ttl, format="turtle")

    # Make sure that both match the expected size (classes, slots, types, and model name for error reporting)
    check_size(g, new_g, URIRef(schema), 19, 126, 14, 1, 1, "meta")


@pytest.mark.parametrize("prefixes", (True, False))
@pytest.mark.parametrize("flatprefixes", (True, False))
def test_context_kwargs(input_path, prefixes: bool, flatprefixes: bool):
    """
    kwargs can be forwarded to the context generator from the cli
    """
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-f",
            "jsonld",
            "-k",
            "prefixes",
            str(prefixes),
            "-k",
            "flatprefixes",
            str(flatprefixes),
            input_path("simple_uri_test.yaml"),
        ],
    )
    assert result.exit_code == 0
    output = json.loads(result.output)
    context = output["@context"]

    # find the dict with the prefixes
    prefs = [p for p in context if isinstance(p, dict) and "@base" not in p]
    assert len(prefs) == 1, "Should only be one dictionary of prefixes in the context"
    pref_dict = prefs[0]

    if prefixes:
        assert len(pref_dict) > 1
        if flatprefixes:
            assert isinstance(pref_dict["bar"], str)
        else:
            assert isinstance(pref_dict["bar"], dict)
            assert pref_dict["bar"]["@prefix"] is True
    else:
        assert len(pref_dict) == 1
        assert "xsd" in pref_dict
