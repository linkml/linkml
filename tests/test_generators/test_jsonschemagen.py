import json
import unittest

import yaml
from linkml_runtime.dumpers import json_dumper, rdf_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.validation import validate_object
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path("kitchen_sink.yaml")
JSONSCHEMA_OUT = env.expected_path("kitchen_sink.schema.json")
PYTHON = env.expected_path("kitchen_sink.py")
DATA = env.input_path("kitchen_sink_inst_01.yaml")
FAILDATA = env.input_path("kitchen_sink_failtest_inst_01.yaml")
DATA_JSON = env.expected_path("kitchen_sink_inst_01.json")
DATA_RDF = env.expected_path("kitchen_sink_inst_01.rdf")
FAILLOG = env.expected_path("kitchen_sink_failtest_log.txt")


class JsonSchemaTestCase(unittest.TestCase):
    """
    Tests generation of JSON-Schema
    """

    def test_jsonschema(self):
        """json schema"""
        kitchen_module = make_python(False)
        inst: Dataset
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
        # p = [p for p in persons if p.id == 'P:002'][0]
        ok_address = False
        ok_history = False
        ok_metadata = True
        for p in inst.persons:
            for a in p.addresses:
                print(f"{p.id} address = {a.street}")
                if a.street.startswith("1 foo"):
                    ok_address = True
            for h in p.has_medical_history:
                print(f"{p.id} history = {h}")
                if h.in_location == "GEO:1234" and h.diagnosis.name == "headache":
                    ok_history = True
                # test the metadata slot, which has an unconstrained range
                if h.metadata:
                    if h.metadata.anything.goes:
                        ok_metadata = True
        assert ok_address
        assert ok_history
        json_dumper.dump(element=inst, to_file=DATA_JSON)
        gen = JsonSchemaGenerator(SCHEMA, mergeimports=True, top_class="Dataset")
        jsonschemastr = gen.serialize()
        with open(JSONSCHEMA_OUT, "w") as io:
            io.write(jsonschemastr)
        validate_object(inst, SCHEMA, closed=True)

        # test for https://github.com/linkml/linkml/issues/579
        jso = json.loads(jsonschemastr)
        assert "$defs" in jso
        any_obj = jso["$defs"]["AnyObject"]
        assert any_obj["additionalProperties"]

        # test for expected failures
        # FAILDATA contains a set of json objects each of which
        # violates the schema in some way
        with open(FAILDATA, "r") as io:
            failobjs = yaml.load(io, Loader=yaml.loader.SafeLoader)

        with open(FAILLOG, "w") as log:
            for failobj in failobjs:
                dataset = failobj["dataset"]
                is_skip = failobj.get("skip", False)
                expected_to_be_valid = failobj.get("valid", False)
                closed = failobj.get("closed", True)
                log.write("-" * 20)
                log.write(f"\n{failobj['description']}:\n")
                log.write(f"\n{failobj['dataset']}:\n")
                if not is_skip:
                    # with self.assertRaises(Exception) as e:
                    #    jsonschema.validate(dataset, schema=jsonschema_obj)
                    validated = False
                    try:
                        validate_object(
                            dataset,
                            SCHEMA,
                            target_class=kitchen_module.Dataset,
                            closed=closed,
                        )
                        validated = True
                        log.write(
                            f"No Exception (expected={expected_to_be_valid}: {failobj}"
                        )
                    except Exception as e:
                        validated = False
                        log.write(
                            f"\nvException (expected={expected_to_be_valid}: {type(e)}:\n\t{e}\n\n"
                        )
                    if expected_to_be_valid:
                        assert validated
                    else:
                        assert not validated
                else:
                    log.write(" SKIPPED\n")


if __name__ == "__main__":
    unittest.main()
