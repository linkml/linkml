"""Tests for the split mode of the JSON Schema generator: one document per schema module.

The modules are in ``input/jsonschema_split/``; its README says what each one is for.
"""

import json
from pathlib import Path

import jsonschema
import pytest
from referencing import Registry, Resource

from linkml.generators.jsonschemagen import JsonSchemaGenerator, _check_cross_document_refs, _relative_ref_base

pytestmark = pytest.mark.jsonschemagen

RELEASE_PATTERN = "https://example.org/release/{{ version }}/meta/{{ schema.name }}.json"

VALID_ARCHITECTURE = {
    "nodes": [{"unique_id": "n1", "check_interval": "week", "vendor": {"vendor_name": "Acme"}}],
    "controls": {"c1": {"review_every": "month", "evidence": {"e1": {"summary": "audited"}}}},
}


# Small modules for cases the fixtures in input/jsonschema_split/ leave out, written to tmp_path.
UNITS_MODULE = """
id: https://example.org/spec/units
name: units
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
enums:
  TimeUnit:
    permissible_values:
      day:
      week:
"""

EXAMPLES_MODULE = """
id: https://example.org/spec/core
name: core
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
  - units
default_range: string
classes:
  Pattern:
    tree_root: true
    examples:
      - object:
          body:
            $ref: "#/$defs/TimeUnit"
          other:
            $ref: "#/$defs/Unknown"
    attributes:
      body:
        range: Anything
      other:
        range: Anything
      examples:
        range: TimeUnit
  Anything:
    class_uri: linkml:Any
"""

URN_CORE_MODULE = """
id: urn:example:core
name: core
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
  - units
default_range: string
classes:
  Architecture:
    tree_root: true
    attributes:
      every:
        range: TimeUnit
"""

# Two modules that give the control namespace different prefix names.
CURIES_CORE_MODULE = """
id: https://example.org/spec/core
name: core
prefixes:
  linkml: https://w3id.org/linkml/
  core: https://example.org/spec/core/
  c: https://example.org/spec/control/
default_prefix: core
imports:
  - linkml:types
  - control
default_range: string
classes:
  Architecture:
    tree_root: true
    attributes:
      detail:
        range: ControlDetail
        inlined: true
"""

CURIES_CONTROL_MODULE = """
id: https://example.org/spec/control
name: control
prefixes:
  linkml: https://w3id.org/linkml/
  ctl: https://example.org/spec/control/
default_prefix: ctl
imports:
  - linkml:types
default_range: string
classes:
  ControlDetail:
    class_uri: https://example.org/spec/control/ControlDetail
    attributes:
      text:
"""


@pytest.fixture
def core(input_path) -> str:
    return input_path("jsonschema_split/core.yaml")


def _refs(node) -> list[str]:
    """Every ``$ref`` value in a generated document."""
    if isinstance(node, dict):
        return [v for k, v in node.items() if k == "$ref"] + [r for v in node.values() for r in _refs(v)]
    if isinstance(node, list):
        return [r for v in node for r in _refs(v)]
    return []


def _validator(documents: list[dict], root_id: str, validator_class=jsonschema.Draft201909Validator):
    """A validator for the document *root_id* that resolves ``$ref`` across *documents* by ``$id``."""
    registry = Registry().with_resources((doc["$id"], Resource.from_contents(doc)) for doc in documents)
    root = next(doc for doc in documents if doc["$id"] == root_id)
    return validator_class(root, registry=registry)


def test_split_emits_only_local_definitions(core):
    """The document of a module defines its own classes, plus private copies for dictionary values."""
    generated = json.loads(JsonSchemaGenerator(core, split=True).serialize())

    assert generated["$id"] == "https://example.org/spec/core"
    assert set(generated["$defs"]) == {
        "Architecture",
        "Node",
        "ControlDetail__identifier_optional",
        "Evidence__identifier_optional",
    }
    # The private copy drops the required identifier, as the copy beside the class does.
    assert "control_id" not in generated["$defs"]["ControlDetail__identifier_optional"].get("required", [])
    assert generated["$defs"]["ControlDetail__identifier_optional"]["title"] == "ControlDetail"


def test_split_refs_are_relative_under_the_same_parent(core):
    """A ``$ref`` to another module is relative when both URIs share a parent, absolute otherwise."""
    generated = json.loads(JsonSchemaGenerator(core, split=True).serialize())
    node = generated["$defs"]["Node"]["properties"]

    assert node["check_interval"]["anyOf"][0] == {"$ref": "units#/$defs/TimeUnit"}
    assert node["vendor"]["anyOf"][0] == {"$ref": "https://vendor.example.com/schemas/vendor#/$defs/VendorInfo"}
    assert generated["properties"]["nodes"]["items"] == {"$ref": "#/$defs/Node"}
    for ref in _refs(generated):
        if ref.startswith("#"):
            assert ref.removeprefix("#/$defs/") in generated["$defs"]


@pytest.mark.parametrize(
    "target,expected",
    [
        ("https://example.org/meta/control.json", "control.json"),
        ("https://example.org/meta/ex:units", "./ex:units"),
        ("https://example.org/units", "https://example.org/units"),
        ("http://example.org/meta/control.json", "http://example.org/meta/control.json"),
        ("https://vendor.example.com/meta/vendor.json", "https://vendor.example.com/meta/vendor.json"),
        ("https://example.org/meta/control.json?v=1", "https://example.org/meta/control.json?v=1"),
        ("https://example.org/meta/control/", "https://example.org/meta/control/"),
        ("urn:example:control", "urn:example:control"),
    ],
)
def test_relative_ref_base(target, expected):
    """A ``$ref`` is relative only when it resolves against the referring ``$id`` back to *target*."""
    assert _relative_ref_base(target, "https://example.org/meta/core.json") == expected


def test_split_refs_between_urns_are_absolute(tmp_path):
    """A URN has no path to resolve a relative reference against, so a ``$ref`` to one is written in full."""
    (tmp_path / "units.yaml").write_text(UNITS_MODULE.replace("https://example.org/spec/units", "urn:example:units"))
    (tmp_path / "core.yaml").write_text(URN_CORE_MODULE)
    documents = [
        json.loads(JsonSchemaGenerator(str(tmp_path / f"{name}.yaml"), split=True).serialize())
        for name in ("core", "units")
    ]

    assert set(_refs(documents[0])) == {"urn:example:units#/$defs/TimeUnit"}
    validator = _validator(documents, "urn:example:core")
    assert validator.is_valid({"every": "day"})
    assert not validator.is_valid({"every": "hour"})


def test_split_off_keeps_one_document(core):
    """Without ``split`` the document covers the import closure, and ``split_pattern`` is not used."""
    default = JsonSchemaGenerator(core).serialize()
    patterned = JsonSchemaGenerator(core, split_pattern=RELEASE_PATTERN, split_context={"version": "1"}).serialize()
    generated = json.loads(default)

    assert default == patterned
    assert generated["$id"] == "https://example.org/spec/core"
    assert {"Architecture", "ControlDetail", "Evidence", "TimeUnit", "VendorInfo"} <= set(generated["$defs"])
    assert all(ref.startswith("#/$defs/") for ref in _refs(generated))


def test_split_root_class_is_the_modules_own(input_path):
    """Each module's document takes its root from its own ``tree_root``, and a module without one has none."""
    control = json.loads(JsonSchemaGenerator(input_path("jsonschema_split/control.yaml"), split=True).serialize())
    units = json.loads(JsonSchemaGenerator(input_path("jsonschema_split/units.yaml"), split=True).serialize())

    assert control["required"] == ["name"]
    assert control["properties"]["details"]["items"] == {"$ref": "#/$defs/ControlDetail"}
    assert "properties" not in units
    assert units["additionalProperties"] is True


def test_generate_split_top_class_names_the_input_modules_root(core, tmp_path, caplog):
    """``top_class`` sets the root of the input module's document; the others keep their own ``tree_root``."""
    results = JsonSchemaGenerator.generate_split(core, tmp_path, top_class="Node")
    by_file = {r.path.name: r.schema_ for r in results}

    assert set(by_file["core.json"]["properties"]) == {"unique_id", "check_interval", "vendor", "note"}
    assert by_file["control.json"]["required"] == ["name"]
    assert "No class in schema named" not in caplog.text


def test_split_top_class_from_another_module_warns(core, caplog):
    """A ``top_class`` that another module defines leaves the input module's document without a root."""
    generated = json.loads(JsonSchemaGenerator(core, split=True, top_class="ControlRequirement").serialize())

    assert "properties" not in generated
    assert "ControlRequirement is defined in an imported module" in caplog.text


def test_split_pattern_with_context(core):
    """``split_pattern`` renders each module's URI, with ``split_context`` available to the template."""
    generated = json.loads(
        JsonSchemaGenerator(
            core, split=True, split_pattern=RELEASE_PATTERN, split_context={"version": "1.3"}
        ).serialize()
    )

    assert generated["$id"] == "https://example.org/release/1.3/meta/core.json"
    node = generated["$defs"]["Node"]["properties"]
    assert node["check_interval"]["anyOf"][0] == {"$ref": "units.json#/$defs/TimeUnit"}
    assert node["vendor"]["anyOf"][0] == {"$ref": "vendor.json#/$defs/VendorInfo"}


def test_split_pattern_giving_two_modules_one_uri_raises(core):
    with pytest.raises(ValueError, match="the same URI https://example.org/same.json"):
        JsonSchemaGenerator(core, split=True, split_pattern="https://example.org/same.json").serialize()


def test_split_with_def_name_style(core):
    """Definition keys follow ``def_name_style`` in every document and in every ``$ref`` between them."""
    generated = json.loads(JsonSchemaGenerator(core, split=True, def_name_style="kebab-case").serialize())

    assert set(generated["$defs"]) == {
        "architecture",
        "node",
        "control-detail__identifier_optional",
        "evidence__identifier_optional",
    }
    assert generated["$defs"]["node"]["properties"]["check_interval"]["anyOf"][0] == {"$ref": "units#/$defs/time-unit"}


def test_split_curies_use_the_defining_modules_prefixes(tmp_path):
    """Under ``use_curies`` both documents key a class with the prefixes of the module that defines it."""
    (tmp_path / "core.yaml").write_text(CURIES_CORE_MODULE)
    (tmp_path / "control.yaml").write_text(CURIES_CONTROL_MODULE)
    results = JsonSchemaGenerator.generate_split(str(tmp_path / "core.yaml"), tmp_path / "out", use_curies=True)
    core, control = (result.schema_ for result in results)

    assert "ctl:ControlDetail" in control["$defs"]
    assert set(_refs(core)) == {"control#/$defs/ctl:ControlDetail"}


def test_split_leaves_instance_data_alone(tmp_path):
    """A ``$ref`` inside an example is data and stays as written; a property named ``examples`` is rewritten."""
    (tmp_path / "units.yaml").write_text(UNITS_MODULE)
    (tmp_path / "core.yaml").write_text(EXAMPLES_MODULE)
    pattern = json.loads(JsonSchemaGenerator(str(tmp_path / "core.yaml"), split=True).serialize())["$defs"]["Pattern"]

    assert pattern["examples"] == [{"body": {"$ref": "#/$defs/TimeUnit"}, "other": {"$ref": "#/$defs/Unknown"}}]
    assert pattern["properties"]["examples"]["anyOf"][0] == {"$ref": "units#/$defs/TimeUnit"}


def test_generate_split_writes_one_file_per_module(core, tmp_path):
    """Modules with a class or an enum get a file named after their URI; type-only modules get none."""
    results = JsonSchemaGenerator.generate_split(
        core, tmp_path, split_pattern=RELEASE_PATTERN, split_context={"version": "1.3"}
    )

    assert sorted(p.name for p in tmp_path.iterdir()) == ["control.json", "core.json", "units.json", "vendor.json"]
    assert [r.main for r in results] == [True, False, False, False]
    assert results[0].path == tmp_path / "core.json"
    for result in results:
        assert json.loads(result.path.read_text()) == json.loads(json.dumps(result.schema_))
        assert result.schema_["$id"] == result.uri


@pytest.mark.parametrize(
    "draft,validator_class",
    [("2019-09", jsonschema.Draft201909Validator), ("2020-12", jsonschema.Draft202012Validator)],
)
def test_generate_split_documents_validate_together(core, tmp_path, draft, validator_class):
    """The written documents resolve each other's ``$ref`` by ``$id`` and validate as one schema."""
    results = JsonSchemaGenerator.generate_split(
        core, tmp_path, split_pattern=RELEASE_PATTERN, split_context={"version": "1.3"}, draft=draft
    )
    documents = [json.loads(Path(r.path).read_text()) for r in results]
    for document in documents:
        validator_class.check_schema(document)
    validator = _validator(documents, results[0].uri, validator_class)

    assert validator.is_valid(VALID_ARCHITECTURE)
    wrong_unit = {"nodes": [{"unique_id": "n1", "check_interval": "hour"}]}
    no_vendor_name = {"nodes": [{"unique_id": "n1", "vendor": {}}]}
    no_summary = {"controls": {"c1": {"review_every": "day", "evidence": {"e1": {}}}}}
    for instance in (wrong_unit, no_vendor_name, no_summary):
        assert not validator.is_valid(instance)


def test_generate_split_with_default_pattern_validates(core, tmp_path):
    """With the default pattern the ``$id`` of each document is its module's ``id``."""
    results = JsonSchemaGenerator.generate_split(core, tmp_path)
    documents = [r.schema_ for r in results]

    assert {r.uri for r in results} == {
        "https://example.org/spec/core",
        "https://example.org/spec/control",
        "https://example.org/spec/units",
        "https://vendor.example.com/schemas/vendor",
    }
    assert sorted(p.name for p in tmp_path.iterdir()) == ["control.json", "core.json", "units.json", "vendor.json"]
    assert _validator(documents, "https://example.org/spec/core").is_valid(VALID_ARCHITECTURE)


@pytest.mark.parametrize(
    "split_pattern",
    ["https://example.org/{{ 'same' }}", "https://example.org/{{ 'Same' if schema.name == 'core' else 'same' }}"],
)
def test_generate_split_rejects_two_modules_in_one_file(core, tmp_path, split_pattern):
    """Two modules may not share a file, nor two files differ in case alone; nothing is written then."""
    with pytest.raises(ValueError, match="would both be written to same.json"):
        JsonSchemaGenerator.generate_split(core, tmp_path, split_pattern=split_pattern)
    assert not any(tmp_path.iterdir())


def test_generate_split_rejects_two_modules_of_one_name_in_one_file(tmp_path):
    """Two modules that share a name but not an ``id`` still may not share a file."""
    for folder, enum in (("a", "TimeUnit"), ("b", "SizeUnit")):
        (tmp_path / folder).mkdir()
        (tmp_path / folder / "units.yaml").write_text(
            UNITS_MODULE.replace("spec/units", f"spec/{folder}/units").replace("TimeUnit", enum)
        )
    (tmp_path / "core.yaml").write_text(
        URN_CORE_MODULE.replace("urn:example:core", "https://example.org/spec/core").replace(
            "  - units\n", "  - a/units\n  - b/units\n"
        )
    )
    with pytest.raises(ValueError, match="Modules units and units would both be written to units.json"):
        JsonSchemaGenerator.generate_split(str(tmp_path / "core.yaml"), tmp_path / "out")
    assert not (tmp_path / "out").exists()


@pytest.mark.parametrize(
    "split_pattern",
    [
        "https://example.org/{{ schema.name }}\\..\\..\\outside",
        "https://example.org/C:{{ schema.name }}",
        "urn:example:{{ schema.name }}",
    ],
)
def test_generate_split_rejects_file_names_that_are_not_plain(core, tmp_path, split_pattern):
    """A module URI cannot name a file outside the output directory, or one that some platforms cannot hold."""
    with pytest.raises(ValueError, match="not a plain file name"):
        JsonSchemaGenerator.generate_split(core, tmp_path, split_pattern=split_pattern)
    assert not any(tmp_path.iterdir())


def test_check_cross_document_refs():
    """A ``$ref`` into another of the generated documents must name one of its definitions."""
    documents = {
        "https://example.org/spec/core": {"properties": {"every": {"$ref": "units#/$defs/Missing"}}},
        "https://example.org/spec/units": {"$defs": {"TimeUnit": {}}},
    }
    with pytest.raises(ValueError, match=r"units#/\$defs/Missing in https://example.org/spec/core names no definition"):
        _check_cross_document_refs(documents)

    documents["https://example.org/spec/core"]["properties"]["every"]["$ref"] = "units#/$defs/TimeUnit"
    _check_cross_document_refs(documents)
