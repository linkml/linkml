from pathlib import Path
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import RDF, RDFS, SKOS, XSD, OWL

__all__ = [
    "SchemaView",
]

# use importlib.metadata to read the version provided
# by the package during installation. Do not hardcode
# the version in the code
import importlib.metadata as importlib_metadata

LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TCCM = CurieNamespace('tccm', 'https://ontologies.r.us/tccm/')
OWL = CurieNamespace('owl', OWL)
RDF = CurieNamespace('rdf', RDF)
RDFS = CurieNamespace('rdfs', RDFS)
SKOS = CurieNamespace('skos', SKOS)
XSD = CurieNamespace('xsd', XSD)

__version__ = importlib_metadata.version(__name__)


THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH / "linkml_model" / "model" / "schema"

MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "meta.yaml"

LINKML_ANNOTATIONS = SCHEMA_DIRECTORY / "annotations.yaml"
LINKML_ARRAY = SCHEMA_DIRECTORY / "array.yaml"
LINKML_EXTENSIONS = SCHEMA_DIRECTORY / "extensions.yaml"
LINKML_MAPPINGS = SCHEMA_DIRECTORY / "mappings.yaml"
LINKML_TYPES = SCHEMA_DIRECTORY / "types.yaml"
LINKML_UNITS = SCHEMA_DIRECTORY / "units.yaml"
LINKML_VALIDATION = SCHEMA_DIRECTORY / "validation.yaml"


URI_TO_LOCAL = {
    'https://w3id.org/linkml/annotations.yaml': str(LINKML_ANNOTATIONS),
    'https://w3id.org/linkml/array.yaml': str(LINKML_ARRAY),
    'https://w3id.org/linkml/extensions.yaml': str(LINKML_EXTENSIONS),
    'https://w3id.org/linkml/mappings.yaml': str(LINKML_MAPPINGS),
    'https://w3id.org/linkml/meta.yaml': str(MAIN_SCHEMA_PATH),
    'https://w3id.org/linkml/types.yaml': str(LINKML_TYPES),
    'https://w3id.org/linkml/units.yaml': str(LINKML_UNITS),
    'https://w3id.org/linkml/validation.yaml': str(LINKML_VALIDATION),
}

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
