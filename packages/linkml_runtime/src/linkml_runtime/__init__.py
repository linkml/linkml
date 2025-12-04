from pathlib import Path

from rdflib import OWL, RDF, RDFS, SKOS, XSD

from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.schemaview import SchemaView

__all__ = [
    "SchemaView",
]

# use importlib.metadata to read the version provided
# by the package during installation. Do not hardcode
# the version in the code
import importlib.metadata as importlib_metadata

LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
TCCM = CurieNamespace("tccm", "https://ontologies.r.us/tccm/")
OWL = CurieNamespace("owl", OWL)
RDF = CurieNamespace("rdf", RDF)
RDFS = CurieNamespace("rdfs", RDFS)
SKOS = CurieNamespace("skos", SKOS)
XSD = CurieNamespace("xsd", XSD)

__version__ = importlib_metadata.version(__name__)


THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH / "linkml_model" / "model" / "schema"

MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "meta.yaml"

LINKML_COMPONENTS = ["annotations", "array", "extensions", "mappings", "meta", "types", "units", "validation"]

# map component names to their schema paths as Path objects
# file paths are of the form SCHEMA_DIRECTORY / "{component}.yaml"
LINKML_PATHS = {c: SCHEMA_DIRECTORY / f"{c}.yaml" for c in LINKML_COMPONENTS}

# map linkml URIs to their local paths as Path objects
# URIs are of the form "https://w3id.org/linkml/{component}.yaml"
URI_TO_PATH = {f"https://w3id.org/linkml/{c}.yaml": str(LINKML_PATHS[c]) for c in LINKML_COMPONENTS}

# map linkml URIs to their local paths in string form
URI_TO_LOCAL = {key: str(path) for key, path in URI_TO_PATH.items()}


class MappingError(ValueError):
    """
    An error when mapping elements of a LinkML model to runtime objects
    """

    pass


class DataNotFoundError(ValueError):
    """
    An error in which data cannot be found
    """

    pass
