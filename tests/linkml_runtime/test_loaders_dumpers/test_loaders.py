import os
from pathlib import Path
from typing import Optional, TextIO, Union

import pytest
from hbreader import FileInfo

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import RDFLoader, json_loader, rdf_loader, yaml_loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.test_loaders_dumpers import LD_11_DIR, LD_11_SSL_SVR, LD_11_SVR
from tests.test_loaders_dumpers.environment import env
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.test_loaders_dumpers.models.termci_schema import Package


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
    REPO_ROOT = Path(__file__).parent.parent.parent
    path = REPO_ROOT / "tests" / "test_loaders_dumpers" / "input" / "obo_sample.json"
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


@pytest.mark.skip(reason="This test will not work until https://github.com/digitalbazaar/pyld/issues/149 is fixed")
def test_rdf_loader(context_server):
    """Load obo_sample.ttl and obo_sample.jsonld, emit yaml and check the results"""
    if context_server == LD_11_DIR:
        pytest.skip("*****> Loading skipped until JSON-LD processor can handle non-http files")

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
