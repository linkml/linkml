import os
import re
import unittest
from typing import List

from pyshex import ShExEvaluator
from pyshex.shex_evaluator import EvaluationResult
from rdflib import Graph, Namespace

from linkml import METAMODEL_NAMESPACE, MODULE_DIR
from linkml.generators.csvgen import CsvGenerator
from linkml.generators.dotgen import DotGenerator
from linkml.generators.golrgen import GolrSchemaGenerator
from linkml.generators.graphqlgen import GraphqlGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.prefixmapgen import PrefixGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from linkml.generators.namespacegen import NamespaceGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.protogen import ProtoGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml_runtime.utils.context_utils import parse_import_map
from linkml_runtime.utils.formatutils import shex_results_as_string
from tests import SKIP_GRAPHVIZ_VALIDATION, SKIP_MARKDOWN_VALIDATION, SKIP_SHEX_VALIDATION, SKIP_SHEX_VALIDATION_REASON, \
    SKIP_MARKDOWN_VALIDATION_REASON
from tests.test_biolink_model.environment import env
from tests.utils.compare_rdf import compare_rdf
from tests.utils.filters import metadata_filter
from tests.utils.generatortestcase import GeneratorTestCase
from tests.utils.python_comparator import compare_python


BIOLINK_NS = Namespace("https://w3id.org/biolink/vocab/")


class CurrentBiolinkModelTestCase(GeneratorTestCase):
    env = env
    model_name = 'biolink-model'
    importmap = parse_import_map(env.input_path('biolink-model-map.json'), MODULE_DIR)

    biolink_yaml = env.input_path('biolink-model.yaml')

    def test_biolink_python(self):
        """ Test the python generator for the biolink model """
        self.single_file_generator('py', PythonGenerator, filtr=metadata_filter,
                                   comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('py')),
                                   output_name='model')

    @unittest.skipIf(SKIP_MARKDOWN_VALIDATION, SKIP_MARKDOWN_VALIDATION_REASON)
    def test_biolink_markdown(self):
        """ Test the markdown generator for the biolink model """
        self.directory_generator('markdown_no_image', MarkdownGenerator, serialize_args=dict(image_dir=False))
        # self.directory_generator('markdown_image', MarkdownGenerator, serialize_args=dict(image_dir=True))

    def test_biolink_tsv(self):
        """ Test the tsv generator for the biolink model """
        def filtr(s: str) -> str:
            return s.replace('\r\n', '\n')

        self.single_file_generator('tsv', CsvGenerator, format="tsv", filtr=filtr)

    @unittest.skipIf(SKIP_GRAPHVIZ_VALIDATION, SKIP_SHEX_VALIDATION_REASON)
    def test_biolink_graphviz(self):
        """ Test the dotty generator for the biolink model """
        # We don't do the comparison step because different graphviz libraries generate slightly different binary output
        # We also don't commit the results -- the graphviz output is in .gitignore
        self.directory_generator('graphviz', DotGenerator)

    def test_biolink_golr(self):
        """ Test the golr schema generator for the biolink model """
        self.directory_generator('golr', GolrSchemaGenerator)

    def test_biolink_graphql(self):
        """ Test the graphql schema generator for the biolink model """
        self.single_file_generator('graphql', GraphqlGenerator)

    def test_biolink_jsonld(self):
        """ Test the jsonld schema generator for the biolink model """
        def filtr(s: str) -> str:
            return re.sub(r'"source_file_date": ".*?",', '"source_file_date": "2019-01-01-12:00",',
                          re.sub(r'"generation_date": ".*?",', '"generation_date": "2019-01-01 12:00",', s))

        self.single_file_generator('jsonld', JSONLDGenerator, filtr=filtr)

    def test_biolink_context(self):
        """ Test the jsonld context generator for the biolink model """
        def filtr(s: str) -> str:
            return re.sub(r'Generation date: .*?\\n', r'Generation date: \\n',
                          re.sub(r' version: .*?\\n', r' version: \\n', s))

        self.single_file_generator('context.jsonld', ContextGenerator, filtr=filtr)
        # Generate a second copy with native identifiers
        self.single_file_generator('model.context.jsonld', ContextGenerator, generator_args=dict(useuris=False),
                                   filtr=filtr)

    def test_biolink_json_schema(self):
        """ Test the jsonld context generator for the biolink model """
        self.single_file_generator('schema.json', JsonSchemaGenerator)

    def test_biolink_owl_schema(self):
        """ Test the owl schema generator for the biolink model """
        self.single_file_generator('owl.ttl', OwlSchemaGenerator, comparator=compare_rdf)
        # Generate a second copy with native identifiers
        self.single_file_generator('model.owl.ttl', OwlSchemaGenerator, generator_args=dict(useuris=False),
                                   comparator=compare_rdf)

    def test_biolink_proto(self):
        """ Test the proto schema generator for the biolink model """
        self.single_file_generator('proto', ProtoGenerator)

    def test_biolink_namespaces(self):
        """ Test the python generator for the biolink model """
        self.output_name = 'namespaces'
        self.single_file_generator('py', NamespaceGenerator, generator_args={'emit_metadata': True},
                                   filtr=metadata_filter,
                                   comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('namespaces.py')),
                                   output_name='namespaces')


    @staticmethod
    def _evaluate_shex_results(results: List[EvaluationResult], printit: bool=True) -> bool:
        """
        Check the results of the ShEx evaluation
        :param results: evaluate output
        :return: success indicator
        """
        success = all(r.result for r in results)
        if not success and printit:
            for r in results:
                if not r.result:
                    print(r.reason)
        return success

    def test_biolink_rdf(self):
        """ Test the rdf generator for the biolink model """
        self.single_file_generator('ttl', RDFGenerator, comparator=compare_rdf)

        # Validate the RDF against the Biolink ShEx
        if SKIP_SHEX_VALIDATION:
            print(f'* test_biolink_rdf: {SKIP_SHEX_VALIDATION_REASON}')
        else:
            g = Graph()
            g.load(env.expected_path('biolink_model.ttl'), format='ttl')
            focus = BIOLINK_NS.biolink_model
            start = METAMODEL_NAMESPACE.SchemaDefinition
            results = ShExEvaluator(g, env.expected_path('biolink_model.shexj'), focus, start).evaluate(debug=False)
            self.assertTrue(self._evaluate_shex_results(results))

    def test_biolink_shex(self):
        """ Just Generate the ShEx file untested """
        self.single_file_generator('shex', ShExGenerator)
        self.single_file_generator('shexj', ShExGenerator, format='json')
        # Generate native ShEx
        self.single_file_generator('native.shex', ShExGenerator, generator_args=dict(useuris=False))
        self.single_file_generator('native.shexj', ShExGenerator, format='json', generator_args=dict(useuris=False))

    @unittest.skip("This test needs revision to meet new testing structure")
    def test_biolink_shex_incorrect_rdf(self):
        """ Test some non-conforming RDF  """
        self.single_file_generator('shexj', ShExGenerator, format='json')
        shex_file = env.expected_path('biolink-model.shexj')

        focus = "http://identifiers.org/drugbank:DB00005"
        start = BIOLINK_NS.Drug
        evaluator = ShExEvaluator(None, shex_file, focus, start)

        # incorrect.ttl has 16 error lines (more or less).
        rdf_file = env.temp_file_path('incorrect.ttl')
        errs_file = env.temp_file_path('incorrect.errs')
        results = evaluator.evaluate(rdf_file)
        self.assertFalse(self._evaluate_shex_results(results, printit=False))
        self.assertEqual(1, len(results))
        self.assertTrue('Unmatched triples in CLOSED shape' in results[0].reason)
        ntabs = results[0].reason.count('\n\t')
        self.assertEqual(13, ntabs)
        if not os.path.exists(errs_file):
            with open(errs_file, 'w') as f:
                f.write(shex_results_as_string(results[0]))
        # TODO:
        #     self.assertTrue(False, f"{errs_file} created - run test again")
        # else:
        #     with open(errs_file) as f:
        #         expected = f.read()
        #     self.assertEqual(expected, shex_results_as_string(results[0]))

    @unittest.skipIf(SKIP_SHEX_VALIDATION, SKIP_SHEX_VALIDATION_REASON)
    def test_biolink_correct_rdf(self):
        """ Test some conforming RDF  """
        self.single_file_generator('shexj', ShExGenerator, format='json')  # Make sure ShEx is current

        shex_file = env.expected_path('biolink-model.shexj')

        focus = "http://identifiers.org/drugbank:DB00005"
        start = BIOLINK_NS.Drug
        evaluator = ShExEvaluator(None, shex_file, focus, start)

        rdf_file = env.input_path('probe.ttl')
        results = evaluator.evaluate(rdf_file, debug=False)
        self.assertTrue(self._evaluate_shex_results(results))


if __name__ == '__main__':
    unittest.main()
