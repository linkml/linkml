import os
import sys

from linkml_runtime.linkml_model import linkml_files
from linkml_runtime.linkml_model.linkml_files import Source, Format
from rdflib.plugins.serializers.turtle import TurtleSerializer

assert sys.version_info > (3, 7, 0), f"LinkML requires python 3.7.1 or later to run.  Current version: {sys.version_info}"

MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Local location of yaml files
LOCAL_METAMODEL_YAML_FILE = linkml_files.LOCAL_PATH_FOR(Source.META, Format.YAML)
LOCAL_TYPES_YAML_FILE = linkml_files.LOCAL_PATH_FOR(Source.TYPES, Format.YAML)
LOCAL_MAPPINGS_YAML_FILE = linkml_files.LOCAL_PATH_FOR(Source.MAPPINGS, Format.YAML)
LOCAL_ANNOTATIONS_YAML_FILE = linkml_files.LOCAL_PATH_FOR(Source.ANNOTATIONS, Format.YAML)
LOCAL_EXTENSIONS_YAML_FILE = linkml_files.LOCAL_PATH_FOR(Source.EXTENSIONS, Format.YAML)

# Local location of jsonld and context.jsonld files
LOCAL_METAMODEL_LDCONTEXT_FILE = linkml_files.LOCAL_PATH_FOR(Source.META, Format.JSONLD)
LOCAL_METAMODEL_JSONLD_FILE = linkml_files.LOCAL_PATH_FOR(Source.META, Format.JSON)
LOCAL_TYPES_LDCONTEXT_FILE = linkml_files.LOCAL_PATH_FOR(Source.TYPES, Format.JSONLD)
LOCAL_TYPES_JSONLD_FILE = linkml_files.LOCAL_PATH_FOR(Source.TYPES, Format.JSON)
LOCAL_MAPPINGS_LDCONTEXT_FILE = linkml_files.LOCAL_PATH_FOR(Source.MAPPINGS, Format.JSONLD)
LOCAL_MAPPINGS_JSONLD_FILE = linkml_files.LOCAL_PATH_FOR(Source.MAPPINGS, Format.JSON)

# Local location of metamodel shex file
LOCAL_SHEXJ_FILE_NAME = linkml_files.LOCAL_PATH_FOR(Source.META, Format.SHEXJ)
LOCAL_SHEXC_FILE_NAME = linkml_files.LOCAL_PATH_FOR(Source.META, Format.SHEXC)

# Local location of the metamodel rdf file
LOCAL_RDF_FILE_NAME = linkml_files.LOCAL_PATH_FOR(Source.META, Format.RDF)

# URI for the entire metamodel itself.
METAMODEL_NAME = linkml_files.Source.META.value
METAMODEL_URI = linkml_files.URL_FOR(Source.META, Format.YAML)
METATYPE_NAME = linkml_files.Source.TYPES.value
METATYPE_URI = linkml_files.URL_FOR(Source.TYPES, Format.YAML)
METAMAPPING_NAME = linkml_files.Source.MAPPINGS.value
METAMAPPING_URI = linkml_files.URL_FOR(Source.MAPPINGS, Format.YAML)

# Preferred local name for metamodel elements
METAMODEL_NAMESPACE_NAME = "linkml"
METATYPE_NAMESPACE_NAME = 'linkml'
METAMAPPING_NAMESPACE_NAME = 'linkml'

# Namespace for metamodel elements
META_BASE_URI = linkml_files.LINKML_NAMESPACE
METAMODEL_NAMESPACE = META_BASE_URI
METATYPE_NAMESPACE = METAMODEL_NAMESPACE
METAMAPPING_NAMESPACE = METAMODEL_NAMESPACE
METAANNOTATIONS_NAMESPACE = METAMODEL_NAMESPACE
METAEXTENSIONS_NAMESPACE = METAMODEL_NAMESPACE

# Metamodel Context URI
METAMODEL_CONTEXT_URI = linkml_files.URL_FOR(Source.META, Format.JSONLD)

# Metamodel ShEx URI
METAMODEL_SHEXJ_URI = linkml_files.URL_FOR(Source.META, Format.SHEXJ)
METAMODEL_SHEXC_URI = linkml_files.URL_FOR(Source.META, Format.SHEXC)

# Metamodel YAML file
METAMODEL_YAML_URI = linkml_files.URL_FOR(Source.META, Format.YAML)

# Biolink model file -- this needs a more official fix
BIOLINK_MODEL_URI = "https://w3id.org/biolink/biolink-model"
BIOLINK_MODEL_PYTHON_LOC = "biolink.model"

TurtleSerializer.roundtrip_prefixes = ['']

