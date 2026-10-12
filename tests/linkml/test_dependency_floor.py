import tomllib
from pathlib import Path

from packaging.requirements import Requirement

# linkml's generators import linkml_runtime.utils.rdf_canonicalize, which first
# shipped in linkml-runtime 1.12.0. A lower floor lets pip install an older
# runtime alongside this package, and importing the generators then fails.
RDF_CANONICALIZE_FIRST_RUNTIME = "1.12.0"

PYPROJECT = Path(__file__).resolve().parents[2] / "packages" / "linkml" / "pyproject.toml"


def test_linkml_requires_runtime_with_rdf_canonicalize():
    dependencies = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["dependencies"]
    (requirement,) = [Requirement(dep) for dep in dependencies if dep.startswith("linkml-runtime")]
    assert requirement.specifier.contains(RDF_CANONICALIZE_FIRST_RUNTIME)
    assert not requirement.specifier.contains("1.11.1")
