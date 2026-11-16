import pytest

from linkml.generators.common.naming import NameCompatibility, check_keyword_collisions, escape_python_keyword


def test_equality_graphql():
    name_compatibility = NameCompatibility(profile="graphql")
    assert name_compatibility.compatible("abc") == "abc"
    assert name_compatibility.compatible("a123") == "a123"
    assert name_compatibility.compatible("_a") == "_a"


@pytest.mark.parametrize(
    "profile",
    ["graphql"],
)
def test_no_heading_digit(profile):
    name_compatibility = NameCompatibility(profile=profile)
    assert name_compatibility.compatible("1a") == "__1a"


@pytest.mark.parametrize(
    "profile",
    ["graphql"],
)
def test_no_special_characters(profile):
    name_compatibility = NameCompatibility(profile=profile)
    assert name_compatibility.compatible("a!") == "a__EXCLAMATION_MARK__"
    assert name_compatibility.compatible("aö") == "a__U_00F6_"


def test_no_reserved_graphql():
    name_compatibility = NameCompatibility(profile="graphql")
    with pytest.raises(NotImplementedError):
        name_compatibility.compatible("__1")
    with pytest.raises(NotImplementedError):
        name_compatibility.compatible("__U_ABCD_")
    with pytest.raises(NotImplementedError):
        name_compatibility.compatible("__xyz__")


def test_no_fix_graphql():
    name_compatibility = NameCompatibility(profile="graphql", do_not_fix=True)
    with pytest.raises(ValueError):
        name_compatibility.compatible("1")
    with pytest.raises(ValueError):
        name_compatibility.compatible("a#")


@pytest.mark.parametrize(
    "name,expected",
    [("from", "from_"), ("class", "class_"), ("None", "None_"), ("to", "to"), ("from_", "from_"), ("match", "match")],
)
def test_escape_python_keyword(name, expected):
    assert escape_python_keyword(name) == expected


@pytest.mark.parametrize(
    "names",
    [
        pytest.param(["from", "to"], id="keyword alone"),
        pytest.param(["from_", "to"], id="from_ alone"),
        pytest.param(["from", "from"], id="two slots with the alias from"),
    ],
)
def test_check_keyword_collisions_accepts(names):
    check_keyword_collisions("Window", names)


def test_check_keyword_collisions_refuses():
    with pytest.raises(
        ValueError, match="Class Window: slots 'from' and 'from_' would both be the Python field 'from_'"
    ):
        check_keyword_collisions("Window", ["from_", "id", "from"])
