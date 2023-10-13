"""Constants for compliance tests. See README.md for more information."""
from tests.test_compliance.helper import (
    JSON_SCHEMA,
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SHACL,
    SHEX,
    SQL_DDL_POSTGRES,
    SQL_DDL_SQLITE,
)

CLASS_CONTAINER = "Container"
CLASS_C = "C"
CLASS_D = "D"
CLASS_X = "X"
CLASS_Y = "Y"
CLASS_U1 = "U1"
CLASS_U2 = "U2"
CLASS_C1 = "C1"
CLASS_C1a = "C1a"
CLASS_C1b = "C1b"
CLASS_C1a1 = "C1a1"
CLASS_C1a2 = "C1a2"
CLASS_C2a1 = "C2a1"
CLASS_C2a2 = "C2a2"
CLASS_ANY = "Any"
CLASS_MC1 = "MC1"
CLASS_MC2 = "MC2"
SLOT_ID = "id"
SLOT_TYPE = "type"
SLOT_S1 = "s1"
SLOT_S2 = "s2"
SLOT_S3 = "s3"
SLOT_S4 = "s4"
SLOT_ID = "id"
SLOT_S1a = "s1a"
SLOT_S1b = "s1b"
EXAMPLE_STRING_VALUE_1 = "foo"
EXAMPLE_STRING_VALUE_2 = "bar"
EXAMPLE_STRING_VALUE_3 = "fuz"
EXAMPLE_STRING_VALUE_4 = "erk"
TYPE_T = "T"
ENUM_E = "E"
PV_1 = "pv1"
PV_2 = "pv2"
SUBSET_SS = "Subset1"

CORE_FRAMEWORKS = [
    PYTHON_DATACLASSES,
    PYDANTIC,
    JSON_SCHEMA,
    SHACL,
    SHEX,
    #    SQL_ALCHEMY_IMPERATIVE,
    #    SQL_ALCHEMY_DECLARATIVE,
    SQL_DDL_SQLITE,
    SQL_DDL_POSTGRES,
    OWL,
]
