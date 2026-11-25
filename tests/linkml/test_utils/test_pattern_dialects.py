"""Tests for the translation of LinkML patterns into the regex dialects of XML Schema and XPath."""

import re
import sys

import pytest

from linkml.utils.pattern_dialects import regex_as_xsd, regex_for_xpath

XSD_SPACE = "\\s\\p{Z}\x85"  # Python's \s over the characters XML allows


@pytest.mark.parametrize(
    ("pattern", "expected"),
    [
        (r"^[a-z_]+$", r"[a-z_]+\n?"),
        (r"[a-z]+", r"(.|\n|\r)*[a-z]+(.|\n|\r)*"),
        (r"^https?:\/\/", r"https?://(.|\n|\r)*"),
        (r"^(this)|(that)|(whatever)$", r"(this)(.|\n|\r)*|(.|\n|\r)*(that)(.|\n|\r)*|(.|\n|\r)*(whatever)\n?"),
        (r"^(?:a|b)$", r"a\n?|b\n?"),
        (r"(a|b)", r"(.|\n|\r)*(a|b)(.|\n|\r)*"),
        (r".*(Z|[+-]\d{2}:\d{2})$", r"(.|\n|\r)*(Z|[+\-]\d{2}:\d{2})\n?"),
        (r"^a.*", r"a(.|\n|\r)*"),
        (r"^.*a", r"(.|\r)*a(.|\n|\r)*"),
        (r"a.*$", r"(.|\n|\r)*a(.|\r)*\n?"),
        (r"^a.b$", r"a(.|\r)b\n?"),
        (r"^a\.b$", r"a\.b\n?"),
        (r"^$", r"\n?"),
        (r"^^a$$", r"a\n?"),
        (r"", r"(.|\n|\r)*"),
        (r".*$", r"(.|\n|\r)*"),
        (r"a|", r"(.|\n|\r)*a(.|\n|\r)*|(.|\n|\r)*"),
        (r"^\d{2,}?-\w+$", r"\d{2,}-[\p{L}\p{N}_]+\n?"),
        (r"^[\w.-]+$", r"[\p{L}\p{N}_.\-]+\n?"),
        (r"^\W+$", r"[^\p{L}\p{N}_]+\n?"),
        (r"^[^\w]$", r"[^\p{L}\p{N}_]\n?"),
        (r"^\S+ \S+$", rf"[^{XSD_SPACE}]+ [^{XSD_SPACE}]+\n?"),
        (r"^[^\s]\s$", rf"[^{XSD_SPACE}][{XSD_SPACE}]\n?"),
        # XML Schema cannot add a negated class to a class
        (r"[\W]", r"(.|\n|\r)*[^\p{L}\p{N}_](.|\n|\r)*"),
        (r"^[\S+.]+$", rf"([+.]|[^{XSD_SPACE}])+\n?"),
        (r"^[\S\W]$", "([^" + XSD_SPACE + r"]|[^\p{L}\p{N}_])\n?"),
        (r"^[]\S]$", rf"([\]]|[^{XSD_SPACE}])\n?"),
        (r"^[\S]]$", rf"[^{XSD_SPACE}]\]\n?"),
        (r"^[^\S]$", rf"[{XSD_SPACE}]\n?"),
        (r"^[^\S\r\n]$", rf"[{XSD_SPACE}-[\r\n]]\n?"),
        (r"^[^\W\d_]+$", r"[\p{L}\p{N}_-[\d_]]+\n?"),
        (r"^[]a]$", r"[\]a]\n?"),
        (r"^[^]a]$", r"[^\]a]\n?"),
        (r"^[\^a]$", r"[\^a]\n?"),
        (r"^[^|]+\|$", r"[^|]+\|\n?"),
        (r"^[--/]$", r"[\-.-/]\n?"),
        (r"^[!-\]]$", r"[!-,\-.-Z\[\\\]]\n?"),
        (r"^[\^-z]$", r"[\^_-z]\n?"),
        (r"^[\t-\r]$", r"[\t\n\r]\n?"),
        (r"^a{,3}$", r"a{0,3}\n?"),
        (r"^a{x}{}$", r"a\{x\}\{\}\n?"),
        (r"^a{,٣}$", r"a\{,٣\}\n?"),
        (r"^\$\d+$", r"$\d+\n?"),
        # a tab, line feed or carriage return is written as an escape, which RDF/XML does not normalize
        ("^a\tb$", r"a\tb\n?"),
        # escapes of characters by code point or name, named groups and comments
        (r"^\x41\u00e9\U0001F600\N{DIGIT ONE}$", "A\u00e9\U0001f6001\\n?"),
        (r"^\x2E$", r"\.\n?"),
        (r"[^\x00-\x1F]", r"(.|\n|\r)*[^\t\n\r](.|\n|\r)*"),
        (r"^(?P<year>\d{4})(?#year)$", r"(\d{4})\n?"),
        # a structured pattern without partial_match resolves to "^(?:syntax)$"
        (r"^(?:^(https?://|(mailto|tel):)\w+$)$", r"(https?://|(mailto|tel):)[\p{L}\p{N}_]+\n?"),
        (r"^(?:^a$|b)$", r"a\n?|b\n?"),
        (r"^(?:a)|(b)$", r"(a)(.|\n|\r)*|(.|\n|\r)*(b)\n?"),
        # constructs the translation leaves out
        (r"^(?=a)a$", None),
        (r"^(a)\1$", None),
        (r"\bword\b", None),
        (r"(?i)a", None),
        (r"(^a)", None),
        (r"(a$)", None),
        (r"a^b", None),
        (r"^a$b", None),
        (r"[^\S\W]", None),
        (r"a++", None),
        (r"[!-\x7f]", "(.|\\n|\\r)*[!-,\\-.-Z\\[\\\\\\]\\^_-\x7f](.|\\n|\\r)*"),
        (r"^(?P<a>x)(?P=a)$", None),
        # a class of characters that XML excludes only
        (r"[\x01-\x08]", None),
        # characters XML excludes
        ("^a\x01b$", None),
        ("^[\x01-\x08]$", None),
        # patterns Python cannot compile
        (r"[", None),
        (r"a{99999999999999999999}", None),
        pytest.param("a{" + "9" * 4500 + "}", None, id="too-many-digits"),
    ],
)
def test_regex_as_xsd(pattern: str, expected: str | None) -> None:
    """Translate a pattern to a regular expression that matches the values in which Python's re.search finds it."""
    assert regex_as_xsd(pattern) == expected


def test_regex_nested_too_deep_for_python_is_left_out() -> None:
    """A pattern nested deeper than Python's recursion limit allows cannot be compiled, so it has no translation."""
    # the limit is read at run time, as an imported module may have raised it
    depth = sys.getrecursionlimit()
    assert regex_as_xsd("^" + "(" * depth + "a" + ")" * depth + "$") is None


# Python's \s as the inside of a class that Python and XPath read alike: \s and the XML characters
# that Python's \s matches and the XPath \s (space, tab, line feed, carriage return) does not
XPATH_SPACE = "\\s\x85\xa0\u1680\u2000-\u200a\u2028-\u2029\u202f\u205f\u3000"

XPATH_CASES = [
    # what both dialects already read alike stays
    (r"^[a-z_]+$", r"^[a-z_]+$"),
    (r"[a-z]+", r"[a-z]+"),
    (r"^\d{2,4}$", r"^\d{2,4}$"),
    (r"^\w+$", r"^\w+$"),
    (r"^[\w-]+$", r"^[\w\-]+$"),
    (r"a*?b+?c??", r"a*?b+?c??"),
    (r"^\$\.\*\+\?\(\)\[\]\{\}\|\^\\-", r"^\$\.\*\+\?\(\)\[\]\{\}\|\^\\-"),
    # "." also matches a carriage return in Python, not in XPath
    (r"^a.b$", r"^a[^\n]b$"),
    # \s and \S are Python's
    (r"^\s*$", rf"^[{XPATH_SPACE}]*$"),
    (r"^\S+ \S+$", rf"^[^{XPATH_SPACE}]+ [^{XPATH_SPACE}]+$"),
    (r"[\s,;]", rf"[{XPATH_SPACE},;]"),
    (r"[^\s]", rf"[^{XPATH_SPACE}]"),
    (r"^[\S+.]+$", rf"^([+.]|[^{XPATH_SPACE}])+$"),
    (r"[\S]", rf"[^{XPATH_SPACE}]"),
    # a negated class with \S keeps it, its other items as both dialects read them
    (r"[^\S\r\n]", r"[^\r\n\S]"),
    # escaped punctuation that XPath does not escape, and a literal "{" or "}"
    (r"^https?:\/\/", r"^https?://"),
    (r"^a\:b\#c\ d$", r"^a:b#c d$"),
    (r"\S+@\S+{\.\w}+", rf"[^{XPATH_SPACE}]+@[^{XPATH_SPACE}]+\{{\.\w\}}+"),
    (r"^[\d\(\)\-]+$", r"^[\d\(\)\-]+$"),
    # characters that XPath requires escaped in a class
    (r"[]a]", r"[\]a]"),
    (r"[a[]", r"[a\[]"),
    (r"[a-]", r"[a\-]"),
    (r"[!-\]]", r"[!-\]]"),
    # non-capturing groups and an omitted lower bound
    (r"^(?:a|b)$", r"^(a|b)$"),
    (r"^a{,3}$", r"^a{0,3}$"),
    # "$" stays: matching an optional final line feed needs \Z or a lookahead in Python
    (r"a$", r"a$"),
    # escapes of characters by code point or name, named groups, comments, and a literal tab
    (r"^\x41\N{DIGIT ONE}\x2E$", r"^A1\.$"),
    (r"^(?P<x>a)(?#comment)$", r"^(a)$"),
    ("^a\tb$", r"^a\tb$"),
]

# patterns XPath has no notation for are returned as they are
XPATH_UNCHANGED = [
    r"^(?=a)a$",
    r"^(a)\1$",
    r"\bword\b",
    r"(?i)a",
    r"(?P<x>a)(?P=x)",
    r"a++",
    r"\Aa\Z",
    r"[",
    r"a{99999999999999999999}",
    # characters that XML excludes cannot be written for XPath
    r"[^\x00-\x1F]",
]

VALUES = [
    "",
    "a",
    "ab",
    "a b",
    "a\nb",
    "a\rb",
    "a\n",
    "a\n\n",
    "\n",
    "\r",
    "snake_case",
    "ID-42x",
    "Fred Bloggs",
    "Fred\xa0Bloggs",
    "x\u2028y",
    "\x85",
    "\u3000",
    "https://x.org",
    "a:b#c d",
    "fred@x.org",
    "{.x}",
    "[a]",
    "a-",
    "(555)-1234",
    "$.*+?()[]{}|^\\-",
    "a-b",
    "\t",
    "aaa",
    "aab",
    "ba",
]


@pytest.mark.parametrize(("pattern", "expected"), XPATH_CASES)
def test_regex_for_xpath(pattern: str, expected: str) -> None:
    """Rewrite a pattern into forms that Python and XPath read with Python's meaning, where they exist."""
    assert regex_for_xpath(pattern) == expected


@pytest.mark.parametrize("pattern", XPATH_UNCHANGED)
def test_regex_for_xpath_keeps_what_xpath_cannot_express(pattern: str) -> None:
    assert regex_for_xpath(pattern) == pattern


@pytest.mark.parametrize("pattern", [p for p, _ in XPATH_CASES])
def test_regex_for_xpath_keeps_the_meaning_in_python(pattern: str) -> None:
    """Python, and so a Python-based SHACL engine, finds the rewritten pattern in the same values."""
    rewritten = re.compile(regex_for_xpath(pattern))
    for value in VALUES:
        assert bool(rewritten.search(value)) == bool(re.search(pattern, value)), value


def test_xpath_space_is_pythons_white_space() -> None:
    """The class that stands for Python's \\s matches exactly the XML characters Python's \\s matches."""
    space, not_space = re.compile(f"[{XPATH_SPACE}]"), re.compile(f"[^{XPATH_SPACE}]")
    assert regex_for_xpath(r"\s") == f"[{XPATH_SPACE}]"
    for code in [0x9, 0xA, 0xD, *range(0x20, 0xD800), *range(0xE000, 0xFFFE), *range(0x10000, sys.maxunicode + 1)]:
        char = chr(code)
        assert bool(space.match(char)) == char.isspace() != bool(not_space.match(char)), hex(code)
