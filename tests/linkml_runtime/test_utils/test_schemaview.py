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
)
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


def test_imports(schema_view_with_imports: SchemaView) -> None:
    """View should by default dynamically include imports chain."""
    view = schema_view_with_imports
    assert view.schema.source_file is not None
    logger.debug(view.imports_closure())
    assert set(view.imports_closure()) == {"kitchen_sink", "core", "linkml:types"}

    for t in view.all_types():
        logger.debug(f"T={t} in={view.in_schema(t)}")
    assert view.in_schema(ClassDefinitionName("Person")) == "kitchen_sink"
    assert view.in_schema(SlotDefinitionName("id")) == "core"
    assert view.in_schema(SlotDefinitionName("name")) == "core"
    assert view.in_schema(SlotDefinitionName(ACTIVITY)) == "core"
    assert view.in_schema(SlotDefinitionName("string")) == "types"

    assert ACTIVITY in view.all_classes()
    assert ACTIVITY not in view.all_classes(imports=False)
    assert "string" in view.all_types()
    assert "string" not in view.all_types(imports=False)
    assert len(view.type_ancestors("SymbolString")) == len(["SymbolString", "string"])

    for tn, t in view.all_types().items():
        assert tn == t.name
        induced_t = view.induced_type(tn)
        assert induced_t.uri is not None
        assert induced_t.base is not None
        if t in view.all_types(imports=False).values():
            assert t.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        else:
            assert t.from_schema in ["https://w3id.org/linkml/tests/core", "https://w3id.org/linkml/types"]

    for en, e in view.all_enums().items():
        assert en == e.name
        if e in view.all_enums(imports=False).values():
            assert e.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        else:
            assert e.from_schema == "https://w3id.org/linkml/tests/core"

    for sn, s in view.all_slots().items():
        assert sn == s.name
        s_induced = view.induced_slot(sn)
        assert s_induced.range is not None
        if s in view.all_slots(imports=False).values():
            assert s.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        else:
            assert s.from_schema == "https://w3id.org/linkml/tests/core"

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

    for c in ["Company", "Person", "Organization", "Thing"]:
        assert view.induced_slot("id", c).identifier
        assert not view.induced_slot("name", c).identifier
        assert not view.induced_slot("name", c).required
        assert view.induced_slot("name", c).range == "string"

    for c in ["Event", "EmploymentEvent", "MedicalEvent"]:
        s = view.induced_slot("started at time", c)
        assert s.range == "date"
        assert s.slot_uri == "prov:startedAtTime"

    assert view.induced_slot(AGE_IN_YEARS, "Person").minimum_value == 0
    assert view.induced_slot(AGE_IN_YEARS, "Adult").minimum_value == 16

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

    # dynamic enums
    e = view.get_enum("HCAExample")
    assert set(e.include[0].reachable_from.source_nodes) == {"GO:0007049", "GO:0022403"}

    # units
    height = view.get_slot("height_in_m")
    assert height.unit.ucum_code == "m"


def test_imports_from_schemaview(schema_view_with_imports: SchemaView) -> None:
    """View should by default dynamically include imports chain."""
    view = schema_view_with_imports
    view2 = SchemaView(view.schema)
    assert len(view.all_classes()) == len(view2.all_classes())
    assert len(view.all_classes(imports=False)) == len(view2.all_classes(imports=False))


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
    for tn in ["uriorcurie", "string", "float"]:
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
                # N.b. BUG: due to caching and how the `from_schema` element is generated,
                # we cannot know whether it will be populated.
                # assert e.from_schema is None
            else:
                # if the source is an imported schema, we expect None without imports
                assert getattr(creature_view, get_fn)(entity_name, imports=False) is None
                if entity != "element":
                    # in strict mode, we expect an error if the entity does not exist
                    with pytest.raises(ValueError, match=f'No such {entity}: "{entity_name}"'):
                        getattr(creature_view, f"get_{entity}")(entity_name, imports=False, strict=True)

            # turn on imports
            e = getattr(creature_view, f"get_{entity}")(entity_name, imports=True)
            assert e.from_schema == f"{CREATURE_SCHEMA_BASE_URL}/{src}"


@pytest.mark.parametrize("entity", argvalues=[e for e in CREATURE_EXPECTED if e != "element"])
def test_get_entity_does_not_exist(creature_view: SchemaView, entity: str) -> None:
    """Test retrieval of a specific entity from the creature schema."""
    get_fn = f"get_{entity}"

    # returns None unless the `strict` flag is passed
    assert getattr(creature_view, get_fn)("does_not_exist") is None

    # raises an error with `strict` flag on
    with pytest.raises(ValueError, match=f'No such {entity}: "does_not_exist"'):
        getattr(creature_view, get_fn)("does_not_exist", strict=True)


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


@pytest.fixture(scope="session")
def schema_view_inlined() -> SchemaView:
    """Fixture for a SchemaView for testing attribute edge cases."""
    return SchemaView(os.path.join(INPUT_DIR, "schemaview_is_inlined.yaml"))


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


def test_enums_and_enum_relationships(schema_view_no_imports: SchemaView) -> None:
    """Test various aspects of Enum representation.

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

    # Test for ValueError when passing incorrect parameters
    with pytest.raises(ValueError, match='No such enum: "not_an_enum"'):
        view.permissible_value_parent("not_a_pv", "not_an_enum")

    for en, e in view.all_enums().items():
        if e.name == "Animals":
            for pv in e.permissible_values:
                if pv == "CAT":
                    assert view.permissible_value_parent(pv, e.name) is None
                    assert view.permissible_value_ancestors(pv, e.name) == ["CAT"]
                    assert "LION" in view.permissible_value_descendants(pv, e.name)
                    assert "ANGRY_LION" in view.permissible_value_descendants(pv, e.name)
                    assert "TABBY" in view.permissible_value_descendants(pv, e.name)
                    assert "TABBY" in view.permissible_value_children(pv, e.name)
                    assert "LION" in view.permissible_value_children(pv, e.name)
                    assert "EAGLE" not in view.permissible_value_descendants(pv, e.name)

                if pv == "LION":
                    assert "ANGRY_LION" in view.permissible_value_children(pv, e.name)

                if pv == "ANGRY_LION":
                    assert view.permissible_value_parent(pv, e.name) == ["LION"]
                    assert view.permissible_value_ancestors(pv, e.name) == ["ANGRY_LION", "LION", "CAT"]
                    assert view.permissible_value_descendants(pv, e.name) == ["ANGRY_LION"]

    for cn, c in view.all_classes().items():
        if c.name == "Adult":
            assert view.class_ancestors(c.name) == ["Adult", "Person", "HasAliases", "Thing"]


def test_schemaview(schema_view_no_imports: SchemaView) -> None:
    """General SchemaView tests."""
    view = schema_view_no_imports
    logger.debug(view.imports_closure())
    assert len(view.imports_closure()) == 1

    all_cls = view.all_classes()
    logger.debug(f"n_cls = {len(all_cls)}")

    assert list(view.annotation_dict(IS_CURRENT).values()) == ["bar"]
    logger.debug(view.annotation_dict(EMPLOYED_AT))
    e = view.get_element(EMPLOYED_AT)
    logger.debug(e.annotations)
    e = view.get_element("has employment history")
    logger.debug(e.annotations)

    elements = view.get_elements_applicable_by_identifier("ORCID:1234")
    assert "Person" in elements
    elements = view.get_elements_applicable_by_identifier("PMID:1234")
    assert "Organization" in elements
    elements = view.get_elements_applicable_by_identifier("http://www.ncbi.nlm.nih.gov/pubmed/1234")
    assert "Organization" in elements
    elements = view.get_elements_applicable_by_identifier("TEST:1234")
    assert "anatomical entity" not in elements

    assert list(view.annotation_dict(SlotDefinitionName(IS_CURRENT)).values()) == ["bar"]
    logger.debug(view.annotation_dict(SlotDefinitionName(EMPLOYED_AT)))
    element = view.get_element(SlotDefinitionName(EMPLOYED_AT))
    logger.debug(element.annotations)
    element = view.get_element(SlotDefinitionName("has employment history"))
    logger.debug(element.annotations)

    assert view.is_mixin("WithLocation")
    assert not view.is_mixin("BirthEvent")

    assert view.inverse("employment history of") == "has employment history"
    assert view.inverse("has employment history") == "employment history of"

    mapping = view.get_mapping_index()
    assert mapping is not None

    category_mapping = view.get_element_by_mapping("GO:0005198")
    assert category_mapping == [ACTIVITY]

    assert view.is_multivalued("aliases")
    assert not view.is_multivalued("id")
    assert view.is_multivalued("dog addresses")

    assert view.slot_is_true_for_metadata_property("aliases", "multivalued")
    assert view.slot_is_true_for_metadata_property("id", "identifier")

    with pytest.raises(ValueError):
        view.slot_is_true_for_metadata_property("aliases", "aliases")

    for tn, t in view.all_types().items():
        logger.info(f"TN = {tn}")
        assert t.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"

    for sn, s in view.all_slots().items():
        logger.info(f"SN = {sn} RANGE={s.range}")
        assert s.from_schema == "https://w3id.org/linkml/tests/kitchen_sink"
        rng = view.induced_slot(sn).range
        assert rng is not None

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

    # -- TEST ANCESTOR/DESCENDANTS FUNCTIONS --

    assert set(view.class_ancestors(COMPANY)) == {"Company", "Organization", "HasAliases", "Thing"}
    assert set(view.class_ancestors(COMPANY, reflexive=False)) == {"Organization", "HasAliases", "Thing"}
    assert set(view.class_descendants("Thing")) == {"Thing", "Person", "Organization", COMPANY, "Adult"}

    # -- TEST CLASS SLOTS --

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

    assert view.get_class(AGENT).class_uri == "prov:Agent"
    assert view.get_uri(AGENT) == "prov:Agent"
    logger.debug(view.get_class(COMPANY).class_uri)

    assert view.get_uri(COMPANY) == "ks:Company"

    # test induced slots
    for c in [COMPANY, "Person", "Organization"]:
        islot = view.induced_slot("aliases", c)
        assert islot.multivalued is True
        assert islot.owner == c
        assert view.get_uri(islot, expand=True) == "https://w3id.org/linkml/tests/kitchen_sink/aliases"

    assert view.get_identifier_slot("Company").name == "id"
    assert view.get_identifier_slot("Thing").name == "id"
    assert view.get_identifier_slot("FamilialRelationship") is None

    for c in [COMPANY, "Person", "Organization", "Thing"]:
        assert view.induced_slot("id", c).identifier
        assert not view.induced_slot("name", c).identifier
        assert not view.induced_slot("name", c).required
        assert view.induced_slot("name", c).range == "string"
        assert view.induced_slot("id", c).owner == c
        assert view.induced_slot("name", c).owner == c

    for c in ["Event", "EmploymentEvent", "MedicalEvent"]:
        s = view.induced_slot("started at time", c)
        logger.debug(f"s={s.range} // c = {c}")
        assert s.range == "date"
        assert s.slot_uri == "prov:startedAtTime"
        assert s.owner == c

        c_induced = view.induced_class(c)
        assert c_induced.slots == []
        assert c_induced.attributes != []
        s2 = c_induced.attributes["started at time"]
        assert s2.range == "date"
        assert s2.slot_uri == "prov:startedAtTime"

    # test slot_usage
    assert view.induced_slot(AGE_IN_YEARS, "Person").minimum_value == 0
    assert view.induced_slot(AGE_IN_YEARS, "Adult").minimum_value == 16
    assert view.induced_slot("name", "Person").pattern is not None
    assert view.induced_slot("type", "FamilialRelationship").range == "FamilialRelationshipType"
    assert view.induced_slot(RELATED_TO, "FamilialRelationship").range == "Person"
    assert view.get_slot(RELATED_TO).range == "Thing"
    assert view.induced_slot(RELATED_TO, "Relationship").range == "Thing"
    assert set(view.induced_slot("name").domain_of) == {"Thing", "Place"}

    a = view.get_class(ACTIVITY)
    assert set(a.exact_mappings) == {"prov:Activity"}
    logger.debug(view.get_mappings(ACTIVITY, expand=True))
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


def test_rollup_rolldown(schema_view_no_imports: SchemaView) -> None:
    """Test rolling up and rolling down."""
    # no import schema
    view = schema_view_no_imports
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
