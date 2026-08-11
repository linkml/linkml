import json
import os
from pathlib import Path
from typing import ClassVar, Optional, TextIO, Union

import pytest
from hbreader import FileInfo
from pydantic import BaseModel

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import RDFLoader, json_loader, rdf_loader, yaml_loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.linkml_runtime.test_loaders_dumpers import LD_11_DIR, LD_11_SSL_SVR, LD_11_SVR
from tests.linkml_runtime.test_loaders_dumpers.environment import env
from tests.linkml_runtime.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.linkml_runtime.test_loaders_dumpers.models.termci_schema import Package


def loader_test(filename: str, model: Union[type[YAMLRoot], type], loader) -> None:
    """
    Standalone loader test function for pytest functions
    """

    # Create a test case instance to use the loader_test method
    test_case = LoaderDumperTestCase()
    test_case.env = env
    test_case.loader_test(filename, model, loader)


@pytest.fixture(scope="module")
def context_server():
    """Set up context server for testing."""
    # Check context servers - this mimics the original setUpClass logic
    context_server = LoaderDumperTestCase.check_context_servers([LD_11_SVR, LD_11_SSL_SVR])
    if not context_server:
        context_server = LD_11_DIR
    return context_server


def test_yaml_loader():
    loader_test("obo_sample.yaml", Package, yaml_loader)


def test_json_loader_path():
    """Load obo_sample.json using Path object and check the results"""
    REPO_ROOT = Path(__file__).parent.parent.parent.parent
    path = REPO_ROOT / "tests" / "linkml_runtime" / "test_loaders_dumpers" / "input" / "obo_sample.json"
    data = json_loader.load(Path(path), Package, base_dir=env.indir)
    assert isinstance(data, Package)
    assert "system" in data


def test_json_loader():
    """Load obo_sample.json, emit obo_sample_json.yaml and check the results"""
    loader_test("obo_sample.json", Package, json_loader)


def test_json_load_to_dict():
    """Test loading JSON file as dictionary"""
    data = json_loader.load_as_dict("obo_sample.json", base_dir=env.indir)
    assert isinstance(data, dict)
    assert "system" in data


def test_yaml_load_to_dict():
    """Test loading YAML file as dictionary"""
    data = yaml_loader.load_as_dict("obo_sample.yaml", base_dir=env.indir)
    assert isinstance(data, dict)
    assert "system" in data


@pytest.mark.integration
def test_rdf_loader(context_server):
    """Load obo_sample.ttl and obo_sample.jsonld, emit yaml and check the results"""
    if context_server == LD_11_DIR:
        pytest.skip("local context server required - start docker server per jsonld_context/README.md")

    contexts = os.path.join(context_server, "termci_schema_inlined.context.jsonld")
    fmt = "turtle"

    class RDFLoaderWrapper(RDFLoader):
        def load(
            self,
            source: Union[str, dict, TextIO],
            target_class: type[YAMLRoot],
            *,
            base_dir: Optional[str] = None,
            metadata: Optional[FileInfo] = None,
            **_,
        ) -> YAMLRoot:
            return rdf_loader.load(
                source,
                target_class,
                base_dir=env.indir,
                fmt=fmt,
                metadata=metadata,
                contexts=contexts,
            )

        def loads(
            self, source: str, target_class: type[YAMLRoot], *, metadata: Optional[FileInfo] = None, **_
        ) -> YAMLRoot:
            return rdf_loader.loads(source, target_class, contexts=contexts, fmt=fmt, metadata=metadata)

    loader_test("obo_sample.ttl", Package, RDFLoaderWrapper())
    fmt = "json-ld"
    loader_test("obo_sample.jsonld", Package, RDFLoaderWrapper())


def test_rdf_loader_jsonld_single_node():
    """A JSON-LD document that is a single top-level node is loaded as before."""
    source = json.dumps(
        {
            "@type": "https://hotecosystem.org/termci/Package",
            "system": {"http://example.org/ns1": {"namespace": "http://example.org/ns1", "prefix": "ex"}},
        }
    )
    result = RDFLoader().load(source, Package, fmt="json-ld")
    assert isinstance(result, Package)
    assert [cs.namespace for cs in result.system] == ["http://example.org/ns1"]


def test_rdf_loader_jsonld_graph_array_picks_matching_type():
    """rdflib's json-ld serialization produces a flat array of nodes (a graph). The loader must
    find the node whose @type matches target_class rather than blindly taking the whole array."""
    source = json.dumps(
        [
            {
                "@id": "_:b0",
                "@type": "https://hotecosystem.org/termci/ConceptSystem",
                "system": {"http://example.org/wrong": {"namespace": "http://example.org/wrong", "prefix": "wrong"}},
            },
            {
                "@id": "_:b1",
                "@type": "https://hotecosystem.org/termci/Package",
                "system": {"http://example.org/right": {"namespace": "http://example.org/right", "prefix": "right"}},
            },
        ]
    )
    result = RDFLoader().load(source, Package, fmt="json-ld")
    assert isinstance(result, Package)
    assert [cs.namespace for cs in result.system] == ["http://example.org/right"]


def test_rdf_loader_jsonld_graph_array_matches_type_list():
    """A node's @type may itself be a list of URIs (multiple rdf:type values); a match anywhere
    in that list should be picked."""
    source = json.dumps(
        [
            {
                "@id": "_:b0",
                "@type": [
                    "http://www.w3.org/ns/prov#Entity",
                    "https://hotecosystem.org/termci/Package",
                ],
                "system": {"http://example.org/right": {"namespace": "http://example.org/right", "prefix": "right"}},
            }
        ]
    )
    result = RDFLoader().load(source, Package, fmt="json-ld")
    assert isinstance(result, Package)
    assert [cs.namespace for cs in result.system] == ["http://example.org/right"]


def test_rdf_loader_jsonld_graph_array_no_match_falls_back_to_first_node():
    """If no node's @type matches target_class, fall back to the first dict node in the graph
    rather than dropping the data entirely."""
    source = json.dumps(
        [
            {
                "@id": "_:b0",
                "@type": "https://hotecosystem.org/termci/Something",
                "system": {"http://example.org/only": {"namespace": "http://example.org/only", "prefix": "only"}},
            },
            {"@id": "_:b1", "@type": "https://hotecosystem.org/termci/SomethingElse"},
        ]
    )
    result = RDFLoader().load(source, Package, fmt="json-ld")
    assert isinstance(result, Package)
    assert [cs.namespace for cs in result.system] == ["http://example.org/only"]


def test_rdf_loader_jsonld_empty_graph_array_returns_none():
    """An empty graph array has no node to load and should yield no result rather than erroring."""
    result = RDFLoader().load("[]  ", Package, fmt="json-ld")
    assert result is None


def test_rdf_loader_jsonld_non_dict_non_list_returns_none():
    """A JSON-LD payload that is neither an object nor an array (e.g. a bare scalar) has no
    node data to load."""
    result = RDFLoader().load(json.dumps("not a node"), Package, fmt="json-ld")
    assert result is None


def test_rdf_loader_jsonld_graph_array_matches_pydantic_basemodel_class_uri():
    """Pydantic BaseModel targets expose class identity via linkml_meta['class_uri'] rather than
    the class_class_uri/class_name attributes that only exist on generated YAMLRoot dataclasses.
    The graph-array matcher must use that too, and must not crash on this class shape."""

    class PydanticPackage(BaseModel):
        linkml_meta: ClassVar[dict] = {"class_uri": "https://hotecosystem.org/termci/Package"}
        marker: str = ""

    source = json.dumps(
        [
            {"@id": "_:b0", "@type": "https://hotecosystem.org/termci/Other", "marker": "wrong"},
            {"@id": "_:b1", "@type": "https://hotecosystem.org/termci/Package", "marker": "right"},
        ]
    )
    result = RDFLoader().load(source, PydanticPackage, fmt="json-ld")
    assert isinstance(result, PydanticPackage)
    assert result.marker == "right"


def test_rdf_loader_jsonld_graph_array_null_type_does_not_crash():
    """A node with an explicit `@type: null` must not blow up the graph-array matcher, which
    should treat it as untyped rather than raising."""
    source = json.dumps(
        [
            {"@id": "_:b0", "@type": None, "system": {}},
            {
                "@id": "_:b1",
                "@type": "https://hotecosystem.org/termci/Package",
                "system": {"http://example.org/ns1": {"namespace": "http://example.org/ns1", "prefix": "ex"}},
            },
        ]
    )
    result = RDFLoader().load(source, Package, fmt="json-ld")
    assert isinstance(result, Package)
    assert [cs.namespace for cs in result.system] == ["http://example.org/ns1"]


def test_rdf_loader_jsonld_no_spurious_type_mismatch_warning(capsys):
    """A correctly-typed load should not print an 'input type mismatch' warning just because
    @type carries a full URI rather than the bare class name."""
    source = json.dumps({"@type": "https://hotecosystem.org/termci/Package", "system": {}})
    RDFLoader().load(source, Package, fmt="json-ld")
    assert "mismatch" not in capsys.readouterr().out
