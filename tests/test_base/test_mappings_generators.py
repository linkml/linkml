import os
import unittest
from typing import List

from pyshex.shex_evaluator import EvaluationResult

from linkml import LOCAL_MAPPINGS_YAML_FILE, LOCAL_METAMODEL_LDCONTEXT_FILE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from tests import SKIP_MARKDOWN_VALIDATION, SKIP_MARKDOWN_VALIDATION_REASON
from tests.utils.generatortestcase import GeneratorTestCase
from tests.test_base.environment import env
from tests.utils.filters import metadata_filter, ldcontext_metadata_filter, json_metadata_context_filter
from tests.utils.python_comparator import compare_python


class MappingsGeneratorTestCase(GeneratorTestCase):
    """ Validate that mappings are available on both a meta and a model level basis """
    model_name = 'mappings'
    env = env

    # Note: this test overlaps w/ test_gen_python. If you re-enable this, you need to get the parameters correct
    # def test_mappings_in_metamodel(self):
    #     """ Generate a copy of mappyings.py """
    #     self.single_file_generator('py', PythonGenerator, subdir='includes', filtr=metadata_filter,
    #                                comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('mappings.py')))
    @unittest.skipIf(SKIP_MARKDOWN_VALIDATION, SKIP_MARKDOWN_VALIDATION_REASON)
    def test_mappings_markdown(self):
        """ Generate documentation for the meta_mappings  """
        self.directory_generator('meta_mappings_docs', MarkdownGenerator, input_file=LOCAL_MAPPINGS_YAML_FILE)

    @staticmethod
    def _evaluate_shex_results(results: List[EvaluationResult]) -> bool:
        """
        Check the results of the ShEx evaluation
        :param results: evaluate output
        :return: success indicator
        """
        success = all(r.result for r in results)
        if not success:
            for r in results:
                if not r.result:
                    print(r.reason)
        return success

    @unittest.skip("test_base/test_mappings_generators.py: This test needs upgrading to latest harness")
    def test_mappings_rdf(self):
        """ Test the imported mappings in the biolink metamodel """
        test_dir = self.env.temp_file_path('mappings_rdf_test', is_dir=True)

        # Create the mappings json file
        json_file = os.path.join(test_dir, 'mappings.jsonld')
        json_str = JSONLDGenerator(env.meta_yaml, importmap=env.import_map).serialize()
        with open(json_file, 'w') as f:
            f.write(json_str)

        # Create the mappings context file
        context_file = os.path.join(test_dir, 'mappings.context.jsonld')
        ContextGenerator(env.meta_yaml, importmap=env.import_map).serialize(output=context_file)
        self.assertTrue(os.path.exists(context_file))

        # Generate context and use it to create the RDF
        self.single_file_generator(LOCAL_METAMODEL_LDCONTEXT_FILE, ContextGenerator, filtr=ldcontext_metadata_filter,
                                   subdir='includes')

        # Generate a copy of the JSON representation of the model
        context_loc = json_file
        context_args = {"context": ['file://' + LOCAL_METAMODEL_LDCONTEXT_FILE, 'file://' + context_loc]}
        msg = ''
        msg += self.single_file_generator('json', JSONLDGenerator,  serialize_args=context_args,
                                         filtr=json_metadata_context_filter, fail_if_expected_missing=False)

        # Make a fresh copy of the RDF and validate it as well
        msg += self.single_file_generator('ttl', RDFGenerator, serialize_args=context_args,
                                          comparator=GeneratorTestCase.rdf_comparator, fail_if_expected_missing=False)
        if msg:
            self.fail(msg)

        g = Graph()
        rdf_file = os.path.join(sourcedir, 'meta_mappings.ttl')
        g.load(rdf_file, format='turtle')
        ns = PrefixLibrary()
        ns.add_rdf(g)
        ns['FULL'] = "http://example.org/fulluri/"
        ns['EX'] = "http://example.org/mappings/"
        ns['META'] = "https://w3id.org/linkml/meta/"
        # Make sure that the expected triples got added

        self.assertEqual({ns.EX.slot1_close, ns.FULL.slot1_close}, set(g.objects(ns.EX.s1, ns.SKOS.closeMatch)))
        self.assertEqual({ns.EX.slot1, ns.FULL.slot1}, set(g.objects(ns.EX.s1, ns.SKOS.exactMatch)))
        self.assertEqual(ns.EX.s3, g.value(ns.EX.s1, ns.META.deprecated_element_has_exact_replacement, any=False))
        self.assertEqual(ns.EX.s4, g.value(ns.EX.s1, ns.META.deprecated_element_has_possible_replacement, any=False))

        self.assertEqual({ns.EX.class1_close, ns.FULL.class1_close}, set(g.objects(ns.EX.C1, ns.SKOS.closeMatch)))
        self.assertEqual({ns.EX.class1, ns.FULL.class1}, set(g.objects(ns.EX.C1, ns.SKOS.exactMatch)))
        self.assertEqual(ns.EX.c2, g.value(ns.EX.C1, ns.META.deprecated_element_has_exact_replacement, any=False))
        self.assertEqual(ns.EX.c3, g.value(ns.EX.C1, ns.META.deprecated_element_has_possible_replacement, any=False))
        if DO_SHEX_VALIDATION:
            EX = Namespace("http://example.org/mappings/")
            focus = EX.testMetamodelMappings
            start = METAMODEL_NAMESPACE.SchemaDefinition
            results = ShExEvaluator(g, LOCAL_SHEXJ_FILE_NAME, focus, start).evaluate(debug=False)
            self.assertTrue(self._evaluate_shex_results(results))
        else:
            print("*** RDF Model validation step was skipped. Set: tests.__init__.DO_SHEX_VALIDATION to run it")


if __name__ == '__main__':
    unittest.main()
