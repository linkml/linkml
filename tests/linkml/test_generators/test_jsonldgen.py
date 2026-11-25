import json
import logging

import pytest
from click.testing import CliRunner
from rdflib import RDF, Graph, Namespace, term
from yaml import safe_load

from linkml.generators import JSONLDGenerator, RDFGenerator
from linkml.generators.jsonldgen import cli as jsonld_cli
from linkml.generators.yamlgen import YAMLGenerator
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)


# network: rdflib fetches the @context URLs in the generated JSON-LD
@pytest.mark.network
def test_class_uri(input_path):
    """`class_uri` should be kept and also result in an `skos:exactMatch` relationship
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
    #   "class_uri": "http://www.w3.org/2000/01/rdf-schema#Resource",
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
        assert classes_jsonld[class_info["uri"]]["class_uri"] == schema_view.expand_curie(class_info["class_uri"])
        assert "exact_mappings" in classes_jsonld[class_info["uri"]].keys()
        assert schema_view.expand_curie(class_info["class_uri"]) in [
            schema_view.expand_curie(m) for m in classes_jsonld[class_info["uri"]]["exact_mappings"]
        ]

    # check generated RDF against following expectation:
    # [...]
    # <http://uri.interlex.org/tgbugs/uris/readable/sparc/Thing> a linkml:ClassDefinition ;
    #     skos:inScheme <https://sparc.olympiangods.org/sparcur/schemas/1/sparc> ;
    #     skos:exactMatch rdfs:Resource ;
    #     linkml:class_uri rdfs:Resource ;
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
        assert class_properties["https://w3id.org/linkml/class_uri"] == schema_view.expand_curie(
            class_info["class_uri"]
        )
        assert "http://www.w3.org/2004/02/skos/core#exactMatch" in class_properties.keys()
        assert schema_view.expand_curie(class_info["class_uri"]) == schema_view.expand_curie(
            class_properties["http://www.w3.org/2004/02/skos/core#exactMatch"]
        ) or schema_view.expand_curie(class_info["class_uri"]) in schema_view.expand_curie(
            class_properties["http://www.w3.org/2004/02/skos/core#exactMatch"]
        )


CLASS_URI_SCHEMA = """
id: https://example.org/class-uri-test
name: class-uri-test
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/class-uri-test/
  owl: http://www.w3.org/2002/07/owl#
imports:
  - linkml:types
default_prefix: ex
default_range: string
classes:
  Mapping:
    class_uri: owl:Axiom
  MappingSet: {}
"""


def test_class_uri_kept_alongside_exact_mapping(tmp_path):
    """An explicit `class_uri` is kept and added to `exact_mappings`; an implicit one adds no mapping.

    Regression test for https://github.com/linkml/linkml/issues/4066: the JSON-LD
    schema dropped `class_uri`, so it no longer round-tripped, and every class
    without an explicit `class_uri` gained an `exact_mappings` entry to itself.
    """
    schema_path = tmp_path / "class_uri_test.yaml"
    schema_path.write_text(CLASS_URI_SCHEMA)

    jsonld = json.loads(JSONLDGenerator(str(schema_path), format="jsonld").serialize())
    classes = {cls["name"]: cls for cls in jsonld["classes"]}
    assert classes["Mapping"]["class_uri"] == "http://www.w3.org/2002/07/owl#Axiom"
    assert classes["Mapping"]["exact_mappings"] == ["owl:Axiom"]
    assert classes["MappingSet"]["class_uri"] == "https://example.org/class-uri-test/MappingSet"
    assert "exact_mappings" not in classes["MappingSet"]

    merged = safe_load(YAMLGenerator(str(schema_path)).serialize())
    assert merged["classes"]["Mapping"]["exact_mappings"] == ["owl:Axiom"]
    assert "exact_mappings" not in merged["classes"]["MappingSet"]


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


LINKML = Namespace("https://w3id.org/linkml/")


def _yaml_element_names(output: str) -> dict[str, set[str]]:
    """Names of the classes, slots and types defined in ``gen-yaml`` output."""
    schema = safe_load(output)
    return {kind: set(schema.get(kind, {})) for kind in ("classes", "slots", "types")}


def _jsonld_element_names(output: str) -> dict[str, set[str]]:
    """Names of the classes, slots and types defined in ``gen-jsonld`` output."""
    schema = json.loads(output)
    return {kind: {element["name"] for element in schema.get(kind, [])} for kind in ("classes", "slots", "types")}


def _rdf_element_names(output: str) -> dict[str, set[str]]:
    """Local names of the classes, slots and types defined in ``gen-rdf`` output."""
    graph = Graph()
    graph.parse(data=output, format="turtle")
    definitions = {"classes": LINKML.ClassDefinition, "slots": LINKML.SlotDefinition, "types": LINKML.TypeDefinition}
    return {
        kind: {str(subject).rsplit("/", 1)[-1] for subject in graph.subjects(RDF.type, definition)}
        for kind, definition in definitions.items()
    }


@pytest.mark.parametrize("mergeimports", [True, False])
@pytest.mark.parametrize(
    "generator,element_names",
    [
        pytest.param(YAMLGenerator, _yaml_element_names, id="yaml"),
        pytest.param(JSONLDGenerator, _jsonld_element_names, id="jsonld"),
        # network: rdflib fetches the linkml:types @context URL in the generated JSON-LD
        pytest.param(RDFGenerator, _rdf_element_names, id="rdf", marks=pytest.mark.network),
    ],
)
def test_mergeimports_controls_imported_elements(tmp_path, generator, element_names, mergeimports):
    """``--no-mergeimports`` leaves imported classes, slots and types out of the output.

    Regression test for https://github.com/linkml/linkml/issues/4212: gen-yaml, gen-jsonld
    and gen-rdf wrote every imported element (including all of ``linkml:types``) whatever
    ``mergeimports`` was set to.
    """
    (tmp_path / "core.yaml").write_text(CORE_SCHEMA)
    (tmp_path / "tiny.yaml").write_text(TINY_SCHEMA)

    names = element_names(generator(str(tmp_path / "tiny.yaml"), mergeimports=mergeimports).serialize())

    assert "Thing" in names["classes"]
    assert "thing__name" in names["slots"]
    # Imported: class Base and its attribute from ./core, type string from linkml:types.
    assert ("Base" in names["classes"]) is mergeimports
    assert ("base__label" in names["slots"]) is mergeimports
    assert ("string" in names["types"]) is mergeimports


def test_yaml_without_merged_imports_resolves_them_through_imports(tmp_path):
    """``gen-yaml --no-mergeimports`` output keeps its ``imports``, so the left-out elements still resolve."""
    (tmp_path / "core.yaml").write_text(CORE_SCHEMA)
    (tmp_path / "tiny.yaml").write_text(TINY_SCHEMA)
    unmerged = tmp_path / "tiny_unmerged.yaml"
    unmerged.write_text(YAMLGenerator(str(tmp_path / "tiny.yaml"), mergeimports=False).serialize())

    view = SchemaView(str(unmerged))

    assert view.schema.imports == ["linkml:types", "./core"]
    assert set(view.all_classes(imports=False)) == {"Thing"}
    assert set(view.all_classes()) == {"Thing", "Base"}
    assert view.get_type("string").from_schema == "https://w3id.org/linkml/types"
