import json
import sys
from pathlib import Path

import pytest
import yaml

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml.generators.yarrrmlgen import YarrrmlGenerator

jsonschema = pytest.importorskip("jsonschema")
rdflib = pytest.importorskip("rdflib")
pyshacl = pytest.importorskip("pyshacl")

pytestmark = pytest.mark.skipif(sys.version_info < (3, 10), reason="YARRRML e2e require Morph-KGC (Python >= 3.10)")

if sys.version_info >= (3, 10):
    morph_kgc = pytest.importorskip("morph_kgc")


def _materialize_with_morph(tmp_path: Path, yarrrml: dict) -> rdflib.Graph:
    mappings_path = tmp_path / "mappings.yml"
    mappings_path.write_text(yaml.safe_dump(yarrrml, sort_keys=False), encoding="utf-8")
    # Morph-KGC takes an INI config pointing to the mappings file
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
      street: {}
      city: {}
"""
DATA_INLINED = {
    "items": [
        {"pid": "A1", "name": "WorkerX", "address": {"street": "Main", "city": "CityA"}},
        {"pid": "A2", "name": "WorkerY", "address": {"street": "High", "city": "CityB"}},
    ]
}


@pytest.mark.yarrrml
def test_yarrrml_e2e_inlined_true_skipped(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(SCHEMA_INLINED, encoding="utf-8")
    data_path.write_text(json.dumps(DATA_INLINED, indent=2), encoding="utf-8")

    js = JsonSchemaGenerator(str(schema_path)).serialize()
    jsonschema.validate(instance=DATA_INLINED, schema=json.loads(js))

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())
    assert "Address" not in yarrrml["mappings"]

    g = _materialize_with_morph(tmp_path, yarrrml)
    EX, RDF = rdflib.Namespace("https://ex.org/inl#"), rdflib.RDF
    assert (EX.A1, RDF.type, EX.Person) in g
    assert (EX.A1, EX.address, None) not in g

    conforms, results_text = _validate_with_shacl(schema_path, g)
    assert conforms, f"SHACL validation failed:\n{results_text}"


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
        assert isinstance(m["sources"][0], list), "CSV source must be list-wrapped (['...~csv'])"
        assert "~csv" in m["sources"][0][0], "CSV source must carry ~csv formulation"

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
