"""Tests for the shared ``--subset`` generator option and the pruning behind it.

The fixture ``subset_profile.yaml`` is a small risk register with three subsets: ``core`` names one
class, ``summary`` names a class and some slots, two of them only through the class's
``slot_usage``, and ``empty_subset`` has no members. It imports ``subset_profile_imported.yaml``,
which has its own namespace and contributes one class that ``core`` reaches and one that no subset
reaches.
"""

import json
import re

import pytest
import yaml
from click.testing import CliRunner

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.generators.docgen import DocGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.jsonschemagen import cli as gen_json_schema
from linkml.generators.linkmlgen import LinkmlGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.utils.subsetting import prune_to_subset, subset_closure
from linkml_runtime import SchemaView

DROPPED = ["Hazard", "Mitigation", "Unused", "HazardKindEnum", "HazardCode", "hazard_code", "mitigates"]
"""Names that no subset of the fixture reaches."""

CORE_CLASSES = {
    "Risk": {"id", "created_on", "name", "severity", "code", "owner", "tags", "title", "notes"},
    "Named": {"name"},
    "Entity": {"id", "created_on"},
    "Person": {"id", "created_on", "address", "title", "owns"},
    "Address": {"street", "country"},
    "Tag": {"label"},
    "Audited": {"reviewed_on"},
}
SUMMARY_CLASSES = {
    "Risk": {"id", "created_on", "name", "owner", "title"},
    "Named": {"name"},
    "Entity": {"id", "created_on"},
    "Person": {"id", "created_on"},
    "Audited": set(),
}
COMPARED_METASLOTS = ["range", "required", "multivalued", "identifier", "inlined", "in_subset", "pattern"]
"""Properties of an induced slot that pruning must leave as they are in the full schema."""


@pytest.fixture(scope="module")
def profile_path(input_path) -> str:
    """Path of the fixture schema."""
    return input_path("subset_profile.yaml")


@pytest.fixture(scope="module")
def profile_view(profile_path) -> SchemaView:
    """View of the fixture schema, imports included."""
    return SchemaView(profile_path)


def mentions(output: str, name: str) -> bool:
    """Return whether generated output names an element, as a whole word."""
    return re.search(rf"\b{name}\b", output) is not None


def test_closure_of_subset_naming_classes_only(profile_view):
    """A subset that names only Risk keeps all of Risk's induced slots, its ancestor and mixin, the
    class that applies itself to Risk, and every element those slots reach: Person and Address
    through ranges, the imported Tag, both enums, and RiskCode with its typeof ancestor BaseCode."""
    closure = subset_closure(profile_view, "core")
    assert closure.classes == CORE_CLASSES
    assert closure.slots == {
        "id",
        "created_on",
        "name",
        "severity",
        "code",
        "owner",
        "owns",
        "tags",
        "title",
        "address",
        "reviewed_on",
    }
    assert closure.enums == {"SeverityEnum", "CountryEnum"}
    assert closure.types == {"RiskCode", "BaseCode", "string"}


def test_closure_of_subset_naming_slots_narrows_each_class(profile_view):
    """Once the subset names slots, a class keeps the induced slots that are members for it, and
    its identifier.

    ``title`` and ``created_on`` are members only through Risk's ``slot_usage``. Person declares
    ``title`` itself, so Person drops it. ``created_on`` is declared on Entity, which must keep
    declaring it for Risk to inherit it, so Person inherits it and keeps it too. Person's own
    ``address`` and ``owns`` are dropped, so Address and CountryEnum are not reached.
    """
    closure = subset_closure(profile_view, "summary")
    assert closure.classes == SUMMARY_CLASSES
    assert closure.slots == {"id", "created_on", "name", "owner", "title"}
    assert closure.enums == set()
    assert closure.types == {"string"}


def test_closure_of_unknown_subset_names_the_declared_ones(profile_view):
    with pytest.raises(ValueError, match=r'No such subset "nope"; the schema declares: core, empty_subset, summary'):
        subset_closure(profile_view, "nope")


def test_closure_of_empty_subset_keeps_only_the_default_range(profile_view, caplog):
    closure = subset_closure(profile_view, "empty_subset")
    assert closure.classes == {}
    assert closure.slots == set()
    assert closure.types == {"string"}
    assert "empty_subset has no members" in caplog.text


def test_prune_merges_imports_and_keeps_their_uris(profile_view):
    pruned = prune_to_subset(profile_view, "core")
    assert list(pruned.imports) == ["linkml:types"]
    assert set(pruned.classes) == set(CORE_CLASSES)
    assert set(pruned.enums) == {"SeverityEnum", "CountryEnum"}
    assert set(pruned.types) == {"RiskCode", "BaseCode"}, "string stays imported from linkml:types"
    assert list(pruned.subsets) == ["core", "summary", "empty_subset"]
    assert pruned.prefixes["imp"].prefix_reference == "https://example.org/subset-profile-imported/"
    tag = pruned.classes["Tag"]
    assert tag.class_uri == "imp:Tag", "a merged class keeps the URI it has in its own schema"
    assert tag.attributes["label"].slot_uri == "imp:label"
    assert pruned.classes["Risk"].class_uri is None, "the root schema's own elements are left as they are"
    risk = pruned.classes["Risk"]
    assert list(risk.slots) == ["severity", "code", "owner", "tags", "title"]
    assert list(risk.attributes) == ["notes"]
    assert len(risk.rules) == 1
    assert list(risk.unique_keys) == ["owner_and_code"]
    assert pruned.slots["owner"].inverse == "owns"
    assert list(pruned.classes["Audited"].apply_to) == ["Risk"]


def test_prune_drops_what_refers_to_dropped_slots(profile_view):
    pruned = prune_to_subset(profile_view, "summary")
    risk = pruned.classes["Risk"]
    assert list(risk.slots) == ["owner", "title"]
    assert list(risk.attributes) == []
    assert list(risk.slot_usage) == ["created_on", "title"]
    assert risk.rules == [], "the rule tests severity, which is dropped"
    assert list(risk.unique_keys) == [], "the key uses code, which is dropped"
    assert list(pruned.classes["Entity"].slots) == ["id", "created_on"]
    assert list(pruned.classes["Person"].slots) == []
    assert list(pruned.classes["Audited"].slots) == []
    assert pruned.slots["owner"].inverse is None, "the inverse, owns, is dropped"
    assert "Address" not in pruned.classes
    assert "CountryEnum" not in pruned.enums


@pytest.mark.parametrize(
    "schema,subset_name",
    [
        ("profile", "core"),
        ("profile", "summary"),
        ("metamodel", "MinimalSubset"),
        ("metamodel", "SpecificationSubset"),
    ],
)
def test_prune_leaves_kept_classes_as_they_were(profile_path, schema, subset_name):
    """Every kept class has exactly the slots that the closure keeps for it, each induced as in the
    full schema and with the same URI, no kept slot's range is dropped, and every ``domain_of`` names
    a class that is still there."""
    path = profile_path if schema == "profile" else str(LOCAL_METAMODEL_YAML_FILE)
    full = SchemaView(path)
    closure = subset_closure(full, subset_name)
    pruned_schema = prune_to_subset(SchemaView(path), subset_name)
    pruned = SchemaView(pruned_schema)
    elements = set(pruned.all_classes()) | set(pruned.all_enums()) | set(pruned.all_types())
    for cls in pruned_schema.classes.values():
        for definition in (*cls.attributes.values(), *cls.slot_usage.values()):
            assert set(definition.domain_of) <= set(pruned.all_classes()), f"{cls.name}.{definition.name}"
    for slot in pruned_schema.slots.values():
        assert set(slot.domain_of) <= set(pruned.all_classes()), slot.name
    for class_name in pruned.all_classes(imports=False):
        assert set(pruned.class_slots(class_name)) == closure.classes[class_name] & set(full.class_slots(class_name))
        assert pruned.get_uri(class_name, expand=True) == full.get_uri(class_name, expand=True)
        for slot_name in pruned.class_slots(class_name):
            before = full.induced_slot(slot_name, class_name)
            after = pruned.induced_slot(slot_name, class_name)
            for metaslot in COMPARED_METASLOTS:
                assert getattr(after, metaslot) == getattr(before, metaslot), f"{class_name}.{slot_name}.{metaslot}"
            assert pruned.get_uri(after, expand=True) == full.get_uri(before, expand=True)
            assert set(pruned.slot_range_as_union(after)) <= elements


@pytest.mark.parametrize(
    "generator_class",
    [
        JsonSchemaGenerator,
        PydanticGenerator,
        LinkmlGenerator,
        YAMLGenerator,
        OwlSchemaGenerator,
        # gen-rdf reads the JSON-LD context of linkml:types from its URL
        pytest.param(RDFGenerator, marks=pytest.mark.network),
    ],
)
def test_generators_see_only_the_subset(generator_class, profile_path):
    output = generator_class(profile_path, subset="core").serialize()
    assert mentions(output, "Risk")
    assert mentions(output, "Tag"), "the class of the imported schema that the subset reaches is kept"
    for name in DROPPED:
        assert not mentions(output, name)


@pytest.mark.parametrize("subset_name", [None, "core"])
def test_schemaloader_applies_a_kept_class_to_its_target(profile_path, subset_name):
    """The SchemaLoader turns Audited's ``apply_to`` into a mixin of Risk, and the subset keeps
    Audited, so Risk gets its slot with the subset as it does without it."""
    risk = YAMLGenerator(profile_path, subset=subset_name).schema.classes["Risk"]
    assert "Audited" in risk.mixins
    assert "reviewed_on" in risk.slots


def test_generator_rejects_unknown_subset(profile_path):
    with pytest.raises(ValueError, match="the schema declares: core, empty_subset, summary"):
        JsonSchemaGenerator(profile_path, subset="nope")


def test_gen_json_schema_cli_defines_exactly_the_kept_classes(profile_path):
    result = CliRunner().invoke(gen_json_schema, ["--subset", "summary", profile_path])
    assert result.exit_code == 0, result.output
    defs = json.loads(result.output)["$defs"]
    assert set(defs) == set(SUMMARY_CLASSES)
    assert set(defs["Risk"]["properties"]) == SUMMARY_CLASSES["Risk"]
    assert set(defs["Person"]["properties"]) == SUMMARY_CLASSES["Person"]


def test_gen_json_schema_cli_unknown_subset(profile_path):
    result = CliRunner().invoke(gen_json_schema, ["--subset", "nope", profile_path])
    assert result.exit_code != 0
    assert "the schema declares: core, empty_subset, summary" in str(result.exception)


def test_gen_pydantic_subset_compiles(profile_path):
    module = PydanticGenerator(profile_path, subset="core").compile_module()
    for name in CORE_CLASSES:
        assert hasattr(module, name)
    assert set(module.Risk.model_fields) == CORE_CLASSES["Risk"]
    assert not hasattr(module, "Hazard")


def test_gen_doc_subset_writes_pages_for_kept_elements_only(profile_path, tmp_path):
    DocGenerator(profile_path, subset="core", directory=str(tmp_path)).serialize()
    pages = {page.stem for page in tmp_path.glob("*.md")}
    assert set(CORE_CLASSES) | {"core", "summary", "empty_subset", "SeverityEnum", "RiskCode"} <= pages
    assert pages.isdisjoint(DROPPED)


def test_gen_jsonld_context_keeps_the_uris_of_merged_classes(profile_path):
    """The imported Tag is merged into the pruned schema but keeps its own namespace."""
    full = json.loads(ContextGenerator(profile_path).serialize())["@context"]
    pruned = json.loads(ContextGenerator(profile_path, subset="core").serialize())["@context"]
    assert pruned["Tag"] == full["Tag"]
    assert "Unused" in full and "Unused" not in pruned


@pytest.mark.parametrize("mergeimports", [True, False])
def test_subset_composes_with_mergeimports(profile_path, mergeimports):
    """The pruned schema keeps linkml:types as an import, so --mergeimports still decides whether
    its types are written out, while the merged sibling import is part of the schema either way."""
    schema = yaml.safe_load(LinkmlGenerator(profile_path, subset="core", mergeimports=mergeimports).serialize())
    assert "Tag" in schema["classes"]
    assert "Unused" not in schema["classes"]
    assert ("string" in schema["types"]) is mergeimports
    assert set(schema["types"]) >= {"RiskCode", "BaseCode"}


def test_subset_prunes_an_included_schema(profile_path, tmp_path):
    """A schema given with ``include`` is merged before pruning, so only what the subset reaches
    stays; without a subset, all of it is included as before."""
    extra = tmp_path / "extra.yaml"
    extra.write_text(
        yaml.safe_dump(
            {
                "id": "https://example.org/extra",
                "name": "extra",
                "classes": {
                    "Review": {"in_subset": ["core"], "attributes": {"reviewed": {"range": "Risk"}}},
                    "Draft": {"attributes": {"text": {}}},
                },
            }
        )
    )
    with_subset = json.loads(JsonSchemaGenerator(profile_path, subset="core", include=str(extra)).serialize())
    assert {"Review", "Risk"} <= set(with_subset["$defs"])
    assert "Draft" not in with_subset["$defs"]
    without_subset = json.loads(JsonSchemaGenerator(profile_path, include=str(extra)).serialize())
    assert {"Review", "Draft"} <= set(without_subset["$defs"])


def test_metamodel_minimal_subset():
    """MinimalSubset prunes the metamodel to the three definition classes that it names, their
    ancestors and mixins, type_definition (the range of default_range) and the ten slots that it
    names. The metamodel's own imports, which hold further mixins, stay imports."""
    sv = SchemaView(str(LOCAL_METAMODEL_YAML_FILE))
    pruned = prune_to_subset(sv, "MinimalSubset")
    assert set(pruned.classes) == {
        "schema_definition",
        "class_definition",
        "slot_definition",
        "type_definition",
        "definition",
        "element",
        "common_metadata",
        "expression",
        "class_expression",
        "slot_expression",
        "type_expression",
    }
    assert set(pruned.slots) == {
        "name",
        "id",
        "default_prefix",
        "default_range",
        "classes",
        "attributes",
        "range",
        "multivalued",
        "required",
        "identifier",
    }
    assert len(pruned.enums) == 0
    assert list(pruned.imports) == list(sv.schema.imports)
    assert (len(sv.schema.classes), len(sv.schema.slots), len(sv.schema.enums)) == (40, 216, 5)
    module = PydanticGenerator(str(LOCAL_METAMODEL_YAML_FILE), subset="MinimalSubset").compile_module()
    assert hasattr(module, "ClassDefinition")
    assert not hasattr(module, "EnumDefinition")
