import os
import unittest
from typing import Union, TextIO, Optional
from pathlib import Path
from hbreader import FileInfo

from linkml_runtime.loaders import yaml_loader, json_loader, rdf_loader, RDFLoader
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.test_loaders_dumpers import LD_11_SVR, LD_11_SSL_SVR, LD_11_DIR
from tests.test_loaders_dumpers.environment import env
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.test_loaders_dumpers.models.termci_schema import Package


class LoadersUnitTest(LoaderDumperTestCase):
    env = env

    @classmethod
    def setUpClass(cls) -> None:
        cls.context_server = cls.check_context_servers([LD_11_SVR, LD_11_SSL_SVR])
        if not cls.context_server:
            cls.context_server = LD_11_DIR

    def test_yaml_loader(self):
        """ Load obo_sample.yaml, emit obo_sample_yaml.yaml and compare to obo_sample_output.yaml """
        self.loader_test('obo_sample.yaml', Package, yaml_loader)

    def test_json_loader_path(self):
        """ Load obo_sample.json, emit obo_sample_json.yaml and check the results """
        REPO_ROOT = Path(__file__).parent.parent.parent
        path = REPO_ROOT / "tests" /  "test_loaders_dumpers" / "input" / "obo_sample.json"
        data = json_loader.load(Path(path), Package, base_dir=self.env.indir)
        assert isinstance(data, Package)
        assert "system" in data

    def test_json_loader(self):
        """ Load obo_sample.json, emit obo_sample_json.yaml and check the results """
        self.loader_test('obo_sample.json', Package, json_loader)

    def test_json_load_to_dict(self):
        data = json_loader.load_as_dict('obo_sample.json', base_dir=self.env.indir)
        assert isinstance(data, dict)
        assert "system" in data

    def test_yaml_load_to_dict(self):
        data = yaml_loader.load_as_dict('obo_sample.yaml', base_dir=self.env.indir)
        assert isinstance(data, dict)
        assert "system" in data

    @unittest.skipIf(True, "This test will not work until https://github.com/digitalbazaar/pyld/issues/149 is fixed")
    def test_rdf_loader(self):
        """ Load obo_sample.ttl, emit obo_sample_ttl.yaml and check the results
            Load obo_sample.jsonld, emit obo_sample_jsonld.yaml and check the results
        """
        if self.context_server == LD_11_DIR:
            raise unittest.SkipTest("*****> Loading skipped until JSON-LD processor can handle non-http files")

        contexts = os.path.join(self.context_server, 'termci_schema_inlined.context.jsonld')
        fmt = 'turtle'

        class RDFLoaderWrapper(RDFLoader):
            def load(self, source: Union[str, dict, TextIO], target_class: type[YAMLRoot], *,
                     base_dir: Optional[str] = None, metadata: Optional[FileInfo] = None, **_) -> YAMLRoot:
                return rdf_loader.load(source, target_class, base_dir=LoadersUnitTest.env.indir, fmt=fmt,
                                       metadata=metadata, contexts=contexts)

            def loads(self, source: str, target_class: type[YAMLRoot], *, metadata: Optional[FileInfo] = None, **_) \
                    -> YAMLRoot:
                return rdf_loader.loads(source, target_class, contexts=contexts, fmt=fmt, metadata=metadata)

        self.loader_test('obo_sample.ttl', Package, RDFLoaderWrapper())
        fmt = 'json-ld'
        self.loader_test('obo_sample.jsonld', Package, RDFLoaderWrapper())


if __name__ == '__main__':
    unittest.main()
