from textwrap import dedent

import pytest
from click.testing import CliRunner
from rdflib import Dataset, URIRef
from rdflib.plugins.sparql import prepareQuery

from linkml.generators.sparqlgen import SparqlGenerator, cli
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper


def test_sparqlgen(kitchen_sink_path):
    """Generate SPARQL queries for the kitchen sink schema."""
    gen = SparqlGenerator(kitchen_sink_path)
    sparql = gen.serialize()
    # TODO: add more checks
    assert "?subject rdf:type ks:Person" in sparql


def test_sparqlgen_does_not_mutate_input_schemaview(kitchen_sink_path):
    """
    The generator must leave a caller-supplied schema as it found it.

    Regression for #3770: sparqlgen moved ``attributes`` into ``slots`` on the shared schema. A later
    generator that reused the same schema object then found the attributes missing. The generator now reads
    the caller's schema with no copy in between, so this compares all of it.

    Two fields are filled in first, because this generator is not what writes them. Reading a view sets
    ``domain_of``, and the base generator sets ``metamodel_version``.
    """
    sv = SchemaView(kitchen_sink_path)
    for class_name in sv.all_classes():
        sv.class_induced_slots(class_name)
    sv.schema.metamodel_version = "0.0.0"
    before = yaml_dumper.dumps(sv.schema)

    gen = SparqlGenerator(sv.schema)
    gen.serialize()

    assert gen.schema is sv.schema, "the generator must read the caller's schema for this test to be meaningful"
    assert any(c.attributes for c in sv.all_classes().values()), "fixture must have attributes to be meaningful"
    assert yaml_dumper.dumps(sv.schema) == before


def test_sparqlgen_path_and_object_inputs_match(kitchen_sink_path):
    """
    Path and pre-parsed-object inputs must produce identical output.

    Regression for #3770: the base ``__post_init__`` rebuilt the SchemaView after ``materialize_schema``
    ran, so path inputs silently dropped the prefixes it had added, yielding SPARQL that referenced
    undeclared prefixes.
    """
    from_path = SparqlGenerator(kitchen_sink_path).serialize()
    from_object = SparqlGenerator(SchemaView(kitchen_sink_path).schema).serialize()
    assert from_path == from_object
    assert "PREFIX rdf:" in from_path


_SPARQLGEN_IMPORTED_BASE = dedent(
    """\
    id: https://example.org/base
    name: base
    prefixes:
      linkml: https://w3id.org/linkml/
      ex: https://example.org/
    default_prefix: ex
    default_range: string
    imports:
      - linkml:types
    classes:
      Thing:
        attributes:
          id:
            identifier: true
          name:
            required: true
    """
)

_SPARQLGEN_IMPORT_ONLY_MAIN = dedent(
    """\
    id: https://example.org/main
    name: main
    prefixes:
      linkml: https://w3id.org/linkml/
      ex: https://example.org/
    default_prefix: ex
    imports:
      - linkml:types
      - ./base
    """
)


def _write_import_only_fixture(tmp_path):
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "base.yaml").write_text(_SPARQLGEN_IMPORTED_BASE)
    main = schemas_dir / "main.yaml"
    main.write_text(_SPARQLGEN_IMPORT_ONLY_MAIN)
    return main


def test_sparqlgen_emits_queries_for_imported_classes(tmp_path):
    """
    A root schema that only ``imports:`` other modules must still produce queries for the imported
    classes when ``mergeimports`` is enabled (the default).

    Regression for #3636: ``SparqlGenerator`` built its queries only from the root ``schema.classes``,
    which holds no imported classes, and left the output directory empty.
    """
    main = _write_import_only_fixture(tmp_path)
    out_dir = tmp_path / "out"

    gen = SparqlGenerator(str(main), mergeimports=True)
    gen.serialize(directory=str(out_dir))

    rq_files = sorted(p.name for p in out_dir.glob("*.rq"))
    assert rq_files, "expected gen-sparql to emit .rq files for imported classes"
    assert "CHECK_permitted_Thing.rq" in rq_files
    assert any(name.startswith("CHECK_required_Thing_") for name in rq_files)

    permitted = (out_dir / "CHECK_permitted_Thing.rq").read_text()
    assert "?s rdf:type ex:Thing" in permitted


def test_sparqlgen_no_mergeimports_skips_imported_classes(tmp_path):
    """
    With ``--no-mergeimports``, the generator should use only the classes declared in the root schema.

    The root schema of the import-only fixture declares no classes, so no ``.rq`` files should be written.
    """
    main = _write_import_only_fixture(tmp_path)
    out_dir = tmp_path / "out"

    gen = SparqlGenerator(str(main), mergeimports=False)
    gen.serialize(directory=str(out_dir))

    assert list(out_dir.glob("*.rq")) == []


_SPARQLGEN_BASE_WITH_OWN_PREFIX = dedent(
    """\
    id: https://example.org/base
    name: base
    prefixes:
      linkml: https://w3id.org/linkml/
      b: https://example.org/b/
    default_prefix: b
    default_range: string
    imports:
      - linkml:types
    classes:
      Thing:
        slots:
          - kind
        attributes:
          id:
            identifier: true
          name:
            required: true
      Part: {}
      SubPart:
        is_a: Part
    slots:
      kind: {}
    """
)

_SPARQLGEN_MAIN_WITH_OWN_PREFIX = dedent(
    """\
    id: https://example.org/main
    name: main
    prefixes:
      linkml: https://w3id.org/linkml/
      m: https://example.org/m/
    default_prefix: m
    default_range: string
    imports:
      - linkml:types
      - ./base
    classes:
      Child:
        is_a: Thing
        slot_usage:
          kind:
            required: true
        attributes:
          part:
            range: Part
      Solo:
        attributes:
          name: {}
    """
)

# The classes declared in the main schema, with the queries each one should get.
_MAIN_SCHEMA_QUERIES = {
    "CHECK_permitted_Child",
    "CHECK_required_Child_id",
    "CHECK_required_Child_kind",
    "CHECK_required_Child_name",
    "CHECK_object_range_Child_part",
    "CHECK_permitted_Solo",
}


def _write_schemas(tmp_path, base=_SPARQLGEN_BASE_WITH_OWN_PREFIX, main=_SPARQLGEN_MAIN_WITH_OWN_PREFIX):
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "base.yaml").write_text(base)
    (schemas_dir / "main.yaml").write_text(main)
    return schemas_dir / "main.yaml", schemas_dir / "base.yaml"


def _statements(query: str) -> list[str]:
    """Return the lines of a query, without its prefixes and the comments that name the next class."""
    return [line for line in query.split("\n") if line.strip() and not line.startswith(("PREFIX", "##"))]


def test_sparqlgen_cli_no_mergeimports_writes_only_the_schemas_own_classes(tmp_path):
    """``--no-mergeimports`` on the command line leaves out the classes of imported schemas."""
    main, _ = _write_schemas(tmp_path)
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(cli, ["--no-mergeimports", "-d", str(out_dir), str(main)])

    assert result.exit_code == 0, result.output
    assert {path.stem for path in out_dir.glob("*.rq")} == _MAIN_SCHEMA_QUERIES


def test_sparqlgen_mergeimports_adds_the_imported_classes(tmp_path):
    """Merging imports writes the same queries for the schema's own classes, and more for the imported ones."""
    main, _ = _write_schemas(tmp_path)

    merged = SparqlGenerator(str(main), mergeimports=True).queries
    not_merged = SparqlGenerator(str(main), mergeimports=False).queries

    assert set(not_merged) == _MAIN_SCHEMA_QUERIES
    assert "CHECK_permitted_Thing" in merged
    assert {name: merged[name] for name in not_merged} == not_merged


@pytest.mark.parametrize("mergeimports", [True, False])
def test_sparqlgen_slots_keep_the_uri_of_the_schema_that_defines_them(tmp_path, mergeimports):
    """
    A slot takes the default prefix of the schema that defines it, whichever schema is given to the generator.

    ``Child`` inherits ``id`` and ``name`` as attributes of an imported class, and ``kind`` as an imported slot
    that its own schema refines with a ``slot_usage``.
    """
    main, _ = _write_schemas(tmp_path)

    queries = SparqlGenerator(str(main), mergeimports=mergeimports).queries

    permitted = queries["CHECK_permitted_Child"]
    for uri in ("m:part", "b:kind", "b:id", "b:name"):
        assert f"{uri}," in permitted
    assert "VALUES ?predicate { b:name }" in queries["CHECK_required_Child_name"]
    assert "VALUES ?predicate { b:kind }" in queries["CHECK_required_Child_kind"]
    object_range = queries["CHECK_object_range_Child_part"]
    assert "VALUES ?predicate { m:part  }" in object_range
    assert "b:Part" in object_range and "b:SubPart" in object_range


@pytest.mark.parametrize("mergeimports", [True, False])
def test_sparqlgen_attributes_with_the_same_name_stay_separate(tmp_path, mergeimports):
    """
    Two classes may each declare an attribute with the same name, and each keeps its own.

    ``Solo.name`` is optional and belongs to the main schema, while ``Thing.name`` is required and belongs to the
    imported one.
    """
    main, _ = _write_schemas(tmp_path)

    queries = SparqlGenerator(str(main), mergeimports=mergeimports).queries

    assert "m:name," in queries["CHECK_permitted_Solo"]
    assert "b:name" not in queries["CHECK_permitted_Solo"]
    assert "CHECK_required_Solo_name" not in queries
    assert "CHECK_required_Child_name" in queries


def test_sparqlgen_imported_class_gets_the_same_queries_from_either_schema(tmp_path):
    """The queries for a class are the same from a merged run and from a run over its own schema."""
    main, base = _write_schemas(tmp_path)

    merged = SparqlGenerator(str(main), mergeimports=True).queries
    alone = SparqlGenerator(str(base), mergeimports=False).queries

    assert "CHECK_required_Thing_name" in alone
    for name, query in alone.items():
        assert _statements(merged[name]) == _statements(query), name


def test_sparqlgen_no_mergeimports_queries_run_on_their_own(tmp_path):
    """Each query declares every prefix it uses, including those of imported schemas that get no queries."""
    main, _ = _write_schemas(tmp_path)

    queries = SparqlGenerator(str(main), mergeimports=False).queries

    assert queries
    for query in queries.values():
        prepareQuery(query)


def test_sparqlgen_no_mergeimports_queries_judge_data_correctly(tmp_path):
    """Data that uses the imported slots conforms, and the same data under the main schema's prefix does not."""
    main, _ = _write_schemas(tmp_path)
    queries = SparqlGenerator(str(main), mergeimports=False).queries

    def violations(turtle):
        dataset = Dataset()
        dataset.graph(URIRef("https://example.org/graph")).parse(
            data="@prefix b: <https://example.org/b/> .\n@prefix m: <https://example.org/m/> .\n" + turtle,
            format="turtle",
        )
        return {name for name, query in queries.items() if list(dataset.query(query))}

    assert not violations('m:c a m:Child ; b:id "c" ; b:name "Child" ; b:kind "k" ; m:part m:p .\nm:p a b:SubPart .')
    assert violations('m:c a m:Child ; m:id "c" ; m:name "Child" ; m:kind "k" .') == {
        "CHECK_permitted_Child",
        "CHECK_required_Child_id",
        "CHECK_required_Child_kind",
        "CHECK_required_Child_name",
    }


def test_sparqlgen_prefix_declared_by_the_given_schema_is_kept(tmp_path):
    """
    The schema given to the generator keeps the meaning of its own prefixes, and imported prefixes are all declared.

    ``title`` is also the name of a schema field, which must not hide a prefix with that name.
    """
    base = _SPARQLGEN_BASE_WITH_OWN_PREFIX.replace(
        "  b: https://example.org/b/\n",
        "  b: https://example.org/b/\n  m: https://example.org/other/\n  title: https://example.org/title/\n",
    )
    main, _ = _write_schemas(tmp_path, base=base)

    sparql = SparqlGenerator(str(main), mergeimports=False).serialize()

    assert "PREFIX m: <https://example.org/m/>" in sparql
    assert "https://example.org/other/" not in sparql
    assert "PREFIX title: <https://example.org/title/>" in sparql
