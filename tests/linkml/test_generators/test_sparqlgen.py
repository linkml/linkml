from textwrap import dedent

from linkml.generators.sparqlgen import SparqlGenerator
from linkml_runtime import SchemaView


def test_sparqlgen(kitchen_sink_path):
    """Generate java classes"""
    gen = SparqlGenerator(kitchen_sink_path)
    sparql = gen.serialize()
    # TODO: add more checks
    assert "?subject rdf:type ks:Person" in sparql


def test_sparqlgen_does_not_mutate_input_schemaview(kitchen_sink_path):
    """
    Materialization must not mutate a caller-supplied schema.

    Regression for #3770: sparqlgen moved ``attributes`` into ``slots`` on the shared schema. A later
    generator that reused the same SchemaView, for example under gen-project, then found the attributes
    missing.
    """
    sv = SchemaView(kitchen_sink_path)
    before = {cn: len(c.attributes) for cn, c in sv.all_classes().items()}

    SparqlGenerator(sv.schema).serialize()

    after = {cn: len(c.attributes) for cn, c in sv.all_classes().items()}
    assert before == after
    assert any(count > 0 for count in before.values()), "fixture must have attributes to be meaningful"


def test_sparqlgen_path_and_object_inputs_match(kitchen_sink_path):
    """
    Path and pre-parsed-object inputs must produce identical output.

    Regression for #3770: the base ``__post_init__`` rebuilt the SchemaView after materialization,
    so path inputs silently dropped the prefixes materialization adds, yielding SPARQL that
    referenced undeclared prefixes.
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
