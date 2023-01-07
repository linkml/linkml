import unittest
from collections import namedtuple

import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.utils.schema_builder import SchemaBuilder
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
DATA = env.input_path("kitchen_sink_inst_01.yaml")
PYDANTIC_OUT = env.expected_path("kitchen_sink_pydantic.py")
PACKAGE = "kitchen_sink"


class PydanticGeneratorTestCase(unittest.TestCase):
    """
    Tests generation of pydantic-style classes from LinkML schemas
    """

    def test_pydantic(self):
        """Generate pydantic classes"""
        gen = PydanticGenerator(SCHEMA, package=PACKAGE)
        code = gen.serialize()
        with open(PYDANTIC_OUT, "w") as stream:
            stream.write(code)
        with open(DATA) as stream:
            dataset_dict = yaml.safe_load(stream)
        # NOTE: compile_python and dynamic compilation in general does not seem to work
        # for pydantic code. As an alternative, we import the generated model within a function
        # that is called *after* the code is generated.
        # note for developers: you will lack IDE support in this section of the code
        def test_dynamic():
            from tests.test_generators.output.kitchen_sink_pydantic import (
                Dataset, EmploymentEvent, Person)

            # NOTE: generated pydantic doesn't yet do validation
            e1 = EmploymentEvent(is_current=True)
            p1 = Person(id="x", has_employment_history=[e1])
            print(p1)
            assert p1.id == "x"
            assert p1.name is None
            json = {"id": "P1", "has_employment_history": [{"is_current": True}]}
            p2 = Person(**json)
            print(p2)
            p2 = Person(**dataset_dict["persons"][0])
            ds1 = Dataset(**dataset_dict)
            print(ds1)
            assert len(ds1.persons) == 2

        test_dynamic()

    def test_compile_pydantic(self):
        """Generate and compile pydantic classes"""
        gen = PydanticGenerator(SCHEMA, package=PACKAGE)
        print(gen.allow_extra)
        code = gen.serialize()
        mod = compile_python(code, PACKAGE)
        p = mod.Person(id="P:1")
        assert p.id == "P:1"
        with self.assertRaises(ValidationError):
            mod.Person(no_such_field="x")
        with self.assertRaises(ValidationError):
            mod.Person(age_in_years="x")

    def test_pydantic_enums(self):

        unit_test_schema = """
id: unit_test
name: unit_test

prefixes:
  ex: https://example.org/
default_prefix: ex

enums:
  TestEnum:
    permissible_values:
      123:
      +:
      This & that, plus maybe a 🎩:
      Ohio:
"""

        sv = SchemaView(unit_test_schema)
        gen = PydanticGenerator(schema=unit_test_schema)
        enums = gen.generate_enums(sv.all_enums())
        assert enums
        enum = enums["TestEnum"]
        assert enum
        assert enum["values"]["number_123"] == "123"
        assert enum["values"]["PLUS_SIGN"] == "+"
        assert (
            enum["values"]["This_AMPERSAND_that_plus_maybe_a_TOP_HAT"]
            == "This & that, plus maybe a 🎩"
        )
        assert enum["values"]["Ohio"] == "Ohio"

    def test_pydantic_inlining(self):
        #Case = namedtuple("multivalued", "inlined", "inlined_as_list", "B_has_identities")
        expected_default_factories = {
            "Optional[List[str]]": "Field(default_factory=list)",
            "Optional[List[B]]": "Field(default_factory=list)",
            "Optional[Dict[str, B]]": "Field(default_factory=dict)",
        }
        cases = [
            # block 1: primitives are NEVER inlined
            ("T", True, False, False, True, "Optional[List[str]]",
             "primitives are never inlined"),
            # attempting to inline a type
            # TBD: does the spec actively forbid this
            ("T", True, True, True, True, "Optional[List[str]]",
             "primitives are never inlined, even if requested"),
            # block 2: referenced element is a class
            ("B", True, False, False, False, "Optional[List[B]]",
             "references to classes without identifiers ALWAYS inlined as list"),
            ("B", True, True, False, False, "Optional[List[B]]",
             "references to classes without identifiers ALWAYS inlined as list"),
            ("B", True, True, True, False, "Optional[List[B]]",
             "references to classes without identifiers ALWAYS inlined as list"),
            ("B", True, True, False, True, "Optional[Dict[str, B]]",
             "references to class with identifier inlined ONLY ON REQUEST, with dict as default"),
            # TODO: fix the next two
            ("B", True, True, True, True, "Optional[List[B]]",
             "references to class with identifier inlined as list ONLY ON REQUEST"),
            ("B", True, False, False, True, "Optional[List[str]]",
             ""),
        ]
        for range, multivalued, inlined, inlined_as_list, B_has_identifier, expected, notes in cases:
            sb = SchemaBuilder("test")
            sb.add_type("T", typeof="string")
            a2b = SlotDefinition("a2b",
                                 range=range,
                                 multivalued=multivalued,
                                 inlined=inlined,
                                 inlined_as_list=inlined_as_list)
            sb.add_class("A", slots=[a2b])
            b_id = SlotDefinition("id", identifier=B_has_identifier)
            sb.add_class("B", slots=[b_id, "name"])
            sb.add_defaults()
            schema = sb.schema
            schema_str = yaml_dumper.dumps(schema)
            gen = PydanticGenerator(schema_str, package=PACKAGE)
            code = gen.serialize()
            # print(code)
            lines = code.splitlines()
            ix = lines.index("class A(ConfiguredBaseModel):")
            self.assertGreater(ix, 0)
            # assume a single blank line separating
            slot_line = lines[ix + 2]
            self.assertIn(f"a2b: {expected}", slot_line)
            if expected not in expected_default_factories:
                raise ValueError(f"unexpected default factory for {expected}")
            self.assertIn(expected_default_factories[expected], slot_line)



if __name__ == "__main__":
    unittest.main()
