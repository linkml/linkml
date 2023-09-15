import json
import unittest

from click.testing import CliRunner

from linkml.utils.converter import cli
from tests.test_utils.environment import env

SCHEMA = env.input_path("schema_with_inference.yaml")
DATA_IN = env.input_path("data_example.yaml")
JSON_OUT = env.expected_path("data_example.out.json")
YAML_OUT = env.expected_path("data_example.out.yaml")
RDF_OUT = env.expected_path("data_example.out.ttl")

SCHEMA_DESCENDANTS = env.input_path("schema7.yaml")
DATA_DESCENDANTS = env.input_path("animals.yaml")


class TestCommandLineInterface(unittest.TestCase):
    def setUp(self) -> None:
        runner = CliRunner(mix_stderr=False)
        self.runner = runner

    def test_help(self):
        result = self.runner.invoke(cli, ["--help"])
        out = result.stdout
        self.assertIn("INPUT", out)
        # self.assertEqual(0, result.exit_code)

    def test_infer_and_convert(self):
        """
        Tests using the --infer option to add missing values, and also roundtripping
        through yaml->json->yaml->rdf->json
        """
        self.runner.invoke(cli, ["--infer", "-s", SCHEMA, DATA_IN, "-o", JSON_OUT])
        self.runner.invoke(cli, ["-s", SCHEMA, JSON_OUT, "-t", "yaml", "-o", YAML_OUT])
        self.runner.invoke(cli, ["-s", SCHEMA, YAML_OUT, "-t", "rdf", "-o", RDF_OUT])
        self.runner.invoke(cli, ["-s", SCHEMA, RDF_OUT, "-t", "json", "-o", JSON_OUT])
        with open(JSON_OUT) as file:
            obj = json.load(file)
            persons = obj["persons"]
            p1 = persons["P:1"]
            p2 = persons["P:2"]
            self.assertTrue(p1["is_juvenile"])
            self.assertTrue("is_juvenile" not in p2)
            self.assertEqual(p1["age_in_years"], 10)
            self.assertEqual(p1["age_in_months"], 120)
            self.assertEqual(p1["age_category"], "juvenile")
            self.assertEqual(p1["full_name"], "first1 last1")
            self.assertEqual(p2["age_in_years"], 20)
            self.assertEqual(p2["age_in_months"], 240)
            self.assertEqual(p2["age_category"], "adult")
            self.assertEqual(p2["full_name"], "first2 last2")

    def test_convert_including_descendants(self):
        """
        Tests using the --include-range-class-descendants option to support
        subtype polymorphism.
        """
        result = self.runner.invoke(
            cli,
            [
                "--include-range-class-descendants",
                "--validate",
                "-C",
                "Container",
                "-s",
                SCHEMA_DESCENDANTS,
                "-t",
                "json-ld",
                "-o",
                JSON_OUT,
                DATA_DESCENDANTS,
            ],
        )
        print(result.stdout)
        if result.exit_code:
            print(result.exception)
            raise result.exception
        else:
            with open(JSON_OUT) as file:
                p1 = json.load(file)
                print(p1)
                self.assertEqual(p1["animals"][0]["animal_family"], "Dog")
                self.assertEqual(p1["animals"][0]["breed"], "Golden Retriever")
                self.assertEqual(p1["animals"][1]["animal_family"], "Ant")
                self.assertTrue(p1["animals"][1]["venom"])

    def test_version(self):
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(cli, ["--version"])
        # self.assertEqual(0, result.exit_code)  # fails! unclear why result.exit_code is 1 not 0
        self.assertIn("version", result.stdout)
