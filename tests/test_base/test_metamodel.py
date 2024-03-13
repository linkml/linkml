import unittest
from typing import List

import pytest
from pyshex.shex_evaluator import EvaluationResult

from linkml import LOCAL_METAMODEL_LDCONTEXT_FILE, LOCAL_METAMODEL_YAML_FILE, METAMODEL_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.shexgen import ShExGenerator
from tests import SKIP_MARKDOWN_VALIDATION, SKIP_MARKDOWN_VALIDATION_REASON
from tests.test_base.environment import env
from tests.utils.compare_rdf import compare_rdf
from tests.utils.filters import ldcontext_metadata_filter, metadata_filter
from tests.utils.generatortestcase import GeneratorTestCase
from tests.utils.python_comparator import compare_python


class MetaModelTestCase(GeneratorTestCase):
    env = env
    model_name = "meta"

    @pytest.mark.slow
    @unittest.skipIf(SKIP_MARKDOWN_VALIDATION, SKIP_MARKDOWN_VALIDATION_REASON)
    def test_meta_markdown(self):
        """Test the markdown generator for the biolink model"""
        self.directory_generator(
            "docs",
            MarkdownGenerator,
            serialize_args=dict(image_dir="images"),
            input_file=LOCAL_METAMODEL_YAML_FILE,
        )

    @pytest.mark.slow
    def test_meta_owl_schema(self):
        """Test the owl schema generator for the linkml model"""
        self.single_file_generator(
            "owl",
            OwlSchemaGenerator,
            comparator=compare_rdf,
            yaml_file=LOCAL_METAMODEL_YAML_FILE,
        )

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

    @pytest.mark.slow
    def test_meta_shexc(self):
        """Test the shex ShExC generation"""
        self.single_file_generator("shex", ShExGenerator, format="shex", yaml_file=LOCAL_METAMODEL_YAML_FILE)

    @pytest.mark.slow
    def test_meta_shecj(self):
        """Test the shex ShExJ generation"""
        self.single_file_generator("shexj", ShExGenerator, format="json", yaml_file=LOCAL_METAMODEL_YAML_FILE)

    @pytest.mark.slow
    def test_meta_rdf(self):
        """Test the rdf generator for the biolink model"""

        # Make a fresh copy of the RDF and validate it as well
        self.single_file_generator(
            "ttl",
            RDFGenerator,
            serialize_args={"context": LOCAL_METAMODEL_LDCONTEXT_FILE},
            comparator=compare_rdf,
            yaml_file=LOCAL_METAMODEL_YAML_FILE,
        )

        # Validate the RDF against the Biolink ShEx
        # TODO: re-enable this or add a new shex comparator
        # if DO_SHEX_VALIDATION:
        #     g = Graph()
        #     rdf_file = LOCAL_RDF_FILE_NAME
        #     g.load(rdf_file, format='turtle')
        #     focus = METAMODEL_NAMESPACE.metamodel
        #     start = METAMODEL_NAMESPACE.SchemaDefinition
        #     results = ShExEvaluator(g, LOCAL_SHEXJ_FILE_NAME, focus, start).evaluate(debug=False)
        #     self.assertTrue(self._evaluate_shex_results(results))
        # else:
        #     print("*** RDF Model validation step was skipped. Set: tests.__init__.DO_SHEX_VALIDATION to run it")

    @pytest.mark.slow
    def test_metamodel_context(self):
        """Build meta.context.jsonld"""
        self.model_name = "meta"
        self.single_file_generator(
            "context.jsonld",
            ContextGenerator,
            yaml_file=LOCAL_METAMODEL_YAML_FILE,
            serialize_args=dict(base=METAMODEL_NAMESPACE),
            filtr=ldcontext_metadata_filter,
        )

    @pytest.mark.slow
    def test_metamodel_python(self):
        """Build meta.py"""
        self.env.generate_single_file(
            "meta.py",
            lambda: PythonGenerator(env.meta_yaml, importmap=env.import_map, genmeta=True).serialize(),
            value_is_returned=True,
            filtr=metadata_filter,
            comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path("meta.py")),
            use_testing_root=True,
        )


if __name__ == "__main__":
    unittest.main()
