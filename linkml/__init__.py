import os
import sys
from warnings import warn

from rdflib import Namespace
from rdflib.plugins.serializers.turtle import TurtleSerializer

""" 
URIs, Local Names and Namespaces 

Physical layout:
    linkml/
        |
        +------ meta.yaml
        |
        +------ context.jsonld  (Master context for metamodel)
        |
        +------ meta.jsonld     (Jsonld representation of metamodel)
        |
        +------ meta.shex       (ShExC representation of metamodel)
        |
        +------ meta.shexj      (ShExJ representation of metamodel)
        |
        +------ meta.ttl        (Metamodel in RDF)
        |
        +------ meta.owl
        |
        +------ includes/
        |          |
        |          +--- mappings.context.jsonld
        |          |
        |          +--- mappings.jsonld
        |          |
        |          +--- mappings.py
        |          |
        |          +--- mappings.yaml
        |          |
        |          +--- types.context.jsonld
        |          |
        |          +--- types.jsonld
        |          |
        |          +--- types.py
        |          |
        |          +--- types.yaml
        |
        +------ linkml/
        |          |
        |           +--- meta.py
        |
        +------ meta_mappings_docs/
                  |
                  +--- abstract.md
                  |
                  +--- Element.md
                  |
                  +---    ...
                  |
                  +--- types/
                         |
                         +--- boolean.md


URI Maps:
    # Access to the root directory -- the whole project
    https://w3id.org/biolink/linkml        --> linkml
    
    # Access to the entire metamodel in various formats
    https://w3id.org/linkml/meta   --> linkml/meta   (.yaml, .shex, .ttl, .owl) -- conneg
    
    # Access to documentation on metamodel components
    https://w3id.org/linkml/meta/  --> biolink/meta_mappings_docs/
    
    # Access to the entire types model in various formats
    https://w3id.org/linkml/types  --> biolink/includes/types (.yaml, .shex, .ttl, .owl) -- conneg
    
    # Access to documentation on type components
    https://w3id.org/linkml/types/ --> biolink/meta_mappings_docs/types/



"""

METAMODEL_FILE_NAME = 'meta.yaml'
METAMODEL_LDCONTEXT_NAME = 'context.jsonld'
METAMODEL_SHEXC_NAME = 'meta.shex'
METAMODEL_SHEXJ_NAME = 'meta.shexj'
METAMODEL_RDF_NAME = 'meta.ttl'
METAMODEL_JSONLD_NAME = 'meta.jsonld'
TYPES_FILE_NAME = 'types.yaml'
TYPES_LDCONTEXT_NAME = 'types.context.jsonld'
TYPES_JSONLD_NAME = 'types.jsonld'
MAPPING_FILE_NAME = 'mappings.yaml'
MAPPING_LDCONTEXT_NAME = 'types.context.jsonld'
MAPPING_JSONLD_NAME = 'types.jsonld'


MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INCLUDES_DIR = os.path.join(MODULE_DIR, 'includes')

# Local location of yaml files
LOCAL_METAMODEL_YAML_FILE = os.path.join(MODULE_DIR, METAMODEL_FILE_NAME)
LOCAL_TYPES_YAML_FILE = os.path.join(INCLUDES_DIR, TYPES_FILE_NAME)
LOCAL_MAPPING_YAML_FILE = os.path.join(INCLUDES_DIR, MAPPING_FILE_NAME)

# Local location of jsonld and context.jsonld files
LOCAL_METAMODEL_LDCONTEXT_FILE = os.path.join(MODULE_DIR, METAMODEL_LDCONTEXT_NAME)
LOCAL_METAMODEL_JSONLD_FILE = os.path.join(MODULE_DIR, METAMODEL_JSONLD_NAME)
LOCAL_TYPES_LDCONTEXT_FILE = os.path.join(INCLUDES_DIR, TYPES_LDCONTEXT_NAME)
LOCAL_TYPES_JSONLD_FILE = os.path.join(INCLUDES_DIR, TYPES_JSONLD_NAME)
LOCAL_MAPPING_LDCONTEXT_FILE = os.path.join(INCLUDES_DIR, MAPPING_LDCONTEXT_NAME)
LOCAL_MAPPING_JSONLD_FILE = os.path.join(INCLUDES_DIR, MAPPING_JSONLD_NAME)

# Local location of metamodel shex file
LOCAL_SHEXJ_FILE_NAME = os.path.join(MODULE_DIR, METAMODEL_SHEXJ_NAME)
LOCAL_SHEXC_FILE_NAME = os.path.join(MODULE_DIR, METAMODEL_SHEXC_NAME)

# Local location of the metamodel rdf file
LOCAL_RDF_FILE_NAME = os.path.join(MODULE_DIR, METAMODEL_RDF_NAME)

# Base URI for all things meta
META_BASE_URI = 'https://w3id.org/linkml/'

# URI for the entire metamodel itself.
METAMODEL_NAME = 'metamodel'
METAMODEL_URI = META_BASE_URI + 'meta'
METATYPE_NAME = 'types'
METATYPE_URI = META_BASE_URI + METATYPE_NAME
METAMAPPING_NAME = 'mappings'
METAMAPPING_URI = META_BASE_URI + METAMAPPING_NAME

# Preferred local name for metamodel elements
METAMODEL_NAMESPACE_NAME = "meta"
METATYPE_NAMESPACE_NAME = 'metatype'
METAMAPPING_NAMESPACE_NAME = 'meta'

# Namespace for metamodel elements
METAMODEL_NAMESPACE = Namespace(METAMODEL_URI + '/')
METATYPE_NAMESPACE = Namespace(META_BASE_URI + 'meta/types/')
METAMAPPING_NAMESPACE = METAMODEL_NAMESPACE

# Metamodel Context URI
METAMODEL_CONTEXT_URI = META_BASE_URI + METAMODEL_LDCONTEXT_NAME

# Metamodel ShEx URI
METAMODEL_SHEXJ_URI = META_BASE_URI + 'meta.shexj'
METAMODEL_SHEXC_URI = META_BASE_URI + 'meta.shexc'

# Metamodel YAML file
METAMODEL_YAML_URI = META_BASE_URI + 'meta.yaml'

# Biolink model file -- this needs a more official fix
BIOLINK_MODEL_URI = "https://w3id.org/biolink/biolink-model"
BIOLINK_MODEL_PYTHON_LOC = "biolink.model"

TurtleSerializer.roundtrip_prefixes = ['']

if sys.version_info < (3, 7, 6):
    warn(f"Some URL processing will fail with python 3.7.5 or earlier.  Current version: {sys.version_info}")
