import unittest

import yaml
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition, ElementName

import linkml_runtime.utils.yamlutils as yutils
from linkml_runtime.utils.dictutils import as_simple_dict
from tests.support.test_environment import TestEnvironmentTestCase
from tests.test_utils.environment import env

def _signature(d):
    if isinstance(d, dict):
        for x in d.values():
            yield x
    elif isinstance(d, list):
        for x in d:
            yield x
    else:
        yield d

def _is_python_type(obj):
    t = type(obj)
    return t in [dict, list, str, int, float, type(None)] or isinstance(obj, ElementName)

def _is_basic_type(obj):
    return _is_python_type(obj) or isinstance(obj, ElementName)


class DictUtilTestCase(TestEnvironmentTestCase):
    env = env

    def test_as_dict(self):
        obj = ClassDefinition('test class')
        obj2 = ClassDefinition('test class', slot_usage={'foo': SlotDefinition(name='foo', range='bar')})
        #obj2.slot_usage = {'foo': SlotDefinition(name='foo', range='bar')}

        # as dict preserves nones and empty lists
        d = yutils.as_dict(obj)
        assert isinstance(d, dict)
        assert d['name'] == 'test class'
        assert d['id_prefixes'] == []
        assert d['description'] is None
        for x in _signature(d):
            if not _is_python_type(x):
                print(f'   ****={x} {type(x)}')
        assert all(_is_basic_type(x) for x in _signature(d))

        d2 = yutils.as_dict(obj2)
        print(d2)
        assert d2['slot_usage']['foo']['range'] == 'bar'
        assert all(_is_basic_type(x) for x in _signature(d2))

        # as_simple_dict removes nones and empty lists
        d = as_simple_dict(obj)
        print(d)
        assert isinstance(d, dict)
        assert all(_is_python_type(x) for x in _signature(d))
        assert d == {'name': 'test class'}

        d2 = as_simple_dict(obj2)
        print(d2)
        assert isinstance(d2, dict)
        assert d2 == {'name': 'test class', 'slot_usage': {'foo': {'name': 'foo', 'range': 'bar'}}}

        s = yutils.as_yaml(obj)
        print(s)
        assert(s.strip() == 'name: test class')

        s2 = yutils.as_yaml(obj2)
        print(s2)
        assert(s2.strip().startswith('name: test class'))





if __name__ == '__main__':
    unittest.main()
