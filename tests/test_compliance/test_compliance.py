"""Constants for compliance tests. See README.md for more information."""

import pytest
import rdflib

from tests.test_compliance.helper import (
    JAVA,
    JSON_SCHEMA,
    JSONLD_CONTEXT,
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
    SHACL,
    SHEX,
    SQL_DDL_POSTGRES,
    SQL_DDL_SQLITE,
)

EXAMPLE_NS = rdflib.Namespace("http://example.org/")

SCHEMA_M1 = "M1"
CLASS_CONTAINER = "Container"
CLASS_C = "C"
CLASS_D = "D"
CLASS_D1 = "D1"
CLASS_X = "X"
CLASS_Y = "Y"
CLASS_Z = "Z"
CLASS_U1 = "U1"
CLASS_U2 = "U2"
CLASS_C1 = "C1"
CLASS_C2 = "C2"
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
ENUM_F = "F"
PV_1 = "pv1"
PV_2 = "pv2"
PV_3 = "pv3"
SUBSET_SS = "Subset1"

CORE_FRAMEWORKS = [
    pytest.param(PYTHON_DATACLASSES, marks=[pytest.mark.pythongen]),
    pytest.param(PYDANTIC, marks=[pytest.mark.pydanticgen]),
    pytest.param(JAVA, marks=[pytest.mark.javagen]),
    pytest.param(JSON_SCHEMA, marks=[pytest.mark.jsonschemagen]),
    pytest.param(SHACL, marks=[pytest.mark.shaclgen]),
    pytest.param(SHEX, marks=[pytest.mark.shexgen]),
    # JSONLD,
    pytest.param(JSONLD_CONTEXT, marks=[pytest.mark.jsonldcontextgen]),
    #    SQL_ALCHEMY_IMPERATIVE,
    #    SQL_ALCHEMY_DECLARATIVE,
    pytest.param(SQL_DDL_SQLITE, marks=[pytest.mark.sqlddlgen]),
    pytest.param(SQL_DDL_POSTGRES, marks=[pytest.mark.sqlddlpostgresgen]),
    pytest.param(OWL, marks=[pytest.mark.owlgen]),
]
