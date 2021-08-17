import os
import sys
from logging import warning
from types import ModuleType


def file_text(txt_or_fname: str) -> str:
    """
    Determine whether text_or_fname is a file name or a string and, if a file name, read it
    :param txt_or_fname:
    :return:
    """
    if len(txt_or_fname) > 4 and '\n' not in txt_or_fname:
        with open(txt_or_fname) as ef:
            return ef.read()
    return txt_or_fname


def compile_python(text_or_fn: str, package_path: str = None) -> ModuleType:
    """
    Compile the text or file and return the resulting module
    @param text_or_fn: Python text or file name that references python file
    @param package_path: Root package path.  If omitted and we've got a python file, the package is the containing
    directory
    @return: Compiled module
    """
    python_txt = file_text(text_or_fn)
    if package_path is None and python_txt != text_or_fn:
        package_path = text_or_fn
    spec = compile(python_txt, 'test', 'exec')
    module = ModuleType('test')
    if package_path:
        package_path_abs = os.path.join(os.getcwd(), package_path)
        # We have to calculate the path to expected path relative to the current working directory
        for path in sys.path:
            if package_path.startswith(path):
                path_from_tests_parent = os.path.relpath(package_path, path)
                break
            if package_path_abs.startswith(path):
                path_from_tests_parent = os.path.relpath(package_path_abs, path)
                break
        else:
            warning(f"There is no established path to {package_path} - compile_python may or may not work")
            path_from_tests_parent = os.path.relpath(package_path, os.path.join(os.getcwd(), '..'))
        module.__package__ = os.path.dirname(os.path.relpath(path_from_tests_parent, os.getcwd())).replace('/', '.')
    exec(spec, module.__dict__)
    return module
