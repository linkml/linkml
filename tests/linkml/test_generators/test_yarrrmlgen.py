import json
import sys
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.yarrrmlgen import YarrrmlGenerator
from linkml.generators.yarrrmlgen import cli as yarrrml_cli

jsonschema = pytest.importorskip("jsonschema")
rdflib = pytest.importorskip("rdflib")
pyshacl = pytest.importorskip("pyshacl")

pytestmark = pytest.mark.skipif(sys.version_info < (3, 10), reason="YARRRML e2e require Morph-KGC (Python >= 3.10)")

if sys.version_info >= (3, 10):
    morph_kgc = pytest.importorskip("morph_kgc")


def _materialize_with_morph(tmp_path: Path, yarrrml: dict) -> rdflib.Graph:
    mappings_path = tmp_path / "mappings.yml"
    mappings_path.write_text(yaml.safe_dump(yarrrml, sort_keys=False), encoding="utf-8")
    config_ini = f"""[CONFIGURATION]
output_format: N-TRIPLES
logging_level: WARNING

[DataSource1]
mappings: {mappings_path}
"""
    return morph_kgc.materialize(config_ini)


def _validate_with_shacl(schema_path: Path, g: rdflib.Graph):
    shacl_ttl = ShaclGenerator(str(schema_path)).serialize()
    shacl_graph = rdflib.Graph()
    shacl_graph.parse(data=shacl_ttl, format="turtle")
    conforms, _, results_text = pyshacl.validate(
        data_graph=g,
        shacl_graph=shacl_graph,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        advanced=True,
        inplace=False,
    )
    return conforms, results_text


SCHEMA_BASIC = """id: https://ex.org/mini
name: mini
prefixes:
  ex: https://ex.org/mini#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  person_id:
    identifier: true
  name: {}
  employer:
    range: Organization
    inlined: false
  org_id:
    identifier: true
  org_name: {}

classes:
  Person:
    attributes:
      person_id:
        identifier: true
      name: {}
      employer:
        range: Organization
        inlined: false
  Organization:
    attributes:
      org_id:
        identifier: true
      org_name: {}
"""
DATA_BASIC = {
    "items": [
        {
            "person_id": "P1",
            "name": "WorkerA",
            "employer": "https://ex.org/mini#O1",
            "org_id": "O1",
            "org_name": "Org_A",
        },
        {
            "person_id": "P2",
            "name": "WorkerB",
            "employer": "https://ex.org/mini#O2",
            "org_id": "O2",
            "org_name": "Org_B",
        },
    ]
}

SCHEMA_ALIAS = """id: https://ex.org/alias
name: alias
prefixes:
  ex: https://ex.org/alias#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  pid:
    identifier: true
  full_name:
    alias: fn
  employer:
    range: Org
    inlined: false
  oid:
    identifier: true
  oname: {}

classes:
  Person:
    attributes:
      pid:
        identifier: true
      full_name:
        alias: fn
      employer:
        range: Org
        inlined: false
  Org:
    attributes:
      oid:
        identifier: true
      oname: {}
"""
DATA_ALIAS = {
    "items": [
        {
            "pid": "U1",
            "fn": "User_Prime",
            "employer": "https://ex.org/alias#M1",
            "oid": "M1",
            "oname": "Vendor_X",
        }
    ]
}

SCHEMA_INLINED = """id: https://ex.org/inl
name: inl
prefixes:
  ex: https://ex.org/inl#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  pid:
    identifier: true
  name: {}
  address:
    range: Address
    inlined: true
  street: {}
  city: {}

classes:
  Person:
    attributes:
      pid:
        identifier: true
      name: {}
      address:
        range: Address
        inlined: true
  Address:
    attributes:
      aid:
        identifier: true
      street: {}
      city: {}
"""
DATA_INLINED = {
    "items": [
        {
            "pid": "A1",
            "name": "WorkerX",
            "address": {
                "aid": "ADDR1",
                "street": "Main",
                "city": "CityA",
            },
        },
        {
            "pid": "A2",
            "name": "WorkerY",
            "address": {
                "aid": "ADDR2",
                "street": "High",
                "city": "CityB",
            },
        },
    ]
}

SCHEMA_PREFIXES = """id: https://ex.org/pfx
name: pfx
prefixes:
  ex: https://ex.org/pfx#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  aid:
    identifier: true
  name: {}
  bid:
    identifier: true
  title: {}

classes:
  A:
    attributes:
      aid:
        identifier: true
      name: {}
  B:
    attributes:
      bid:
        identifier: true
      title: {}
"""
DATA_PREFIXES = {"items": [{"aid": "X1", "name": "AlphaUnit", "bid": "Y1", "title": "BetaTitle"}]}

SCHEMA_MISSING = """id: https://ex.org/neg
name: neg
prefixes:
  ex: https://ex.org/neg#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  pid:
    identifier: true
  employer:
    range: Org
    inlined: false
  oid:
    identifier: true

classes:
  Person:
    attributes:
      pid:
        identifier: true
      employer:
        range: Org
        inlined: false
  Org:
    attributes:
      oid:
        identifier: true
"""
DATA_MISSING = {"items": [{"pid": "Z1", "employer": "https://ex.org/neg#O9"}]}

SCHEMA_NO_ID = """id: https://ex.org/noid
name: noid
prefixes:
  ex: https://ex.org/noid#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string

classes:
  Note:
    attributes:
      text: {}
"""

SCHEMA_PREDICATE_URI = """id: https://ex.org/pred
name: pred
prefixes:
  ex: https://ex.org/pred#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
default_range: string

slots:
  employer:
    range: Org
    inlined: false

classes:
  Person:
    attributes:
      id:
        identifier: true
      employer:
        range: Org
        inlined: false
  Org:
    attributes:
      oid:
        identifier: true
"""


@pytest.mark.yarrrml
def test_regression_no_yaml_python_object_garbage(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(SCHEMA_PREDICATE_URI, encoding="utf-8")
    yg = YarrrmlGenerator(str(schema_path))
    ytxt = yg.serialize()
    assert "!!python/object" not in ytxt
    yobj = yaml.safe_load(ytxt)
    for m in yobj["mappings"].values():
        for po in m["po"]:
            assert isinstance(po["p"], str)
            if isinstance(po.get("o"), dict):
                assert isinstance(po["o"]["value"], str)
            else:
                assert isinstance(po["o"], str)


@pytest.mark.yarrrml
def test_regression_classes_without_identifier_are_included(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(SCHEMA_NO_ID, encoding="utf-8")
    yg = YarrrmlGenerator(str(schema_path))
    yobj = yaml.safe_load(yg.serialize())
    assert "Note" in yobj["mappings"]
    subj = yobj["mappings"]["Note"]["s"]
    assert subj.startswith("ex:Note/$(")
    assert yobj["mappings"]["Note"]["po"][0]["o"] == "ex:Note"


@pytest.mark.yarrrml
def test_cli_sanity(monkeypatch):
    runner = CliRunner()
    res = runner.invoke(yarrrml_cli, ["--help"])
    assert res.exit_code == 0


@pytest.mark.yarrrml
def test_yarrrml_e2e_basic_json_morph_shacl(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(SCHEMA_BASIC, encoding="utf-8")
    data_path.write_text(json.dumps(DATA_BASIC, indent=2), encoding="utf-8")
    js = JsonSchemaGenerator(str(schema_path)).serialize()
    jsonschema.validate(instance=DATA_BASIC, schema=json.loads(js))
    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())
    for m in yarrrml["mappings"].values():
        assert isinstance(m["sources"][0], list) and "~jsonpath" in m["sources"][0][0]
    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/mini#"), rdflib.RDF
    assert (EX.P1, RDF.type, EX.Person) in g
    assert (EX.P1, EX.name, rdflib.Literal("WorkerA")) in g
    assert (EX.P2, EX.name, rdflib.Literal("WorkerB")) in g
    assert (EX.P1, EX.employer, rdflib.URIRef("https://ex.org/mini#O1")) in g
    assert (EX.O1, RDF.type, EX.Organization) in g
    assert (EX.O1, EX.org_name, rdflib.Literal("Org_A")) in g
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed:\n{results_text}"


@pytest.mark.yarrrml
def test_yarrrml_e2e_alias_support(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(SCHEMA_ALIAS, encoding="utf-8")
    data_path.write_text(json.dumps(DATA_ALIAS, indent=2), encoding="utf-8")
    js = JsonSchemaGenerator(str(schema_path)).serialize()
    jsonschema.validate(instance=DATA_ALIAS, schema=json.loads(js))
    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())
    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/alias#"), rdflib.RDF
    assert (EX.U1, RDF.type, EX.Person) in g
    assert (EX.U1, EX.full_name, rdflib.Literal("User_Prime")) in g
    assert (EX.U1, EX.employer, rdflib.URIRef("https://ex.org/alias#M1")) in g
    assert (EX.M1, RDF.type, EX.Org) in g
    assert (EX.M1, EX.oname, rdflib.Literal("Vendor_X")) in g
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed:\n{results_text}"


@pytest.mark.yarrrml
def test_yarrrml_e2e_inlined_true_included(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(SCHEMA_INLINED, encoding="utf-8")
    data_path.write_text(json.dumps(DATA_INLINED, indent=2), encoding="utf-8")
    js = JsonSchemaGenerator(str(schema_path)).serialize()
    jsonschema.validate(instance=DATA_INLINED, schema=json.loads(js))
    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())
    assert "Address" in yarrrml["mappings"]
    addr_map = yarrrml["mappings"]["Address"]
    assert any(po["p"].endswith("street") for po in addr_map["po"])
    assert any(po["p"].endswith("city") for po in addr_map["po"])
    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/inl#"), rdflib.RDF
    assert (EX.A1, RDF.type, EX.Person) in g
    assert (EX.A1, EX.name, rdflib.Literal("WorkerX")) in g
    assert (EX.A1, EX.address, EX.ADDR1) in g
    assert (EX.ADDR1, RDF.type, EX.Address) in g
    assert (EX.ADDR1, EX.street, rdflib.Literal("Main")) in g
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed:\n{results_text}"


@pytest.mark.yarrrml
def test_yarrrml_e2e_prefixes_and_multiple_classes(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(SCHEMA_PREFIXES, encoding="utf-8")
    data_path.write_text(json.dumps(DATA_PREFIXES, indent=2), encoding="utf-8")
    js = JsonSchemaGenerator(str(schema_path)).serialize()
    jsonschema.validate(instance=DATA_PREFIXES, schema=json.loads(js))
    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())
    assert "rdf" in yarrrml["prefixes"] and "ex" in yarrrml["prefixes"]
    assert set(yarrrml["mappings"].keys()) >= {"A", "B"}
    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/pfx#"), rdflib.RDF
    assert (EX.X1, RDF.type, EX.A) in g
    assert (EX.Y1, RDF.type, EX.B) in g
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed:\n{results_text}"


@pytest.mark.yarrrml
@pytest.mark.xfail(reason="SHACL should fail when target instances are missing", strict=False)
def test_yarrrml_e2e_missing_target_instances(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(SCHEMA_MISSING, encoding="utf-8")
    data_path.write_text(json.dumps(DATA_MISSING, indent=2), encoding="utf-8")
    js = JsonSchemaGenerator(str(schema_path)).serialize()
    jsonschema.validate(instance=DATA_MISSING, schema=json.loads(js))
    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())
    g = _materialize_with_morph(tmp_path, yarrrml)
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"Expected SHACL failure but got:\n{results_text}"


@pytest.mark.yarrrml
def test_yarrrml_e2e_basic_csv_morph_shacl(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(SCHEMA_BASIC, encoding="utf-8")
    csv_path = tmp_path / "people.csv"
    csv_path.write_text(
        "person_id,name,employer,org_id,org_name\n"
        "P1,WorkerA,https://ex.org/mini#O1,O1,Org_A\n"
        "P2,WorkerB,https://ex.org/mini#O2,O2,Org_B\n",
        encoding="utf-8",
    )
    yg = YarrrmlGenerator(str(schema_path), source=str(csv_path.resolve()) + "~csv")
    yarrrml = yaml.safe_load(yg.serialize())
    for m in yarrrml["mappings"].values():
        assert isinstance(m["sources"][0], list)
        assert "~csv" in m["sources"][0][0]
    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/mini#"), rdflib.RDF
    assert (EX.P1, RDF.type, EX.Person) in g
    assert (EX.P1, rdflib.URIRef("https://ex.org/mini#name"), rdflib.Literal("WorkerA")) in g
    assert (EX.P2, rdflib.URIRef("https://ex.org/mini#name"), rdflib.Literal("WorkerB")) in g
    assert (EX.P1, rdflib.URIRef("https://ex.org/mini#employer"), rdflib.URIRef("https://ex.org/mini#O1")) in g
    assert (EX.O1, RDF.type, EX.Organization) in g
    assert (EX.O1, rdflib.URIRef("https://ex.org/mini#org_name"), rdflib.Literal("Org_A")) in g
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed for CSV:\n{results_text}"


@pytest.mark.yarrrml
def test_yarrrml_e2e_basic_tsv_morph_shacl(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(SCHEMA_BASIC, encoding="utf-8")
    tsv_path = tmp_path / "people.tsv"
    tsv_path.write_text(
        "person_id\tname\temployer\torg_id\torg_name\n"
        "P1\tWorkerA\thttps://ex.org/mini#O1\tO1\tOrg_A\n"
        "P2\tWorkerB\thttps://ex.org/mini#O2\tO2\tOrg_B\n",
        encoding="utf-8",
    )
    yg = YarrrmlGenerator(str(schema_path), source=str(tsv_path.resolve()) + "~csv")
    yarrrml = yaml.safe_load(yg.serialize())
    for m in yarrrml["mappings"].values():
        assert isinstance(m["sources"][0], list)
        assert m["sources"][0][0].endswith("~csv")
    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/mini#"), rdflib.RDF
    assert (EX.P1, RDF.type, EX.Person) in g
    assert (EX.O2, RDF.type, EX.Organization) in g
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed for TSV:\n{results_text}"


@pytest.mark.yarrrml
def test_yarrrml_e2e_csv_source_suffix_inference(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(SCHEMA_BASIC, encoding="utf-8")
    csv_path = tmp_path / "minimal.csv"
    csv_path.write_text(
        "person_id,name,employer,org_id,org_name\nP9,UserZ,https://ex.org/mini#O9,O9,Org_Z\n",
        encoding="utf-8",
    )
    yg = YarrrmlGenerator(str(schema_path), source=str(csv_path.resolve()))
    yarrrml = yaml.safe_load(yg.serialize())
    for m in yarrrml["mappings"].values():
        assert isinstance(m["sources"][0], list)
        assert m["sources"][0][0].endswith("~csv")
    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/mini#"), rdflib.RDF
    assert (EX.P9, RDF.type, EX.Person) in g
    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed for suffix inference:\n{results_text}"


@pytest.mark.yarrrml
def test_yarrrml_uses_correct_uris_and_default_prefix(tmp_path: Path):
    schema_text = """
id: https://ex.org/uri-test
name: uri-test
prefixes:
  ex: https://ex.org/test#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Human:
    class_uri: ex:Person
    attributes:
      name:
        slot_uri: ex:fullName
      friend:
        range: Human
        inlined: false
"""
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(schema_text, encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path))
    yobj = yaml.safe_load(yg.serialize())

    assert "ex" in yobj["prefixes"]
    assert "mappings" in yobj

    m = yobj["mappings"]["Human"]
    type_po = next(p for p in m["po"] if p["p"] == "rdf:type")
    assert type_po["o"] == "ex:Person"

    pred_names = [p["p"] for p in m["po"]]
    assert "ex:fullName" in pred_names

    iri_obj = next(p for p in m["po"] if p["p"].endswith("friend"))
    assert iri_obj["o"]["type"] == "iri"


@pytest.mark.yarrrml
def test_yarrrml_adds_default_prefix_when_missing(tmp_path: Path):
    schema_text = """
id: https://no.prefix/test
name: noprefix
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Note:
    attributes:
      text: {}
"""
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(schema_text, encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path))
    yobj = yaml.safe_load(yg.serialize())

    assert "ex" in yobj["prefixes"]
    assert yobj["prefixes"]["ex"] == "https://example.org/default#"

    assert "mappings" in yobj and isinstance(yobj["mappings"], dict)


@pytest.mark.yarrrml
def test_yarrrml_does_not_override_existing_default_prefix(tmp_path: Path):
    schema_text = """
id: https://ex.org/custom
name: custom
prefixes:
  my: https://ex.org/my#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: my

classes:
  Thing:
    attributes:
      id:
        identifier: true
"""
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(schema_text, encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path))
    yobj = yaml.safe_load(yg.serialize())

    assert "ex" not in yobj["prefixes"]
    assert "my" in yobj["prefixes"]

    m = yobj["mappings"]["Thing"]
    assert m["s"] == "my:$(id)"
    type_po = next(p for p in m["po"] if p["p"] == "rdf:type")
    assert type_po["o"] == "my:Thing"


@pytest.mark.yarrrml
def test_yarrrml_slot_uri_full_iri_used_verbatim(tmp_path: Path):
    schema_text = """
id: https://ex.org/full-iri
name: full-iri
prefixes:
  ex: https://ex.org/ns#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex

slots:
  name:
    slot_uri: "https://example.org/vocab/fullName"

classes:
  Human:
    attributes:
      id:
        identifier: true
      name: {}
"""
    data = {"items": [{"id": "H1", "name": "Alice"}]}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema_text, encoding="utf-8")
    data_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())

    m = yarrrml["mappings"]["Human"]
    preds = [po["p"] for po in m["po"]]
    assert "https://example.org/vocab/fullName" in preds

    g = _materialize_with_morph(tmp_path, yarrrml)
    FULL = rdflib.URIRef("https://example.org/vocab/fullName")
    EXNS = rdflib.Namespace("https://ex.org/ns#")

    assert (EXNS.H1, FULL, rdflib.Literal("Alice")) in g


@pytest.mark.yarrrml
def test_yarrrml_single_class_without_slots_has_mapping_and_type(tmp_path: Path):
    schema_text = """
id: https://ex.org/only-class
name: only-class
prefixes:
  ex: https://ex.org/only#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex

classes:
  Lonely:
    description: Just a lonely class
"""
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(schema_text, encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path))
    yobj = yaml.safe_load(yg.serialize())

    assert "mappings" in yobj
    assert "Lonely" in yobj["mappings"]

    m = yobj["mappings"]["Lonely"]

    assert m["s"].startswith("ex:Lonely/$(")

    type_po = next(p for p in m["po"] if p["p"] == "rdf:type")
    assert isinstance(type_po["o"], str)
    assert type_po["o"]


@pytest.mark.yarrrml
def test_yarrrml_e2e_inline_object_not_separate_mapping(tmp_path: Path):
    schema = """
id: https://ex.org/inl2
name: inl2
prefixes:
  ex: https://ex.org/inl2#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex

classes:
  Person:
    attributes:
      id:
        identifier: true
      address:
        range: Address
        inlined: true

  Address:
    attributes:
      aid:
        identifier: true
      street: {}
      city: {}

"""
    data = {"items": [{"id": "P1", "address": {"aid": "A1", "street": "Main", "city": "X"}}]}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    y = yaml.safe_load(yg.serialize())

    # Address mapping now MUST exist (join-based inline)
    assert "Address" in y["mappings"]

    # Person must reference Address via mapping + condition
    person_po = y["mappings"]["Person"]["po"]
    addr_po = next(po for po in person_po if po["p"].endswith("address"))

    assert "mapping" in addr_po["o"]
    assert addr_po["o"]["mapping"] == "Address"

    assert "condition" in addr_po["o"]
    assert addr_po["o"]["condition"]["function"] == "equal"

    params = addr_po["o"]["condition"]["parameters"]
    assert any("address." in p[1] for p in params)


@pytest.mark.yarrrml
def test_yarrrml_e2e_object_link_is_iri(tmp_path: Path):
    schema = """
id: https://ex.org/obj
name: obj
prefixes:
  ex: https://ex.org/obj#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex

classes:
  Person:
    attributes:
      id:
        identifier: true
      employer:
        range: Organization
        inlined: false
  Organization:
    attributes:
      oid:
        identifier: true
"""
    data = {"items": [{"id": "P1", "employer": "https://ex.org/obj#O1", "oid": "O1"}]}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    y = yaml.safe_load(yg.serialize())

    person_po = y["mappings"]["Person"]["po"]
    emp_po = next(po for po in person_po if po["p"].endswith("employer"))

    assert emp_po["o"]["type"] == "iri"

    g = _materialize_with_morph(tmp_path, y)
    EX = rdflib.Namespace("https://ex.org/obj#")

    assert (EX.P1, EX.employer, rdflib.URIRef("https://ex.org/obj#O1")) in g


@pytest.mark.yarrrml
def test_yarrrml_e2e_multivalued_object_links_are_iris(tmp_path: Path):
    schema = """
id: https://ex.org/friends
name: friends
prefixes:
  ex: https://ex.org/friends#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex

classes:
  Person:
    attributes:
      id:
        identifier: true
      friends:
        range: Person
        multivalued: true
        inlined: false
"""
    data = {
        "items": [
            {"id": "A", "friends": ["https://ex.org/friends#B", "https://ex.org/friends#C"]},
            {"id": "B"},
            {"id": "C"},
        ]
    }

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    y = yaml.safe_load(yg.serialize())

    friends_po = next(po for po in y["mappings"]["Person"]["po"] if po["p"].endswith("friends"))

    assert isinstance(friends_po["o"], list)
    assert all(o["type"] == "iri" for o in friends_po["o"])


@pytest.mark.yarrrml
def test_yarrrml_e2e_inline_without_identifier_raises(tmp_path: Path):
    schema = """
id: https://ex.org/neg1
name: neg1
prefixes:
  ex: https://ex.org/neg1#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
classes:
  Person:
    attributes:
      id:
        identifier: true
      address:
        range: Address
        inlined: true
  Address:
    attributes:
      street: {}
"""

    data = {"items": [{"id": "P1", "address": {"street": "Main"}}]}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"

    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="must define an identifier"):
        YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath").serialize()


@pytest.mark.yarrrml
def test_yarrrml_e2e_multi_owner_inline_raises(tmp_path: Path):
    schema = """
id: https://ex.org/neg2
name: neg2
prefixes:
  ex: https://ex.org/neg2#
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
default_prefix: ex
classes:
  Person:
    attributes:
      id:
        identifier: true
      address:
        range: Address
        inlined: true

  Company:
    attributes:
      id:
        identifier: true
      hq:
        range: Address
        inlined: true

  Address:
    attributes:
      aid:
        identifier: true
"""

    data = {"items": [{"id": "P1"}]}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"

    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="used in multiple owners"):
        YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath").serialize()
