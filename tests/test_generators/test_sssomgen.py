import os
import unittest
from linkml.generators.sssomgen import SSSOMGenerator
from tests.test_generators.environment import env
import yaml

SCHEMA = env.input_path("kitchen_sink_sssom.yaml")
OUTPUT_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "output/ks/sssom"
)
OUTPUT_FILENAME = "test_sssom.tsv"

# generate SSSOM file
SSSOMGenerator(
    SCHEMA, output=os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
).serialize()


class SSSOMGenTestCase(unittest.TestCase):
    def test_sssomgen(self):
        # Test if the generator actually created the output file
        self.assertTrue(
            os.path.exists(os.path.join(OUTPUT_DIR, OUTPUT_FILENAME))
        )

    def test_sssom_metadata(self):
        meta = {}
        curie_map = {}
        curie_flag = False
        msdf_as_dict = {}

        # Read Input file
        with open(SCHEMA, "r") as input_yaml:
            try:
                input_data = yaml.safe_load(input_yaml)
            except yaml.YAMLError as exc:
                print(exc)

        # Read output files
        output_file = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
        with open(output_file) as sssom_file:
            row_count = -1
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
                else:
                    # This is the MappingSetDataFrame
                    row_count += 1
                    ln = ln.split("\t")
                    ln[-1] = ln[-1].strip()

                    if row_count == 0:
                        msdf_columns = ln
                        for col in msdf_columns:
                            msdf_as_dict[col] = []
                    else:
                        for idx, value in enumerate(msdf_columns):
                            msdf_as_dict[value].append(ln[idx])

        # Assertions
        self.assertEqual(len(meta), 5)
        self.assertEqual(len(curie_map), len(input_data["prefixes"]))
        self.assertFalse(" " in msdf_as_dict["subject_id"])


if __name__ == "__main__":
    unittest.main()
