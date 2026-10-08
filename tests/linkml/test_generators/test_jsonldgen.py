import json
import logging

import pytest
from click.testing import CliRunner
from rdflib import Graph, term
from yaml import safe_load

from linkml.generators import JSONLDGenerator, RDFGenerator
from linkml.generators.jsonldgen import cli as jsonld_cli
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)


# network: rdflib fetches the @context URLs in the generated JSON-LD
@pytest.mark.network
def test_class_uri(input_path):
    """`class_uri` should result in an `skos:exactMatch` relationship
    in the generated JSON-LD and RDF."""
    # focusing on the class `Thing` of the schema jsonld_context_class_uri_prefix.yaml:
    # [...]
    #   Thing:
    #     class_uri: rdfs:Resource
    # [...]
    schema_path = str(input_path("jsonld_context_class_uri_prefix.yaml"))

    # get the classes declaring a `class_uri`
    schema_view = SchemaView(schema_path)
    with open(schema_path) as f:
        schema_yaml = safe_load(f)
    classes_with_custom_uri = {}
    for class_name, cls in schema_yaml["classes"].items():
        if "class_uri" in cls.keys():
            # save class
            classes_with_custom_uri[class_name] = {
                "uri": schema_view.get_uri(class_name, expand=True, native=True),
                "class_uri": cls["class_uri"],
            }

    # check generated JSON-LD against following expectation:
    # [...]
    # {
    #   "name": "Thing",
    #   "definition_uri": "http://uri.interlex.org/tgbugs/uris/readable/sparc/Thing",
    #   "from_schema": "https://sparc.olympiangods.org/sparcur/schemas/1/sparc",
    #   "exact_mappings": [
    #     "rdfs:Resource"
    #   ],
    #   "slot_usage": {},
    #   "@type": "ClassDefinition"
    # }
    # [...]
    schema_jsonld = json.loads(JSONLDGenerator(schema_path, format="jsonld").serialize())
    # get all the schema classes according the generated JSON-LD
    classes_jsonld = {cls["definition_uri"]: cls for cls in schema_jsonld["classes"]}
    logger.info(classes_jsonld)
    # check each of the schema classes (according the SchemaView)
    for class_name, class_info in classes_with_custom_uri.items():
        assert class_info["uri"] in classes_jsonld.keys()
        assert "class_uri" not in classes_jsonld[class_info["uri"]].keys()
        assert "exact_mappings" in classes_jsonld[class_info["uri"]].keys()
        assert class_info["class_uri"] in classes_jsonld[class_info["uri"]]["exact_mappings"]

    # check generated RDF against following expectation:
    # [...]
    # <http://uri.interlex.org/tgbugs/uris/readable/sparc/Thing> a linkml:ClassDefinition ;
    #     skos:inScheme <https://sparc.olympiangods.org/sparcur/schemas/1/sparc> ;
    #     skos:exactMatch rdfs:Resource ;
    #     linkml:definition_uri <http://uri.interlex.org/tgbugs/uris/readable/sparc/Thing> ;
    #     linkml:slot_usage [ ] .
    # [...]
    schema_rdf = RDFGenerator(schema_path).serialize()
    schema_graph = Graph().parse(data=schema_rdf, format="turtle")
    classes_rdf = []
    # get all the schema classes according the generated RDF
    for class_name in schema_graph.objects(
        term.URIRef("http://uri.interlex.org/tgbugs/uris/readable/sparc/sparc-linkml"),
        term.URIRef("https://w3id.org/linkml/classes"),
    ):
        classes_rdf.append(str(class_name))
    # check each of the schema classes (according the SchemaView)
    for class_name, class_info in classes_with_custom_uri.items():
        assert class_info["uri"] in classes_rdf
        class_properties = {}
        for p, o in schema_graph.predicate_objects(term.URIRef(class_info["uri"])):
            if str(p) not in class_properties.keys():
                class_properties[str(p)] = str(o)
            else:
                if isinstance(class_properties[str(p)], str):
                    single_item = class_properties[str(p)]
                    class_properties[str(p)] = [single_item]
                class_properties[str(p)].append(str(o))
        assert "https://w3id.org/linkml/class_uri" not in class_properties.keys()
        assert "http://www.w3.org/2004/02/skos/core#exactMatch" in class_properties.keys()
        assert schema_view.expand_curie(class_info["class_uri"]) == schema_view.expand_curie(
            class_properties["http://www.w3.org/2004/02/skos/core#exactMatch"]
        ) or schema_view.expand_curie(class_info["class_uri"]) in schema_view.expand_curie(
            class_properties["http://www.w3.org/2004/02/skos/core#exactMatch"]
        )


CORE_SCHEMA = """
id: https://example.org/core
name: core
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/tiny/
imports:
  - linkml:types
default_prefix: ex
default_range: string
classes:
  Base:
    attributes:
      label: {}
"""

TINY_SCHEMA = """
id: https://example.org/tiny
name: tiny
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/tiny/
imports:
  - linkml:types
  - ./core
default_prefix: ex
default_range: string
classes:
  Thing:
    is_a: Base
    attributes:
      name: {}
"""


@pytest.mark.parametrize(
    "make_output",
    [
        pytest.param(
            lambda schema_dir: CliRunner().invoke(jsonld_cli, ["--no-metadata", "dist/tiny.yaml"]).output,
            id="cli-relative-path",
        ),
        pytest.param(
            lambda schema_dir: JSONLDGenerator("dist/tiny.yaml", metadata=False).serialize(),
            id="api-relative-path",
        ),
        pytest.param(
            lambda schema_dir: JSONLDGenerator("tiny.yaml", base_dir="dist", metadata=False).serialize(),
            id="api-relative-base-dir",
        ),
        pytest.param(
            lambda schema_dir: JSONLDGenerator("tiny.yaml", base_dir=str(schema_dir), metadata=False).serialize(),
            id="api-absolute-base-dir",
        ),
    ],
)
def test_relative_schema_locations(tmp_path, monkeypatch, make_output):
    """`gen-jsonld` finds the schema and its relative imports however its location is given.

    Regression test: the nested ContextGenerator was handed the schema path together with
    the base_dir SchemaLoader derived from it, so ``dist/tiny.yaml`` was looked up as
    ``dist/dist/tiny.yaml``. Forwarding the caller's own base_dir instead must keep an
    explicit ``base_dir`` and a sibling ``./core`` import working.
    """
    schema_dir = tmp_path / "dist"
    schema_dir.mkdir()
    (schema_dir / "core.yaml").write_text(CORE_SCHEMA)
    (schema_dir / "tiny.yaml").write_text(TINY_SCHEMA)
    expected = JSONLDGenerator(str(schema_dir / "tiny.yaml"), metadata=False).serialize()
    monkeypatch.chdir(tmp_path)

    output = make_output(schema_dir)

    assert '"name": "Base"' in output
    assert output.rstrip() == expected.rstrip()
