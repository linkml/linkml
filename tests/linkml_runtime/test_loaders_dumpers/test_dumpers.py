import os
import unittest
from typing import cast

from rdflib import Namespace, SKOS, Literal

from linkml_runtime.dumpers import yaml_dumper, json_dumper, rdf_dumper
from linkml_runtime.utils.yamlutils import as_json_object
from tests.support.clicktestcase import ClickTestCase
from tests.test_loaders_dumpers import LD_11_DIR, LD_11_SSL_SVR, LD_11_SVR, HTTP_TEST_PORT, HTTPS_TEST_PORT, \
    GITHUB_LD10_CONTEXT, GITHUB_LD11_CONTEXT
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.test_loaders_dumpers.models.termci_schema import ConceptReference, ConceptSystem, Package

OBO = Namespace("http://purl.obolibrary.org/obo/")
NCIT = Namespace("http://purl.obolibrary.org/obo/NCI_")


class DumpersTestCase(LoaderDumperTestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        """ Generate a small sample TermCI instance for testing purposes """
        LoaderDumperTestCase.setUpClass()
        e1 = ConceptReference(OBO.NCI_C147796, code="C147796", defined_in=OBO,
                              designation="TSCYC - Being Frightened of Men",
                              definition="Trauma Symptom Checklist for Young Children (TSCYC) Please indicate how often"
                                         " the child has done, felt, or experienced each of the following things in "
                                         "the last month: Being frightened of men.",
                              narrower_than=OBO.NCI_C147557, reference=OBO.NCI_C147796)
        e2 = ConceptReference(OBO.NCI_C147557, code="C147557", defined_in=OBO,
                              designation="TSCYC Questionnaire Question",
                              definition="A question associated with the TSCYC questionnaire.",
                              narrower_than=OBO.NCI_C91102)
        c1 = ConceptSystem(OBO, "OBO", contents=[e1, e2])
        cls.test_package = Package([c1])

    def test_yaml_dumper(self):
        """ Test the yaml emitter """
        # TODO: Once this is entered into the BiolinkML test package, compare this to input/obo_test.yaml
        self.dump_test('obo_sample.yaml', lambda out_fname: yaml_dumper.dump(self.test_package, out_fname))
        self.dumps_test('obo_sample.yaml', lambda: yaml_dumper.dumps(self.test_package))

    def test_json_dumper(self):
        """ Test the json emitter """
        # TODO: Same as test_yaml_dumper
        self.dump_test('obo_sample.json', lambda out_fname: json_dumper.dump(self.test_package, out_fname))

        obo_json_obj = cast(Package, as_json_object(self.test_package))
        self.assertEqual(OBO, obo_json_obj.system[0].namespace)
        self.assertEqual('C147796', obo_json_obj.system[0].contents[0].code)

        self.dumps_test('obo_sample.json', lambda: json_dumper.dumps(self.test_package))
        self.dump_test('obo_sample_context.json',
                       lambda out_fname: json_dumper.dump(self.test_package, out_fname,
                                                          GITHUB_LD10_CONTEXT + 'termci_schema.context.jsonld'))
        self.dumps_test('obo_sample_context.json',
                        lambda: json_dumper.dumps(self.test_package,
                                                  GITHUB_LD11_CONTEXT + 'termci_schema_inlined.context.jsonld'))

    @unittest.skipIf(True, "This needs an enhanced (https://github.com/hsolbrig/pyld) version of pyld")
    def test_rdf_dumper(self):
        """ Test the rdf dumper """
        contexts = os.path.join(LD_11_DIR, 'termci_schema_inlined.context.jsonld')
        self.dump_test('obo_sample.ttl', lambda out_file: rdf_dumper.dump(self.test_package, out_file, contexts),
                       comparator=ClickTestCase.rdf_comparator)

        g = rdf_dumper.as_rdf_graph(self.test_package, contexts)
        self.assertIn(OBO[''], g.subjects())
        self.assertIn(NCIT.C147796, g.subjects())
        self.assertIn(Literal('C147796'), g.objects(NCIT.C147796, SKOS.notation))

        self.dumps_test('obo_sample.ttl', lambda: rdf_dumper.dumps(self.test_package, contexts),
                        comparator=ClickTestCase.rdf_comparator)

        # Build a vanilla jsonld image for subsequent testing
        fname = 'obo_sample.jsonld'
        self.dump_test(fname, lambda out_file: rdf_dumper.dump(self.test_package, out_file, contexts, fmt='json-ld'),
                       comparator=lambda e, a: ClickTestCase.rdf_comparator(e, a, fmt='json-ld'))
        with open(self.env.expected_path('dump', fname)) as f:
            txt = f.read()
        with open(self.env.input_path('obo_sample.jsonld'), 'w') as f:
            f.write(txt)


    @unittest.skip("Waiting until PyLD learns to handle relative context URI's")
    def test_nested_contexts(self):
        """ Test JSON-LD with fully nested contexts """

        context_servers = []
        for possible_server in [LD_11_SVR, LD_11_SSL_SVR]:
            svr = self.check_context_servers([possible_server])
            if svr:
                context_servers.append(svr)

        if not context_servers:
            raise unittest.SkipTest(f"*****> Nested contexts test skipped - no servers found on sockets "
                                    f"{HTTP_TEST_PORT} or {HTTPS_TEST_PORT}")

        for context_base in context_servers:
            nested_context = context_base + 'Package.context.jsonld'
            self.dump_test('obo_sample_nested.ttl', lambda out_file: rdf_dumper.dump(self.test_package, out_file,
                                                                                     nested_context))
            self.dumps_test('obo_sample_nested.ttl', lambda: rdf_dumper.dumps(self.test_package, nested_context))


if __name__ == '__main__':
    unittest.main()
