import pytest

from linkml_runtime.utils.compile_python import compile_python


@pytest.fixture
def module_1():
    return """
x: int = 2

def fun(value: int):
    return f'known value {value}'
"""


@pytest.fixture
def module_2():
    return """
import module_1 as m

def more_fun(message: str):
    return f'got "{message}"'
"""


def test_compile(module_1, module_2):
    m1 = compile_python(module_1, module_name="module_1")
    assert m1.__name__ == "module_1"
    assert m1.x == 2
    assert m1.fun(3) == "known value 3"
    m2 = compile_python(module_2, module_name="module_2", package_path=".")
    assert m2.__name__ == "module_2"
    assert m2.more_fun("hello") == 'got "hello"'
    assert m2.m.fun(4) == "known value 4"
    assert m2.m.x == 2


def test_default_module_name(module_1):
    m = compile_python(module_1)
    assert m.__name__ == "test"
