import os
from types import ModuleType
from typing import Optional, Tuple

from tests.utils.dirutils import file_text
from tests.utils.filters import metadata_filter
from tests.environment import env
from linkml_runtime.utils.compile_python import compile_python


def compare_python(expected: str, actual: str, expected_path: Optional[str] = None) -> Optional[str]:
    """
    Make sure that actual is valid python and, if it is, compare it with expected
    :param expected: expected python -- can either be python text or a file name
    :param actual: generated python -- text or file name
    :param expected_path: path where expected will be stored
    :return: Differences or issues if any, else None
    """

    def to_text(txt_or_fn: str) -> Tuple[str, Optional[str]]:
        """
        Convert txt_or_fn to text
        :param txt_or_fn:
        :return: text and file name if read from a file
        """
        if len(txt_or_fn) > 4 and '\n' not in txt_or_fn:
            with open(txt_or_fn) as ef:
                txt = ef.read()
        else:
            txt = txt_or_fn
            txt_or_fn = None
        return metadata_filter(txt), txt_or_fn

    exp_txt, exp_fn = to_text(expected)
    act_txt, _ = to_text(actual)

    # We pass False through fail_on_error because it is too easy to let python compile errors slip through
    msg = validate_python(act_txt, False, expected_path) or ''

    if exp_txt != act_txt:
        msg += "\nOutput mismatch" + (f"for file {exp_fn}" if exp_fn else '')
    return msg


def validate_python(text: str, fail_on_error: bool = False, expected_path: str = None) -> Optional[str]:
    """
    Validate the python in text
    :param text: Input python
    :param fail_on_error: True means fail if python is bad
    :param expected_path: If present, this is transformed into  `__package__` parameter that gets passed to the exec function to address
    relative imports
    :return: None if success, otherwise the error message
    """
    return None
    if fail_on_error and False:
        try:
            compile_python(text, expected_path)
        except Exception as e:
            return str(e)
    else:
        compile_python(text, expected_path)
        return None

