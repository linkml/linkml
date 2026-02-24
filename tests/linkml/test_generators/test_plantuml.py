import os
import tempfile
from unittest.mock import MagicMock, patch
from xml.dom import minidom

import pytest
from docker.errors import ImageNotFound
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from linkml.generators.plantumlgen import PlantumlGenerator
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    EnumDefinition,
    PermissibleValue,
    SchemaDefinition,
    SlotDefinition,
)

pytestmark = pytest.mark.plantumlgen

MARKDOWN_HEADER = """@startuml
skinparam nodesep 10
hide circle
hide empty members
"""

MARKDOWN_FOOTER = """
@enduml
"""

PERSON = """
class "Person" [[{A person, living or dead}]] {
    {field} id : string
    {field} name : string
    {field} age_in_years : integer
    {field} species_name : string
    {field} stomach_count : integer
    {field} is_living : LifeStatusEnum
    {field} aliases : string  [0..*]
}
"""

PERSON2MEDICALEVENT = """
"Person" *--> "0..*" "MedicalEvent" : "has medical history"
"""

FAMILIALRELATIONSHIP2PERSON = """
"FamilialRelationship" --> "1" "Person" : "related to"
"""

DATASET2PERSON = """
"Dataset" *--> "0..*" "Person" : "persons"
"""

PERSON_URL = "https://kroki.io/plantuml/svg/eNp9VE1rwzAMvfdXiBzLMrZrD4Nu69hhHWM7lhK0RG0EsR0st1BK__ucj2ZJWycnR3p6T3oyTgsUgeiLrBgdwWp1nENZ_9xBwXvWWzAWMsLstF7DcQL-O26YiuwEnMEMxNkKBIOMRkWhHG4pYZ0cCK14DGtHW7IXICkpZZJkjEicUZjmSWp22gWZWJJ2jhl88IZ-HLqdLPROXfZVMApJT231cH8_XU9Ok7Qx6Zmtyxd70q426tNoakz5h8yzzJJIML-kjFMsxkneULFvpvimAh0bLTmXQfBClYU5KM83TvpiVIn6EMy_ovPjh-uXaC373Y2rvKPMGx-vId0lm8bxE0Te3MdoaOoMohwFfqsQUB27UTWNej77EmzOXjIAHpreiqgmCDn7e2QPodrbu2g5Nm0SbC8bbONqUy0LdfFeM7d1a7rKtbOAp6i1KQNnfFm35b7FPXBKFarb9aC_Hqx5AapJLtYeoFUV6tzDOR7Hw_vggTt_-AOKp2gk"

DATASET2PERSON_URL = "https://kroki.io/plantuml/svg/eNp9kLEKwjAQhvc-xZGxWNHVQRB1VcFRHM7klEhzKUksFvHdjSlWFOuWn_s-7vLLEr0HgTLoWodGwG53Q6icrYklFSdichg0n-CF3Pd7uGXZPZOtuiHnLSdxBlUKAygjGh3rQBGqb2WBAT2F5Kws0_d8bhVtGx_I_EFMhdz0zmfcrA9nku2S5RVNVRLYI1xYWvbBoWZSkOjOfR-WF8UUxGg4zMXnORMQMkbwKXvR57wLnXRBUz_f_ScteL7_0a_OI9w2_hsdi48iIm0ooIqceAA8u58V"

PERSON2MEDICALEVENT_URL = "https://kroki.io/plantuml/svg/eNqNUctuwjAQvOcrVj61qEHtlUMl1HLs445otNgLbOWsI9tBRVH-vRYhkQj04Zt3ZjyeWW0xBFDv3mkytacnJ5qqqGC5bF6dULtaQZNlbaZPRIuafkRfyLBGu9iTjJ-AdJoNkzUthIg-kikwFpFLuuFbmIHBSABnPBLzDxaHQtfeJ8uOsnbOEkpiDf96ZtyKCxz-jEc-ODnCc6iOlzuwvGfZgvNgCM1Yci1sQkddTPL8EdT9dPqgrrU9A1X1Q_Wr9jJK0pp-eKE9s-12l_gsYJ3GyClrNoQefCZqvMqk2WGAshvCjkN0_pC0J_wjz0eSvp65HN7Wn6S7ihZfWFaWwG2gFu0kRI8sZODI7sv7BsIk1Pk="

FAMILIALRELATIONSHIP2PERSON_URL = "https://kroki.io/plantuml/svg/eNp9kMEKwjAMhu99itCTihO9ehC8eBQRb6IS1qiB2o42CDL27nZT1Ikzt-b7_h-a3GKMoNdkUdi7eOZCw3ZbLr2jareDUqlK5Q9pRSF61-A5FM1jCJav7E7gAxhC8x1Z4IUto_3TD2nKI5M1FeQ-mGQ7StkpRAl1NbQUuRWU2K_iTY3adhQMQuaAchC-UI_7KWtQvj1ypsOqVMcnsmwGeqLfZ5mCDrVBBsRr9doPGnM8Gg1010FS9IwRjk8I4YPGVNW291nWUXQHmaCZ4w=="


@pytest.fixture(scope="module")
def kroki_url(request):
    kroki_container = DockerContainer("yuzutech/kroki").with_exposed_ports(8000)

    def stop_container():
        kroki_container.stop()

    try:
        kroki_container.start()
        wait_for_logs(kroki_container, ".*Succeeded in deploying verticle.*")
        request.addfinalizer(stop_container)

        return f"http://{kroki_container.get_container_host_ip()}:{kroki_container.get_exposed_port(8000)}"
    except ImageNotFound:
        pytest.skip(
            "PlantUML Kroki Container image could not be started, but docker tests were not skipped! "
            "Either fix the docker invocation, the _docker_server_running function, "
            "or find a more reliable way to test PlantUML!"
        )


@pytest.mark.parametrize(
    "input_class,expected",
    [
        # check that expected plantUML class diagram blocks are present
        # when diagrams are generated for different classes
        ("Person", PERSON_URL),
        ("Dataset", DATASET2PERSON_URL),
        ("MedicalEvent", PERSON2MEDICALEVENT_URL),
        ("FamilialRelationship", FAMILIALRELATIONSHIP2PERSON_URL),
    ],
)
def test_create_request(input_class, expected, kitchen_sink_path):
    """Test serialization of select plantUML class diagrams from schema."""
    generator = PlantumlGenerator(
        kitchen_sink_path,
        dry_run=True,
    )
    plantuml = generator.serialize(classes=[input_class])
    assert plantuml == expected


@pytest.mark.parametrize(
    "input_class,expected",
    [
        # check that expected plantUML class diagram blocks are present
        # when diagrams are generated for different classes
        ("Person", PERSON),
        ("Dataset", DATASET2PERSON),
        ("MedicalEvent", PERSON2MEDICALEVENT),
        ("FamilialRelationship", FAMILIALRELATIONSHIP2PERSON),
    ],
)
@pytest.mark.network
@pytest.mark.kroki
@pytest.mark.docker
def test_serialize_selected(input_class, expected, kitchen_sink_path, kroki_url):
    """Test serialization of select plantUML class diagrams from schema."""
    generator = PlantumlGenerator(
        kitchen_sink_path,
        kroki_server=kroki_url,
    )
    plantuml = generator.serialize(classes=[input_class])

    # check that the expected block/relationships are present
    # in class-selected diagrams
    # Strip whitespace from each line to normalize comparison
    expected_stripped = "\n".join(line.rstrip() for line in expected.splitlines())
    plantuml_stripped = "\n".join(line.rstrip() for line in plantuml.splitlines())
    assert expected_stripped in plantuml_stripped

    # make sure that random classes like `MarriageEvent` which
    # have no defined relationships with classes like `FamilialRelationship`
    # have crept into class-selected diagrams
    if input_class == "FamilialRelationship":
        assert 'class "MarriageEvent"' not in plantuml, f"MarriageEvent not reachable from {input_class}"


@pytest.mark.network
@pytest.mark.kroki
@pytest.mark.docker
def test_serialize(kitchen_sink_path, kroki_url):
    """Test serialization of complete plantUML class diagram from schema."""
    generator = PlantumlGenerator(
        kitchen_sink_path,
        kroki_server=kroki_url,
    )
    plantuml = generator.serialize()

    # check that plantUML start and end blocks are present
    assert MARKDOWN_HEADER in plantuml
    assert MARKDOWN_FOOTER in plantuml

    # check that Markdown code blocks are not present
    assert "```" not in plantuml, "Markdown code block should not be present"

    # check that classes like `MarriageEvent` are present
    # in complete UML class diagram
    assert 'class "MarriageEvent"' in plantuml


@pytest.mark.network
@pytest.mark.kroki
@pytest.mark.docker
def test_generate_svg(tmp_path, kitchen_sink_path, kroki_url):
    """Test the correctness of SVG rendering of plantUML diagram."""
    generator = PlantumlGenerator(
        kitchen_sink_path,
        kroki_server=kroki_url,
    )
    generator.serialize(directory=tmp_path)

    # name of SVG file will be inferred from schema name because
    # we are passing a value to the directory argument
    svg_file = tmp_path / "KitchenSink.svg"

    # check that SVG file is generated correctly
    assert svg_file.is_file()

    svg_dom = minidom.parse(os.fspath(tmp_path / "KitchenSink.svg"))

    classes_list = []  # list of all classes in schema
    relationships_list = []  # list of all links/relationships in schema
    groups = svg_dom.getElementsByTagName("g")
    for group in groups:
        id = group.getAttribute("id")
        if id.startswith("entity_"):
            class_name = id[len("entity_") :]
            classes_list.append(class_name)
        if id.startswith("link_"):
            link_name = id[len("link_") :]
            relationships_list.append(link_name)

    assert "Person" in classes_list
    assert "Dataset" in classes_list
    assert "FamilialRelationship" in classes_list
    assert "MedicalEvent" in classes_list

    assert "Person_MedicalEvent" in relationships_list
    assert "FamilialRelationship_Person" in relationships_list
    assert "Dataset_Person" in relationships_list
    assert "Dataset_MarriageEvent" not in relationships_list


def test_preserve_names():
    """Test preserve_names option preserves original LinkML names in PlantUML diagram output"""
    schema = SchemaDefinition(
        id="https://example.com/test_schema",
        name="test_underscore_schema",
        imports=["linkml:types"],
        prefixes={"linkml": "https://w3id.org/linkml/"},
        classes={
            "My_Class": ClassDefinition(name="My_Class", slots=["my_slot", "related_object"]),
            "Another_Class_Name": ClassDefinition(name="Another_Class_Name", slots=["class_specific_slot"]),
        },
        slots={
            "my_slot": SlotDefinition(name="my_slot", range="string"),
            "class_specific_slot": SlotDefinition(name="class_specific_slot", range="string"),
            "related_object": SlotDefinition(name="related_object", range="Another_Class_Name"),
        },
    )

    # Test default behavior (names are normalized)
    gen_default = PlantumlGenerator(schema=schema)
    diagram_default = gen_default.visit_schema()

    # Check that slot names and ranges are normalized (underscore)
    assert "my_slot" in diagram_default
    assert "class_specific_slot" in diagram_default
    assert ": string" in diagram_default

    # Test preserve_names behavior (names are preserved)
    gen_preserve = PlantumlGenerator(schema=schema, preserve_names=True)
    diagram_preserve = gen_preserve.visit_schema()

    # Check that slot names and ranges are preserved
    assert "my_slot" in diagram_preserve
    assert "class_specific_slot" in diagram_preserve
    assert ": string" in diagram_preserve

    # Test filename generation with directory for branch coverage
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.iter_content.return_value = [b"svg"]

    with tempfile.TemporaryDirectory() as temp_dir, patch("requests.get", return_value=mock_response):
        gen = PlantumlGenerator(schema=schema, preserve_names=True, dry_run=False)
        gen.visit_schema(classes={"My_Class"}, directory=temp_dir)
        assert gen.output_file_name.endswith("My_Class.svg")


@pytest.fixture()
def enum_schema() -> SchemaDefinition:
    """A minimal schema with two classes and two enumerations, one inheriting the other."""
    schema = SchemaDefinition(
        id="https://example.com/enum_schema",
        name="enum_schema",
        imports=["linkml:types"],
        prefixes={"linkml": "https://w3id.org/linkml/"},
    )
    schema.enums["StatusEnum"] = EnumDefinition(
        name="StatusEnum",
        permissible_values={
            "ACTIVE": PermissibleValue(text="ACTIVE"),
            "INACTIVE": PermissibleValue(text="INACTIVE"),
        },
    )
    schema.enums["ExtendedStatusEnum"] = EnumDefinition(
        name="ExtendedStatusEnum",
        inherits=["StatusEnum"],
        permissible_values={
            "PENDING": PermissibleValue(text="PENDING"),
        },
    )
    schema.slots["status"] = SlotDefinition(name="status", range="StatusEnum", domain_of=["Thing"])
    schema.classes["Thing"] = ClassDefinition(
        name="Thing",
        slots=["status"],
    )
    schema.classes["Thing"].slots = ["status"]
    return schema


def test_include_enums_disabled_by_default(enum_schema: SchemaDefinition) -> None:
    """Enum blocks must not appear unless include_enums=True."""
    gen = PlantumlGenerator(schema=enum_schema, include_enums=False)
    output = gen.visit_schema()
    assert 'enum "StatusEnum"' not in output
    assert 'enum "ExtendedStatusEnum"' not in output


def test_include_enums_generates_enum_blocks(enum_schema: SchemaDefinition) -> None:
    """Enum blocks are emitted for all enumerations referenced by the schema's classes."""
    gen = PlantumlGenerator(schema=enum_schema, include_enums=True)
    output = gen.visit_schema()
    assert 'enum "StatusEnum"' in output
    assert "ACTIVE" in output
    assert "INACTIVE" in output


def test_include_enums_unreferenced_enum_excluded(enum_schema: SchemaDefinition) -> None:
    """Enumerations not referenced by any slot are not rendered."""
    gen = PlantumlGenerator(schema=enum_schema, include_enums=True)
    output = gen.visit_schema()
    # ExtendedStatusEnum is not used by any slot, so it must be absent
    assert 'enum "ExtendedStatusEnum"' not in output


def test_include_enums_generates_association_arrow(enum_schema: SchemaDefinition) -> None:
    """An association arrow is emitted from each class to its enum-typed slots."""
    gen = PlantumlGenerator(schema=enum_schema, include_enums=True)
    output = gen.visit_schema()
    assert '"Thing" --> "StatusEnum" : "status"' in output


@pytest.mark.parametrize(
    "include_enums,expect_enum_block,expect_arrow",
    [
        (True, True, True),
        (False, False, False),
    ],
)
def test_include_enums_parametrized(
    enum_schema: SchemaDefinition,
    include_enums: bool,
    expect_enum_block: bool,
    expect_arrow: bool,
) -> None:
    """Parametrized check: enum blocks and arrows appear iff include_enums=True."""
    gen = PlantumlGenerator(schema=enum_schema, include_enums=include_enums)
    output = gen.visit_schema()
    if expect_enum_block:
        assert 'enum "StatusEnum"' in output
    else:
        assert 'enum "StatusEnum"' not in output
    if expect_arrow:
        assert '"Thing" --> "StatusEnum"' in output
    else:
        assert '"Thing" --> "StatusEnum"' not in output


def test_include_enums_inheritance_arrow(enum_schema: SchemaDefinition) -> None:
    """Enum inheritance arrows are emitted when both parent and child enums are rendered."""
    # Add a slot referencing the child enum so both get included
    enum_schema.slots["ext_status"] = SlotDefinition(name="ext_status", range="ExtendedStatusEnum", domain_of=["Thing"])
    enum_schema.classes["Thing"].slots.append("ext_status")
    gen = PlantumlGenerator(schema=enum_schema, include_enums=True)
    output = gen.visit_schema()
    assert 'enum "StatusEnum"' in output
    assert 'enum "ExtendedStatusEnum"' in output
    assert '"StatusEnum" <|-- "ExtendedStatusEnum"' in output


def test_include_all_generates_all_classes(enum_schema: SchemaDefinition) -> None:
    """include_all=True includes every class in the schema."""
    enum_schema.classes["Other"] = ClassDefinition(name="Other")
    gen = PlantumlGenerator(schema=enum_schema, include_all=True)
    output = gen.visit_schema()
    assert 'class "Thing"' in output or '"Thing"' in output
    assert '"Other"' in output


def test_include_all_generates_all_enums(enum_schema: SchemaDefinition) -> None:
    """include_all=True renders every enumeration, including unreferenced ones."""
    gen = PlantumlGenerator(schema=enum_schema, include_all=True)
    output = gen.visit_schema()
    # StatusEnum is referenced, ExtendedStatusEnum is not — both must appear
    assert 'enum "StatusEnum"' in output
    assert 'enum "ExtendedStatusEnum"' in output
    assert '"StatusEnum" <|-- "ExtendedStatusEnum"' in output


def test_include_all_overrides_explicit_classes(enum_schema: SchemaDefinition) -> None:
    """include_all=True overrides an explicit classes selection."""
    enum_schema.classes["Other"] = ClassDefinition(name="Other")
    gen = PlantumlGenerator(schema=enum_schema, include_all=True)
    # Even when passing a restricted class set, include_all should expand it
    output = gen.visit_schema(classes={"Thing"})
    assert '"Other"' in output


def test_include_all_does_not_need_include_enums(enum_schema: SchemaDefinition) -> None:
    """include_all=True renders enums even when include_enums=False."""
    gen = PlantumlGenerator(schema=enum_schema, include_all=True, include_enums=False)
    output = gen.visit_schema()
    assert 'enum "StatusEnum"' in output
    assert 'enum "ExtendedStatusEnum"' in output


# ---------------------------------------------------------------------------
# --format behaviour
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("fmt", ["puml", "plantuml"])
def test_format_text_returns_plantuml(fmt: str, kitchen_sink_path) -> None:
    """Text formats (puml/plantuml) always return @startuml source without hitting Kroki."""
    gen = PlantumlGenerator(kitchen_sink_path, format=fmt)
    output = gen.serialize()
    assert output.startswith("@startuml")
    assert "@enduml" in output


@pytest.mark.parametrize(
    "fmt,expected_kroki_segment",
    [
        ("svg", "/plantuml/svg/"),
        ("png", "/plantuml/png/"),
        ("json", "/plantuml/json/"),
        ("puml", "/plantuml/svg/"),  # text format → svg for Kroki
        ("plantuml", "/plantuml/svg/"),  # text format → svg for Kroki
    ],
)
def test_format_dry_run_url_uses_format(fmt: str, expected_kroki_segment: str, kitchen_sink_path) -> None:
    """dry_run=True returns the Kroki URL with the correct format segment."""
    gen = PlantumlGenerator(kitchen_sink_path, format=fmt, dry_run=True)
    url = gen.serialize()
    assert expected_kroki_segment in url


@pytest.mark.parametrize("fmt", ["png", "pdf", "jpg"])
def test_format_binary_stdout_raises(fmt: str, kitchen_sink_path) -> None:
    """Binary formats raise ValueError when no --directory is given."""
    gen = PlantumlGenerator(kitchen_sink_path, format=fmt)
    with pytest.raises(ValueError, match="--directory"):
        gen.serialize()


@pytest.mark.network
@pytest.mark.kroki
@pytest.mark.docker
def test_format_svg_stdout(kitchen_sink_path, kroki_url) -> None:
    """format='svg' without --directory returns SVG text from Kroki."""
    gen = PlantumlGenerator(kitchen_sink_path, format="svg", kroki_server=kroki_url)
    output = gen.serialize(classes=["Person"])
    assert output is not None
    assert "<svg" in output


# ---------------------------------------------------------------------------
# --mark-mixins behaviour
# ---------------------------------------------------------------------------


@pytest.fixture()
def mixin_schema() -> SchemaDefinition:
    """A minimal schema with one mixin class and one regular class that uses it."""
    schema = SchemaDefinition(
        id="https://example.com/mixin_schema",
        name="mixin_schema",
        imports=["linkml:types"],
        prefixes={"linkml": "https://w3id.org/linkml/"},
    )
    schema.classes["HasName"] = ClassDefinition(name="HasName", mixin=True, slots=["name"])
    schema.classes["Person"] = ClassDefinition(name="Person", mixins=["HasName"])
    schema.slots["name"] = SlotDefinition(name="name", range="string")
    return schema


def test_mark_mixins_disabled_by_default(mixin_schema: SchemaDefinition) -> None:
    """Mixin stereotype must not appear unless mark_mixins=True."""
    gen = PlantumlGenerator(schema=mixin_schema, mark_mixins=False)
    output = gen.visit_schema()
    assert "<<(M,orchid) mixin>>" not in output


def test_mark_mixins_adds_stereotype(mixin_schema: SchemaDefinition) -> None:
    """mark_mixins=True adds the spot stereotype to mixin class definitions."""
    gen = PlantumlGenerator(schema=mixin_schema, mark_mixins=True)
    output = gen.visit_schema()
    assert "<<(M,orchid) mixin>>" in output


def test_mark_mixins_only_on_mixin_classes(mixin_schema: SchemaDefinition) -> None:
    """Regular (non-mixin) classes must not receive the mixin stereotype."""
    gen = PlantumlGenerator(schema=mixin_schema, mark_mixins=True)
    output = gen.visit_schema()
    # Person is not a mixin — count occurrences: should appear exactly once (for HasName)
    assert output.count("<<(M,orchid) mixin>>") == 1


@pytest.mark.parametrize(
    "mark_mixins,expect_stereotype",
    [(True, True), (False, False)],
)
def test_mark_mixins_parametrized(
    mixin_schema: SchemaDefinition,
    mark_mixins: bool,
    expect_stereotype: bool,
) -> None:
    """Parametrized check: stereotype appears iff mark_mixins=True."""
    gen = PlantumlGenerator(schema=mixin_schema, mark_mixins=mark_mixins)
    output = gen.visit_schema()
    if expect_stereotype:
        assert "<<(M,orchid) mixin>>" in output
    else:
        assert "<<(M,orchid) mixin>>" not in output
