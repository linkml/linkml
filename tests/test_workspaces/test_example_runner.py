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
        self.schemaview = schemaview
        ctxt = load_multi_context(["obo", "linked_data", "prefixcc"])
        self.ctxt = ctxt
        self.example_runner = self.get_example_runner()

    def get_example_runner(self) -> ExampleRunner:
        """Get an example runner."""
        return ExampleRunner(schemaview=self.schemaview,
                      input_directory=INPUT_EXAMPLES_PATH,
                      counter_example_input_directory=COUNTER_EXAMPLES_PATH,
                      output_directory=env.outdir,
                      prefix_map=self.ctxt.as_dict())

    def test_load_from_dict(self):
        """test loading from a dict object, including using type designators."""
        er = self.example_runner
        obj = er._load_from_dict(
            {"persons": [
                {'id': 'p1', 'name': 'John'}
            ]})
        print(obj)

    def test_example_runner(self):
        """Process all YAML examples in input folder."""
        er = self.example_runner
        er.process_examples()
        md = str(er.summary)
        self.assertIn("Container-001", er.summary.inputs)
        self.assertIn("Container-001.yaml", er.summary.outputs)
        self.assertIn("Container-001.json", er.summary.outputs)
        self.assertIn("Container-001.ttl", er.summary.outputs)
        self.assertIn("Container-001", md)
        self.assertNotIn("Container-002", md)

    def test_example_runner_non_defaults(self):
        """
        Process all JSON examples in input folder,
        using only ttl writing.
        :return:
        """
        er = self.get_example_runner()
        er.input_formats = ['json']
        er.output_formats = ['ttl']
        er.process_examples()
        md = str(er.summary)
        self.assertIn("Container-002", er.summary.inputs)
        self.assertNotIn("Container-002.yaml", er.summary.outputs)
        self.assertNotIn("Container-002.json", er.summary.outputs)
        self.assertIn("Container-002.ttl", er.summary.outputs)
        self.assertNotIn("Container-001", md)
        self.assertIn("Container-002", md)



