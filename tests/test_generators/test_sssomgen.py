import os

import pytest
import yaml

from linkml.generators.sssomgen import SSSOMGenerator


@pytest.fixture
def schema_path(input_path) -> str:
    return str(input_path("kitchen_sink_sssom.yaml"))


@pytest.fixture
def sssom_path(schema_path, tmp_path) -> str:
    output_path = str(tmp_path / "test_sssom.tsv")
    gen = SSSOMGenerator(schema_path, output=output_path)
    gen.serialize()
    return output_path


def test_sssomgen(sssom_path):
    # Test if the generator actually created the output file
    assert os.path.exists(sssom_path)


def test_sssom_metadata(schema_path, sssom_path):
    meta = {}
    curie_map = {}
    curie_flag = False
    msdf_as_dict = {}

    # Read Input file
    with open(schema_path) as input_yaml:
        try:
            input_data = yaml.safe_load(input_yaml)
        except yaml.YAMLError as exc:
            print(exc)

    # Read output files

    with open(sssom_path) as sssom_file:
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
    assert len(meta) == 5
    assert len(curie_map) == len(input_data["prefixes"])
    assert " " not in msdf_as_dict["subject_id"]
