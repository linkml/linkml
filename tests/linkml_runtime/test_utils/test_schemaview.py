"""Tests of the SchemaView package."""

from __future__ import annotations

import logging
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from jsonasobj2 import JsonObj

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import (
    ClassDefinition,
    ClassDefinitionName,
    EnumDefinition,
    Example,
    Prefix,
    SchemaDefinition,
    SlotDefinition,
    SlotDefinitionName,
    SubsetDefinition,
    TypeDefinition,
)
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.utils.schemaops import roll_down, roll_up
from linkml_runtime.utils.schemaview import (
    CLASSES,
    ENUMS,
    PREFIXES,
    SCHEMA_ELEMENTS,
    SLOTS,
    SUBSETS,
    TYPES,
    SchemaUsage,
    SchemaView,
    detect_cycles,
)
from linkml_runtime.utils.schemaview import _closure as graph_closure
from tests.test_utils import INPUT_DIR

INPUT_DIR_PATH = Path(INPUT_DIR)

logger = logging.getLogger(__name__)

SCHEMA_NO_IMPORTS = INPUT_DIR_PATH / "kitchen_sink_noimports.yaml"
SCHEMA_WITH_IMPORTS = INPUT_DIR_PATH / "kitchen_sink.yaml"
# one of the schemas (along with linkml:types) imported by kitchen_sink.yaml
SCHEMA_CORE = INPUT_DIR_PATH / "core.yaml"
SCHEMA_RELATIVE_IMPORT_TREE = INPUT_DIR_PATH / "imports_relative" / "L0_0" / "L1_0_0" / "main.yaml"
SCHEMA_RELATIVE_IMPORT_TREE2 = INPUT_DIR_PATH / "imports_relative" / "L0_2" / "main.yaml"

CREATURE_SCHEMA = "creature_schema"
CREATURE_SCHEMA_BASE_URL = "https://github.com/linkml/linkml-runtime/tests/test_utils/input/mcc"
CREATURE_SCHEMA_RAW_URL = (
    "https://github.com/linkml/linkml-runtime/raw/main/tests/test_utils/input/mcc/creature_schema.yaml"
)

CREATURE_SCHEMA_BASE_PATH = INPUT_DIR_PATH / "mcc"

yaml_loader = YAMLLoader()
IS_CURRENT = "is current"
EMPLOYED_AT = "employed at"
COMPANY = "Company"
PERSON = "Person"
ADULT = "Adult"
THING = "Thing"
AGENT = "agent"
ACTIVITY = "activity"
RELATED_TO = "related to"
AGE_IN_YEARS = "age in years"
EMPTY = ""
ID = "identifier"
KEY = "key"

ALL_ELEMENTS = [PREFIXES, *SCHEMA_ELEMENTS]
EXPECTED = {
    PREFIXES: {"sc1p1", "sc2p1"},
    CLASSES: {"sc1c1", "sc1c2", "sc2c1", "sc2c2"},
    SLOTS: {"sc1s1", "sc1s2", "sc2s1", "sc2s2"},
    ENUMS: {"sc1e1", "sc2e1"},
    TYPES: {"sc1t1", "sc2t1"},
    SUBSETS: {"sc1ss1", "sc2ss1"},
}

# workaround for the annoying plural version of "class"
PLURAL = {
    "class": CLASSES,
}


@pytest.fixture
def schema_view_no_imports() -> SchemaView:
    """Fixture for a SchemaView of the kitchen_sink_no_imports.yaml schema."""
    return SchemaView(SCHEMA_NO_IMPORTS)


@pytest.fixture
def schema_view_with_imports() -> SchemaView:
    """Fixture for a SchemaView of the kitchen_sink.yaml schema, which uses imports."""
    return SchemaView(SCHEMA_WITH_IMPORTS)


@pytest.fixture(scope="module")
def sv_merged_imports_keyword() -> SchemaView:
    """Kitchen sink SchemaView with imports merged through the `merge_imports` keyword."""
    return SchemaView(SCHEMA_WITH_IMPORTS, merge_imports=True)


@pytest.fixture(scope="module")
def sv_merged_imports_method() -> SchemaView:
    """Kitchen sink SchemaView with imports merged through running the `merge_imports()` method."""
    sv = SchemaView(SCHEMA_WITH_IMPORTS, merge_imports=False)
    sv.merge_imports()
    return sv


@pytest.fixture(scope="module")
def schema_view_core() -> SchemaView:
    """Fixture for SchemaView containing the core schema, as imported by kitchen_sink.yaml."""
    return SchemaView(SCHEMA_CORE, merge_imports=False)


@pytest.fixture(scope="session")
def sv_import_tree() -> SchemaView:
    """Fixture for a SchemaView for testing imports and ordering."""
    return SchemaView(INPUT_DIR_PATH / "imports" / "main.yaml")


@pytest.fixture(scope="session")
def sv_attributes() -> SchemaView:
    """Fixture for a SchemaView for testing attribute edge cases."""
    return SchemaView(INPUT_DIR_PATH / "attribute_edge_cases.yaml")


@pytest.fixture(scope="session")
def sv_inlined() -> SchemaView:
    """Fixture for a SchemaView for testing inlined slots."""
    return SchemaView(INPUT_DIR_PATH / "schemaview_is_inlined.yaml")


@pytest.fixture(scope="session")
def sv_structured_patterns() -> SchemaView:
    """Fixture for a SchemaView for testing structured patterns."""
    return SchemaView(INPUT_DIR_PATH / "pattern-example.yaml")


@pytest.fixture(scope="session")
def creature_view() -> SchemaView:
    return SchemaView(CREATURE_SCHEMA_BASE_PATH / "creature_schema.yaml")


@pytest.fixture(scope="session")
def creature_view_remote() -> SchemaView:
    """Fixture for a SchemaView for testing remote imports."""
    return SchemaView(CREATURE_SCHEMA_BASE_PATH / "creature_schema_remote.yaml")


@pytest.fixture(scope="session")
def creature_view_local() -> SchemaView:
    """Fixture for a SchemaView for testing local relative file path imports."""
    return SchemaView(CREATURE_SCHEMA_BASE_PATH / "creature_schema_local.yaml")


@pytest.fixture(scope="session")
def creature_view_direct_url() -> SchemaView:
    """Fixture for a SchemaView called directly by using the URL."""
    return SchemaView(CREATURE_SCHEMA_RAW_URL)


def make_schema(
    name: str,
    prefixes: list[Prefix] | None = None,
    classes: list[ClassDefinition] | None = None,
    slots: list[SlotDefinition] | None = None,
    enums: list[EnumDefinition] | None = None,
    types: list[TypeDefinition] | None = None,
    subsets: list[SubsetDefinition] | None = None,
) -> SchemaView:
    """Make a schema with the given elements.

    :param name:
    :param prefixes:
    :param classes:
    :param slots:
    :param enums:
    :param types:
    :param subsets:
    :return:
    """
    schema = SchemaDefinition(id=name, name=name)
    for p in prefixes or []:
        schema.prefixes[p.prefix_prefix] = p

    for c in classes or []:
        schema.classes[c.name] = c
    for s in slots or []:
        schema.slots[s.name] = s
    for e in enums or []:
        schema.enums[e.name] = e
    for t in types or []:
        schema.types[t.name] = t
    for s in subsets or []:
        schema.subsets[s.name] = s
    return SchemaView(schema)


@pytest.fixture
def sv_merge_1() -> SchemaView:
    """Simple schema for testing schema merges."""
    return make_schema(
        "s1",
        prefixes=[Prefix(prefix_prefix="sc1p1", prefix_reference="http://example.org/sc1url1")],
        classes=[ClassDefinition(name="sc1c1", slots=["sc1s1"]), ClassDefinition(name="sc1c2", slots=["sc1s2"])],
        slots=[SlotDefinition(name="sc1s1", range="string"), SlotDefinition(name="sc1s2", range="float")],
        enums=[
            EnumDefinition(
                name="sc1e1",
                permissible_values={
                    "sc1e1v1": "sc1e1v1",
                },
            )
        ],
        types=[TypeDefinition(name="sc1t1", base="string")],
        subsets=[SubsetDefinition(name="sc1ss1", description="sc1ss1")],
    )


@pytest.fixture
def sv_merge_2() -> SchemaView:
    """Another simple schema for testing schema merges."""
    return make_schema(
        "s2",
        prefixes=[Prefix(prefix_prefix="sc2p1", prefix_reference="http://example.org/sc2url1")],
        classes=[ClassDefinition(name="sc2c1", slots=["sc2s1"]), ClassDefinition(name="sc2c2", slots=["sc2s2"])],
        slots=[SlotDefinition(name="sc2s1", range="string"), SlotDefinition(name="sc2s2", range="float")],
        enums=[
            EnumDefinition(
                name="sc2e1",
                permissible_values={
                    "sc2e1v1": "sc2e1v1",
                },
            )
        ],
        types=[TypeDefinition(name="sc2t1", base="string")],
        subsets=[SubsetDefinition(name="sc2ss1", description="sc2ss1")],
    )


@pytest.fixture
def sv_empty() -> SchemaView:
    """Return an empty schema."""
    return make_schema("s3")


@pytest.fixture
def sv_issue_998() -> SchemaView:
    """SchemaView for tests related to https://github.com/linkml/linkml/issues/998."""
    schema = """
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
prefixes:
  linkml: https://w3id.org/linkml/
  schema: http://schema.org/
imports:
  - linkml:types
default_range: string

classes:
  Person:
    class_uri: schema:Person
    attributes:
      id:
        identifier: true
      employed:
        range: EmploymentStatusEnum
      past_relationship:
        range: RelationshipStatusEnum
    slots:
      - type
      - past_employer
  Programmer:
    attributes:
        employed:
            range: EmploymentStatusEnum
    slots:
      - type
      - past_employer
    slot_usage:
      type:
        range: TypeEnum

slots:
    status:
      range: PersonStatusEnum
    relationship:
      range: RelationshipStatusEnum
    type:
    past_employer:
        range: EmploymentStatusEnum
enums:
  PersonStatusEnum:
    permissible_values:
      ALIVE:
      DEAD:
      UNKNOWN:
  EmployedStatusEnum:
    permissible_values:
      EMPLOYED:
      UNEMPLOYED:
      UNKNOWN:
  RelationshipStatusEnum:
    permissible_values:
      UNKNOWN:
  TypeEnum:
    permissible_values:
      UNKNOWN:
"""
    return SchemaView(schema)


@pytest.fixture(scope="session")
def sv_induced_slots() -> SchemaView:
    """Schema for testing induced slots."""
    schema_str = """
id: https://example.com/test-induced
name: test-induced
title: test induced

description: >-
    test schema view's finding of induced slot information.

classes:
    class1:
        slots:
            - slot1
            - slot2
            - slot3
        slot_usage:
            slot2:
                description: induced slot2
                required: true
                range: class1
    class2:
        is_a: class1

    mixin1a:
        mixin: true
        slot_usage:
            slot2:
                description: mixin slot2
                required: false
                range: mixin1a

    mixin1b:
        mixin: true
        slot_usage:
            slot2:
                description: mixin slot2
                required: false
                range: mixin1b

    class2_1a:
        is_a: class2
        mixins:
          - mixin1a
          - mixin1b

    class2_1b:
        is_a: class2
        mixins:
          - mixin1b
          - mixin1a

    class0:

slots:
    slot1:
        description: non-induced slot1
        range: class0
    slot2:
        description: non-induced slot2
        required: false
        range: class0
    slot3:
        range: class0

"""
    return SchemaView(schema_str)


@pytest.fixture
def sv_ordering_tests() -> SchemaView:
    """SchemaView for testing class ordering."""
    schema = """
id: https://example.com/ordering-tests
name: ordering-tests
classes:
    Clarinet:
        rank: 5
        is_a: wind instrument
    instrument:
        rank: 2
    Bassoon:
        is_a: wind instrument
    wind instrument:
        rank: 1
        is_a: instrument
    Abacus:
        is_a: counting instrument
    counting instrument:
        rank: 4
        is_a: instrument
    Didgeridoo:
        rank: 3
        is_a: wind instrument
"""
    return SchemaView(schema)


def test_imports_from_schemaview(schema_view_with_imports: SchemaView) -> None:
    """View should by default dynamically include imports chain."""
    view = schema_view_with_imports
    view2 = SchemaView(view.schema)
    assert set(view.all_classes()) == set(view2.all_classes())
    assert set(view.all_classes(imports=False)) == set(view2.all_classes(imports=False))


@pytest.mark.parametrize(
    ("schema", "imports_closure"),
    [
        ("schema_view_no_imports", {"kitchen_sink"}),
        ("schema_view_with_imports", {"kitchen_sink", "core", "linkml:types"}),
    ],
)
def test_imports_closure(schema: str, imports_closure: set[str], request: pytest.FixtureRequest) -> None:
    """Test the imports closure on a schema with or without imports."""
    view = request.getfixturevalue(schema)
    assert set(view.imports_closure()) == imports_closure


def test_imports_closure_order(sv_import_tree: SchemaView) -> None:
    """Imports should override in a python-like order."""
    closure = sv_import_tree.imports_closure(imports=True)
    target = [
        "linkml:types",
        "s1_1",
        "s1_2_1_1_1",
        "s1_2_1_1_2",
        "s1_2_1_1",
        "s1_2_1",
        "s1_2",
        "s1",
        "s2_1",
        "s2_2",
        "s2",
        "s3_1",
        "s3_2",
        "s3",
        "main",
    ]
    assert closure == target


def test_imports_overrides(sv_import_tree: SchemaView) -> None:
    """Classes defined in the importing module should override same-named classes in imported modules."""
    defaults = {}
    target = {}
    for name, cls in sv_import_tree.all_classes(imports=True).items():
        target[name] = name
        defaults[name] = cls.attributes["value"].ifabsent

    assert defaults == target


def test_imports_relative() -> None:
    """Relative imports from relative imports should evaluate relative to the *importing* schema."""
    sv = SchemaView(SCHEMA_RELATIVE_IMPORT_TREE)
    closure = sv.imports_closure(imports=True)

    assert len(closure) == len(sv.schema_map.keys())
    assert closure == [
        "linkml:types",
        "../neighborhood_parent",
        "neighbor",
        "../parent",
        "../L1_0_1/L2_0_1_0/grandchild",
        "../../L0_1/L1_1_0/L2_1_0_0/apple",
        "../../L0_1/L1_1_0/L2_1_0_0/index",
        "../../L0_1/L1_1_0/L2_1_0_1/banana",
        "../../L0_1/L1_1_0/L2_1_0_1/index",
        "../../L0_1/L1_1_0/index",
        "../../L0_1/cousin",
        "../L1_0_1/dupe",
        "./L2_0_0_0/child",
        "./L2_0_0_1/child",
        "L2_0_0_2/two",
        "L2_0_0_2/one",
        "L2_0_0_2/four",
        "L2_0_0_2/three",
        "L2_0_0_2/stepchild",
        "main",
    ]

    # check that we can actually get the classes from the same-named schema
    classes = sv.all_classes(imports=True)
    assert "L110Index" in classes
    assert "L2100Index" in classes
    assert "L2101Index" in classes


# crap test
def test_imports_relative_load() -> None:
    """Relative imports from relative imports should load without FileNotFoundError."""
    sv = SchemaView(SCHEMA_RELATIVE_IMPORT_TREE2)
    sv.imports_closure(imports=True)


def test_imports_direct_remote_imports() -> None:
    """Tests that building a SchemaView directly from a remote URL works."""
    view = SchemaView("https://w3id.org/linkml/meta.yaml")
    main_classes = ["class_definition", "prefix"]
    imported_classes = ["annotation"]
    for c in main_classes:
        assert c in view.all_classes(imports=True)
        assert c in view.all_classes(imports=False)
    for c in imported_classes:
        assert c in view.all_classes(imports=True)
        assert c not in view.all_classes(imports=False)


def test_imports_remote_url_with_imports() -> None:
    """Test_remote_modular_schema_view."""
    url = (
        "https://raw.githubusercontent.com/linkml/linkml-runtime/"
        "2a46c65fe2e7db08e5e524342e5ff2ffb94bec92/tests/test_utils/input/kitchen_sink.yaml"
    )
    sv = SchemaView(url)
    assert sv.schema.name == "kitchen_sink"

    assert ACTIVITY in sv.all_classes()
    assert ACTIVITY in sv.all_classes(imports=True)
    assert ACTIVITY not in sv.all_classes(imports=False)


def test_imports_remote_repo_mixs() -> None:
    """Test loading from a remote repo.

    Note this test case involves using an external github repo.

    We use commit hashes to avoid false positive test fails caused by repo changes,
    but in theory this test could break if the mixs repo is deleted or changes its
    name or org.

    We will likely keep skipping this for now, but once stabilized it can be unskipped

    Note that the same functionality is likely captured in the other tests that use
    a more stable repo.
    """
    pytest.skip("Test is slow and may be fragile")
    mixs_revision_url = (
        "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/"
        "83be82a99d0a210e83b371b20b3dadb6423ec612/model/schema/mixs.yaml"
    )

    sv = SchemaView(mixs_revision_url)
    assert sv.schema.name == "MIxS"
    assert len(sv.all_classes()) > 0


@pytest.mark.skip("Skipped as fragile: will break if the remote schema changes")
def test_direct_remote_imports_additional() -> None:
    """Alternative test to: https://github.com/linkml/linkml/pull/1379."""
    url = "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/model/schema/mixs.yaml"
    view = SchemaView(url)
    assert view.schema.name == "MIxS"
    assert len(view.all_classes()) > 0


@pytest.mark.parametrize("importmap", [{"core": "/no/such/file"}, {"linkml:": "/no/such/file"}])
def test_import_map_fail(importmap: dict[str, Any]) -> None:
    view = SchemaView(SCHEMA_WITH_IMPORTS, importmap=importmap)
    with pytest.raises(FileNotFoundError, match="No such file or directory:"):
        view.all_classes()


@pytest.mark.parametrize("importmap", [None, {}, {"core": "core"}, {"core": str(INPUT_DIR_PATH / "core")}])
def test_import_map(importmap: dict[str, Any]) -> None:
    """Path to import file should be configurable."""
    view = SchemaView(SCHEMA_WITH_IMPORTS, importmap=importmap)
    view.all_classes()
    # ensure that all imports have loaded
    assert set(view.imports_closure()) == {"kitchen_sink", "core", "linkml:types"}
    # ensure that ACTIVITY only appears in all_classes if imports are enabled
    assert ACTIVITY in view.all_classes()
    assert ACTIVITY not in view.all_classes(imports=False)


def test_merge_imports_kwargs(schema_view_with_imports: SchemaView, sv_merged_imports_keyword: SchemaView) -> None:
    """Ensure that imports are or are not merged, depending on the kwargs."""

    assert ACTIVITY in schema_view_with_imports.all_classes()
    # ACTIVITY is only present in the imported schema
    assert ACTIVITY not in schema_view_with_imports.all_classes(imports=False)
    assert ACTIVITY not in schema_view_with_imports.schema.classes

    # all the imports have been merged together, so it doesn't matter if we call `all_classes`
    # with imports=True or imports=False
    assert ACTIVITY in sv_merged_imports_keyword.all_classes()
    assert ACTIVITY in sv_merged_imports_keyword.all_classes(imports=False)
    assert ACTIVITY in sv_merged_imports_keyword.schema.classes

    assert "was generated by" not in schema_view_with_imports.schema.slots
    assert "was generated by" in sv_merged_imports_keyword.schema.slots

    ks_prefixes = {"pav", "dce", "lego", "linkml", "biolink", "ks", "RO", "BFO", "tax"}
    assert set(schema_view_with_imports.schema.prefixes.keys()) == ks_prefixes

    merged_ks_prefixes = {*ks_prefixes, "core", "prov", "xsd", "schema", "shex"}
    assert set(sv_merged_imports_keyword.schema.prefixes.keys()) == merged_ks_prefixes


@pytest.mark.parametrize("fn_name", [f"all_{el}" for el in [*SCHEMA_ELEMENTS, "elements"]])
@pytest.mark.parametrize("merge_type", ["keyword", "method"])
def test_merge_imports_merge_method(
    fn_name: str,
    merge_type: str,
    schema_view_with_imports: SchemaView,
    request: pytest.FixtureRequest,
) -> None:
    """Ensure merging via keyword and or via the merge_imports method work identically."""

    # use the schemaview with imports not merged on init as the base for comparison
    view = schema_view_with_imports

    all_elements = set(view.all_elements())
    all_elements_no_imports = set(view.all_elements(imports=False))
    # there should be more elements in the schema when imports are included
    assert len(all_elements) > len(all_elements_no_imports)
    assert all_elements.issuperset(all_elements_no_imports)

    # compare it to the SV with imports already merged
    if merge_type == "keyword":
        # sv with imports merged using SchemaView(path, merge_imports=True)
        test_view = request.getfixturevalue("sv_merged_imports_keyword")
    else:
        # sv with imports merged using sv.merge_imports()
        test_view = request.getfixturevalue("sv_merged_imports_method")

    # check the merged view has the same classes as the original version, with or without imports
    assert set(getattr(view, fn_name)(imports=True)) == set(getattr(test_view, fn_name)(imports=True))

    # if we merged on init or by calling merge_imports, then the imports should be merged and it
    # shouldn't matter if we call with or without imports
    assert set(getattr(test_view, fn_name)(imports=False)) == set(getattr(test_view, fn_name)(imports=True))


def test_metamodel_imports() -> None:
    """Tests imports of the metamodel.

    Note: this test and others should be able to run without network connectivity.
    SchemaView should make use of the version of the metamodel distributed with the package
    over the network available version.
    """
    schema = SchemaDefinition(id="test", name="metamodel-imports-test", imports=["linkml:meta"])
    sv = SchemaView(schema)
    all_classes = sv.all_classes()
    assert len(all_classes) > 20
    schema_str = yaml_dumper.dumps(schema)
    sv = SchemaView(schema_str)
    assert len(sv.all_classes()) > 20
    assert all_classes == sv.all_classes()


def test_non_linkml_remote_import() -> None:
    """Test that a remote import _not_ using the linkml prefix works.

    See: https://github.com/linkml/linkml/issues/1627.
    """
    schema = SchemaDefinition(
        id="test_non_linkml_remote_import",
        name="test_non_linkml_remote_import",
        prefixes=[Prefix(prefix_prefix="foo", prefix_reference="https://w3id.org/linkml/")],
        imports=["foo:types"],
        slots=[SlotDefinition(name="an_int", range="integer")],
        classes=[ClassDefinition(name="AClass", slots=["an_int"])],
    )
    sv = SchemaView(schema)
    slots = sv.class_induced_slots("AClass", imports=True)
    assert len(slots) == 1


def test_metamodel_in_schemaview() -> None:
    """Test using SchemaView with the metamodel."""
    view = package_schemaview("linkml_runtime.linkml_model.meta")
    assert "meta" in view.imports_closure()
    assert "linkml:types" in view.imports_closure()
    assert "meta" in view.imports_closure(imports=False)
    assert "linkml:types" not in view.imports_closure(imports=False)
    assert len(view.imports_closure(imports=False)) == 1
    all_classes = list(view.all_classes().keys())
    all_classes_no_imports = list(view.all_classes(imports=False).keys())
    for cn in ["class_definition", "type_definition", "slot_definition"]:
        assert cn in all_classes
        assert cn in all_classes_no_imports
        assert view.get_identifier_slot(cn).name == "name"
    for cn in ["annotation", "extension"]:
        assert cn in all_classes, "imports should be included by default"
        assert cn not in all_classes_no_imports, "imported class unexpectedly included"
    for sn in ["id", "name", "description"]:
        assert sn in view.all_slots()
    for tn in ["uriorcurie", "string", "float"]:
        assert tn in view.all_types()
        assert tn not in view.all_types(imports=False)
    for cn, c in view.all_classes().items():
        uri = view.get_uri(cn, expand=True)
        assert uri is not None
        if cn not in ["structured_alias", "UnitOfMeasure", "ValidationReport", "ValidationResult"]:
            assert "https://w3id.org/linkml/" in uri
        induced_slots = view.class_induced_slots(cn)
        for s in induced_slots:
            exp_slot_uri = view.get_uri(s, expand=True)
            assert exp_slot_uri is not None


def test_in_schema(schema_view_with_imports: SchemaView) -> None:
    """Test the in_schema function for determining the source schema of a class or slot."""
    view = schema_view_with_imports

    assert view.in_schema(ClassDefinitionName("Person")) == "kitchen_sink"
    assert view.in_schema(SlotDefinitionName("id")) == "core"
    assert view.in_schema(SlotDefinitionName("name")) == "core"
    assert view.in_schema(SlotDefinitionName(ACTIVITY)) == "core"
    assert view.in_schema(SlotDefinitionName("string")) == "types"


CREATURE_EXPECTED = {
    "class": {
        CREATURE_SCHEMA: {"MythicalCreature", "HasMagic", "MagicalAbility", "Dragon", "Phoenix", "Unicorn"},
        "creature_basics": {"Entity", "Creature", "Location", "CreatureAttribute", "HasHabitat"},
    },
    "slot": {
        CREATURE_SCHEMA: {"creature_class", "magical_abilities", "level_of_magic"},
        "creature_basics": {"id", "name", "description", "species", "habitat"},
    },
    "type": {
        CREATURE_SCHEMA: {"MagicLevel"},
        "creature_types": {"string", "integer", "boolean"},
    },
    "enum": {CREATURE_SCHEMA: {"CreatureClass"}},
    "subset": {CREATURE_SCHEMA: set(), "creature_subsets": {"mythical_creature", "generic_creature"}},
    "element": {},
}

# add in the elements
for value in CREATURE_EXPECTED.values():
    for s_name, el in value.items():
        if s_name not in CREATURE_EXPECTED["element"]:
            CREATURE_EXPECTED["element"][s_name] = set()
        CREATURE_EXPECTED["element"][s_name].update(el)


@pytest.mark.parametrize(
    "schema", ["creature_view", "creature_view_remote", "creature_view_local", "creature_view_direct_url"]
)
@pytest.mark.parametrize("entity", CREATURE_EXPECTED.keys())
def test_creature_schema_entities_with_without_imports(
    schema: str, entity: str, request: pytest.FixtureRequest
) -> None:
    """Test retrieval of entities from the creature schema.

    Tests the following methods:
    - all_{entity}s (e.g. all_classes, all_slots, etc.) with and without imports
    - get_{entity} (e.g. get_class, get_slot, etc.)
    - the "from_schema" attribute of the retrieved entities

    The schemas tested are:
    - creature_view: the main schema with all entities
    - creature_view_remote: imports the creature schema using a curie and a remote URL
    - creature_view_local: imports the creature schema using a local relative file path
    - creature_view_direct_url: imports the creature schema using a direct URL
    """
    creature_view = request.getfixturevalue(schema)

    # use the PLURAL mapping to get the correct method name to retrieve all entities of the given type
    get_all_fn = "all_" + PLURAL.get(entity, f"{entity}s")
    if schema in ("creature_view", "creature_view_direct_url"):
        assert set(getattr(creature_view, get_all_fn)(imports=False)) == CREATURE_EXPECTED[entity][CREATURE_SCHEMA]
    else:
        assert set(getattr(creature_view, get_all_fn)(imports=False)) == set()

    # merge the values from all the sources to get the complete set of entities
    all_entities = set().union(*CREATURE_EXPECTED[entity].values())
    assert set(getattr(creature_view, get_all_fn)(imports=True)) == all_entities

    # run creature_view.get_{entity} for each entity and check the source
    for src in CREATURE_EXPECTED[entity]:
        for entity_name in CREATURE_EXPECTED[entity][src]:
            e = getattr(creature_view, f"get_{entity}")(entity_name, imports=True)
            assert e.from_schema == f"{CREATURE_SCHEMA_BASE_URL}/{src}"
            # N.b. this may fail in schemas where there are different types
            # of element with the same name
            assert e == creature_view.get_element(entity_name)


@pytest.mark.parametrize("entity", CREATURE_EXPECTED.keys())
def test_get_entities_with_without_imports(creature_view: SchemaView, entity: str) -> None:
    """Test retrieval of a specific entity from the creature schema."""
    get_fn = f"get_{entity}"

    for src in CREATURE_EXPECTED[entity]:
        for entity_name in CREATURE_EXPECTED[entity][src]:
            if src == CREATURE_SCHEMA:
                # if the source is the main schema, we can use the method directly
                e = getattr(creature_view, get_fn)(entity_name, imports=False)
                assert e.name == entity_name
                assert e == creature_view.get_element(entity_name, imports=False)
                # N.b. BUG: due to caching and how the `from_schema` element is generated,
                # we cannot know whether it will be populated.
                # assert e.from_schema is None
            else:
                # if the source is an imported schema, we expect None without imports
                assert getattr(creature_view, get_fn)(entity_name, imports=False) is None
                assert creature_view.get_element(entity_name, imports=False) is None

                if entity != "element":
                    # in strict mode, we expect an error if the entity does not exist
                    with pytest.raises(ValueError, match=f'No such {entity}: "{entity_name}"'):
                        getattr(creature_view, f"get_{entity}")(entity_name, imports=False, strict=True)

            # turn on imports
            e = getattr(creature_view, f"get_{entity}")(entity_name, imports=True)
            assert e.from_schema == f"{CREATURE_SCHEMA_BASE_URL}/{src}"
            assert e == creature_view.get_element(entity_name, imports=True)


@pytest.mark.parametrize("entity", argvalues=[e for e in CREATURE_EXPECTED if e != "element"])
def test_get_entity_does_not_exist(creature_view: SchemaView, entity: str) -> None:
    """Test retrieval of a specific entity from the creature schema."""
    get_fn = f"get_{entity}"

    # returns None unless the `strict` flag is passed
    assert getattr(creature_view, get_fn)("does_not_exist") is None
    assert creature_view.get_element("does_not_exist") is None

    # raises an error with `strict` flag on
    with pytest.raises(ValueError, match=f'No such {entity}: "does_not_exist"'):
        getattr(creature_view, get_fn)("does_not_exist", strict=True)


# creature schema ancestry
def test_get_class_roots_class_leaves(creature_view: SchemaView) -> None:
    """Test the retrieval of class roots and leaves in the creature schema."""

    # roots are classes with no is_a parents and no mixins
    assert set(creature_view.class_roots()) == {"CreatureAttribute", "Entity", "Location", "MagicalAbility"}
    # leaves are classes with no subclasses and not used as mixins
    assert set(creature_view.class_leaves()) == {"Dragon", "Phoenix", "Unicorn", "Location", "MagicalAbility"}

    for fn in ["class_leaves", "class_roots"]:
        # disabling both mixins and is_a destroys all links between classes
        assert set(getattr(creature_view, fn)(mixins=False, is_a=False)) == set(creature_view.all_classes())


""" Relationship tests, courtesy of the mythical creatures schema.

    Creature schema basics:

    is_a relationships:
    Entity
    [i] Creature --mixin-- HasHabitat
        [i] MythicalCreature --mixin-- HasMagic
            [i] Dragon
            [i] Phoenix
            [i] Unicorn

    CreatureAttribute
    [i] HasHabitat
    [i] HasMagic

    Mixins:
    Creature: mixin HasHabitat
    MythicalCreature: mixin HasMagic

    Classes used as a range, with no relationships to other classes
    - Location
    - MagicalAbility
"""


def test_class_is_a_children_descendants(creature_view: SchemaView) -> None:
    """Tests for retrieving is_a child classes and descendant classes."""
    # subclasses of 'Entity'
    assert set(creature_view.class_children("Entity")) == {"Creature"}
    assert set(creature_view.class_children("Creature")) == {"MythicalCreature"}
    assert set(creature_view.class_children("MythicalCreature")) == {"Dragon", "Phoenix", "Unicorn"}

    entity_descendants = set(creature_view.class_descendants("Entity"))
    assert entity_descendants == {
        "Entity",
        "Creature",
        "MythicalCreature",
        "Dragon",
        "Phoenix",
        "Unicorn",
    }
    # all are is_a relationships
    assert entity_descendants == set(creature_view.class_descendants("Entity", mixins=False))
    # no is_a relationships ==> no descendants
    assert creature_view.class_descendants("Entity", is_a=False) == ["Entity"]

    # direct children of "CreatureAttribute"
    assert set(creature_view.class_children("CreatureAttribute")) == {"HasHabitat", "HasMagic"}
    # no is_a => no children
    assert creature_view.class_children("CreatureAttribute", is_a=False) == []
    # is_a descendants of "CreatureAttribute"
    assert set(creature_view.class_descendants("CreatureAttribute", mixins=False)) == {
        "CreatureAttribute",
        "HasHabitat",
        "HasMagic",
    }


def test_class_mixin_children_descendants(creature_view: SchemaView) -> None:
    """Tests for retrieving mixin child classes and descendant classes."""
    # mixins
    for mixin, mixed_into in [("HasHabitat", "Creature"), ("HasMagic", "MythicalCreature")]:
        assert creature_view.class_children(mixin) == [mixed_into]
        assert creature_view.class_children(mixin, is_a=False) == [mixed_into]
        assert creature_view.class_children(mixin, mixins=False) == []


def test_class_is_a_mixin_children_descendants(creature_view: SchemaView) -> None:
    """Tests for retrieving is_a AND mixin child classes and descendant classes."""
    # HasHabitat is a mixin of Creature (see prev test)
    assert set(creature_view.class_descendants("HasHabitat", is_a=False)) == {"HasHabitat", "Creature"}
    # Creature has subclasses, so with is_a relationships turned on,
    # HasHabitat gains these as descendants
    assert set(creature_view.class_descendants("HasHabitat")) == {
        "HasHabitat",
        "Creature",
        "MythicalCreature",
        "Dragon",
        "Phoenix",
        "Unicorn",
    }
    # without the mixin relationship, HasHabitat has descendants (except itself)
    assert creature_view.class_descendants("HasHabitat", mixins=False) == ["HasHabitat"]

    # Similar case for HasMagic, a mixin for MythicalCreature
    assert set(creature_view.class_descendants("HasMagic", is_a=False)) == {"HasMagic", "MythicalCreature"}
    assert set(creature_view.class_descendants("HasMagic")) == {
        "HasMagic",
        "MythicalCreature",
        "Dragon",
        "Phoenix",
        "Unicorn",
    }
    assert creature_view.class_descendants("HasMagic", mixins=False) == ["HasMagic"]

    # HasMagic and HasHabitat are both is_a children of CreatureAttribute
    assert set(creature_view.class_children("CreatureAttribute")) == {"HasHabitat", "HasMagic"}
    assert creature_view.class_children("CreatureAttribute", is_a=False) == []
    assert set(creature_view.class_descendants("CreatureAttribute")) == {
        "CreatureAttribute",
        "HasHabitat",
        "HasMagic",
        "Creature",
        "MythicalCreature",
        "Dragon",
        "Phoenix",
        "Unicorn",
    }
    assert set(creature_view.class_descendants("CreatureAttribute", mixins=False)) == {
        "CreatureAttribute",
        "HasHabitat",
        "HasMagic",
    }
    assert set(creature_view.class_descendants("CreatureAttribute", is_a=False)) == {"CreatureAttribute"}

    # The two "CreatureAttribute" subclasses are mixins to classes
    # in the "Creature" hierarchy, so the full descendant list includes
    # "Creature" and its subclasses
    assert set(creature_view.class_descendants("CreatureAttribute")) == {
        "CreatureAttribute",
        "HasHabitat",
        "HasMagic",
        "Creature",
        "MythicalCreature",
        "Dragon",
        "Phoenix",
        "Unicorn",
    }
    # with mixins disabled, only the is_a descendants of CreatureAttribute are returned
    assert set(creature_view.class_descendants("CreatureAttribute", mixins=False)) == {
        "CreatureAttribute",
        "HasHabitat",
        "HasMagic",
    }
    assert creature_view.class_descendants("CreatureAttribute", is_a=False) == ["CreatureAttribute"]


def test_class_relatives_no_neighbours(creature_view: SchemaView) -> None:
    """Test relationships for classes with no relationships!"""
    # lonesome classes
    for cn in ["Location", "MagicalAbility"]:
        assert creature_view.class_children(cn) == []
        assert creature_view.class_descendants(cn) == [cn]
        assert creature_view.class_descendants(cn, reflexive=False) == []
        assert creature_view.class_parents(cn) == []
        assert creature_view.class_ancestors(cn) == [cn]
        assert creature_view.class_ancestors(cn, reflexive=False) == []


def test_class_parents_ancestors(creature_view: SchemaView) -> None:
    """Test class parentage and ancestry, creature-style!"""
    # Creature is_a Entity and mixes in HasHabitat
    assert creature_view.class_parents("Creature", mixins=False) == ["Entity"]
    assert creature_view.class_parents("Creature", is_a=False) == ["HasHabitat"]

    # MythicalCreature is_a Creature and mixes in HasMagic
    assert creature_view.class_parents("MythicalCreature", mixins=False) == ["Creature"]
    assert creature_view.class_parents("MythicalCreature", is_a=False) == ["HasMagic"]

    # HasHabitat and HasMagic are both is_a children of CreatureAttribute
    for attr in ["HasHabitat", "HasMagic"]:
        assert creature_view.class_parents(attr) == ["CreatureAttribute"]
        assert creature_view.class_parents(attr, is_a=False) == []
        assert set(creature_view.class_ancestors(attr)) == {attr, "CreatureAttribute"}

    # Creature ancestry
    assert set(creature_view.class_ancestors("Creature")) == {"Creature", "Entity", "HasHabitat", "CreatureAttribute"}
    # mixins only
    assert set(creature_view.class_ancestors("Creature", is_a=False)) == {"Creature", "HasHabitat"}
    # is_a only
    assert set(creature_view.class_ancestors("Creature", mixins=False)) == {"Creature", "Entity"}

    # MythicalCreature ancestry
    assert set(creature_view.class_ancestors("MythicalCreature")) == {
        "MythicalCreature",
        "HasMagic",
        "Creature",
        "HasHabitat",
        "Entity",
        "CreatureAttribute",
    }
    assert set(creature_view.class_ancestors("MythicalCreature", is_a=False)) == {"MythicalCreature", "HasMagic"}
    assert set(creature_view.class_ancestors("MythicalCreature", mixins=False)) == {
        "MythicalCreature",
        "Creature",
        "Entity",
    }

    # Dragon, Phoenix, and Unicorn are subclasses of MythicalCreature,
    # Creature, and Entity
    for mc in ["Dragon", "Phoenix", "Unicorn"]:
        assert set(creature_view.class_parents(mc, mixins=False)) == {"MythicalCreature"}
        assert set(creature_view.class_ancestors(mc, mixins=False)) == {mc, "MythicalCreature", "Creature", "Entity"}
        # no direct mixins
        assert creature_view.class_ancestors(mc, is_a=False) == [mc]
        # all ancestors
        assert set(creature_view.class_ancestors(mc)) == {
            mc,
            "HasMagic",
            "Creature",
            "CreatureAttribute",
            "HasHabitat",
            "MythicalCreature",
            "Entity",
        }


ORDERING_TESTS = {
    # Bassoon and Abacus are unranked, so appear at the end of the list.
    "rank": ["wind instrument", "instrument", "Didgeridoo", "counting instrument", "Clarinet", "Bassoon", "Abacus"],
    "preserve": [
        "Clarinet",
        "instrument",
        "Bassoon",
        "wind instrument",
        "Abacus",
        "counting instrument",
        "Didgeridoo",
    ],
    # lexical ordering is case-sensitive, so all the capitalized words come first.
    "lexical": ["Abacus", "Bassoon", "Clarinet", "Didgeridoo", "counting instrument", "instrument", "wind instrument"],
    # TODO: this looks very dodgy
    "inheritance": [
        "instrument",
        "wind instrument",
        "Clarinet",
        "Bassoon",
        "counting instrument",
        "Abacus",
        "Didgeridoo",
    ],
}


@pytest.mark.parametrize(
    ("ordered_by"),
    ORDERING_TESTS.keys(),
)
def test_all_classes_ordered_by(sv_ordering_tests: SchemaView, ordered_by: str) -> None:
    """Test the ordered_by method."""
    assert list(sv_ordering_tests.all_classes(ordered_by=ordered_by).keys()) == ORDERING_TESTS[ordered_by]


def test_all_classes_class_induced_slots(schema_view_with_imports: SchemaView) -> None:
    """Test all_classes and class_induced_slots."""
    view = schema_view_with_imports

    for cn, c in view.all_classes().items():
        assert cn == c.name
        if c in view.all_classes(imports=False).values():
            assert c.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        else:
            assert c.from_schema == "https://w3id.org/linkml/tests/core"
        for s in view.class_induced_slots(cn):
            if s in view.all_classes(imports=False).values():
                assert s.slot_uri is not None
                assert s.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"

    assert ACTIVITY in view.all_classes()
    assert ACTIVITY not in view.all_classes(imports=False)


def test_class_slots(schema_view_no_imports: SchemaView) -> None:
    """Test class_slots method."""
    view = schema_view_no_imports

    assert set(view.class_slots(PERSON)) == {
        "id",
        "name",
        "has employment history",
        "has familial relationships",
        "has medical history",
        AGE_IN_YEARS,
        "addresses",
        "has birth event",
        "reason_for_happiness",
        "aliases",
    }
    assert view.class_slots(PERSON) == view.class_slots(ADULT)
    assert set(view.class_slots(COMPANY)) == {"id", "name", "ceo", "aliases"}


def test_all_slots_induced_slots(schema_view_with_imports: SchemaView) -> None:
    """Test all_slots and induced_slot."""
    view = schema_view_with_imports

    for sn, s in view.all_slots().items():
        assert sn == s.name
        s_induced = view.induced_slot(sn)
        assert s_induced.range is not None
        if s in view.all_slots(imports=False).values():
            assert s.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        else:
            assert s.from_schema == "https://w3id.org/linkml/tests/core"


def test_all_types_induced_types(schema_view_with_imports: SchemaView) -> None:
    """Test all_types and the induced_type functions."""
    view = schema_view_with_imports
    for tn, t in view.all_types().items():
        assert tn == t.name
        induced_t = view.induced_type(tn)
        assert induced_t.uri is not None
        assert induced_t.base is not None
        if t in view.all_types(imports=False).values():
            assert t.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        else:
            assert t.from_schema in ["https://w3id.org/linkml/tests/core", "https://w3id.org/linkml/types"]

    assert "string" in view.all_types()
    assert "string" not in view.all_types(imports=False)
    assert len(view.type_ancestors("SymbolString")) == len(["SymbolString", "string"])


@pytest.mark.parametrize(
    ("schema", "type_roots"),
    [
        (
            """
  string:
    uri: xsd:string
    base: str
  integer:
    uri: xsd:integer
    base: int
  boolean:
    uri: xsd:boolean
    base: Bool
""",
            {"string", "integer", "boolean"},
        ),
        (
            """
  string:
    uri: xsd:string
    base: str
  acronym:
    typeof: string
  TLA:
    typeof: acronym
  even_number:
    typeof: integer
  integer:
    uri: xsd:integer
    base: int
""",
            {"string", "integer"},
        ),
        (
            """
  circular_type:
    uri: xsd:Circle
    typeof: type_circle

  type_circle:
    typeof: circular_type

  semi_circular_type:
    typeof: circular_type
""",
            set(),
        ),
    ],
)
def test_type_roots(schema: str, type_roots: set[str]) -> None:
    """Test the retrieval of types with no parent type."""
    schema_head = "id: https://w3id.org/linkml/tests/types\nname: types\ntypes:\n"

    sv = SchemaView(f"{schema_head}\n{schema}")
    assert set(sv.type_roots()) == type_roots


def test_all_enums(schema_view_with_imports: SchemaView) -> None:
    """Test all_enums"""
    view = schema_view_with_imports

    for en, e in view.all_enums().items():
        assert en == e.name
        if e in view.all_enums(imports=False).values():
            assert e.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        else:
            assert e.from_schema == "https://w3id.org/linkml/tests/core"


def test_get_uri(schema_view_with_imports: SchemaView) -> None:
    """Test the get_uri function."""
    view = schema_view_with_imports

    assert view.get_class("agent").class_uri == "prov:Agent"
    assert view.get_uri(AGENT) == "prov:Agent"
    logger.debug(view.get_class("Company").class_uri)

    assert view.get_uri(COMPANY) == "ks:Company"
    assert view.get_uri(COMPANY, expand=True) == "https://w3id.org/linkml/tests/kitchen_sink/Company"
    logger.debug(view.get_uri("TestClass"))
    assert view.get_uri("TestClass") == "core:TestClass"
    assert view.get_uri("TestClass", expand=True) == "https://w3id.org/linkml/tests/core/TestClass"

    assert (
        view.get_uri("TestClass", expand=True, use_element_type=True)
        == "https://w3id.org/linkml/tests/core/class/TestClass"
    )
    assert view.get_uri("TestClass", use_element_type=True) == "core:class/TestClass"
    assert view.get_uri("name", use_element_type=True) == "core:slot/name"

    assert view.get_uri("string") == "xsd:string"


def test_uris_without_default_prefix() -> None:
    """Test if uri is correct if no default_prefix is defined for the schema.

    See: https://github.com/linkml/linkml/issues/2578
    """
    schema_definition = SchemaDefinition(id="https://example.org/test#", name="test_schema")

    view = SchemaView(schema_definition)
    view.add_class(ClassDefinition(name="TestClass", from_schema="https://example.org/another#"))
    view.add_slot(SlotDefinition(name="test_slot", from_schema="https://example.org/another#"))

    assert view.get_uri("TestClass", imports=True) == "https://example.org/test#TestClass"
    assert view.get_uri("test_slot", imports=True) == "https://example.org/test#test_slot"


def test_slot_unit(schema_view_with_imports: SchemaView) -> None:
    """Test the ability to capture unit information in a slot."""
    view = schema_view_with_imports
    # units
    height = view.get_slot("height_in_m")
    assert height.unit.ucum_code == "m"


def test_children_method(schema_view_no_imports: SchemaView) -> None:
    """Test retrieval of the children of a class."""
    view = schema_view_no_imports
    assert view.get_children(PERSON) == [ADULT]


def test_all_aliases(schema_view_no_imports: SchemaView) -> None:
    """Test the aliases slot (not: alias)."""
    view = schema_view_no_imports
    aliases = view.all_aliases()
    assert "identifier" in aliases["id"]
    assert "A" in aliases["subset A"]
    assert "B" in aliases["subset B"]
    assert "dad" in aliases[ADULT]


def test_alias_slot(schema_view_no_imports: SchemaView) -> None:
    """Tests the alias slot.

    The induced slot alias should always be populated. For induced slots, it should default to the
    name field if not present.
    """
    view = schema_view_no_imports
    for c in view.all_classes().values():
        for s in view.class_induced_slots(c.name):
            assert s.alias is not None  # Assert that alias is not None

    postal_code_slot = view.induced_slot("postal code", "Address")
    assert postal_code_slot.name == "postal code"  # Assert name is 'postal code'
    assert postal_code_slot.alias == "zip"  # Assert alias is 'zip'


"""Tests of SchemaView range-related functions.

    These tests cover range determination for slots in schemas with various combinations of default_range values and linkml:Any range declarations.

    There are three schemas used in these tests:

    The `range_local` (RL) schema
        - based on RANGE_DATA["schema_path"]["range_local"]
        - the default_range value in this schema is referred to as local_default;

    The `range_importer` (RI) schema, which imports the range_local schema
        - the range referred to as importer_default;
        - the file contents are based on RANGE_DATA["schema_path"]["range_importer"]

    The `range_import_importer` (RII) schema, which imports the range_importer schema
        - the range is import_importer_default;
        - the schema is generated as a text string, rather than being read from a file.

    The range_tuple parameter specifies the default_range values for each of these schemas in the order
    range_local, range_importer, range_import_importer.

    A value of "" (EMPTY) means that there is no default_range set.
    A value of None means that this file should not be generated.

    RANGE_TUPLES contains all the combinations of range_tuple that are valid.

"""

RL = "range_local"
RI = "range_importer"
RII = "range_import_importer"

RANGE_DATA = {
    # value of the default_range in the schema
    "default": {r: f"{r}_default" for r in [RL, RI, RII]},
    # path to the original schema file
    "schema_path": {r: INPUT_DIR_PATH / f"{r}.yaml" for r in [RL, RI]},
}

RLD = RANGE_DATA["default"][RL]
RID = RANGE_DATA["default"][RI]
RIID = RANGE_DATA["default"][RII]

RANGE_TUPLES = [
    # local schema only
    (EMPTY, None, None),
    (RLD, None, None),
    # local imported by `importer` schema
    (EMPTY, EMPTY, None),
    (RLD, EMPTY, None),
    (EMPTY, RID, None),
    (RLD, RID, None),
    # `importer` schema imported by a third schema
    (EMPTY, EMPTY, EMPTY),
    (EMPTY, RID, EMPTY),
    (EMPTY, EMPTY, RIID),
    (EMPTY, RID, RIID),
    (RLD, EMPTY, EMPTY),
    (RLD, RID, EMPTY),
    (RLD, EMPTY, RIID),
    (RLD, RID, RIID),
]


def save_temp_file(contents: str, filename: str, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Save contents to a temporary file and return the path.

    :param contents: the contents to save
    :type contents: str
    :param filename: the name of the file to create
    :type filename: str
    :param tmp_path_factory: pytest fixture for generating temporary paths
    :type tmp_path_factory: pytest.TempPathFactory
    :return: path to the generated file
    :rtype: Path
    """
    tmp_file = tmp_path_factory.mktemp("test_schemaview") / filename
    tmp_file.write_text(contents)
    return tmp_file


def gen_schema_name(range_tuple: tuple[str, str | None, str | None]) -> str | None:
    """Generate a schema name from a range tuple.

    :param range_tuple: tuple of the values for the local, importer, and import_importer default_range values.
    :type range_tuple: tuple[str, str | None, str | None]
    :raises ValueError: if the tuple is not the correct length
    :return: a generated schema name, or None if the combination is invalid
    :rtype: str | None
    """
    if len(range_tuple) != 3:
        err_msg = (
            "A schema name requires three parts: local, importer, and import_importer. You supplied\n"
            + range_tuple
            + "\n"
        )
        raise ValueError(err_msg)

    (local, importer, import_importer) = range_tuple

    # invalid combination
    if importer is None and import_importer is not None:
        return None

    schema_name = "sv_range"
    schema_name += "_local_default" if local else "_local"

    if importer:
        schema_name += "__importer_default"
    elif importer == EMPTY:
        schema_name += "__importer"

    if import_importer:
        schema_name += "__import_importer_default"
    elif import_importer == EMPTY:
        schema_name += "__import_importer"
    return schema_name


def gen_range_file_with_default(range_id: str, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Generate a copy of the range file with a default_range added and return the path.
    Obviates the need for maintaining a copy with a default_range tagged to the end.

    :param range_id: the range file to use; must be one of RL, RI
    :type range_id: str
    :param tmp_path_factory: pytest fixture for generating temporary paths
    :type tmp_path_factory: pytest.TempPathFactory
    :return: path to the generated file
    :rtype: Path
    """
    schema_yaml = RANGE_DATA["schema_path"][range_id].read_text()
    default_range = RANGE_DATA["default"][range_id]
    range_default_yaml = f"{schema_yaml}\n\ndefault_range: {default_range}\n"
    return save_temp_file(range_default_yaml, f"{default_range}.yaml", tmp_path_factory)


@pytest.fixture(scope="session")
def range_local_default_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Generate a copy of the range_local file with a default range specified and return the path."""
    return gen_range_file_with_default(RL, tmp_path_factory)


@pytest.fixture(scope="session")
def range_importer_default_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Generate a copy of the range importer file with a default range specified and return the path."""
    return gen_range_file_with_default(RI, tmp_path_factory)


def sv_range_import_whatever(
    request: pytest.FixtureRequest, range_tuple: tuple[str, str | None, str | None]
) -> tuple[SchemaView, tuple[str, str | None, str | None]]:
    """Generate a schema and optionally, schemas that import that schema.

    There are three potential schemas generated:
    - the range schema, based on RANGE_DATA["schema_path"]["range_local"]; the range is referred to as local_default;
    - the importer schema, which imports the range schema; the range referred to as importer_default;
      the file contents are based on RANGE_DATA["schema_path"]["range_importer"]
    - the import_importer schema, which imports the importer schema; the range is import_importer_default;
      the schema is constructed in this function.

    The range_tuple parameter specifies the default_range values for each of these schemas in the order
    range_local, range_importer, range_import_importer.

    A value of "" (EMPTY) means that there is no default_range set.
    A value of None means that this file should not be generated.

    :param request: fixture request object for retrieving fixture-related stuff
    :type request: pytest.FixtureRequest
    :param range_tuple: the default_range for the range schema; if the value of local_default is "", the default_range is not set.
    :type range_tuple: tuple[str, str|None, str|None]
    :return: a loaded SchemaView for the appropriate schema(s)
    :rtype: SchemaView
    """
    (local_default, importer_default, import_importer_default) = range_tuple

    if importer_default is None and import_importer_default is not None:
        err_msg = "If the importer is not used, any import_importer value other than None is not valid"
        raise ValueError(err_msg)

    range_local_path = RANGE_DATA["schema_path"][RL]
    range_importer_path = RANGE_DATA["schema_path"][RI]
    importmap = {}

    if local_default:
        # make a copy of RANGE_DATA["schema_path"][RL] with a default added
        range_local_path = request.getfixturevalue("range_local_default_path")

    if importer_default:
        # make a copy of RANGE_DATA["schema_path"][RI] with a default added
        range_importer_path = request.getfixturevalue("range_importer_default_path")

    importmap[RL] = str(range_local_path.parent / range_local_path.stem)
    importmap[RI] = str(range_importer_path.parent / range_importer_path.stem)

    if import_importer_default is None:
        sv = None
        # no import, so just use the range_local schema
        if importer_default is None:
            sv = SchemaView(range_local_path)
        else:
            # importing the range_local schema using the range_importer schema
            sv = SchemaView(range_importer_path, importmap=importmap)
        return check_generated_schemaview(sv, range_tuple)

    # schema that imports the range_importer schema (just specified as text, no need to save it)
    schema_text = f"id: https://example.com/{RII}\nname: {RII}\nimports:\n  - {RI}\n"

    if import_importer_default:
        schema_text += f"\ndefault_range: {import_importer_default}\n\n"

    sv = SchemaView(schema_text, importmap=importmap)

    return check_generated_schemaview(sv, range_tuple)


def check_generated_schemaview(
    sv: SchemaView, range_tuple: tuple[str, str | None, str | None]
) -> tuple[SchemaView, tuple[str, str | None, str | None]]:
    """Check that the generated SchemaView has the expected default_range values.

    :param sv: the SchemaView to check
    :type sv: SchemaView
    :param range_tuple: the default_range values for the local, importer, and import_importer schemas
    :type range_tuple: tuple[str, str | None, str | None]
    :return: _description_
    :rtype: tuple[SchemaView, tuple[str, str | None, str | None]]
    """
    (local_default, importer_default, import_importer_default) = range_tuple

    sv.all_schema()

    if local_default:
        assert sv.schema_map[RL].default_range == local_default
    else:
        assert sv.schema_map[RL].default_range is None

    # importer_default is None => there are no imports, sv.schema == sv.schema_map[RL]
    if importer_default is None:
        assert RI not in sv.schema_map
        assert RII not in sv.schema_map
        assert sv.schema.default_range == sv.schema_map[RL].default_range
        return sv, range_tuple

    if importer_default == EMPTY:
        assert sv.schema_map[RI].default_range is None
    else:
        assert sv.schema_map[RI].default_range == importer_default

    # import_importer_default is None => importer imports local
    # therefore sv.schema == sv.schema_map[RI]
    if import_importer_default is None:
        assert RII not in sv.schema_map
        assert sv.schema.default_range == sv.schema_map[RI].default_range
        return sv, range_tuple

    # import_importer_default is populated => top level schema imports importer,
    # which imports local
    # therefore sv.schema == sv.schema_map[RII]
    assert RII in sv.schema_map
    assert sv.schema.default_range == sv.schema_map[RII].default_range

    if import_importer_default == EMPTY:
        assert sv.schema_map[RII].default_range is None
    else:
        assert sv.schema_map[RII].default_range == import_importer_default

    return sv, range_tuple


@pytest.fixture(scope="module", params=RANGE_TUPLES, ids=lambda i: gen_schema_name(i))
def sv_range_riid_gen(request: pytest.FixtureRequest) -> tuple[SchemaView, tuple[str, str | None, str | None]]:
    """Generate a set of fixtures comprising a SchemaView and the appropriate range_tuple.

    See sv_range_import_whatever for details of the schema generation.

    :param request: fixture request object for retrieving the parameters for schema generation
    :type request: pytest.FixtureRequest
    :return: tuple of the generated SchemaView and the range_tuple used to generate it
    :rtype: tuple[SchemaView, tuple[str, str | None, str | None]]
    """
    # the range tuple of (local, importer, import_importer) is stored in request.param
    return sv_range_import_whatever(request, range_tuple=request.param)


CD = "class_definition"
ED = "enum_definition"
TD = "type_definition"
# Expected results for the various range tests run in test_slot_range.
# The values are:
# - the expected value of slot.range
# - the expected set of values returned by slot_range_as_union()
# - the expected set of values returned by induced_slot_range() - COMING SOON!
# - the expected set of class/enum/type definitions returned by slot_applicable_range_elements()
ranges_no_defaults = {
    "none_range": [None, set(), set(), ValueError],
    "string_range": ["string", {"string"}, {"string"}, {TD}],
    "class_range": ["RangeClass", {"RangeClass"}, {"RangeClass"}, {CD}],
    "enum_range": ["RangeEnum", {"RangeEnum"}, {"RangeEnum"}, {ED}],
    "any_range": ["AnyOldRange", {"AnyOldRange"}, {"AnyOldRange"}, {CD, ED, TD}],
    "exactly_one_of_range": [
        "AnyOldRange",
        {"AnyOldRange", "range_string", "string"},
        {"range_string", "string"},
        {CD, ED, TD},
    ],
    "any_of_range": [
        "AnyOldRange",
        {"AnyOldRange", "RangeEnum", "RangeClass", "string"},
        {"RangeEnum", "RangeClass", "string"},
        {CD, ED, TD},
    ],
    "any_of_and_exactly_one_of_range": [
        "AnyOldRange",
        {"AnyOldRange", "RangeEnum", "RangeClass", "string", "range_string"},
        {"RangeEnum", "RangeClass", "string", "range_string"},
        {CD, ED, TD},
    ],
    "invalid_any_range_no_linkml_any": [None, {"string", "range_string"}, set(), {TD}],
    "invalid_any_range_enum": ["RangeEnum", {"RangeEnum", "string", "range_string"}, {"RangeEnum"}, {ED, TD}],
    "invalid_any_range_class": ["RangeClass", {"RangeClass", "string", "range_string"}, {"RangeClass"}, {CD, TD}],
}

# These are the expected ranges for slots where the range is replaced by
# the default_range of the local, importer, or import_importer schema.
# Same ordering as ranges_no_defaults.
ranges_replaced_by_defaults = {
    "none_range": {
        # these tuples replicate what is in RANGE_TUPLES
        # local schema only
        (EMPTY, None, None): [None, {None}, set()],
        (RLD, None, None): [RLD, {RLD}, {RLD}, {TD}],
        # local imported by `importer` schema
        (EMPTY, EMPTY, None): [None, {None}, set()],
        (EMPTY, RID, None): [RID, {RID}, {RID}, {TD}],
        (RLD, EMPTY, None): [None, {None}, set()],
        (RLD, RID, None): [RID, {RID}, {RID}, {TD}],
        # `importer` schema imported by a third schema
        (EMPTY, EMPTY, EMPTY): [None, {None}, set()],
        (EMPTY, RID, EMPTY): [None, {None}, set()],
        (EMPTY, EMPTY, RIID): [RIID, {RIID}, {RIID}, {TD}],
        (EMPTY, RID, RIID): [RIID, {RIID}, {RIID}, {TD}],
        (RLD, EMPTY, EMPTY): [None, {None}, set()],
        (RLD, RID, EMPTY): [None, {None}, set()],
        (RLD, EMPTY, RIID): [RIID, {RIID}, {RIID}, {TD}],
        (RLD, RID, RIID): [RIID, {RIID}, {RIID}, {TD}],
    }
}
ranges_replaced_by_defaults["invalid_any_range_no_linkml_any"] = {
    key: [value[0], {*value[1], "string", "range_string"}, value[2]]
    for key, value in ranges_replaced_by_defaults["none_range"].items()
}

induced_range_strict_errors = {
    "any_of_and_exactly_one_of_range": "ClassWithRanges slot any_of_and_exactly_one_of_range has range specified in both `exactly_one_of` and `any_of`",
    "invalid_any_range_no_linkml_any": "ClassWithRanges slot invalid_any_range_no_linkml_any has range specified in `exactly_one_of` or `any_of` but the slot range is not linkml:Any",
    "invalid_any_range_enum": "ClassWithRanges slot invalid_any_range_enum has range specified in `exactly_one_of` or `any_of` but the slot range is not linkml:Any",
    "invalid_any_range_class": "ClassWithRanges slot invalid_any_range_class has range specified in `exactly_one_of` or `any_of` but the slot range is not linkml:Any",
}


def test_generated_range_schema(sv_range_riid_gen: tuple[SchemaView, tuple[str, str | None, str | None]]) -> None:
    """Tests for generation of range schemas.

    This is a "meta-test" to ensure that the sv_range_import_whatever function is
    generating the correct schemas.
    """
    (sv_range, range_tuple) = sv_range_riid_gen
    schema_name = gen_schema_name(range_tuple)
    if schema_name is None:
        # not a valid combination -- no tests required
        pytest.skip("Invalid combination of local, importer, and import_importer arguments; skipping test")

    assert isinstance(sv_range, SchemaView)


@pytest.mark.parametrize("slot_name", ranges_no_defaults.keys())
@pytest.mark.parametrize(
    "range_function",
    [
        "slot_range",
        "slot_range_as_union",
        "induced_slot_range",
        "induced_range_strict",
        "slot_applicable_range_elements",
    ],
)
def test_slot_range(
    range_function: str,
    slot_name: str,
    sv_range_riid_gen: tuple[SchemaView, tuple[str, str | None, str | None]],
) -> None:
    """Test the range of a slot using various methods.

    :param range_function: name of the range function or property to call
    :type range_function: str
    :param slot_name: name of the slot to test
    :type slot_name: str
    :param sv_range_riid_gen: tuple of the SchemaView and the range_tuple used to generate it
    :type sv_range_riid_gen: tuple[SchemaView, tuple[str, str | None, str | None]]
    """
    (sv_range, range_tuple) = sv_range_riid_gen
    slot_object = sv_range.induced_slot(slot_name, "ClassWithRanges")
    expected = ranges_no_defaults[slot_name]

    if slot_name in ranges_replaced_by_defaults:
        expected = ranges_replaced_by_defaults[slot_name][range_tuple]

    if range_function == "slot_range":
        assert slot_object.range == expected[0]
    elif range_function == "slot_range_as_union":
        assert set(sv_range.slot_range_as_union(slot_object)) == expected[1]
    elif range_function == "induced_slot_range":
        assert sv_range.induced_slot_range(slot_object) == expected[2]
    elif range_function == "induced_range_strict":
        # err_msg will be None if there is no error in the slot range specification
        err_msg = induced_range_strict_errors.get(slot_name)
        if not err_msg and expected[2] == set():
            err_msg = f"ClassWithRanges slot {slot_name} has no range specified"

        if err_msg:
            with pytest.raises(ValueError, match=err_msg):
                sv_range.induced_slot_range(slot_object, strict=True)
        else:
            assert sv_range.induced_slot_range(slot_object, strict=True) == expected[2]
    elif range_function == "slot_applicable_range_elements":
        if slot_name in ranges_replaced_by_defaults and len(expected) < 4:
            expected = ranges_no_defaults[slot_name]
        if isinstance(expected[3], set):
            assert set(sv_range.slot_applicable_range_elements(slot_object)) == expected[3]
        else:
            with pytest.raises(expected[3], match="Unrecognized range: None"):
                sv_range.slot_applicable_range_elements(slot_object)
    else:
        pytest.fail(f"Unexpected range_function value: {range_function}")


"""End of range-related tests. Phew!"""


def test_permissible_value_relationships(schema_view_no_imports: SchemaView) -> None:
    """Test relationships between permissible values.

    These tests use valid permissible_value / enum combinations.

    See test_permissible_value_relationships_fail for invalid enum-PV pairings.

    CAT:
    LION:
      is_a: CAT
    ANGRY_LION:
      is_a: LION
    TABBY:
      is_a: CAT
    BIRD:
    EAGLE:
      is_a: BIRD
    """
    view = schema_view_no_imports

    animals = "Animals"
    animal_enum = view.get_enum(animals)
    assert animal_enum.name == animals

    pv_cat = animal_enum.permissible_values["CAT"]
    assert pv_cat.text == "CAT"
    assert pv_cat.is_a is None
    assert view.permissible_value_parent("CAT", animals) == []
    assert view.permissible_value_ancestors("CAT", animals) == ["CAT"]
    assert set(view.permissible_value_children("CAT", animals)) == {"LION", "TABBY"}
    assert set(view.permissible_value_descendants("CAT", animals)) == {"CAT", "LION", "ANGRY_LION", "TABBY"}

    pv_tabby = animal_enum.permissible_values["TABBY"]
    assert pv_tabby.is_a == "CAT"
    assert view.permissible_value_parent("TABBY", animals) == ["CAT"]
    assert view.permissible_value_ancestors("TABBY", animals) == ["TABBY", "CAT"]
    assert view.permissible_value_children("TABBY", animals) == []
    assert view.permissible_value_descendants("TABBY", animals) == ["TABBY"]

    pv_lion = animal_enum.permissible_values["LION"]
    assert pv_lion.is_a == "CAT"
    assert view.permissible_value_parent("LION", animals) == ["CAT"]
    assert view.permissible_value_ancestors("LION", animals) == ["LION", "CAT"]
    assert view.permissible_value_children("LION", animals) == ["ANGRY_LION"]
    assert view.permissible_value_descendants("LION", animals) == ["LION", "ANGRY_LION"]

    pv_angry_lion = animal_enum.permissible_values["ANGRY_LION"]
    assert pv_angry_lion.is_a == "LION"
    assert view.permissible_value_parent("ANGRY_LION", animals) == ["LION"]
    assert view.permissible_value_ancestors("ANGRY_LION", animals) == ["ANGRY_LION", "LION", "CAT"]
    assert view.permissible_value_children("ANGRY_LION", animals) == []
    assert view.permissible_value_descendants("ANGRY_LION", animals) == ["ANGRY_LION"]


@pytest.mark.parametrize("fn", ["parent", "children", "ancestors", "descendants"])
def test_permissible_value_relationships_fail(schema_view_no_imports: SchemaView, fn: str) -> None:
    """Test permissible_value relationships with incorrect enum/PV pairs."""
    method_name = f"permissible_value_{fn}"
    # invalid enum
    with pytest.raises(ValueError, match='No such enum: "invalid_enum"'):
        getattr(schema_view_no_imports, method_name)("invalid_pv", "invalid_enum")

    # invalid pv, valid enum
    with pytest.raises(ValueError, match='"invalid_pv" is not a permissible value of the enum "Animals"'):
        getattr(schema_view_no_imports, method_name)("invalid_pv", "Animals")


# FIXME: improve testing of dynamic enums
def test_dynamic_enum(schema_view_with_imports: SchemaView) -> None:
    """Rudimentary test of dynamic enum."""
    view = schema_view_with_imports

    # dynamic enums
    e = view.get_enum("HCAExample")
    assert set(e.include[0].reachable_from.source_nodes) == {"GO:0007049", "GO:0022403"}


def test_get_elements_applicable_by_identifier(schema_view_no_imports: SchemaView) -> None:
    """Test get_elements_applicable_by_identifier method."""
    view = schema_view_no_imports
    elements = view.get_elements_applicable_by_identifier("ORCID:1234")
    assert PERSON in elements
    elements = view.get_elements_applicable_by_identifier("PMID:1234")
    assert "Organization" in elements
    elements = view.get_elements_applicable_by_identifier("http://www.ncbi.nlm.nih.gov/pubmed/1234")
    assert "Organization" in elements
    elements = view.get_elements_applicable_by_identifier("TEST:1234")
    assert "anatomical entity" not in elements


# FIXME: improve test to actually test the annotations
def test_annotation_dict_annotations(schema_view_no_imports: SchemaView) -> None:
    """Test annotation_dict method for both annotations and slot_definition_annotations."""
    view = schema_view_no_imports

    assert list(view.annotation_dict(IS_CURRENT).values()) == ["bar"]
    logger.debug(view.annotation_dict(EMPLOYED_AT))
    e = view.get_element(EMPLOYED_AT)
    logger.debug(e.annotations)
    e = view.get_element("has employment history")
    logger.debug(e.annotations)

    assert list(view.annotation_dict(SlotDefinitionName(IS_CURRENT)).values()) == ["bar"]
    logger.debug(view.annotation_dict(SlotDefinitionName(EMPLOYED_AT)))
    element = view.get_element(SlotDefinitionName(EMPLOYED_AT))
    logger.debug(element.annotations)
    element = view.get_element(SlotDefinitionName("has employment history"))
    logger.debug(element.annotations)


def test_is_mixin(schema_view_no_imports: SchemaView) -> None:
    """Test is_mixin method."""
    view = schema_view_no_imports
    assert view.is_mixin("WithLocation")
    assert not view.is_mixin("BirthEvent")


def test_inverse(schema_view_no_imports: SchemaView) -> None:
    """Test inverse method."""
    view = schema_view_no_imports
    assert view.inverse("employment history of") == "has employment history"
    assert view.inverse("has employment history") == "employment history of"


# FIXME: improve test - use simpler schema if needed
def test_get_mapping_index(schema_view_no_imports: SchemaView) -> None:
    """Test get_mapping_index method."""
    view = schema_view_no_imports
    mapping = view.get_mapping_index()
    assert mapping is not None


def test_get_element_by_mapping(schema_view_no_imports: SchemaView) -> None:
    """Test get_element_by_mapping method."""
    view = schema_view_no_imports
    category_mapping = view.get_element_by_mapping("GO:0005198")
    assert category_mapping == [ACTIVITY]


def test_is_multivalued(schema_view_no_imports: SchemaView) -> None:
    """Test is_multivalued method."""
    view = schema_view_no_imports
    assert view.is_multivalued("aliases")
    assert not view.is_multivalued("id")
    assert view.is_multivalued("dog addresses")


def test_slot_is_true_for_metadata_property(schema_view_no_imports: SchemaView) -> None:
    """Test slot_is_true_for_metadata_property method."""
    view = schema_view_no_imports
    assert view.slot_is_true_for_metadata_property("aliases", "multivalued")
    assert view.slot_is_true_for_metadata_property("id", "identifier")

    with pytest.raises(ValueError, match='property to introspect must be of type "boolean"'):
        view.slot_is_true_for_metadata_property("aliases", "aliases")


# FIXME: improve tests, remove debug logging
def test_relativity(schema_view_no_imports: SchemaView) -> None:
    """Log the output of various methods that depend on class hierarchy."""
    view = schema_view_no_imports

    all_cls = view.all_classes()
    logger.debug(f"n_cls = {len(all_cls)}")

    for cn in all_cls.keys():
        c = view.get_class(cn)
        assert c.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        logger.debug(f"{cn} PARENTS = {view.class_parents(cn)}")
        logger.debug(f"{cn} ANCS = {view.class_ancestors(cn)}")
        logger.debug(f"{cn} CHILDREN = {view.class_children(cn)}")
        logger.debug(f"{cn} DESCS = {view.class_descendants(cn)}")
        logger.debug(f"{cn} SCHEMA = {view.in_schema(cn)}")
        logger.debug(f"  SLOTS = {view.class_slots(cn)}")
        for sn in view.class_slots(cn):
            slot = view.get_slot(sn)
            assert slot.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
            logger.debug(f"  SLOT {sn} R: {slot.range} U: {view.get_uri(sn)} ANCS: {view.slot_ancestors(sn)}")
            induced_slot = view.induced_slot(sn, cn)
            logger.debug(f"    INDUCED {sn}={induced_slot}")
            assert induced_slot.range is not None

    logger.debug(f"ALL = {view.all_elements().keys()}")


def test_ancestors_descendants(schema_view_no_imports: SchemaView) -> None:
    """Test class_ancestors and class_descendants methods."""
    view = schema_view_no_imports

    assert set(view.class_ancestors(ADULT)) == {ADULT, PERSON, "HasAliases", THING}
    assert set(view.class_ancestors(COMPANY)) == {COMPANY, "Organization", "HasAliases", THING}
    assert set(view.class_ancestors(COMPANY, reflexive=False)) == {"Organization", "HasAliases", THING}
    assert set(view.class_descendants(THING)) == {THING, PERSON, "Organization", COMPANY, ADULT}


def test_get_mappings(schema_view_no_imports: SchemaView) -> None:
    """Test get_mappings and *_mappings methods."""
    view = schema_view_no_imports

    a = view.get_class(ACTIVITY)
    assert view.get_mappings(ACTIVITY) == {
        "self": ["ks:Activity"],
        "native": ["ks:Activity"],
        "exact": ["prov:Activity"],
        "narrow": ["GO:0005198"],
        "broad": [],
        "related": [],
        "close": [],
        "undefined": [],
    }
    assert view.get_mappings(ACTIVITY, expand=True) == {
        "self": ["https://w3id.org/linkml/tests/kitchen_sink/Activity"],
        "native": ["https://w3id.org/linkml/tests/kitchen_sink/Activity"],
        "exact": ["http://www.w3.org/ns/prov#Activity"],
        "narrow": ["http://purl.obolibrary.org/obo/GO_0005198"],
        "broad": [],
        "related": [],
        "close": [],
        "undefined": [],
    }

    assert a.exact_mappings == ["prov:Activity"]
    assert a.narrow_mappings == ["GO:0005198"]
    assert a.broad_mappings == []
    assert a.related_mappings == []
    assert a.close_mappings == []

    assert set(view.get_mappings(ACTIVITY)["exact"]) == {"prov:Activity"}
    assert set(view.get_mappings(ACTIVITY, expand=True)["exact"]) == {"http://www.w3.org/ns/prov#Activity"}


def test_schema_usage(schema_view_no_imports: SchemaView) -> None:
    """Test usage_index method and SchemaUsage objects."""
    view = schema_view_no_imports
    u = view.usage_index()
    for k, v in u.items():
        logger.debug(f" {k} = {v}")

    assert (
        SchemaUsage(used_by="FamilialRelationship", slot=RELATED_TO, metaslot="range", used=PERSON, inferred=False)
        in u[PERSON]
    )
    assert [
        SchemaUsage(
            used_by=PERSON,
            slot="reason_for_happiness",
            metaslot="any_of[range]",
            used="MarriageEvent",
            inferred=True,
        ),
        SchemaUsage(
            used_by=ADULT,
            slot="reason_for_happiness",
            metaslot="any_of[range]",
            used="MarriageEvent",
            inferred=False,
        ),
    ] == u["MarriageEvent"]
    assert [
        SchemaUsage(
            used_by=PERSON, slot="has employment history", metaslot="range", used="EmploymentEvent", inferred=True
        ),
        SchemaUsage(
            used_by=PERSON,
            slot="reason_for_happiness",
            metaslot="any_of[range]",
            used="EmploymentEvent",
            inferred=True,
        ),
        SchemaUsage(
            used_by=ADULT, slot="has employment history", metaslot="range", used="EmploymentEvent", inferred=False
        ),
        SchemaUsage(
            used_by=ADULT,
            slot="reason_for_happiness",
            metaslot="any_of[range]",
            used="EmploymentEvent",
            inferred=False,
        ),
    ] == u["EmploymentEvent"]


def test_attributes(schema_view_no_imports: SchemaView) -> None:
    """Test slot methods also work for attributes."""
    view = schema_view_no_imports
    leaves = view.class_leaves()
    logger.debug(f"LEAVES={leaves}")
    assert "MedicalEvent" in leaves
    roots = view.class_roots()
    logger.debug(f"ROOTS={roots}")
    assert "Dataset" in roots
    ds_slots = view.class_slots("Dataset")
    logger.debug(ds_slots)
    assert len(ds_slots) == 3
    assert len(["persons", "companies", "activities"]) == len(ds_slots)
    for sn in ds_slots:
        s = view.induced_slot(sn, "Dataset")
        logger.debug(s)


def test_get_classes_modifying_slot() -> None:
    """Test getting classes that modify a slot.

    https://github.com/linkml/linkml/issues/1126
    """
    classes_mod_slot_file = INPUT_DIR_PATH / "issue_1126.yaml"
    view = SchemaView(str(classes_mod_slot_file))
    slot_definition = view.get_slot("type")
    slot_classes = view.get_classes_modifying_slot(slot_definition)
    assert len(slot_classes) == 2
    for element in slot_classes:
        assert type(element) is ClassDefinitionName
    assert slot_classes[0] == ClassDefinitionName("Programmer")
    assert slot_classes[1] == ClassDefinitionName("Administrator")


# FIXME: this test modifies the schema - may be better to use simpler schema
# FIXME: remove debug logging and replace with assertions
def test_rollup_rolldown() -> None:
    """Test rolling up and rolling down."""
    # create the schemaview within the test to avoid modifying the test fixture
    view = SchemaView(SCHEMA_NO_IMPORTS)
    element_name = "Event"
    roll_up(view, element_name)
    for slot in view.class_induced_slots(element_name):
        logger.debug(slot)
    induced_slot_names = [s.name for s in view.class_induced_slots(element_name)]
    logger.debug(induced_slot_names)
    assert len(["started at time", "ended at time", IS_CURRENT, "in location", EMPLOYED_AT, "married to"]) == len(
        induced_slot_names
    )
    # check to make sure rolled-up classes are deleted
    assert view.class_descendants(element_name, reflexive=False) == []
    roll_down(view, view.class_leaves())

    for element_name in view.all_classes():
        logger.debug(f"{element_name}")
        logger.debug(f"  {element_name} SLOTS(i) = {view.class_slots(element_name)}")
        logger.debug(f"  {element_name} SLOTS(d) = {view.class_slots(element_name, direct=True)}")
        assert len(view.class_slots(element_name)) == len(view.class_slots(element_name, direct=True))
        assert THING not in view.all_classes()
        assert PERSON not in view.all_classes()
        assert ADULT in view.all_classes()


def test_caching() -> None:
    """Determine if cache is reset after modifications made to schema."""
    schema = SchemaDefinition(id="test", name="test")
    view = SchemaView(schema)
    assert len([]) == len(view.all_classes())
    view.add_class(ClassDefinition("X"))
    assert len(["X"]) == len(view.all_classes())
    view.add_class(ClassDefinition("Y"))
    assert len(["X", "Y"]) == len(view.all_classes())
    # bypass view method and add directly to schema;
    # in general this is not recommended as the cache will
    # not be updated
    view.schema.classes["Z"] = ClassDefinition("Z")
    # as expected, the view doesn't know about Z
    assert len(["X", "Y"]) == len(view.all_classes())
    # inform the view modifications have been made
    view.set_modified()
    # should be in sync
    assert len(["X", "Y", "Z"]) == len(view.all_classes())
    # recommended way to make updates
    view.delete_class("X")
    # cache will be up to date
    assert len(["Y", "Z"]) == len(view.all_classes())
    view.add_class(ClassDefinition("W"))
    assert len(["Y", "Z", "W"]) == len(view.all_classes())


def test_traversal() -> None:
    """Test schema traversal."""
    schema = SchemaDefinition(id="test", name="traversal-test")
    view = SchemaView(schema)
    view.add_class(ClassDefinition("Root", mixins=["RootMixin"]))
    view.add_class(ClassDefinition("A", is_a="Root", mixins=["Am1", "Am2", "AZ"]))
    view.add_class(ClassDefinition("B", is_a="A", mixins=["Bm1", "Bm2", "BY"]))
    view.add_class(ClassDefinition("C", is_a="B", mixins=["Cm1", "Cm2", "CX"]))
    view.add_class(ClassDefinition("RootMixin", mixin=True))
    view.add_class(ClassDefinition("Am1", is_a="RootMixin", mixin=True))
    view.add_class(ClassDefinition("Am2", is_a="RootMixin", mixin=True))
    view.add_class(ClassDefinition("Bm1", is_a="Am1", mixin=True))
    view.add_class(ClassDefinition("Bm2", is_a="Am2", mixin=True))
    view.add_class(ClassDefinition("Cm1", is_a="Bm1", mixin=True))
    view.add_class(ClassDefinition("Cm2", is_a="Bm2", mixin=True))
    view.add_class(ClassDefinition("AZ", is_a="RootMixin", mixin=True))
    view.add_class(ClassDefinition("BY", is_a="RootMixin", mixin=True))
    view.add_class(ClassDefinition("CX", is_a="RootMixin", mixin=True))

    # class ancestors, depth first order
    anc_df = ["C", "Cm1", "Cm2", "CX", "B", "Bm1", "Bm2", "BY", "A", "Am1", "Am2", "AZ", "Root", "RootMixin"]
    assert view.class_ancestors("C", depth_first=True) == anc_df

    # class ancestors, not in depth first order
    anc_not_df = ["C", "Cm1", "Cm2", "CX", "B", "Bm1", "Bm2", "RootMixin", "BY", "A", "Am1", "Am2", "AZ", "Root"]
    assert view.class_ancestors("C", depth_first=False) == anc_not_df

    assert view.class_ancestors("C", mixins=False) == ["C", "B", "A", "Root"]
    assert view.class_ancestors("C", is_a=False) == ["C", "Cm1", "Cm2", "CX"]


def test_slot_inheritance() -> None:
    """Test slot inheritance."""
    schema = SchemaDefinition(id="test", name="test")
    view = SchemaView(schema)
    view.add_class(ClassDefinition("C", slots=["s1", "s2"]))
    view.add_class(ClassDefinition("D"))
    view.add_class(ClassDefinition("Z"))
    view.add_class(ClassDefinition("W"))

    view.add_slot(SlotDefinition("s1", multivalued=True, range="D"))
    view.add_slot(SlotDefinition("s2", is_a="s1"))
    view.add_slot(SlotDefinition("s3", is_a="s2", mixins=["m1"]))
    view.add_slot(SlotDefinition("s4", is_a="s2", mixins=["m1"], range="W"))
    view.add_slot(SlotDefinition("m1", mixin=True, multivalued=False, range="Z"))

    slot1 = view.induced_slot("s1", "C")
    assert slot1.is_a is None
    assert slot1.range == "D"
    assert slot1.multivalued is not None

    slot2 = view.induced_slot("s2", "C")
    assert slot2.is_a == "s1"
    assert slot2.range == "D"
    assert slot2.multivalued is not None

    slot3 = view.induced_slot("s3", "C")
    assert slot3.multivalued is not None
    assert slot3.range == "Z"

    slot4 = view.induced_slot("s4", "C")
    assert slot4.multivalued is not None
    assert slot4.range == "W"

    # Test dangling
    view.add_slot(SlotDefinition("s5", is_a="does-not-exist"))
    with pytest.raises(ValueError, match='No such slot: "does-not-exist"'):
        view.slot_ancestors("s5")


def test_induced_slot(sv_induced_slots: SchemaView) -> None:
    """Test induced slots and load order of mixins and is_a.

    See https://github.com/linkml/linkml/issues/479 and
    https://github.com/linkml/linkml-runtime/issues/68 for details.
    """
    # test description for slot1
    s1 = sv_induced_slots.get_slot("slot1")
    assert s1.description == "non-induced slot1"
    assert s1.range == "class0"

    s2 = sv_induced_slots.get_slot("slot2")
    assert not s2.required
    assert s2.range == "class0"

    s2_induced = sv_induced_slots.induced_slot("slot2", "class1")
    assert s2_induced.required
    assert s2_induced.range == "class1"

    # test description for slot2
    # this behavior is expected see: https://github.com/linkml/linkml-runtime/issues/68
    assert s2_induced.description == "induced slot2"

    s2_induced_c2 = sv_induced_slots.induced_slot("slot2", "class2")
    assert s2_induced_c2.required
    assert s2_induced_c2.description == "induced slot2"
    assert s2_induced.range == "class1"

    s3_induced_c2 = sv_induced_slots.induced_slot("slot3", "class2")
    assert not s3_induced_c2.required
    assert s3_induced_c2.description is None
    assert s3_induced_c2.range == "class0"

    # mixins take priority over is-a
    # mixins specified in order of priority
    s2_induced_c2_1a = sv_induced_slots.induced_slot("slot2", "class2_1a")
    assert not s2_induced_c2_1a.required
    assert s2_induced_c2_1a.description == "mixin slot2"
    assert s2_induced_c2_1a.range == "mixin1a"

    s2_induced_c2_1b = sv_induced_slots.induced_slot("slot2", "class2_1b")
    assert not s2_induced_c2_1b.required
    assert s2_induced_c2_1b.description == "mixin slot2"
    assert s2_induced_c2_1b.range == "mixin1b"


def test_induced_slot_again(schema_view_no_imports: SchemaView) -> None:
    """Test induced slots (again)."""
    view = schema_view_no_imports

    for sn, s in view.all_slots().items():
        assert s.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        rng = view.induced_slot(sn).range
        assert rng is not None

    # test induced slots
    for cn in [COMPANY, PERSON, "Organization"]:
        islot = view.induced_slot("aliases", cn)
        assert islot.multivalued is True
        assert islot.owner == cn
        assert view.get_uri(islot, expand=True) == "https://w3id.org/linkml/tests/kitchen_sink/aliases"

    assert view.get_identifier_slot(COMPANY).name == "id"
    assert view.get_identifier_slot(THING).name == "id"
    assert view.get_identifier_slot("FamilialRelationship") is None

    for cn in [COMPANY, PERSON, "Organization", THING]:
        assert view.induced_slot("id", cn).identifier
        assert not view.induced_slot("name", cn).identifier
        assert not view.induced_slot("name", cn).required
        assert view.induced_slot("name", cn).range == "string"
        assert view.induced_slot("id", cn).owner == cn
        assert view.induced_slot("name", cn).owner == cn

    for cn in ["Event", "EmploymentEvent", "MedicalEvent"]:
        s = view.induced_slot("started at time", cn)
        assert s.range == "date"
        assert s.slot_uri == "prov:startedAtTime"
        assert s.owner == cn

        c_induced = view.induced_class(cn)
        assert c_induced.slots == []
        assert c_induced.attributes != []
        s2 = c_induced.attributes["started at time"]
        assert s2.range == "date"
        assert s2.slot_uri == "prov:startedAtTime"

    # test slot_usage
    assert view.induced_slot(AGE_IN_YEARS, PERSON).minimum_value == 0
    assert view.induced_slot(AGE_IN_YEARS, ADULT).minimum_value == 16
    assert view.induced_slot("name", PERSON).pattern is not None
    assert view.induced_slot("type", "FamilialRelationship").range == "FamilialRelationshipType"
    assert view.induced_slot(RELATED_TO, "FamilialRelationship").range == PERSON
    assert view.get_slot(RELATED_TO).range == THING
    assert view.induced_slot(RELATED_TO, "Relationship").range == THING
    assert set(view.induced_slot("name").domain_of) == {THING, "Place"}


@pytest.mark.parametrize(
    ("cn", "sn", "req", "desc"),
    [
        ("Root", "a1", None, "a1"),
        ("Root", "a2", None, "a2"),
        ("Root", "a3", None, "a3"),
        ("C1", "a1", True, "a1m1"),
        ("C1", "a2", True, "a2c1"),
        ("C1", "a3", None, "a3"),
        ("C1", "a4", None, "a4"),
        ("C2", "a1", False, "a1m2"),
        ("C2", "a2", True, "a2c2"),
        ("C2", "a3", None, "a3"),
        ("C2", "a4", True, "a4m2"),
        ("C1x", "a1", True, "a1m1"),
        ("C1x", "a2", True, "a2c1x"),
        ("C1x", "a3", None, "a3"),
        ("C1x", "a4", None, "a4"),
    ],
)
def test_attribute_inheritance(sv_attributes: SchemaView, cn: str, sn: str, req: bool, desc: str) -> None:
    """Tests attribute inheritance edge cases."""
    slot = sv_attributes.induced_slot(sn, cn)
    assert req == slot.required, f"in: {cn}.{sn}"
    assert desc == slot.description, f"in: {cn}.{sn}"
    assert slot.range == "string", f"in: {cn}.{sn}"


def test_ambiguous_attributes() -> None:
    schema = SchemaDefinition(id="test", name="test")
    view = SchemaView(schema)
    a1 = SlotDefinition("a1", range="string")
    a2 = SlotDefinition("a2", range="FooEnum")
    a3 = SlotDefinition("a3", range="C3")
    view.add_class(ClassDefinition("C1", attributes={a1.name: a1, a2.name: a2, a3.name: a3}))
    a1x = SlotDefinition("a1", range="integer")
    a2x = SlotDefinition("a2", range="BarEnum")
    view.add_class(ClassDefinition("C2", attributes={a1x.name: a1x, a2x.name: a2x}))

    assert view.get_slot(a1.name).range is None
    assert view.get_slot(a2.name).range is None
    assert view.get_slot(a3.name).range is not None
    assert len(view.all_slots(attributes=True)) == 3
    assert len(view.all_slots(attributes=False)) == 0
    assert len(view.all_slots()) == 3
    assert view.induced_slot(a3.name).range == a3.range
    assert view.induced_slot(a1.name, "C1").range == a1.range
    assert view.induced_slot(a2.name, "C1").range == a2.range
    assert view.induced_slot(a1x.name, "C2").range == a1x.range
    assert view.induced_slot(a2x.name, "C2").range == a2x.range


def test_get_classes_by_slot(schema_view_with_imports: SchemaView) -> None:
    """Test getting classes by slot."""
    view = schema_view_with_imports
    slot = view.get_slot(AGE_IN_YEARS)
    actual_result = view.get_classes_by_slot(slot)
    expected_result = [PERSON]
    assert sorted(actual_result) == sorted(expected_result)

    actual_result = view.get_classes_by_slot(slot, include_induced=True)
    expected_result = [PERSON, ADULT]
    assert sorted(actual_result) == sorted(expected_result)


def test_materialize_patterns(sv_structured_patterns: SchemaView) -> None:
    """Test pattern materialization."""
    sv_structured_patterns.materialize_patterns()

    height_slot = sv_structured_patterns.get_slot("height")
    weight_slot = sv_structured_patterns.get_slot("weight")

    assert height_slot.pattern == r"\d+[\.\d+] (centimeter|meter|inch)"
    assert weight_slot.pattern == r"\d+[\.\d+] (kg|g|lbs|stone)"


def test_materialize_patterns_slot_usage(sv_structured_patterns: SchemaView) -> None:
    """Test pattern materialization with slot_usage."""
    sv_structured_patterns.materialize_patterns()

    name_slot_usage = sv_structured_patterns.get_class("FancyPersonInfo").slot_usage["name"]
    assert name_slot_usage.pattern == r"\S+ \S+-\S+"


def test_materialize_patterns_attribute(sv_structured_patterns: SchemaView) -> None:
    """Test pattern materialization with attributes."""
    sv_structured_patterns.materialize_patterns()

    weight_attribute = sv_structured_patterns.get_class("ClassWithAttributes").attributes["weight"]
    assert weight_attribute.pattern == r"\d+[\.\d+] (kg|g|lbs|stone)"


@pytest.mark.parametrize(
    ("slot_name", "expected_result"),
    [
        ("a_thing_with_id", False),
        ("inlined_thing_with_id", True),
        ("inlined_as_list_thing_with_id", True),
        ("a_thing_without_id", True),
        ("inlined_thing_without_id", True),
        ("inlined_as_list_thing_without_id", True),
        ("an_integer", False),
        ("inlined_integer", False),
        ("inlined_as_list_integer", False),
    ],
)
def test_is_inlined(sv_inlined: SchemaView, slot_name: str, expected_result: bool) -> None:
    """Tests for slots being inlined or not."""
    slot = sv_inlined.get_slot(slot_name)
    assert sv_inlined.is_inlined(slot) == expected_result


def test_materialize_nonscalar_slot_usage() -> None:
    sv = SchemaView(str(INPUT_DIR_PATH / "DJ_controller_schema.yaml"))
    cls = sv.induced_class("DJController")

    assert cls.attributes["jog_wheels"].range == "integer"
    assert isinstance(cls.attributes["jog_wheels"].examples, list)
    for example in cls.attributes["jog_wheels"].examples:
        assert example.value == "2"
    for example in cls.attributes["volume_faders"].examples:
        assert example.value == "4"
    for example in cls.attributes["crossfaders"].examples:
        assert example.value == "1"

    assert isinstance(cls.attributes["jog_wheels"].annotations, JsonObj)
    assert cls.attributes["jog_wheels"].annotations.expected_value.value == "an integer between 0 and 4"
    assert cls.attributes["volume_faders"].annotations.expected_value.value == "an integer between 0 and 8"

    assert cls.attributes["tempo"].examples == [
        Example(value="120.0"),
        Example(value="144.0"),
        Example(value="126.8"),
        Example(value="102.6"),
    ]
    assert cls.attributes["tempo"].annotations.expected_value.value == "a number between 0 and 200"
    assert cls.attributes["tempo"].annotations.preferred_unit.value == "BPM"
    assert cls.attributes["tempo"].domain_of == ["DJController"]
    assert cls.slot_usage["tempo"].domain_of == []


def test_type_and_slot_with_same_name() -> None:
    """Test that checks the case where a URI needs to be resolved and a name is ambiguously used for a slot and a type."""
    schema_definition = SchemaDefinition(id="https://example.org/test#", name="test_schema", default_prefix="ex")

    view = SchemaView(schema_definition)
    view.add_slot(SlotDefinition(name="test", from_schema="https://example.org/another#"))
    view.add_type(TypeDefinition(name="test", from_schema="https://example.org/imported#"))

    assert view.get_uri("test", imports=True) == "ex:test"


@pytest.fixture(scope="module")
def identifier_key_schema() -> str:
    """Return a schema that defines a set of slots with identifiers and keys, and a test class to populate."""
    return """
# yaml-language-server: $schema=https://linkml.io/linkml-model/linkml_model/jsonschema/meta.schema.json
id: https://w3id.org/linkml/examples/identifiers
title: Identifiers and Keys
name: identifiers
description: Schema for testing identifiers and keys
slots:
  slot_a:
  slot_b:
  id_slot_a:
    identifier: true
  id_slot_b:
    identifier: true
  id_slot_false:
    identifier: false
  key_slot_a:
    key: true
  key_slot_b:
    key: true
  key_slot_false:
    key: false

classes:
  TestClass:
    slots:
      - slot_a
      - slot_b
"""


@pytest.mark.parametrize("id_slot_a", [EMPTY, "id_slot_a"])
@pytest.mark.parametrize("id_slot_b", [EMPTY, "id_slot_b"])
@pytest.mark.parametrize("id_slot_false", [EMPTY, "id_slot_false"])
@pytest.mark.parametrize("key_slot_a", [EMPTY, "key_slot_a"])
@pytest.mark.parametrize("key_slot_b", [EMPTY, "key_slot_b"])
@pytest.mark.parametrize("key_slot_false", [EMPTY, "key_slot_false"])
def test_get_identifier_get_key_slot(
    identifier_key_schema: str,
    id_slot_a: str,
    id_slot_b: str,
    id_slot_false: str,
    key_slot_a: str,
    key_slot_b: str,
    key_slot_false: str,
) -> None:
    """Test the retrieval of "identifier" and "key" slots in classes in the schema.

    The parameters represent the slots to be added to the test class; if the value of the parameter is EMPTY,
    the slot is not added. If the parameter is a string, that slot is added to the test class.

    For example, given the following set of parameters:

    id_slot_a: "id_slot_a"
    id_slot_b: EMPTY
    id_slot_false: "id_slot_false"
    key_slot_a: EMPTY
    key_slot_b: EMPTY
    key_slot_false: "key_slot_false"

    The following lines would be added to the bottom of the identifier_key_schema:

          - id_slot_a
          - id_slot_false
          - key_slot_false

    resulting in the following structure for `TestClass`:

    classes:
      TestClass:
        slots:
          - slot_a
          - slot_b
          - id_slot_a
          - id_slot_false
          - key_slot_false

    This allows the testing of a large number of combinations without having to generate all 2^^6 (64) manually.
    """
    all_id_slots = [id_slot_a, id_slot_b, id_slot_false]
    all_key_slots = [key_slot_a, key_slot_b, key_slot_false]

    for k in [*all_id_slots, *all_key_slots]:
        if k:
            identifier_key_schema += f"      - {k}\n"

    sv = SchemaView(identifier_key_schema)
    test_class_slots = sv.class_slots("TestClass")
    # ensure that the correct slots are in the schema
    assert set(test_class_slots) == {"slot_a", "slot_b", *[s for s in [*all_id_slots, *all_key_slots] if s]}

    # Generate the expected slots to be returned by `get_***_slot` for identifiers and keys.
    # Note that id_slot_false and key_slot_false have `identifier` and `key` set to `false`,
    # so we would not expect `get_identifier_slot` or `get_key_slot` to return these slots.
    # If the value from the parameters is EMPTY, the attribute is not present.
    expected = {
        # expected result of get_identifier_slot
        ID: id_slot_a or id_slot_b,
        # expected result of get_identifier_slot, falling back on get_key_slot
        f"{ID}_or_{KEY}": id_slot_a or id_slot_b or key_slot_a or key_slot_b,
        # expected result of get_key_slot
        KEY: key_slot_a or key_slot_b,
    }

    got = {
        ID: sv.get_identifier_slot("TestClass", use_key=False),
        f"{ID}_or_{KEY}": sv.get_identifier_slot("TestClass", use_key=True),
        KEY: sv.get_key_slot("TestClass"),
    }

    for id_key, exp in expected.items():
        if exp:
            assert got[id_key].name == exp
        else:
            assert got[id_key] is None


"""
merge_schema tests: https://github.com/linkml/linkml/issues/1143
"""


def test_merge_schema_merge_into_empty(sv_merge_1: SchemaView, sv_empty: SchemaView) -> None:
    """Trivial case: merge a schema into an empty schema."""
    sv_empty.merge_schema(sv_merge_1.schema)
    for k in ALL_ELEMENTS:
        assert getattr(sv_empty.schema, k) == getattr(sv_merge_1.schema, k)


def test_merge_schema_merge_empty(sv_merge_1: SchemaView, sv_empty: SchemaView) -> None:
    """Trivial case: merge an empty schema into a non-empty schema."""
    sv_merge_1_orig = deepcopy(sv_merge_1)
    sv_merge_1.merge_schema(sv_empty.schema)

    for k in ALL_ELEMENTS:
        assert getattr(sv_merge_1_orig.schema, k) == getattr(sv_merge_1.schema, k)


def test_merge_schema_disjoint_elements(sv_merge_1: SchemaView, sv_merge_2: SchemaView) -> None:
    """Merge two schemas with disjoint elements."""
    sv_merge_2.merge_schema(sv_merge_1.schema)

    for k, vs in EXPECTED.items():
        assert set(getattr(sv_merge_2.schema, k).keys()) == vs


def _get_clobbered_field_val(element: str) -> tuple[str, str]:
    if element == "prefixes":
        return "prefix_reference", "http://example.org/clobbered"
    return "description", "clobbered"


def test_merge_schema_no_clobber(sv_merge_1: SchemaView, sv_merge_2: SchemaView) -> None:
    """Merge non-disjoint schemas, ensuring that elements in the source schema are not clobbered."""
    sv_merge_2.merge_schema(sv_merge_1.schema)
    for element in ALL_ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for v in getattr(sv_merge_1.schema, element).values():
            setattr(v, field, val)

    sv_merge_2.merge_schema(sv_merge_1.schema, clobber=False)
    for element in ALL_ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for k, v in getattr(sv_merge_2.schema, element).items():
            if k in getattr(sv_merge_1.schema, element):
                assert getattr(v, field) != val


def test_merge_schema_clobber(sv_merge_1: SchemaView, sv_merge_2: SchemaView) -> None:
    """Merge non-disjoint schemas, ensuring that elements in source schema are clobbered."""
    sv_merge_2.merge_schema(sv_merge_1.schema)
    for element in ALL_ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for v in getattr(sv_merge_1.schema, element).values():
            setattr(v, field, val)

    sv_merge_2.merge_schema(sv_merge_1.schema, clobber=True)
    for element in ALL_ELEMENTS:
        (field, val) = _get_clobbered_field_val(element)
        for k, v in getattr(sv_merge_2.schema, element).items():
            if k in getattr(sv_merge_1.schema, element):
                assert getattr(v, field) == val


def test_get_slots_by_enum_schema_slot(sv_issue_998: SchemaView) -> None:
    enum_slots = sv_issue_998.get_slots_by_enum("EmploymentStatusEnum")
    assert len(enum_slots) == 2


def test_get_slots_by_enum_no_duplicates(sv_issue_998: SchemaView) -> None:
    enum_slots = sv_issue_998.get_slots_by_enum("PersonStatusEnum")
    assert len(enum_slots) == 1
    assert enum_slots[0].name == "status"


def test_get_slots_by_enum_attribute_slot(sv_issue_998: SchemaView) -> None:
    enum_slots = sv_issue_998.get_slots_by_enum("EmploymentStatusEnum")
    assert len(enum_slots) == 2
    assert sorted([slot.name for slot in enum_slots]) == ["employed", "past_employer"]


def test_get_slots_by_enum_schema_and_attribute_slots(sv_issue_998: SchemaView) -> None:
    enum_slots = sv_issue_998.get_slots_by_enum("RelationshipStatusEnum")
    assert len(enum_slots) == 2
    assert enum_slots[0].name == "relationship"
    assert enum_slots[1].name == "past_relationship"


def test_get_slots_by_enum_slot_usage_range(sv_issue_998: SchemaView) -> None:
    enum_slots = sv_issue_998.get_slots_by_enum("TypeEnum")
    assert len(enum_slots) == 1
    assert enum_slots[0].name == "type"


def test_get_slot_gets_attr_not_slot() -> None:
    """Test that get_slot() returns attribute not top level slot.

    See https://github.com/linkml/linkml/issues/998.
    """
    schema_file = INPUT_DIR_PATH / "issue_590.yaml"

    sv = SchemaView(str(schema_file))
    # check that multivalued is set to False as in schema
    assert sv.get_slot("a").multivalued is False


def test_class_name_mappings() -> None:
    """Test the retrieval of normalised names and the original versions.

    See https://github.com/linkml/linkml/issues/478
    """
    schema_file = INPUT_DIR_PATH / "issue_478.yaml"
    view = SchemaView(str(schema_file))

    # class names => normalised class names:
    class_names = {
        "foo bar": "FooBar",
        "named thing": "NamedThing",
        "biosample_processing": "BiosampleProcessing",
        "too   much   whitespace": "TooMuchWhitespace",
        "5' sequencing": "5'Sequencing",
    }

    assert set(view.all_classes()) == set(class_names)
    assert set(view.class_name_mappings()) == set(class_names.values())
    assert {cnm_def.name: cnm for cnm, cnm_def in view.class_name_mappings().items()} == class_names

    slot_names = {
        "id": "id",
        "preferred label": "preferred_label",
        "5' sequence": "5'_sequence",
        # note that these slot names are unchanged
        "SOURCE": "SOURCE",
        "processingMethod": "processingMethod",
    }

    assert set(view.all_slots()) == set(slot_names)
    assert set(view.slot_name_mappings()) == set(slot_names.values())
    assert {snm_def.name: snm for snm, snm_def in view.slot_name_mappings().items()} == slot_names


@pytest.fixture(scope="module")
def sv_cycles_schema() -> SchemaView:
    """A schema containing cycles!"""
    return SchemaView(INPUT_DIR_PATH / "cycles.yaml")


CYCLES = {
    TYPES: {
        # types in cycles, either directly or via ancestors
        # key: type, value: node where the cycle starts
        0: {
            "curve_type": "circular_type",
            "semi_circular_type": "circular_type",
            "circular_type": "circular_type",
            "type_circular": "type_circular",
            "circle": "circle",
            "circle_of_life": "circle",
        },
        # types not involved in cycles
        # key: the type, value: ancestors of the type
        1: {
            "supreme_string": {"supreme_string", "super_string", "string"},
            "super_string": {"super_string", "string"},
            "string": {"string"},
            "integer": {"integer"},
            "boolean": {"boolean"},
        },
    },
    CLASSES: {
        # classes involved in cycles
        # key: class name, value: node where the cycle starts
        0: {
            "ClassA": "ClassA",
            "ClassB": "ClassB",
            "ClassC": "ClassC",
            "ClassD": "ClassA",
            "ClassE": "ClassA",
            "ClassF": "ClassF",
            "ClassG": "ClassF",
            "Mixin1": "Mixin1",
            "Mixin2": "Mixin2",
            "MixedClass": "Mixin2",
        },
        # class ancestors for classes not in cycles
        # key: class name, value: class ancestors
        1: {
            "BaseClass": {"BaseClass"},
            "MixinA": {"MixinA"},
            "MixinB": {"MixinB"},
            "NonCycleClassA": {"NonCycleClassA", "BaseClass"},
            "NonCycleClassB": {"MixinA", "NonCycleClassB", "NonCycleClassA", "BaseClass"},
            "NonCycleClassC": {"MixinB", "NonCycleClassC", "NonCycleClassA", "BaseClass"},
            "IdentifierCycleClassA": {"IdentifierCycleClassA"},
            "IdentifierCycleClassB": {"IdentifierCycleClassB"},
            "IdentifierCycleClassC": {"IdentifierCycleClassC"},
            "IdentifierCycleClassD": {"IdentifierCycleClassD"},
        },
    },
}


@pytest.mark.parametrize(("target", "cycle_start_node"), [(k, v) for k, v in CYCLES[TYPES][0].items()])
@pytest.mark.parametrize("fn", ["detect_cycles", "graph_closure", "type_ancestors"])
def test_detect_type_cycles_error(sv_cycles_schema: SchemaView, target: str, cycle_start_node: str, fn: str) -> None:
    """Test detection of cycles in the types segment of the cycles schema."""
    if fn == "detect_cycles":
        with pytest.raises(ValueError, match=f"Cycle detected at node '{cycle_start_node}'"):
            detect_cycles(lambda x: sv_cycles_schema.type_parents(x), target)
    elif fn == "graph_closure":
        with pytest.raises(ValueError, match=f"Cycle detected at node '{cycle_start_node}'"):
            graph_closure(lambda x: sv_cycles_schema.type_parents(x), target, detect_cycles=True)
    else:
        with pytest.raises(ValueError, match=f"Cycle detected at node '{cycle_start_node}'"):
            sv_cycles_schema.type_ancestors(type_name=target, detect_cycles=True)


@pytest.mark.parametrize(("target", "expected"), [(k, v) for k, v in CYCLES[TYPES][1].items()])
@pytest.mark.parametrize("fn", ["detect_cycles", "graph_closure", "type_ancestors"])
def test_detect_type_cycles_no_cycles(sv_cycles_schema: SchemaView, target: str, expected: set[str], fn: str) -> None:
    """Ensure that types without cycles in their ancestry do not throw an error."""
    if fn == "detect_cycles":
        detect_cycles(lambda x: sv_cycles_schema.type_parents(x), target)
    elif fn == "graph_closure":
        got = graph_closure(lambda x: sv_cycles_schema.type_parents(x), target, detect_cycles=True)
        assert set(got) == expected
    else:
        got = sv_cycles_schema.type_ancestors(target, detect_cycles=True)
        assert set(got) == expected


@pytest.mark.parametrize(("target", "cycle_start_node"), [(k, v) for k, v in CYCLES[CLASSES][0].items()])
@pytest.mark.parametrize("fn", ["detect_cycles", "graph_closure", "class_ancestors"])
def test_detect_class_cycles_error(sv_cycles_schema: SchemaView, target: str, cycle_start_node: str, fn: str) -> None:
    """Test detection of class cycles in the cycles schema."""
    if fn == "detect_cycles":
        with pytest.raises(ValueError, match=f"Cycle detected at node '{cycle_start_node}'"):
            detect_cycles(lambda x: sv_cycles_schema.class_parents(x), target)

    elif fn == "graph_closure":
        with pytest.raises(ValueError, match=f"Cycle detected at node '{cycle_start_node}'"):
            graph_closure(lambda x: sv_cycles_schema.class_parents(x), target, detect_cycles=True)
    else:
        with pytest.raises(ValueError, match=f"Cycle detected at node '{cycle_start_node}'"):
            sv_cycles_schema.class_ancestors(target, detect_cycles=True)


@pytest.mark.parametrize(("target", "expected"), [(k, v) for k, v in CYCLES[CLASSES][1].items()])
@pytest.mark.parametrize("fn", ["detect_cycles", "graph_closure", "class_ancestors"])
def test_detect_class_cycles_no_cycles(sv_cycles_schema: SchemaView, target: str, expected: set[str], fn: str) -> None:
    """Ensure that classes without cycles in their ancestry do not throw an error."""
    if fn == "detect_cycles":
        detect_cycles(lambda x: sv_cycles_schema.class_parents(x), target)
    elif fn == "graph_closure":
        got = graph_closure(lambda x: sv_cycles_schema.class_parents(x), target, detect_cycles=True)
        assert set(got) == expected
    else:
        got = sv_cycles_schema.class_ancestors(target, detect_cycles=True)
        assert set(got) == expected


@pytest.mark.parametrize("target", CYCLES[CLASSES][1].keys())
def test_detect_class_as_range_cycles(sv_cycles_schema: SchemaView, target: str) -> None:
    """Test cycle detection in cases where a class is used as a range."""

    def check_recursive_id_slots(class_name: str) -> list[str]:
        """Given a class, retrieve any classes used as the range for the class identifier slot."""
        id_slot = sv_cycles_schema.get_identifier_slot(class_name, use_key=True)
        if not id_slot:
            return []
        ind_range = sv_cycles_schema.slot_range_as_union(id_slot)
        return [sv_cycles_schema.get_class(x).name for x in ind_range if sv_cycles_schema.get_class(x)] or []

    # classes with a cycle in the class identifier slot range are cunningly named
    if "IdentifierCycle" in target:
        with pytest.raises(ValueError, match="Cycle detected at node "):
            detect_cycles(lambda x: check_recursive_id_slots(x), target)

    else:
        detect_cycles(lambda x: check_recursive_id_slots(x), target)


@pytest.mark.parametrize(
    ("entity_type", "entity_name", "type_for_methods", "get_all_method"),
    [
        (ClassDefinition, "ToDeleteClass", "class", "all_classes"),
        (SlotDefinition, "ToDeleteSlot", "slot", "all_slots"),
        (EnumDefinition, "ToDeleteEnum", "enum", "all_enums"),
        (TypeDefinition, "ToDeleteType", "type", "all_types"),
        (SubsetDefinition, "ToDeleteSubset", "subset", "all_subsets"),
    ],
)
def test_add_delete_get_entity(
    entity_type: ClassDefinition | SlotDefinition | EnumDefinition | TypeDefinition | SubsetDefinition,
    entity_name: str,
    type_for_methods: str,
    get_all_method: str,
) -> None:
    """Test that entities can be added and deleted from a schema."""
    # method for adding an entity, e.g. view.add_class(...)
    add_method = f"add_{type_for_methods}"
    # method for deleting an entity, e.g. view.delete_subset(...)
    delete_method = f"delete_{type_for_methods}"
    # method for getting a specific entity, e.g. view.get_enum(...)
    get_method = f"get_{type_for_methods}"

    # Build the schema
    builder = SchemaBuilder(name="test_schema", id="test_schema")
    schema = builder.schema
    view = SchemaView(schema)

    assert view.modifications == 0
    # create the entity definition object, e.g. ClassDefinition
    entity = entity_type(name=entity_name)
    # add the entity to the schemaview, e.g. view.add_class(...)
    getattr(view, add_method)(entity)

    # check that the entity is returned when running the get all command, e.g. view.all_classes(...)
    assert {entity_name} == set(getattr(view, get_all_method)())
    assert view.modifications == 1

    # retrieve the individual class, e.g. view.get_class(...)
    just_added_entity = getattr(view, get_method)(entity_name)
    assert isinstance(just_added_entity, entity_type)

    # delete the entity from the schema , e.g. view.delete_class(...)
    getattr(view, delete_method)(entity_name)
    assert getattr(view, get_all_method)() == {}
    assert view.modifications == 2

    # try to retrieve the entity again using get_{type_for_methods}, e.g. view.get_class(...)
    assert getattr(view, get_method)(entity_name, strict=False) is None

    # expect that retrieving the entity will return an error if strict mode is on
    with pytest.raises(ValueError, match=f"No such {type_for_methods}"):
        getattr(view, get_method)(entity_name, strict=True)
