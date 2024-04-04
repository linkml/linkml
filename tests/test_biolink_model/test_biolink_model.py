import sys
from pathlib import Path

import pytest
from linkml_runtime.utils.compile_python import compile_python
from rdflib import Namespace

from linkml.generators.csvgen import CsvGenerator
from linkml.generators.golrgen import GolrSchemaGenerator
from linkml.generators.graphqlgen import GraphqlGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.namespacegen import NamespaceGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.protogen import ProtoGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.shexgen import ShExGenerator

BIOLINK_NS = Namespace("https://w3id.org/biolink/vocab/")


@pytest.mark.slow
@pytest.mark.parametrize(
    "generator,extension,gen_kwargs,serialize_kwargs",
    [
        # (MarkdownGenerator, "markdown", {}, {"image_dir": False}),
        (OwlSchemaGenerator, ".owl.ttl", {"useuris": False}, {}),
        pytest.param(
            RDFGenerator,
            ".ttl",
            {},
            {},
            marks=pytest.mark.skipif(
                sys.version_info < (3, 9),
                reason="prefix expansion issue. see: https://github.com/RDFLib/rdflib/issues/2606.",
            ),
        ),
        (ContextGenerator, ".context.jsonld", {"useuris": False}, {}),
        (JSONLDGenerator, ".json", {}, {}),
        (PythonGenerator, ".py", {}, {}),
        (CsvGenerator, ".tsv", {"format": "tsv"}, {}),
        # (DotGenerator, "graphviz", {}, {}),
        (GolrSchemaGenerator, "golr", {}, {}),
        (GraphqlGenerator, ".graphql", {}, {}),
        (JsonSchemaGenerator, ".schema.json", {}, {}),
        (ProtoGenerator, ".proto", {}, {}),
        (NamespaceGenerator, ".namespace.py", {"emit_metadata": True}, {}),
        (ShExGenerator, ".shex", {}, {}),
        (ShExGenerator, ".shexj", {"format": "json"}, {}),
        (ShExGenerator, ".native.shex", {"useuris": False}, {}),
    ],
)
def test_biolink(generator, extension, gen_kwargs, serialize_kwargs, temp_dir, snapshot, input_path):
    BIOLINK_YAML = input_path("biolink-model.yaml")
    if not extension.startswith("."):
        # is a directory!
        output_dir = Path(extension) / "biolink"
        generator(BIOLINK_YAML, directory=str(temp_dir), **gen_kwargs).serialize(
            directory=str(temp_dir), **serialize_kwargs
        )
        assert temp_dir == snapshot(str(output_dir))
    else:
        generated = generator(BIOLINK_YAML, **gen_kwargs).serialize(**serialize_kwargs)
        output_file = "biolink" + extension
        if extension.endswith(".py"):
            compile_python(generated, "test")
        assert generated == snapshot(output_file)


@pytest.mark.skip("Needs to be refactored for snapshot rather than unittest")
def test_biolink_correct_rdf():
    """Test some conforming RDF"""
    # self.single_file_generator("shexj", ShExGenerator, format="json")  # Make sure ShEx is current
    #
    # shex_file = env.expected_path("biolink-model.shexj")
    #
    # focus = "http://identifiers.org/drugbank:DB00005"
    # start = BIOLINK_NS.Drug
    # evaluator = ShExEvaluator(None, shex_file, focus, start)
    #
    # rdf_file = env.input_path("probe.ttl")
    # results = evaluator.evaluate(rdf_file, debug=False)
    # self.assertTrue(self._evaluate_shex_results(results))
