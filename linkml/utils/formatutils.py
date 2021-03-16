import re
from typing import List

from pyshex.shex_evaluator import EvaluationResult

ws_pattern = re.compile(r'\s+')
us_pattern = re.compile(r'_+')


def camelcase(txt: str) -> str:
    def _up(s: str):
        return s[0].upper() + (s[1:] if len(s) > 1 else '')

    return ''.join([_up(word) for word in us_pattern.sub(' ', txt.strip().replace(',', '')).split()])


def underscore(txt: str) -> str:
    return ws_pattern.sub('_', txt.strip()).replace(',', '')


def lcamelcase(txt: str) -> str:
    s = camelcase(txt)
    return s[0].lower() + s[1:]


def be(entry: object) -> str:
    """ Return a stringified version of object replacing Nones with empty strings """
    return str(entry).strip() if entry else ''


def mangled_attribute_name(clsname: str, attributename: str) -> str:
    """ Return the mangling we use for attributes definitions """
    return lcamelcase(clsname) + '__' + underscore(attributename)


split_col = 115


def sfx(uri: str) -> str:
    """
    Add a separator to a uri if none exists.

    Note: This should only be used with module id's -- it is not uncommon to use partial prefixes,
    e.g. PREFIX bfo: http://purl.obolibrary.org/obo/BFO_
    :param uri: uri to be suffixed
    :return: URI with suffix
    """
    return str(uri) + ('' if uri.endswith(('/', '#', '_', ':')) else '/')


def uri_for(prefix: str, suffix: str) -> str:
    """ Generator for predicate and identifier URI's """
    if ':' in prefix:
        return sfx(prefix) + suffix
    else:
        return prefix + ':' + suffix


def split_line(txt: str, split_len: int = split_col) -> List[str]:
    # TODO: consider replacing by textwrap.fill function, but note that its behavior is a bit different
    out_lines = []
    words = txt.split()
    cur_line = ""
    for word in words:
        word += ' '
        if len(cur_line) + len(word) > split_len:
            out_lines.append(cur_line if cur_line else word)
            if not cur_line:
                word = ""
            else:
                cur_line = ""
        cur_line += word
    if cur_line:
        out_lines.append(cur_line)
    return out_lines


def wrapped_annotation(txt: str) -> str:
    rval = []
    for line in [l.strip() for l in txt.split('\n')]:
        if len(line) > split_col:
            rval += split_line(line)
        else:
            rval.append(line)
    return '\n\t'.join(rval)


def shex_results_as_string(rslts: EvaluationResult) -> str:
    """ Pretty print ShEx Evaluation result """
    # TODO: Add this method to ShEx itself
    rval = [f"Evalutating: {str(rslts.focus)} against {str(rslts.start)}"]
    if rslts.result:
        rval.append("Result: CONFORMS")
    else:
        rval.append("Result: NonConforming")
    rval += rslts.reason.split('\n')
    return '\n'.join(rval)
