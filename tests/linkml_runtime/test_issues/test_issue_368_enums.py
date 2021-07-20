import unittest
from typing import Callable

from linkml_runtime.dumpers import json_dumper, yaml_dumper, rdf_dumper
from tests.test_issues.environment import env
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from linkml_runtime.utils.compile_python import compile_python


class Issue368TestCase(LoaderDumperTestCase):
    env = env

    def header(self, txt: str) -> str:
        return '\n' + ("=" * 20) + f" {txt} " + ("=" * 20)

    def test_issue_368_enums(self):
        """ Test Enum generation """

        module = compile_python(env.input_path('issue_368.py'))

        enum_inst = module.SampleEnum("pva") # EnumInstanceImpl
        example = module.SampleClass(slot_1="pva")
        assert hasattr(example, "slot_1")
        assert example.slot_1.code.text == enum_inst.code.text
        assert str(example.slot_1) == "pva"

        def dump_and_load(dumper: Callable, sfx: str) -> None:
            fname = env.actual_path(f'issue_368_1.{sfx}')
            dumper(example, fname)
            with open(fname) as f:
                print(f'\n----- {sfx} -----')
                print(f.read())

        dump_and_load(json_dumper.dump, 'json')
        dump_and_load(yaml_dumper.dump, 'yaml')
        dump_and_load(lambda obj, fname: rdf_dumper.dump(obj, fname, env.input_path("issue_368.context.jsonld")), 'ttl')


if __name__ == '__main__':
    unittest.main()
