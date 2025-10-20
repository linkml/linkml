import logging
import os
import sys
from types import ModuleType

logger = logging.getLogger(__file__)


def _file_text(txt_or_fname: str) -> str:
    """
    Determine whether text_or_fname is a file name or a string and, if a file name, read it
    :param txt_or_fname:
    :return:
    """
    if len(txt_or_fname) > 4 and "\n" not in txt_or_fname:
        with open(txt_or_fname) as ef:
            return ef.read()
    return txt_or_fname


def compile_python(text_or_fn: str, package_path: str = None, module_name: None = None) -> ModuleType:
    """
    Compile the text or file and return the resulting module
    @param text_or_fn: Python text or file name that references python file
    @param package_path: Root package path.  If omitted and we've got a python file,
    the package is the containing directory
    @param module_name: to be used in an import statement, default 'test'
    @return: Compiled module
    """
    logging.warning("compile_python is deprecated - use linkml_runtime.utils.compile_python instead")
    if module_name is None:
        module_name = "test"
    python_txt = _file_text(text_or_fn)
    if package_path is None and python_txt != text_or_fn:
        package_path = text_or_fn
    spec = compile(python_txt, module_name, "exec")
    module = ModuleType(module_name)
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
            path_from_tests_parent = os.path.relpath(package_path, os.path.join(os.getcwd(), ".."))
        module.__package__ = os.path.dirname(os.path.relpath(path_from_tests_parent, os.getcwd())).replace(
            os.path.sep, "."
        )
    sys.modules[module.__name__] = module
    exec(spec, module.__dict__)
    return module
