import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import rdflib
from rdflib import Graph, URIRef

from linkml import METAMODEL_CONTEXT_URI
from linkml.generators.rdfgen import RDFGenerator

pytestmark = pytest.mark.xdist_group("rdfgen")

schema = """
id: http://example.org/interval

default_curi_maps:
  - semweb_context

prefixes:
  ex: http://example.org/
  schema: http://schema.org/
  linkml: https://w3id.org/linkml/

imports:
  - linkml:types

default_prefix: ex

classes:

  c:
    annotations:
      - tag: my_tag1
        value: my_value1
      - tag: my_tag2
        value: my_value2
"""

JSONLD = """
{
  "slots": [
    {
      "name": "type",
      "slot_uri": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    }
  ],
  "@context": [
  {
      "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "@vocab": "https://w3id.org/linkml/",
      "slot_uri": {
         "@type": "@id"
      }
    }
  ]
}"""


# network: rdflib fetches the @context URLs in the generated JSON-LD
@pytest.mark.network
def test_annotation_extensions():
    """Test that annotation extensions are properly serialized"""
    s = RDFGenerator(schema, mergeimports=False).serialize()
    rdf_graph = Graph()
    rdf_graph.parse(data=s, format="turtle")

    # Query for annotations in the ClassDefinition
    query = """
        SELECT ?example ?tag
        WHERE {
            ex:C linkml:annotations ?annotation .
            ?annotation skos:example ?example .
            ?annotation linkml:tag ?tag .
        }
        """

    results = list(rdf_graph.query(query))

    # Check if there are exactly two annotations
    assert len(results) == 2

    # Check each annotation for the required properties
    for example, tag in results:
        assert isinstance(example, rdflib.Literal)
        assert isinstance(tag, rdflib.URIRef | rdflib.Literal)


# network: rdflib fetches the @context URLs in the generated JSON-LD
@pytest.mark.network
def test_generation_date_suppressed_by_default():
    """The generation_date timestamp triple is off by default and opt-in via the flag.

    Regression test for https://github.com/linkml/linkml/issues/3516 (bullet 2): the
    load-time ``generation_date`` stamp is serialized as a data triple in RDF output,
    which defeats byte-stable/reproducible generation. It is suppressed by default;
    ``include_generation_date=True`` restores the old behaviour for callers that want it.
    """
    generation_date = URIRef("https://w3id.org/linkml/generation_date")

    default_output = RDFGenerator(schema, mergeimports=False).serialize()
    default_graph = Graph()
    default_graph.parse(data=default_output, format="turtle")
    assert not list(default_graph.triples((None, generation_date, None))), (
        "generation_date should be suppressed by default"
    )

    # With the timestamp gone, output is byte-stable across runs.
    rerun = RDFGenerator(schema, mergeimports=False).serialize()
    assert default_output == rerun

    opted_in = Graph()
    opted_in.parse(data=RDFGenerator(schema, mergeimports=False, include_generation_date=True).serialize())
    assert list(opted_in.triples((None, generation_date, None))), (
        "generation_date should be present when explicitly requested"
    )


# network: rdflib fetches the @context URLs in the generated JSON-LD
@pytest.mark.network
def test_output_is_byte_identical_across_processes():
    """RDF output is byte-identical across fresh processes with different hash seeds.

    Regression test for https://github.com/linkml/linkml/issues/3516. Two things can
    make repeated generation differ: the ``generation_date`` timestamp (now suppressed
    by default) and ``PYTHONHASHSEED``-dependent iteration order upstream of
    canonicalization. Running in-process would catch neither, so each run gets its own
    interpreter with a deliberately different seed.
    """
    program = textwrap.dedent(
        f"""
        from linkml.generators.rdfgen import RDFGenerator
        print(RDFGenerator({schema!r}, mergeimports=False).serialize(), end="")
        """
    )

    def run(seed: str) -> str:
        # Inherit the real environment and vary only the hash seed. Replacing it
        # wholesale drops SystemRoot on Windows, which breaks winsock init.
        # A fresh interpreter never imports tests/conftest.py, so the offline
        # network guard is installed via sitecustomize on PYTHONPATH instead
        # (same mechanism as the notebook kernels).
        kernel_startup_dir = Path(__file__).resolve().parents[2] / "_kernel_startup"
        existing = os.environ.get("PYTHONPATH", "")
        pythonpath = os.pathsep.join([str(kernel_startup_dir), *([existing] if existing else [])])
        env = {**os.environ, "PYTHONHASHSEED": seed, "PYTHONPATH": pythonpath}
        result = subprocess.run(
            [sys.executable, "-c", program],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        return result.stdout

    outputs = [run(seed) for seed in ("0", "1", "42")]

    # Empty output would be trivially "identical" and hide a broken generator.
    assert outputs[0].strip(), "generator produced no output"
    assert len(set(outputs)) == 1, "RDF output differs across PYTHONHASHSEED values"


@pytest.mark.network
def test_issue_388_attribute_slot_uri_conflicts_stay_disambiguated_in_rdf(input_path):
    generated_rdf = RDFGenerator(input_path("linkml_issue_388.yaml")).serialize(context=[METAMODEL_CONTEXT_URI])
    rdf_graph = Graph()
    rdf_graph.parse(data=generated_rdf, format="turtle")

    for slot in ("c1__a", "c2__a", "c3__a"):
        assert len(list(rdf_graph.triples((URIRef(f"https://example.org/this/{slot}"), None, None)))) > 0


@pytest.mark.skip("TODO")
def test_rdfgen(kitchen_sink_path):
    """rdf"""
    s = RDFGenerator(kitchen_sink_path, mergeimports=False).serialize()
    g = Graph()
    g.parse(data=s, format="turtle")


@pytest.mark.skip("TODO")
def test_rdf_type_in_jsonld(self):
    graph = Graph()
    graph.parse(data=JSONLD, format="json-ld", prefix=True)
    ttl_str = graph.serialize(format="turtle")
    graph.parse(data=ttl_str, format="turtle")


# ----------------------------------------------------------------------------
# Regression: gen-rdf must not 404 on per-module @context refs
# ----------------------------------------------------------------------------

_RDFGEN_RELATIVE_IMPORT_BASE = """\
id: https://example.org/rdfbase
name: rdfbase
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
default_range: string
imports:
  - linkml:types
classes:
  Base:
    attributes:
      id:
        identifier: true
"""

_RDFGEN_RELATIVE_IMPORT_MAIN = """\
id: https://example.org/rdfmain
name: rdfmain
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
default_prefix: ex
default_range: string
imports:
  - linkml:types
  - ./base
classes:
  Thing:
    is_a: Base
    attributes:
      label:
"""


# network: rdflib fetches the absolute @context URLs that survive the filter
@pytest.mark.network
def test_rdfgen_strips_unresolvable_per_module_context_refs(tmp_path):
    """``gen-rdf`` must not 404 on per-module ``@context`` refs.

    ``JSONLDGenerator.end_schema`` appends one ``<import>.context.jsonld``
    string per loaded import. For a sibling import such as ``./base`` the
    resulting entry is ``./base.context.jsonld`` - a relative path that
    rdflib resolves against ``@base`` (the schema's ``https://`` URI) and
    then fetches via HTTP. That file is never published anywhere, so if it
    reached rdflib unchanged the fetch would 404 and ``RDFGenerator.serialize``
    would raise ``urllib.error.HTTPError``.

    ``rdfgen._strip_relative_context_refs`` prevents this by dropping string
    entries from the ``@context`` array that have no resolvable URI scheme
    before handing the JSON-LD to rdflib. The merged inline ``@context`` (and
    the fully merged schema body) cover everything the per-module refs would
    have contributed, so the filtering is non-destructive.
    """
    schemas_dir = tmp_path / "schemas"
    schemas_dir.mkdir()
    (schemas_dir / "base.yaml").write_text(_RDFGEN_RELATIVE_IMPORT_BASE)
    (schemas_dir / "main.yaml").write_text(_RDFGEN_RELATIVE_IMPORT_MAIN)

    turtle = RDFGenerator(str(schemas_dir / "main.yaml")).serialize()

    # Parse back through rdflib to confirm the output is well-formed and
    # contains classes from both the main and the sibling-imported schema.
    g = Graph()
    g.parse(data=turtle, format="turtle")
    subjects = {str(s) for s in g.subjects()}
    assert "https://example.org/Thing" in subjects
    assert "https://example.org/Base" in subjects


def test_strip_relative_context_refs_preserves_absolute_uris_and_dicts():
    """Unit-test the ``@context`` filter directly.

    The helper must keep:
      * inline ``@context`` dicts (carry prefix bindings and the ``@base``
        directive),
      * absolute ``http(s)://`` URIs (published context documents like
        ``https://w3id.org/linkml/types.context.jsonld``),
      * ``file://`` URIs (the vendored metamodel context, absolutized by
        ``JSONLDGenerator.end_schema``),

    and drop only scheme-less string entries that rdflib would dereference
    against ``@base``.
    """
    from linkml.generators.rdfgen import _strip_relative_context_refs

    payload = {
        "@context": [
            "file:///vendored/meta.context.jsonld",
            "https://w3id.org/linkml/types.context.jsonld",
            "./base.context.jsonld",
            "base.context.jsonld",
            "../other.context.jsonld",
            {"ex": "https://example.org/"},
            {"@base": "https://example.org/"},
        ],
        "@id": "https://example.org/x",
    }
    filtered = json.loads(_strip_relative_context_refs(json.dumps(payload)))

    assert filtered["@context"] == [
        "file:///vendored/meta.context.jsonld",
        "https://w3id.org/linkml/types.context.jsonld",
        {"ex": "https://example.org/"},
        {"@base": "https://example.org/"},
    ]
    # Untouched siblings round-trip.
    assert filtered["@id"] == "https://example.org/x"
