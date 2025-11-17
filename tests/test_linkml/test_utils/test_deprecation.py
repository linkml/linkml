import warnings
from copy import deepcopy
from operator import eq, ge, gt, le, lt
from unittest.mock import patch

import pytest

from linkml.utils import deprecation as dep_mod
from linkml.utils.deprecation import DEPRECATIONS, EMITTED, Deprecation, SemVer, deprecation_warning

all_ops = {le, lt, gt, ge, eq}


@pytest.fixture(scope="function")
def patch_deprecations():
    save_deps = deepcopy(dep_mod.DEPRECATIONS)
    yield dep_mod.DEPRECATIONS
    dep_mod.DEPRECATIONS = save_deps


@pytest.fixture()
def linkml_version() -> SemVer:
    try:
        return SemVer.from_package("linkml")
    except "PackageNotFoundError":
        return SemVer.from_str("1.0.1")


@pytest.mark.parametrize(
    "v1,v2,ops",
    [
        ["1.0.0", "2.0.0", [le, lt]],
        ["2.0.0", "1.0.0", [ge, gt]],
        ["0.1.0", "0.2.0", [le, lt]],
        ["0.2.0", "0.1.0", [ge, gt]],
        ["0.0.1", "0.0.2", [le, lt]],
        ["0.0.2", "0.0.1", [ge, gt]],
        ["1.1.1", "1.1.1", [le, ge, eq]],
        ["1.2.3", "3.2.1", [le, lt]],
        ["3.2.1", "1.2.3", [ge, gt]],
        ["v1.2.3", "1.2.3", [le, ge, eq]],
        ["0.0.0.post2223.dev0+0c3afa90", "0.0.0.post9999.dev9+0c3afa90", [le, ge, eq]],
    ],
)
def test_semver(v1, v2, ops):
    v1 = SemVer.from_str(v1)
    v2 = SemVer.from_str(v2)
    for op in ops:
        assert op(v1, v2)
    for false_op in all_ops - set(ops):
        assert not false_op(v1, v2)


def test_semver_nomatch():
    """
    If no match, return None
    """
    ver = SemVer.from_str("definitely not a version specifier")
    assert ver is None


def test_deprecation_warning(patch_deprecations):
    current_ver = SemVer.from_package("linkml")
    not_dep_yet = Deprecation(
        name="test-not-dep-yet",
        deprecated_in=SemVer(major=current_ver.major + 1, minor=0, patch=0),
        message="not deprecated yet",
    )
    is_dep = Deprecation(
        name="test-is-deprecated",
        deprecated_in=SemVer(major=current_ver.major - 1, minor=0, patch=0),
        removed_in=SemVer(major=current_ver.major + 1, minor=0, patch=0),
        message="is deprecated but not removed",
        recommendation="do nothing because this is a test",
    )
    is_removed = Deprecation(
        name="test-is-removed",
        deprecated_in=SemVer(major=current_ver.major - 2, minor=0, patch=0),
        removed_in=SemVer(major=current_ver.major - 1, minor=0, patch=0),
        message="is removed and deprecated",
        recommendation="you are fine, this is still a test",
    )
    dup_1 = Deprecation(
        name="test-duplicate",
        deprecated_in=SemVer(major=current_ver.major - 2, minor=0, patch=0),
        removed_in=SemVer(major=current_ver.major - 1, minor=0, patch=0),
        message="Same name deprecation",
        recommendation="you are fine, this is still a test",
    )
    dup_2 = Deprecation(
        name="test-duplicate",
        deprecated_in=SemVer(major=current_ver.major - 2, minor=0, patch=0),
        removed_in=SemVer(major=current_ver.major - 1, minor=0, patch=0),
        message="Same name deprecation",
        recommendation="you are fine, this is still a test",
    )
    dep_mod.DEPRECATIONS = (not_dep_yet, is_dep, is_removed, dup_1, dup_2)

    # no warnings emitted for not deprecated
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        deprecation_warning("test-not-dep-yet")

    # deprecation warning emitted only once for deprecated feature
    with pytest.warns() as record:
        deprecation_warning("test-is-deprecated")
        deprecation_warning("test-is-deprecated")
        assert len(record) == 1
        assert isinstance(record[0].message, DeprecationWarning)
        msg = str(record[0].message)
        for part in ("DEPRECATED", "Deprecated In:", "Removed In:", "Recommendation:", is_dep.message):
            assert part in msg

    # removed behaves similarly
    with pytest.warns() as record:
        deprecation_warning("test-is-removed")
        deprecation_warning("test-is-removed")
        assert len(record) == 1
        assert isinstance(record[0].message, DeprecationWarning)
        msg = str(record[0].message)
        for part in ("REMOVED", "Deprecated In:", "Removed In:", "Recommendation:", is_removed.message):
            assert part in msg

    # duplicates raise an exception
    with pytest.raises(RuntimeError):
        deprecation_warning("test-duplicate")

    deprecation_warning("temporary-dep")

    # emitted deprecation warnings are added to the emitted set
    assert "test-is-deprecated" in EMITTED
    assert "test-is-removed" in EMITTED
    assert "temporary-dep" in EMITTED


def test_deprecation_postinit():
    """
    Deprecation class should try to coerce basic types
    """
    dep = Deprecation(name="test-dep", message="just a test", deprecated_in="v1.0.0", removed_in="v1.2.0")
    assert dep.deprecated_in == SemVer(major=1, minor=0, patch=0)
    assert dep.removed_in == SemVer(major=1, minor=2, patch=0)


@patch("linkml.utils.deprecation.version")
def test_deprecation_str(version_mock):
    """
    Deprecation should render a pretty string
    """
    version_mock.return_value = "2.0.0"

    dep = Deprecation(
        name="test-dep",
        message="testing strings",
        deprecated_in=SemVer.from_str("1.0.0"),
        recommendation="See if this test passes",
        issue=123,
    )
    dep_str = str(dep)
    assert (
        dep_str
        == """[test-dep] DEPRECATED
testing strings
Deprecated In: 1.0.0
Recommendation: See if this test passes
See: https://github.com/linkml/linkml/issues/123"""
    )


@patch("linkml.utils.deprecation.version")
def test_deprecation_removed_in_str(version_mock):
    """
    Deprecation with removed_in should render a pretty string
    """
    version_mock.return_value = "2.0.0"

    dep = Deprecation(
        name="test-dep",
        message="testing strings",
        deprecated_in=SemVer.from_str("1.0.0"),
        removed_in=SemVer.from_str("1.2.1"),
        recommendation="See if this test passes",
        issue=456,
    )
    dep_str = str(dep)
    assert (
        dep_str
        == """[test-dep] REMOVED
testing strings
Deprecated In: 1.0.0
Removed In: 1.2.1
Recommendation: See if this test passes
See: https://github.com/linkml/linkml/issues/456"""
    )


@pytest.mark.parametrize("deprecated,deprecated_val", [[0, True], [-1, True], [1, False]])
@pytest.mark.parametrize("removed,removed_val", [[None, False], [0, True], [-1, True], [1, False]])
def test_deprecation_props(deprecated, deprecated_val, removed, removed_val, linkml_version):
    """
    Properties should tell us if we have passed the deprecation or not
    """

    depver = SemVer(major=linkml_version.major + deprecated)
    remver = None
    if removed is not None:
        remver = SemVer(major=linkml_version.major + removed)

    dep = Deprecation(name="test-dep", message="testing our properties", deprecated_in=depver, removed_in=remver)
    assert dep.deprecated == deprecated_val
    assert dep.removed == removed_val


def test_deprecation_warns_selectively(linkml_version):
    """
    We should only warn when we are actually deprecated
    """
    dep = Deprecation(name="test-dep", message="", deprecated_in=SemVer(major=linkml_version.major + 1))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        dep.warn()

    dep = Deprecation(name="test-dep", message="", deprecated_in=SemVer(major=linkml_version.major - 1))
    with pytest.warns() as record:
        dep.warn()
        assert len(record) == 1


def test_removed_are_removed():
    """
    Test that any Deprecation marked as having been removed in this version have been.

    If the tests are being run after having been checked out without tags, then will emit a warning.

    This test should not be renamed, see ``conftest.pytest_collection_modifyitems`` , which uses its
    name to ensure that it runs last
    """

    ver = SemVer.from_package("linkml")
    if ver.major == 0 and ver.minor == 0 and ver.patch == 0:
        warnings.warn(f"Version detected as {str(ver)}, deprecations will not be tested")
        return

    removed = [dep for dep in DEPRECATIONS if dep.removed and not dep.name.startswith("test-")]
    for removed in removed:
        assert removed.name not in EMITTED
