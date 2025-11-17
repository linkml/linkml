from pathlib import PurePath

import pytest
from jsonasobj2 import loads
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.yamlutils import as_rdf

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.pythongen import PythonGenerator
from tests.utils.compare_jsonld_context import CompareJsonldContext


@pytest.mark.jsonldgen
@pytest.mark.jsonldcontextgen
@pytest.mark.pythongen
def test_uri_and_curie(input_path, snapshot, snapshot_path):
    """Compile a model of URI's and Curies and then test the various types"""
    model_name = "uriandcurie"
    model_path = input_path(f"{model_name}.yaml")

    pythongen_output = PythonGenerator(model_path).serialize()
    assert pythongen_output == snapshot(f"{model_name}.py")

    # Check that the interpretations are correct
    contextgen_output = ContextGenerator(model_path).serialize()
    CompareJsonldContext.compare_with_snapshot(contextgen_output, snapshot_path(f"{model_name}.jsonld"))

    jsonldgen_output = JSONLDGenerator(model_path).serialize(context_kwargs={"model": True})
    assert jsonldgen_output == snapshot(f"{model_name}.json")

    module = compile_python(pythongen_output)

    curie_obj = module.C1(
        "ex:obj1",
        hasCurie="ex:curie",
        hasURI="http://example.org/test/uri",
        hasNcName="A123",
        id2="ex:id2",
    )
    instance_jsonld = loads('{ "ex": "http://example.org/test/inst#" }')

    g = as_rdf(
        curie_obj,
        [
            PurePath(input_path(f"{model_name}.jsonld")).as_uri(),
            instance_jsonld,
        ],
    )
    assert g.serialize(format="ttl") == snapshot(f"{model_name}.ttl")
