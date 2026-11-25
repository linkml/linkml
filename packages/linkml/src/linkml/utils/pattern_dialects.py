"""Translate LinkML patterns into the regular-expression dialects of the formats LinkML generates.

A LinkML ``pattern`` is a Python regular expression, and a value conforms where Python's
``re.search`` finds it, as LinkML's validators read it. Generated formats read a pattern in
their own dialect:

- XML Schema regular expressions (``xsd:pattern``, which OWL 2 uses for string facets) match
  the whole value; ``^`` and ``$`` are ordinary characters, and ``.``, ``\\s`` and ``\\w``
  cover other characters than in Python (XML Schema 1.1 Part 2, Appendix G).
  :func:`regex_as_xsd` translates a pattern into this dialect.
- XPath regular expressions (``fn:matches``, which SPARQL's ``REGEX`` and SHACL's
  ``sh:pattern`` use) are searched in the value as in Python, with ``^`` and ``$`` as anchors,
  but with XML Schema's character classes, and ``$`` does not match before a final line feed
  (XPath and XQuery Functions and Operators 3.1, §5.6.1). Python-based SHACL engines such as
  pyshacl compile ``sh:pattern`` with Python's ``re``, which has no ``\\p{...}``.
  :func:`regex_for_xpath` therefore rewrites only what both dialects can read alike.
"""

import re
import sys
import unicodedata
from dataclasses import dataclass
from functools import cache

# Python's \s and \w over the characters XML allows, as the inside of a class: the XML
# Schema \s is only tab, line feed, carriage return and space, and the XML Schema \w
# excludes "_" and includes symbols. U+0085 has no escape, so it stands as itself.
_CLASS_ESCAPES = {"s": "\\s\\p{Z}\x85", "w": r"\p{L}\p{N}_"}
# Python's "." also matches a carriage return. The XML Schema "." matches neither a
# carriage return nor a line feed, so any characters are spelled out, rather than as
# [\s\S], which reasoners that read a pattern as a dk.brics automaton misread.
_DOT = r"(.|\r)"
_ANY = r"(.|\n|\r)*"
# Python's "$" also matches before a line feed that ends the value.
_END = r"\n?"
# Python reads only ASCII digits in a quantifier.
_REPEAT = re.compile(r"\{([0-9]*)(?:(,)([0-9]*))?\}")
# The characters a range of a class is split around, in code point order, with their escapes
_RANGE_SPLITS = {"\t": r"\t", "\n": r"\n", "\r": r"\r"} | {char: "\\" + char for char in "-[\\]^"}


def _is_xml_char(char: str) -> bool:
    """Whether XML 1.0 allows the character (production [2] Char)."""
    return char in "\t\n\r" or " " <= char <= "퟿" or "" <= char <= "�" or char >= "\U00010000"


def _ranges(chars: list[str]) -> str:
    """Write sorted characters as the inside of a class, consecutive ones as a range."""
    parts: list[str] = []
    start = prev = None
    for char in chars + [None]:
        if prev is not None and (char is None or ord(char) != ord(prev) + 1):
            parts.append(start if start == prev else f"{start}-{prev}")
            start = None
        if start is None:
            start = char
        prev = char
    return "".join(parts)


@cache
def _xpath_space() -> str:
    """Python's ``\\s`` as the inside of a class that Python and XPath read alike.

    That is ``\\s`` and the XML characters that Python's ``\\s`` matches (``str.isspace``)
    and the XPath ``\\s`` does not, as the XPath ``\\s`` is only space, tab, line feed and
    carriage return. They are written as themselves, as XPath has no escapes for them.
    """
    extra = [c for c in map(chr, range(sys.maxunicode + 1)) if c.isspace() and c not in " \t\n\r" and _is_xml_char(c)]
    return "\\s" + _ranges(extra)


@dataclass(frozen=True)
class _Token:
    """A token of a Python regular expression.

    ``kind`` is one of ``char``, ``escape`` (``value`` is the escaped character), ``class``
    (``items`` are the class's items and ``value`` its text), ``open`` (``value`` is ``""``
    for a group, ``":"`` for a non-capturing group and ``"?"`` for another extension),
    ``close``, ``alt``, ``start``, ``end``, ``dot`` and ``quant`` (``value`` is the
    quantifier with an omitted lower bound written as 0).
    """

    kind: str
    value: str = ""
    items: tuple = ()
    negated: bool = False
    lazy: bool = False
    possessive: bool = False


def _escaped_char(pattern: str, pos: int) -> tuple[str, int] | None:
    """Return the character that the escape ``\\x``, ``\\u``, ``\\U`` or ``\\N{...}`` at ``pattern[pos]`` stands for.

    ``pos`` is the position of the letter after the backslash. Return None for another escape.
    """
    letter = pattern[pos]
    if letter in "xuU":
        width = {"x": 2, "u": 4, "U": 8}[letter]
        return chr(int(pattern[pos + 1 : pos + 1 + width], 16)), pos + 1 + width
    if letter == "N":
        end = pattern.index("}", pos)
        return unicodedata.lookup(pattern[pos + 2 : end]), end + 1
    return None


def _class_item(pattern: str, pos: int) -> tuple[tuple[str, str], int]:
    """Read the character or escape of a class at ``pattern[pos]``."""
    if pattern[pos] == "\\":
        if (escaped := _escaped_char(pattern, pos + 1)) is not None:
            return ("char", escaped[0]), escaped[1]
        return ("escape", pattern[pos + 1]), pos + 2
    return ("char", pattern[pos]), pos + 1


def _class_token(pattern: str, pos: int) -> tuple[_Token, int]:
    """Split the character class whose "[" precedes ``pattern[pos]`` into its items."""
    begin = pos - 1
    negated = pattern.startswith("^", pos)
    pos += negated
    first = pos
    items: list[tuple] = []
    # Python reads a "]" right after "[" or "[^" as a literal.
    while pattern[pos] != "]" or pos == first:
        low, pos = _class_item(pattern, pos)
        if pattern[pos] == "-" and pattern[pos + 1] != "]" and low not in (("escape", "S"), ("escape", "W")):
            high, pos = _class_item(pattern, pos + 1)
            items.append(("range", low, high))
        else:
            items.append(low)
    return _Token("class", pattern[begin : pos + 1], tuple(items), negated), pos + 1


def _quantifier_token(pattern: str, pos: int) -> tuple[_Token, int]:
    """Read the quantifier at ``pattern[pos]``, or a "{" that Python reads as a literal."""
    if pattern[pos] == "{":
        match = _REPEAT.match(pattern, pos)
        if match is None or match.group() == "{}":
            return _Token("char", "{"), pos + 1
        low, comma, high = match.groups()
        value, pos = f"{{{low or 0}{comma or ''}{high or ''}}}", match.end()
    else:
        value, pos = pattern[pos], pos + 1
    possessive = pattern.startswith("+", pos)
    lazy = not possessive and pattern.startswith("?", pos)
    return _Token("quant", value, lazy=lazy, possessive=possessive), pos + (possessive or lazy)


def _tokens(pattern: str) -> list[_Token]:
    """Split a Python regular expression that compiles into its tokens."""
    tokens: list[_Token] = []
    pos = 0
    while pos < len(pattern):
        char = pattern[pos]
        pos += 1
        if char == "\\":
            if (escaped := _escaped_char(pattern, pos)) is not None:
                tokens.append(_Token("char", escaped[0]))
                pos = escaped[1]
            else:
                tokens.append(_Token("escape", pattern[pos]))
                pos += 1
        elif char == "[":
            token, pos = _class_token(pattern, pos)
            tokens.append(token)
        elif char == "(" and pattern.startswith("?#", pos):
            # a comment
            pos = pattern.index(")", pos) + 1
        elif char == "(" and pattern.startswith("?P<", pos):
            # a named group is a group; a backreference to it makes the pattern untranslatable
            pos = pattern.index(">", pos) + 1
            tokens.append(_Token("open", ""))
        elif char == "(":
            extension = ":" if pattern.startswith("?:", pos) else "?" if pattern.startswith("?", pos) else ""
            pos += len(extension) + (extension == ":")
            tokens.append(_Token("open", extension))
        elif char in "*+?{":
            token, pos = _quantifier_token(pattern, pos - 1)
            tokens.append(token)
        else:
            kind = {")": "close", "|": "alt", "^": "start", "$": "end", ".": "dot"}.get(char, "char")
            tokens.append(_Token(kind, char))
    return tokens


def _is_regex(pattern: str) -> bool:
    """Whether Python compiles *pattern*; LinkML's validators cannot use a pattern it does not."""
    try:
        re.compile(pattern)
    except (re.error, OverflowError, RecursionError, ValueError):
        return False
    return True


def _xsd_char(char: str, in_class: bool) -> str | None:
    """Escape a literal character for an XML Schema regular expression, or return None if XML excludes it."""
    if not _is_xml_char(char):
        return None
    if char in "\t\n\r":
        # written as escapes, as RDF/XML would normalize a carriage return
        return {"\t": r"\t", "\n": r"\n", "\r": r"\r"}[char]
    return "\\" + char if char in ("\\[]-^" if in_class else ".\\?*+{}()[]|") else char


def _xsd_escape(char: str, in_class: bool) -> str | None:
    """Translate the escape ``\\char`` of a Python regular expression, or return None.

    In a class, :func:`_xsd_class` translates ``\\S`` and ``\\W`` itself.
    """
    if char in "dDnrt":
        return "\\" + char
    if char in "sw":
        chars = _CLASS_ESCAPES[char]
        return chars if in_class else f"[{chars}]"
    if char in "SW":
        return f"[^{_CLASS_ESCAPES[char.lower()]}]"
    if char.isascii() and char.isalnum():
        # backreferences, \b, \A, \Z, \x, \u and the like
        return None
    return _xsd_char(char, in_class)


def _xsd_class_item(item: tuple[str, str]) -> str | None:
    """Translate a character or escape of a class, or return None."""
    kind, char = item
    return _xsd_escape(char, in_class=True) if kind == "escape" else _xsd_char(char, in_class=True)


def _range_end(item: tuple[str, str]) -> str:
    """Return the character that the end of a range stands for."""
    kind, char = item
    return {"n": "\n", "r": "\r", "t": "\t"}.get(char, char) if kind == "escape" else char


def _plain_range(start: int, end: int) -> str:
    """Write the range of code points from *start* to *end* without the C0 controls XML excludes."""
    # C0 controls other than tab, LF and CR are not XML characters.
    start = max(start, 0x20)
    if start > end:
        return ""
    return chr(start) if start == end else f"{chr(start)}-{chr(end)}"


def _xsd_range(low: str, high: str) -> str:
    """Translate the range from ``low`` to ``high`` of a character class.

    XML Schema allows an escaped character at either end of a range, but libxml2 and
    elementpath misread some of these ranges. The range is therefore split around
    each character that needs an escape, which then stands alone.
    """
    parts: list[str] = []
    start = ord(low)
    for char, escape in _RANGE_SPLITS.items():
        if start <= ord(char) <= ord(high):
            parts += [_plain_range(start, ord(char) - 1), escape]
            start = ord(char) + 1
    parts.append(_plain_range(start, ord(high)))
    return "".join(parts)


def _xsd_class(token: _Token) -> str | None:
    """Translate a character class.

    XML Schema cannot add a negated class to a class, so a class with ``\\S`` or
    ``\\W`` becomes a choice of classes, or a class subtraction if it is negated.
    """
    parts: list[str] = []
    # for each \S or \W, the characters it does not match
    negations: list[str] = []
    for item in token.items:
        if item in (("escape", "S"), ("escape", "W")):
            negations.append(_CLASS_ESCAPES[item[1].lower()])
            continue
        if item[0] == "range":
            _, low, high = item
            # a C0 control can end a range, which keeps the characters XML allows
            if not all(_xsd_class_item(end) is not None or _range_end(end) < " " for end in (low, high)):
                return None
            part = _xsd_range(_range_end(low), _range_end(high))
        else:
            part = _xsd_class_item(item)
        if part is None:
            return None
        parts.append(part)
    items = "".join(parts)
    if not items and not negations:
        # a class of characters that XML excludes only
        return None
    if not negations:
        return f"[{'^' if token.negated else ''}{items}]"
    if not token.negated:
        choices = ([f"[{items}]"] if items else []) + [f"[^{chars}]" for chars in negations]
        return choices[0] if len(choices) == 1 else f"({'|'.join(choices)})"
    if len(negations) > 1:
        # the characters each of them does not match, which no subtraction expresses
        return None
    # the characters the \S or \W does not match and no other item matches
    return f"[{negations[0]}-[{items}]]" if items else f"[{negations[0]}]"


def _xsd_branch(body: list[str], starts: bool, ends: bool) -> str:
    """Write a top-level branch so that it matches the whole value as a search of it would."""
    # A search finds an unanchored branch that begins or ends with ".*" without it.
    if not starts and body[:2] == [_DOT, "*"]:
        body = body[2:]
    if not ends and body[-2:] == [_DOT, "*"]:
        body = body[:-2]
    if not body and not (starts and ends):
        return _ANY
    return ("" if starts else _ANY) + "".join(body) + (_END if ends else _ANY)


def regex_as_xsd(pattern: str) -> str | None:
    """Translate a LinkML ``pattern`` into an XML Schema regular expression.

    The result matches exactly the values in which Python's ``re.search``, as used by
    LinkML's validators, finds the pattern. An XML Schema regular expression matches
    the whole value and reads ``^`` and ``$`` as ordinary characters (XML Schema 1.1
    Part 2, Appendix G). Each top-level branch therefore loses its anchors and gets
    ``(.|\\n|\\r)*`` at an end without one, and ``\\n?`` at an end with one, as
    Python's ``$`` also matches before a line feed that ends the value. Python's
    ``.``, ``\\s`` and ``\\w`` are spelled out, non-capturing groups become groups,
    and lazy quantifiers greedy ones.

    >>> regex_as_xsd("^[a-z_]+$")
    '[a-z_]+\\\\n?'
    >>> regex_as_xsd(r"\\bword\\b") is None
    True

    :param pattern: the regular expression, in Python's dialect
    :return: the XML Schema regular expression, or None if the pattern is invalid or
        uses what XML Schema cannot express, such as a lookaround, a backreference,
        an anchor inside a group or a character that XML excludes
    """
    if not _is_regex(pattern):
        return None
    # A structured pattern without partial_match resolves to "^(?:syntax)$", which
    # matches the whole value with any branch of the syntax, anchored or not.
    whole = pattern.startswith("^(?:") and pattern.endswith(")$") and _is_regex(pattern[4:-2])
    if whole:
        pattern = pattern[4:-2]
    branches: list[str] = []
    body: list[str] = []
    depth = 0
    starts = ends = False
    for token in _tokens(pattern):
        if ends and token.kind not in ("alt", "end"):
            return None
        if token.kind == "alt" and not depth:
            branches.append(_xsd_branch(body, starts or whole, ends or whole))
            body, starts, ends = [], False, False
            continue
        part: str | None
        if token.kind == "start":
            if body:
                return None
            starts, part = True, ""
        elif token.kind == "end":
            ends, part = True, ""
        elif token.kind == "escape":
            part = _xsd_escape(token.value, in_class=False)
        elif token.kind == "class":
            part = _xsd_class(token)
        elif token.kind == "open":
            if token.value == "?":
                return None
            depth += 1
            part = "("
        elif token.kind == "close":
            depth -= 1
            part = ")"
        elif token.kind == "dot":
            part = _DOT
        elif token.kind == "quant":
            # possessive quantifiers reject strings the greedy ones match; a lazy quantifier
            # matches the same strings as a greedy one
            part = None if token.possessive else token.value
        elif token.kind == "alt":
            part = "|"
        else:
            part = _xsd_char(token.value, in_class=False)
        if part is None:
            return None
        if part:
            body.append(part)
    branches.append(_xsd_branch(body, starts or whole, ends or whole))
    return "|".join(branches)


# The characters XPath escapes as themselves: XML Schema's SingleCharEsc (Part 2, G.4.2) and
# "$" (XPath and XQuery Functions and Operators 3.1, §5.6.1)
_XPATH_ESCAPES = "\\|.?*+(){}-[]^$"


def _xpath_char(char: str, in_class: bool) -> str | None:
    """Escape a literal character for both Python and XPath, or return None if XML excludes it."""
    if not _is_xml_char(char):
        return None
    if char in "\t\n\r":
        return {"\t": r"\t", "\n": r"\n", "\r": r"\r"}[char]
    return "\\" + char if char in ("\\[]-^" if in_class else ".\\?*+{}()[]|^$") else char


def _xpath_escape(char: str, in_class: bool) -> str | None:
    """Rewrite the escape ``\\char`` so that Python and XPath read it alike, or return None.

    ``\\w`` and ``\\W`` stay, as no notation for Python's ``\\w`` is valid in both
    dialects; ``\\d`` and ``\\D`` mean the Unicode decimal digits in both.
    """
    if char == "s":
        return _xpath_space() if in_class else f"[{_xpath_space()}]"
    if char == "S" and not in_class:
        return f"[^{_xpath_space()}]"
    if char in "dDwWnrt":
        return "\\" + char
    if char.isascii() and char.isalnum():
        # backreferences, \b, \A, \Z, \x, \u and the like, which XPath does not have
        return None
    if char in _XPATH_ESCAPES:
        return "\\" + char
    # Python reads another escaped character as itself, which XPath does not escape.
    return _xpath_char(char, in_class)


def _xpath_class_item(item: tuple) -> str | None:
    """Rewrite an item of a class, a range included, or return None."""
    if item[0] == "range":
        low, high = _xpath_class_item(item[1]), _xpath_class_item(item[2])
        return None if low is None or high is None else f"{low}-{high}"
    kind, char = item
    return _xpath_escape(char, in_class=True) if kind == "escape" else _xpath_char(char, in_class=True)


def _xpath_class(token: _Token) -> str | None:
    """Rewrite a character class so that Python and XPath read it alike, or return None.

    A class with ``\\S`` becomes a choice between the other items and the characters
    that are not white space. A negated class keeps its ``\\S``, as neither dialect can
    subtract a class from Python's ``\\S`` in a form the other reads.
    """
    parts: list[str] = []
    not_space = False
    for item in token.items:
        if item == ("escape", "S"):
            not_space = True
            continue
        part = _xpath_class_item(item)
        if part is None:
            return None
        parts.append(part)
    items = "".join(parts)
    if not not_space:
        return f"[{'^' if token.negated else ''}{items}]"
    if token.negated:
        return f"[^{items}\\S]"
    return f"([{items}]|[^{_xpath_space()}])" if items else f"[^{_xpath_space()}]"


def regex_for_xpath(pattern: str) -> str:
    """Rewrite a LinkML ``pattern`` so that XPath engines read it as Python does, where both can.

    XPath regular expressions (``fn:matches``), which SPARQL's ``REGEX`` and SHACL's
    ``sh:pattern`` use, are searched in the value as Python's ``re.search`` does, but
    ``$`` does not match before a final line feed, ``.`` does not match a carriage
    return, ``\\s`` is only space, tab, line feed and carriage return, some escapes and
    ``(?:`` do not exist, and ``{`` always starts a quantifier. Python-based engines such
    as pyshacl compile the same text with Python's ``re``. The rewrite uses only forms that
    both dialects read with Python's meaning: ``.`` becomes ``[^\\n]``, ``\\s`` an
    explicit class, ``(?:`` a group, an escaped punctuation character or a literal ``{``
    the form both read as that character, and ``{,n}`` ``{0,n}``. Two constructs stay as
    written, as no form has Python's meaning in both dialects: ``\\w`` and ``\\W``, as
    XPath's ``\\w`` excludes ``_`` and Python's ``re`` has no ``\\p{...}``; and ``$``,
    as matching an optional final line feed needs ``\\Z`` or a lookahead in Python.

    >>> regex_for_xpath(r"^a.b{,2}$")
    '^a[^\\\\n]b{0,2}$'
    >>> regex_for_xpath(r"^https?:\\/\\/\\S+$")
    '^https?://[^\\\\s\\x85\\xa0\\u1680\\u2000-\\u200a\\u2028-\\u2029\\u202f\\u205f\\u3000]+$'

    :param pattern: the regular expression, in Python's dialect
    :return: the rewritten regular expression, or *pattern* as it is if it is invalid or
        uses what XPath does not have, such as a lookaround, a backreference, ``\\b`` or
        an inline flag
    """
    if not _is_regex(pattern):
        return pattern
    parts: list[str] = []
    for token in _tokens(pattern):
        part: str | None
        if token.kind == "char":
            part = _xpath_char(token.value, in_class=False)
        elif token.kind == "escape":
            part = _xpath_escape(token.value, in_class=False)
        elif token.kind == "class":
            part = _xpath_class(token)
        elif token.kind == "open":
            # a backreference returns the pattern unchanged, so groups need no renumbering
            part = None if token.value == "?" else "("
        elif token.kind == "quant":
            part = None if token.possessive else token.value + ("?" if token.lazy else "")
        else:
            part = {"close": ")", "alt": "|", "start": "^", "end": "$", "dot": "[^\\n]"}[token.kind]
        if part is None:
            return pattern
        parts.append(part)
    return "".join(parts)
