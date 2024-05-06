"""
Utilities for deprecating functionality and dependencies.

- Emitting DeprecationWarnings
- Tracking deprecated and removed in versions
- Fail tests when something marked as removed_in is still present in the specified version

Initial draft for deprecating Pydantic 1, to make more general, needs
- function wrapper version
- ...

To deprecate something:

- Create a :class:`.Deprecation` object within the `DEPRECATIONS` tuple
- Use the :func:`.deprecation_warning` function wherever the deprecated feature would be used to emit the warning

"""

import re
import warnings
from dataclasses import dataclass
from importlib.metadata import version
from typing import Optional

# Stolen from https://github.com/pypa/packaging/blob/main/src/packaging/version.py
# Updated to include major, minor, and patch versions
PEP440_PATTERN = r"""
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
"""
PEP440 = re.compile(r"^\s*" + PEP440_PATTERN + r"\s*$", re.VERBOSE | re.IGNORECASE)


@dataclass
class SemVer:
    """
    Representation of semantic version that supports inequality comparisons.

    .. note::

        The inequality methods _only_ test the numeric major, minor, and patch components
        of the version - ie. they do not evaluate the prerelease versions as described in the semver
        spec. This is not intended to be a general SemVer inequality calculator, but used
        only for testing deprecations

    """

    major: int = 0
    minor: int = 0
    patch: int = 0
    epoch: Optional[int] = None
    pre: Optional[str] = None
    pre_l: Optional[str] = None
    pre_n: Optional[str] = None
    post: Optional[str] = None
    post_n1: Optional[str] = None
    post_l: Optional[str] = None
    post_n2: Optional[str] = None
    dev: Optional[str] = None
    dev_l: Optional[str] = None
    dev_n: Optional[str] = None
    local: Optional[str] = None

    def __post_init__(self):
        self.major = int(self.major)
        self.minor = int(self.minor)
        self.patch = int(self.patch)

    @classmethod
    def from_str(cls, v: str) -> Optional["SemVer"]:
        """
        Create a SemVer from a string using `PEP 440 <https://peps.python.org/pep-0440/>`_
        syntax.

        Examples:

            .. code-block:: python

                >>> version = SemVer.from_str("v0.1.0")
                >>> print(version)
                0.1.0

        """
        match = PEP440.search(v)
        if match is None:
            return None
        return SemVer(**match.groupdict())

    @classmethod
    def from_package(cls, package: str) -> "SemVer":
        """Get semver from package name"""
        v = version(package)
        return SemVer.from_str(v)

    def __eq__(self, other: "SemVer"):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __lt__(self, other: "SemVer"):
        # fall through each if elif only if version component is equal
        for field in ("major", "minor", "patch"):
            if getattr(self, field) < getattr(other, field):
                return True
            elif getattr(self, field) > getattr(other, field):
                return False

        # otherwise, equal (which is False)
        return False

    def __gt__(self, other: "SemVer"):
        return not (self < other) and not (self == other)

    def __le__(self, other: "SemVer"):
        return (self < other) or (self == other)

    def __ge__(self, other: "SemVer"):
        return (self > other) or (self == other)

    def __str__(self) -> str:
        return ".".join([str(item) for item in [self.major, self.minor, self.patch]])


@dataclass
class Deprecation:
    """
    Parameterization of a deprecation.
    """

    name: str
    """Shorthand, unique name used to refer to this deprecation"""
    message: str
    """Message to be displayed explaining the deprecation"""
    deprecated_in: SemVer
    """Version that the feature was deprecated in"""
    removed_in: Optional[SemVer] = None
    """Version that the feature will be removed in"""
    recommendation: Optional[str] = None
    """Recommendation about what to do to replace the deprecated behavior"""
    issue: Optional[int] = None
    """GitHub version describing deprecation"""

    def __post_init__(self):
        if self.deprecated_in is not None and isinstance(self.deprecated_in, str):
            self.deprecated_in = SemVer.from_str(self.deprecated_in)
        if self.removed_in is not None and isinstance(self.removed_in, str):
            self.removed_in = SemVer.from_str(self.removed_in)

    def __str__(self) -> str:
        msg = f"[{self.name}] "
        if self.removed:
            msg += "REMOVED"
        elif self.deprecated:
            msg += "DEPRECATED"

        msg += f"\n{self.message}"
        msg += f"\nDeprecated In: {str(self.deprecated_in)}"
        if self.removed_in is not None:
            msg += f"\nRemoved In: {str(self.removed_in)}"
        if self.recommendation is not None:
            msg += f"\nRecommendation: {self.recommendation}"
        if self.issue is not None:
            msg += f"\nSee: https://github.com/linkml/linkml/issues/{self.issue}"
        return msg

    @property
    def deprecated(self) -> bool:
        return SemVer.from_package("linkml") >= self.deprecated_in

    @property
    def removed(self) -> bool:
        if self.removed_in is None:
            return False
        return SemVer.from_package("linkml") >= self.removed_in

    def warn(self, **kwargs):
        if self.deprecated:
            warnings.warn(message=str(self), category=DeprecationWarning, stacklevel=3, **kwargs)


DEPRECATIONS = (
    Deprecation(
        name="pydanticgen-v1",
        deprecated_in=SemVer.from_str("1.7.5"),
        removed_in=SemVer.from_str("1.8.0"),
        message="Support for generating Pydantic v1.*.* models with pydanticgen is deprecated",
        recommendation="Migrate any existing models to Pydantic v2",
        issue=1925,
    ),
    Deprecation(
        name="pydantic-v1",
        deprecated_in=SemVer.from_str("1.7.5"),
        removed_in=SemVer.from_str("1.9.0"),
        message=(
            "LinkML will set a dependency of pydantic>=2 and become incompatible "
            "with packages with pydantic<2 as a runtime dependency"
        ),
        recommendation="Update dependent packages to use pydantic>=2",
        issue=1925,
    ),
)  # type: tuple[Deprecation, ...]

EMITTED = set()  # type: set[str]


def deprecation_warning(name: str):
    """
    Call this with the name of the deprecation object wherever the deprecated functionality will be used

    This function will

    - emit a warning if the current version is greater than ``deprecated_in``
    - log that the deprecated feature was accessed in ``EMITTED`` for testing deprecations and muting warnings

    """
    global DEPRECATIONS
    global EMITTED

    dep = [dep for dep in DEPRECATIONS if dep.name == name]
    if len(dep) == 1:
        dep = dep[0]
    elif len(dep) > 1:
        raise RuntimeError(f"Duplicate deprecations found with name {name}")
    else:
        EMITTED.add(name)
        return

    if dep.name not in EMITTED:
        dep.warn()

    EMITTED.add(name)
