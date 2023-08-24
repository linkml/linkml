import logging
import os
import shutil
import tempfile
import unittest
from copy import copy
from typing import List

from linkml.generators.plantumlgen import PlantumlGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
PLANTUML_OUT = env.expected_path("kitchen_sink.plantuml.md")
SVG_DIR = env.expected_path("kitchen_sink_svg")

MARKDOWN_HEADER = """@startuml
"""

MARKDOWN_FOOTER = """
@enduml
"""

PERSON = """
class "Person" {
    {field} "id": "string" [req]
    {field} "name": "string" [opt]
    {field} "age_in_years": "integer" [opt]
    {field} "species_name": "string" [opt]
    {field} "stomach_count": "integer" [opt]
    {field} "is_living": "LifeStatusEnum" [opt]
    {field} "aliases": "string" [0..*]
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


def assert_svgfile_contains(
    filename,
    text,
    after: str = None,
    followed_by: List[str] = None,
    outdir=SVG_DIR,
    invert=False,
) -> None:
    found = False
    is_after = False  # have we reached the after mark?
    with open(os.path.join(outdir, filename)) as stream:
        lines = stream.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if text in line:
                if after is None:
                    found = True
                else:
                    if is_after:
                        found = True
                if found and followed_by:
                    todo = copy(followed_by)
                    for j in range(i + 1, len(lines)):
                        subsequent_line = lines[j]
                        if len(todo) > 0 and todo[0] in subsequent_line:
                            todo = todo[1:]
                    if len(todo) > 0:
                        if not invert:
                            logging.error(f"Did not find: {todo}")
                        assert invert
                    else:
                        return
            if after is not None and after in line:
                is_after = True
    if not found and not invert:
        logging.error(f"Failed to find {text} in {filename}")
    if invert:
        assert not found
    else:
        assert found


class PlantumlDiagramGeneratorTestCase(unittest.TestCase):
    """
    Tests generation of PlantUML from LinkML schemas
    """

    def test_serialize(self):
        """Test default serialization (structural)"""
        gen = PlantumlGenerator(SCHEMA)
        plantuml = gen.serialize()
        with open(PLANTUML_OUT, "w") as stream:
            stream.write(plantuml)
        self._in(MARKDOWN_HEADER, plantuml, "diagram header is missing")
        self._in(MARKDOWN_FOOTER, plantuml, "diagram footer is missing")
        self._in(PERSON, plantuml)
        self._in(PERSON2MEDICALEVENT, plantuml)
        self._in(FAMILIALRELATIONSHIP2PERSON, plantuml)

    def test_serialize_direct(self):
        """Test default serialization (structural), no markdown block"""
        gen = PlantumlGenerator(SCHEMA)
        plantuml = gen.serialize()
        self.assertNotIn("```", plantuml, "markdown header should not be present")
        self._in(PERSON, plantuml)
        self._in(PERSON2MEDICALEVENT, plantuml)

    def test_serialize_selected(self):
        """Test serialization of selected elements"""
        gen = PlantumlGenerator(SCHEMA)
        plantuml = gen.serialize(classes=["FamilialRelationship"])
        self.assertNotIn("MarriageEvent", plantuml, "MarriageEvent not reachable from selected")
        self._in(FAMILIALRELATIONSHIP2PERSON, plantuml, "dangling references should be included")

    def test_generate_svg(self):
        gen = PlantumlGenerator(SCHEMA)
        svg_temp_dir = tempfile.mkdtemp()
        gen.serialize(directory=svg_temp_dir)
        assert_svgfile_contains(
            "KitchenSink.svg",
            "<svg xmlns=",
            outdir=svg_temp_dir,
        )
        assert_svgfile_contains(
            "KitchenSink.svg",
            '<!--class FakeClass--><g id="elem_FakeClass">',
            outdir=svg_temp_dir,
        )
        assert_svgfile_contains(
            "KitchenSink.svg",
            ">FakeClass</text>",
            outdir=svg_temp_dir,
        )
        assert_svgfile_contains(
            "KitchenSink.svg",
            "<line style=",
            outdir=svg_temp_dir,
        )
        assert_svgfile_contains(
            "KitchenSink.svg",
            "</svg>",
            outdir=svg_temp_dir,
        )
        shutil.rmtree(svg_temp_dir)

    def _in(self, s1, s2, message: str = None):
        self.assertIn(s1.replace(" ", ""), s2.replace(" ", ""), message)


if __name__ == "__main__":
    unittest.main()
