"""Data test."""
import unittest

from linkml_runtime import SchemaView
from prefixmaps.io.parser import load_multi_context

from linkml.workspaces.example_runner import ExampleRunner
from tests.test_workspaces.environment import env

INPUT_EXAMPLES_PATH = env.input_path("examples")
COUNTER_EXAMPLES_PATH = env.input_path("counter_examples")
SCHEMA = env.input_path("personinfo.yaml")


class TestExampleRunner(unittest.TestCase):
    """Test example runner using a simulated setup.

     - input/personinfo.yaml
     - input/examples
     - input/counter_examples
    ."""

    def setUp(self) -> None:
        schemaview = SchemaView(str(SCHEMA))
        ctxt = load_multi_context(["obo", "linked_data", "prefixcc"])
        self.example_runner = ExampleRunner(schemaview=schemaview,
                                            input_directory=INPUT_EXAMPLES_PATH,
                                            counter_example_input_directory=COUNTER_EXAMPLES_PATH,
                                            output_directory=env.outdir,
                                            prefix_map=ctxt.as_dict())

    def test_load_from_dict(self):
        """test loading from a dict object, including using type designators."""
        er = self.example_runner
        obj = er._load_from_dict(
            {"persons": [
                {'id': 'p1', 'name': 'John'}
            ]})
        print(obj)

    def test_example_runner(self):
        """Example runner test."""
        er = self.example_runner
        er.process_examples()

