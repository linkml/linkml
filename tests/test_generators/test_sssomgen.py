import os
import unittest
from linkml.generators.sssomgen import SSSOMGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
OUTPUT_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "output/ks/sssom"
)
OUTPUT_FILENAME = "test_sssom.tsv"


class SSSOMGenTestCase(unittest.TestCase):
    def test_sssomgen(self):
        # generate SSSOM file
        SSSOMGenerator(
            SCHEMA, output=os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
        ).serialize()

        # Test if the generator actually created the output file
        self.assertTrue(
            os.path.exists(os.path.join(OUTPUT_DIR, OUTPUT_FILENAME))
        )

    def test_sssom_metadata(self):
        meta = {}
        curie_map = {}
        curie_flag = False
        with open(os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)) as sssom_file:
            for ln in sssom_file:
                if ln.startswith("#"):
                    if "curie_map" in ln:
                        curie_flag = True
                    if not curie_flag:
                        clean_ln_list = ln.lstrip("#").rstrip("\n").split(": ")
                        meta[clean_ln_list[0]] = clean_ln_list[1]
                    else:
                        if "curie_map" not in ln:
                            curie_ln = ln.lstrip("#").rstrip("\n").split(": ")
                            curie_map[curie_ln[0]] = curie_ln[1]

        self.assertEqual(len(meta), 5)
        self.assertEqual(len(curie_map), 16)


if __name__ == "__main__":
    unittest.main()
