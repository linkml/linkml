import json
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

DATA_BASIC = [
    {
        "person_id": "P1",
        "name": "WorkerA",
        "employer": "O1",
        "org_id": "O1",
        "org_name": "Org_A",
    },
    {
        "person_id": "P2",
        "name": "WorkerB",
        "employer": "O2",
        "org_id": "O2",
        "org_name": "Org_B",
    },
]

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
DATA_ALIAS = [
    {
        "pid": "U1",
        "fn": "User_Prime",
        "employer": "M1",
        "oid": "M1",
        "oname": "Vendor_X",
    }
]

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
DATA_INLINED = [
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
DATA_PREFIXES = [{"aid": "X1", "name": "AlphaUnit", "bid": "Y1", "title": "BetaTitle"}]

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
DATA_MISSING = [{"pid": "Z1", "employer": "O9"}]

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
                if "value" in po["o"]:
                    assert isinstance(po["o"]["value"], str)
            else:
                assert isinstance(po["o"], (str, list))


@pytest.mark.yarrrml
def test_regression_classes_without_identifier_are_included(tmp_path: Path):
    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(SCHEMA_NO_ID, encoding="utf-8")
    yg = YarrrmlGenerator(str(schema_path))
    yobj = yaml.safe_load(yg.serialize())
    assert "Note" in yobj["mappings"]
    subj = yobj["mappings"]["Note"]["s"]
    assert subj.startswith("ex:Note/$(")

    types = [po for po in yobj["mappings"]["Note"]["po"] if po["p"] == "a" or po["p"] == "rdf:type"]
    assert len(types) == 1
    assert types[0]["o"] == "ex:Note"


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

    schema_person = JsonSchemaGenerator(str(schema_path), top_class="Person").generate()
    schema_person["$ref"] = "#/$defs/Person"
    schema_person["$defs"]["Person"]["additionalProperties"] = True
    schema_org = JsonSchemaGenerator(str(schema_path), top_class="Organization").generate()
    schema_org["$ref"] = "#/$defs/Organization"
    schema_org["$defs"]["Organization"]["additionalProperties"] = True
    for item in DATA_BASIC:
        if "person_id" in item:
            jsonschema.validate(instance=item, schema=schema_person)
        elif "org_id" in item:
            jsonschema.validate(instance=item, schema=schema_org)

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

    schema_person = JsonSchemaGenerator(str(schema_path), top_class="Person").generate()
    schema_person["$ref"] = "#/$defs/Person"
    schema_person["$defs"]["Person"]["additionalProperties"] = True
    for item in DATA_ALIAS:
        if "pid" in item:
            jsonschema.validate(instance=item, schema=schema_person)

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

    schema_person = JsonSchemaGenerator(str(schema_path), top_class="Person").generate()
    schema_person["$ref"] = "#/$defs/Person"
    for item in DATA_INLINED:
        jsonschema.validate(instance=item, schema=schema_person)

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

    schema_a = JsonSchemaGenerator(str(schema_path), top_class="A").generate()
    schema_a["$ref"] = "#/$defs/A"
    schema_a["$defs"]["A"]["additionalProperties"] = True

    schema_b = JsonSchemaGenerator(str(schema_path), top_class="B").generate()
    schema_b["$ref"] = "#/$defs/B"
    schema_b["$defs"]["B"]["additionalProperties"] = True

    for item in DATA_PREFIXES:
        if "aid" in item:
            jsonschema.validate(instance=item, schema=schema_a)
        if "bid" in item:
            jsonschema.validate(instance=item, schema=schema_b)

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

    schema_person = JsonSchemaGenerator(str(schema_path), top_class="Person").generate()
    schema_person["$ref"] = "#/$defs/Person"
    for item in DATA_MISSING:
        jsonschema.validate(instance=item, schema=schema_person)

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
        "person_id,name,employer,org_id,org_name\nP1,WorkerA,O1,O1,Org_A\nP2,WorkerB,O2,O2,Org_B\n",
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
        "person_id\tname\temployer\torg_id\torg_name\nP1\tWorkerA\tO1\tO1\tOrg_A\nP2\tWorkerB\tO2\tO2\tOrg_B\n",
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
        "person_id,name,employer,org_id,org_name\nP9,UserZ,O9,O9,Org_Z\n",
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
    type_po = next(p for p in m["po"] if p["p"] == "a")
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
    type_po = next(p for p in m["po"] if p["p"] == "a")
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
    data = [{"id": "H1", "name": "Alice"}]

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

    type_po = next(p for p in m["po"] if p["p"] == "a")
    assert isinstance(type_po["o"], str)
    assert type_po["o"]


@pytest.mark.yarrrml
def test_yarrrml_e2e_inline_object_join_mapping(tmp_path: Path):
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
    data = [{"id": "P1", "address": {"aid": "A1", "street": "Main", "city": "X"}}]

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    y = yaml.safe_load(yg.serialize())

    assert "Address" in y["mappings"]

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
    data = [{"id": "P1", "employer": "O1", "oid": "O1"}]

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
    data = [
        {"id": "A", "friends": ["B", "C"]},
        {"id": "B"},
        {"id": "C"},
    ]

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
def test_yarrrml_e2e_inline_multivalued_without_identifier_raises(tmp_path: Path):
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
      addresses:
        range: Address
        inlined: true
        multivalued: true
  Address:
    attributes:
      street: {}
"""

    data = [{"id": "P1", "addresses": [{"street": "Main"}]}]

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"

    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    expected_error = "is an inlined list \\(multivalued: true\\), but the target class 'Address' lacks an identifier"
    with pytest.raises(ValueError, match=expected_error):
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
      street: {}
"""

    data = [{"id": "P1"}]

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"

    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="without an identifier is used by multiple owners"):
        YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath").serialize()


@pytest.mark.yarrrml
def test_fix1_inlined_slots_without_id_synthetic_iri(tmp_path: Path):
    schema = """
id: https://example.org/test1
name: test1
prefixes:
  ex: https://example.org/test1/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
types:
  string:
    base: str
    uri: xsd:string
classes:
  Car:
    tree_root: true
    attributes:
      id:
        identifier: true
      engine:
        range: Engine
        inlined: true
  Engine:
    attributes:
      name: {}
"""
    data = {"id": "car1", "engine": {"name": "V8-Turbo"}}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    schema_root = JsonSchemaGenerator(str(schema_path), top_class="Car").generate()
    jsonschema.validate(instance=data, schema=schema_root)

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())

    assert "Engine" in yarrrml["mappings"]
    synth_iri = yarrrml["mappings"]["Engine"]["s"]
    assert synth_iri == "ex:Engine_$(id)"

    g = _materialize_with_morph(tmp_path, yarrrml)
    EX = rdflib.Namespace("https://example.org/test1/")

    assert (EX.car1, EX.engine, EX.Engine_car1) in g
    assert (EX.Engine_car1, EX.name, rdflib.Literal("V8-Turbo")) in g


@pytest.mark.yarrrml
def test_fix2_preserve_xsd_datatypes(tmp_path: Path):
    schema = """
id: https://example.org/test2
name: test2
prefixes:
  ex: https://example.org/test2/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
types:
  string:
    base: str
    uri: xsd:string
  integer:
    base: int
    uri: xsd:integer
classes:
  Person:
    tree_root: true
    attributes:
      id:
        identifier: true
      age:
        range: integer
"""
    data = {"id": "p1", "age": 27}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    schema_root = JsonSchemaGenerator(str(schema_path), top_class="Person").generate()
    jsonschema.validate(instance=data, schema=schema_root)

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())

    age_po = next(p for p in yarrrml["mappings"]["Person"]["po"] if p["p"] == "ex:age")
    assert age_po["o"]["datatype"] == "xsd:integer"

    g = _materialize_with_morph(tmp_path, yarrrml)
    EX = rdflib.Namespace("https://example.org/test2/")
    assert (EX.p1, EX.age, rdflib.Literal("27", datatype=rdflib.XSD.integer)) in g


@pytest.mark.yarrrml
def test_fix3_readable_yaml_flow_lists(tmp_path: Path):
    schema = """
id: https://example.org/test3
name: test3
prefixes:
  ex: https://example.org/test3/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
types:
  string:
    base: str
    uri: xsd:string
classes:
  Thing:
    tree_root: true
    attributes:
      id:
        identifier: true
"""
    data = {"id": "t1"}

    schema_path = tmp_path / "schema.yaml"
    schema_path.write_text(schema, encoding="utf-8")

    schema_root = JsonSchemaGenerator(str(schema_path), top_class="Thing").generate()
    jsonschema.validate(instance=data, schema=schema_root)

    yg = YarrrmlGenerator(str(schema_path))
    raw_yaml = yg.serialize()

    assert "[data.json~jsonpath" in raw_yaml


@pytest.mark.yarrrml
def test_fix4_unusable_defaults_and_tree_root(tmp_path: Path):
    schema = """
id: https://example.org/test4
name: test4
prefixes:
  ex: https://example.org/test4/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
types:
  string:
    base: str
    uri: xsd:string
classes:
  RootNode:
    tree_root: true
    attributes:
      id:
        identifier: true
  IgnoredNode:
    attributes:
      id:
        identifier: true
"""
    data = {"id": "r1"}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    schema_root = JsonSchemaGenerator(str(schema_path), top_class="RootNode").generate()
    jsonschema.validate(instance=data, schema=schema_root)

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())

    assert "RootNode" in yarrrml["mappings"]
    assert "IgnoredNode" not in yarrrml["mappings"]

    source_array = yarrrml["mappings"]["RootNode"]["sources"][0]
    assert source_array[1] == "$"


@pytest.mark.yarrrml
def test_fix5_incorrect_classes_for_non_inlined_slots(tmp_path: Path):
    schema = """
id: https://example.org/test5
name: test5
prefixes:
  ex: https://example.org/test5/
  schema: http://schema.org/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
types:
  string:
    base: str
    uri: xsd:string
classes:
  Person:
    class_uri: schema:Person
    tree_root: true
    attributes:
      id:
        identifier: true
      owns:
        range: Product
        multivalued: true
        inlined: false
  Product:
    class_uri: schema:Product
    attributes:
      id:
        identifier: true
"""
    data = {"id": "p1", "owns": ["prod1"]}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    schema_root = JsonSchemaGenerator(str(schema_path), top_class="Person").generate()
    jsonschema.validate(instance=data, schema=schema_root)

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())
    g = _materialize_with_morph(tmp_path, yarrrml)

    EX = rdflib.Namespace("https://example.org/test5/")
    SCHEMA = rdflib.Namespace("http://schema.org/")

    assert (EX.p1, rdflib.RDF.type, SCHEMA.Person) in g
    assert (EX.p1, rdflib.RDF.type, SCHEMA.Product) not in g


@pytest.mark.yarrrml
def test_fix6_incorrect_subjects_for_mixins(tmp_path: Path):
    schema = """
id: https://example.org/test6
name: test6
prefixes:
  ex: https://example.org/test6/
  schema: http://schema.org/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
types:
  string:
    base: str
    uri: xsd:string
classes:
  Named:
    mixin: true
    class_uri: ex:Named
    attributes:
      name: {}
  Person:
    class_uri: schema:Person
    tree_root: true
    mixins:
      - Named
    attributes:
      id:
        identifier: true
"""
    data = {"id": "p1", "name": "Alice"}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    schema_root = JsonSchemaGenerator(str(schema_path), top_class="Person").generate()
    jsonschema.validate(instance=data, schema=schema_root)

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())

    assert "Named" not in yarrrml["mappings"]

    g = _materialize_with_morph(tmp_path, yarrrml)
    EX = rdflib.Namespace("https://example.org/test6/")
    SCHEMA = rdflib.Namespace("http://schema.org/")

    assert (EX.p1, rdflib.RDF.type, SCHEMA.Person) in g
    assert (EX.p1, rdflib.RDF.type, EX.Named) in g


@pytest.mark.yarrrml
def test_fix7_identifier_missing_triple_mapping(tmp_path: Path):
    schema = """
id: https://example.org/test7
name: test7
prefixes:
  ex: https://example.org/test7/
  schema: http://schema.org/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
types:
  string:
    base: str
    uri: xsd:string
classes:
  Thing:
    tree_root: true
    attributes:
      id:
        identifier: true
        slot_uri: schema:identifier
"""
    data = {"id": "thing_001"}

    schema_path = tmp_path / "schema.yaml"
    data_path = tmp_path / "data.json"
    schema_path.write_text(schema, encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")

    schema_root = JsonSchemaGenerator(str(schema_path), top_class="Thing").generate()
    jsonschema.validate(instance=data, schema=schema_root)

    yg = YarrrmlGenerator(str(schema_path), source=f"{data_path.resolve()}~jsonpath")
    yarrrml = yaml.safe_load(yg.serialize())

    g = _materialize_with_morph(tmp_path, yarrrml)
    EX = rdflib.Namespace("https://example.org/test7/")
    SCHEMA = rdflib.Namespace("http://schema.org/")

    assert (EX.thing_001, SCHEMA.identifier, rdflib.Literal("thing_001")) in g
