import unittest
from collections import namedtuple

import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError

from linkml.generators.erdiagramgen import ERDiagramGenerator
from linkml.generators.pydanticgen import PydanticGenerator
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
MERMAID_OUT = env.expected_path("kitchen_sink.mermaid.md")

MARKDOWN_HEADER = """```mermaid
erDiagram
"""

PERSON = """
Person {
    string id
    string name
    integer age_in_years
    string species_name
    integer stomach_count
    LifeStatusEnum is_living
    stringList aliases
}
"""

PERSON2MEDICALEVENT = """
Person ||--}o MedicalEvent : "has medical history"
"""

FAMILIALRELATIONSHIP2PERSON = """
FamilialRelationship ||--|| Person : "related to"
"""

DATASET2PERSON = """
Dataset ||--}o Person : "persons"
"""


class ERDiagramGeneratorTestCase(unittest.TestCase):
    """
    Tests generation of mermaidfrom LinkML schemas
    """

    def test_serialize(self):
        """Test default serialization (structural)"""
        gen = ERDiagramGenerator(SCHEMA)
        mermaid = gen.serialize()
        with open(MERMAID_OUT, "w") as stream:
            stream.write(mermaid)
        self._in(MARKDOWN_HEADER, mermaid, "default format should be markdown")
        self._in(PERSON, mermaid)
        self._in(PERSON2MEDICALEVENT, mermaid)
        self._in(FAMILIALRELATIONSHIP2PERSON, mermaid)
        self.assertNotIn("FakeClass", mermaid, "FakeClass should not be reachable from root")

    def test_serialize_direct(self):
        """Test default serialization (structural), no markdown block"""
        gen = ERDiagramGenerator(SCHEMA, format="mermaid")
        mermaid = gen.serialize()
        self.assertNotIn("```", mermaid, "markdown header should not be present")
        self._in(PERSON, mermaid)
        self._in(PERSON2MEDICALEVENT, mermaid)
        self.assertNotIn("FakeClass", mermaid, "FakeClass should not be reachable from root")

    def test_serialize_exclude_attributes(self):
        """Test default serialization (structural), excluding attributes"""
        gen = ERDiagramGenerator(SCHEMA, exclude_attributes=True)
        mermaid = gen.serialize()
        self.assertNotIn("string", mermaid, "attributes should be excluded")
        self._in(PERSON2MEDICALEVENT, mermaid)
        self._in(FAMILIALRELATIONSHIP2PERSON, mermaid)

    def test_serialize_all(self):
        """Test serialization of all elements"""
        gen = ERDiagramGenerator(SCHEMA, structural=False)
        mermaid = gen.serialize()
        self._in(PERSON, mermaid)
        self._in(PERSON2MEDICALEVENT, mermaid)
        self.assertIn("FakeClass", mermaid, "FakeClass be included even if not reachable")

    def test_serialize_selected(self):
        """Test serialization of selected elements"""
        gen = ERDiagramGenerator(SCHEMA)
        mermaid = gen.serialize_classes(["FamilialRelationship"])
        self.assertNotIn("Person {", mermaid, "Person not reachable from selected")
        self._in(FAMILIALRELATIONSHIP2PERSON, mermaid, "dangling references should be included")

    def test_follow_references(self):
        """Test serialization of selected elements following non-inlined references"""
        gen = ERDiagramGenerator(SCHEMA)
        mermaid = gen.serialize_classes(["FamilialRelationship"], follow_references=True)
        self._in(PERSON, mermaid)
        self._in(FAMILIALRELATIONSHIP2PERSON, mermaid)

    def test_max_hops(self):
        """Test truncation at depth"""
        gen = ERDiagramGenerator(SCHEMA)
        mermaid = gen.serialize_classes(["Dataset"], max_hops=0)
        self.assertNotIn("Person {", mermaid, "Person not reachable from selected in zero hops")
        self._in(DATASET2PERSON, mermaid, "dangling references should be included")
        mermaid = gen.serialize_classes(["Dataset"], max_hops=1)
        self._in(PERSON, mermaid, "Person reachable from selected in one hop")
        self.assertNotIn("FamilialRelationship {", mermaid, "FamilialRelationship not reachable from selected in zero hops")

    def _in(self, s1, s2, message: str = None):
        self.assertIn(s1.replace(' ', ''), s2.replace(' ', ''), message)


if __name__ == "__main__":
    unittest.main()
