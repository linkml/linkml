import unittest
from typing import Callable

from linkml_runtime.dumpers import json_dumper, yaml_dumper, rdf_dumper
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.filters import ldcontext_metadata_filter
from tests.utils.python_comparator import compare_python
from linkml_runtime.utils.compile_python import compile_python
from tests.utils.loaderdumpertestcase import LoaderDumperTestCase


@unittest.skip("Need to get the correct pyld installed for this to rune")
class Issue368TestCase(LoaderDumperTestCase):
    env = env

    def header(self, txt: str) -> str:
        return '\n' + ("=" * 20) + f" {txt} " + ("=" * 20)

    def test_issue_368(self):
        """ Make sure that types are generated as part of the output """
        env.generate_single_file('issue_368_imports.py',
                                lambda: PythonGenerator(env.input_path('issue_368_imports.yaml'),
                                                     mergeimports=False).serialize(),
                                comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_368_imports.py')),
                                value_is_returned=True)
        env.generate_single_file('issue_368.py',
                                 lambda: PythonGenerator(env.input_path('issue_368.yaml'),
                                                         mergeimports=False).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_368.py')),
                                 value_is_returned=True)

        with open(env.expected_path('issue_368.py')) as f:
            python= f.read()

        has_imports = False
        for line in python.split("\n"):
            if line.startswith("from . issue_368_imports"):
                imps = line.replace("from . issue_368_imports import ","").split(", ")
                assert 'SampleEnum' in imps
                assert 'ParentClass' in imps
                has_imports = True
        assert has_imports
        module = compile_python(env.expected_path('issue_368.py'))

        enum_inst = module.SampleEnum("pva") # EnumInstanceImpl
        example = module.SampleClass(slot_1="pva")
        assert hasattr(example, "slot_1")
        assert example.slot_1.code.text == enum_inst.code.text
        assert str(example.slot_1) == "pva: PVA description"

        def dump_and_load(dumper: Callable, sfx: str) -> None:
            fname = env.actual_path(f'issue_368_1.{sfx}')
            dumper(example, fname)
            with open(fname) as f:
                print(f'\n----- {sfx} -----')
                print(f.read())

        dump_and_load(json_dumper.dump, 'json')
        dump_and_load(yaml_dumper.dump, 'yaml')

        env.generate_single_file('issue_368.context.jsonld',
                                 lambda: ContextGenerator(env.input_path('issue_368.yaml'),
                                                          emit_metadata=False).serialize(),
                                 filtr=ldcontext_metadata_filter,
                                 value_is_returned=True)
        dump_and_load(lambda obj, fname: rdf_dumper.dump(obj, fname, env.expected_path("issue_368.context.jsonld")), 'ttl')


if __name__ == '__main__':
    unittest.main()
