import os
import unittest
from types import ModuleType

from jsonasobj2 import loads

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.yamlutils import as_rdf
from tests.test_utils.environment import env
from tests.utils.filters import ldcontext_metadata_filter, metadata_filter, json_metadata_filter


from tests.utils.generatortestcase import GeneratorTestCase
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.compare_rdf import compare_rdf


# Note: GeneratorTestCase is the
class URIAndCurieTestCase(GeneratorTestCase):
    model_name: str = 'uriandcurie'
    env = env

    def test_uri_and_curie(self):
        """ Compile a model of URI's and Curies and then test the various types """
        self.single_file_generator('py', PythonGenerator, filtr=metadata_filter,
                                   comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('foo.py')))

        # Check that the interpretations are correct
        self.single_file_generator('jsonld', ContextGenerator, filtr=ldcontext_metadata_filter,
                                   comparator=lambda expected, actual: compare_rdf(expected, actual, fmt="json-ld"))
        self.single_file_generator('json', JSONLDGenerator, filtr=json_metadata_filter)

        module = compile_python(env.expected_path(self.model_name + '.py'))

        curie_obj = module.C1("ex:obj1",
                              hasCurie="ex:curie",
                              hasURI="http://example.org/test/uri",
                              hasNcName="A123",
                              id2="ex:id2")
        instance_jsonld = loads('{ "ex": "http://example.org/test/inst#" }')

        g = as_rdf(curie_obj, [env.input_path(self.model_name + '.jsonld'), instance_jsonld])
        env.eval_single_file(env.expected_path('uriandcurie.ttl'), g.serialize(format='ttl').decode(), lambda s: s,
                             compare_rdf)


if __name__ == '__main__':
    unittest.main()
