from __future__ import annotations

from types import ModuleType

import pytest

from linkml_runtime.utils.compile_python import compile_python


@pytest.fixture(scope="module")
def base_module() -> str:
    return """
x: int = 2

def fun(value: int):
    return f'known value {value}'
"""


@pytest.fixture(scope="module")
def importing_module() -> str:
    return """
import MODULE_NAME as m

def more_fun(message: str):
    return f'got "{message}"'
"""


def check_generated_module(module: ModuleType, module_name: str) -> None:
    assert isinstance(module, ModuleType)
    assert module.__name__ == module_name
    assert module.x == 2
    assert module.fun(3) == "known value 3"


@pytest.mark.parametrize(("name_arg", "module_name"), [(None, "test"), ("", "test"), ("base_module", "base_module")])
def test_compile_python_module_name(base_module: str, name_arg: str | None, module_name: str) -> None:
    """Test the compilation of python code to create a module."""
    m = compile_python(base_module, module_name=name_arg)
    check_generated_module(m, module_name)


@pytest.mark.parametrize(("name_arg", "module_name"), [(None, "test"), ("", "test"), ("base_module", "base_module")])
def test_compile_python_importing_module_local_module(
    base_module: str,
    importing_module: str,
    name_arg: str | None,
    module_name: str,
) -> None:
    """Test the compilation of python code to create a local module and then compile a second module that imports the first."""
    m = compile_python(base_module, module_name=name_arg)
    check_generated_module(m, module_name)

    # switch in the appropriate module name
    importing_module_text = importing_module.replace("MODULE_NAME", module_name)
    m2 = compile_python(importing_module_text, package_path=".", module_name="module_2")
    assert isinstance(m2, ModuleType)
    assert m2.__name__ == "module_2"
    assert m2.more_fun("hello") == 'got "hello"'

    # check the imported module, m2.m, has the correct type, name, etc.
    check_generated_module(m2.m, module_name)
