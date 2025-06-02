import os
from xml.dom import minidom

import pytest
from docker.errors import ImageNotFound
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from linkml.generators.plantumlgen import PlantumlGenerator

pytestmark = [pytest.mark.plantumlgen, pytest.mark.docker]

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
def test_serialize_selected(input_class, expected, kitchen_sink_path, kroki_url):
    """Test serialization of select plantUML class diagrams from schema."""
    generator = PlantumlGenerator(
        kitchen_sink_path,
        kroki_server=kroki_url,
    )
    plantuml = generator.serialize(classes=[input_class])

    # check that the expected block/relationships are present
    # in class-selected diagrams
    assert expected in plantuml

    # make sure that random classes like `MarriageEvent` which
    # have no defined relationships with classes like `FamilialRelationship`
    # have crept into class-selected diagrams
    if input_class == "FamilialRelationship":
        assert 'class "MarriageEvent"' not in plantuml, f"MarriageEvent not reachable from {input_class}"


@pytest.mark.network
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
