from textwrap import dedent

from linkml.generators.sparqlgen import SparqlGenerator


def test_sparqlgen(kitchen_sink_path):
    """Generate java classes"""
    gen = SparqlGenerator(kitchen_sink_path)
    sparql = gen.serialize()
    # TODO: add more checks
    assert "?subject rdf:type ks:Person" in sparql


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
    """A root schema that only ``imports:`` other modules must still produce
    queries for the imported classes when ``mergeimports`` is enabled
    (the default). Regression for the bug where ``SparqlGenerator`` rendered
    against the unmaterialised root ``schema.classes``, leaving the output
    directory empty."""
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
    """With ``--no-mergeimports`` the generator should restrict itself to
    classes declared in the root schema. The import-only fixture defines no
    direct classes, so no ``.rq`` files should be written."""
    main = _write_import_only_fixture(tmp_path)
    out_dir = tmp_path / "out"

    gen = SparqlGenerator(str(main), mergeimports=False)
    gen.serialize(directory=str(out_dir))

    out_dir.mkdir(exist_ok=True)
    assert list(out_dir.glob("*.rq")) == []
