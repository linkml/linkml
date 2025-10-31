"""
Tests for aliasing compliance.

Aliases include:

- the ``alias`` metaslot
- uri aliases for RDF translation: class_uri, slot_uri
"""

import pytest
import rdflib

from tests.test_compliance.helper import (
    JSONLD_CONTEXT,
    PANDERA_POLARS_CLASS,
    SHACL,
    SQL_DDL_SQLITE,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C,
    CLASS_D,
    CLASS_D1,
    CORE_FRAMEWORKS,
    SCHEMA_M1,
    SLOT_S1,
    SLOT_S2,
    SLOT_S3,
    TYPE_T,
)

SDO_C = "schema:C"
SDO_D = "schema:D"
SDO_S1 = "schema:s1"
ALIAS_S1 = "s1alias"
ALIAS_S2 = "s2alias"
SDO_T = "schema:T"
SDO_E = "schema:E"
SDO_PV1 = "schema:pv1"

EX = rdflib.Namespace("http://example.org/")
SCHEMA = rdflib.Namespace("http://schema.org/")
OWLNS = rdflib.Namespace("http://www.w3.org/2002/07/owl#")

SKIP_JSONLD_CONTEXT = True


@pytest.mark.parametrize(
    "class_c_uri,class_d_uri,slot_1_uri,slot_2_uri,slot_1_alias,slot_2_alias,type_uri,data_name,instance,is_valid",
    [
        (None, None, None, None, None, None, None, "empty", {}, True),
        (None, None, None, None, None, None, None, "basic", {SLOT_S1: 1}, True),
        (None, None, None, None, None, None, None, "basic_viol", {SLOT_S1: "x"}, False),
        (None, SDO_D, SDO_S1, None, None, None, None, "uri_aliases_CS", {SLOT_S1: 1}, True),
        (None, None, None, None, None, None, SDO_T, "uri_aliases_T", {SLOT_S1: 1}, True),
        (None, None, None, None, ALIAS_S1, None, None, "aliased_s1", {ALIAS_S1: 1}, True),
        (None, None, None, None, ALIAS_S1, None, None, "aliased_s1_viol", {SLOT_S1: 1}, False),
        (None, None, None, None, None, ALIAS_S2, None, "aliased_s2", {ALIAS_S2: {SLOT_S3: "x"}}, True),
        (
            None,
            None,
            None,
            None,
            ALIAS_S1,
            ALIAS_S2,
            None,
            "aliased_s1_s2",
            {ALIAS_S1: 1, ALIAS_S2: {SLOT_S3: "x"}},
            True,
        ),
        (None, None, None, None, ALIAS_S2, ALIAS_S2, None, "conflict_s2", {ALIAS_S2: {SLOT_S3: "x"}}, True),
        (SDO_C, SDO_C, None, None, None, None, None, "conflict_c", {SLOT_S1: 1}, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_import(
    framework,
    class_c_uri,
    class_d_uri,
    slot_1_uri,
    slot_2_uri,
    slot_1_alias,
    slot_2_alias,
    type_uri,
    data_name,
    instance,
    is_valid,
):
    """
    Tests import.

    This test creates an imported module M1 with a class C and a slot s1.
    The main schema imports M1 and adds a class D that extends C and adds a slot s2.

    all classes and slots are potentially aliased and given alternate primary URIs.

    The following do not support non-merged-imports:

    - pydantic
    - jsonschema
    - jsonld-context

    :param framework: framework to test
    :param class_d_uri: optional class URI for C
    :param slot_2_uri: optional slot URI for s1
    :param slot_2_alias: optional slot alias for s1
    :param type_uri: optional type URI for type T
    :param data_name: name of the test data
    :param instance: instance data to test
    :param is_valid: whether the instance is expected to validate
    :return:
    """
    imported_schema = {
        "id": f"http://example.org/{SCHEMA_M1}",
        "name": SCHEMA_M1,
        "imports": ["linkml:types"],
        "prefixes": {
            "linkml": "https://w3id.org/linkml/",
            SCHEMA_M1: f"http://example.org/{SCHEMA_M1}/",
        },
        "default_prefix": SCHEMA_M1,
        "description": "Test imported schema",
        "classes": {
            CLASS_C: {
                "slots": [SLOT_S1],
                "class_uri": class_c_uri,
            }
        },
        "slots": {
            SLOT_S1: {
                "range": TYPE_T,
                "alias": slot_1_alias,
                "slot_uri": slot_1_uri,
            },
        },
        "types": {
            TYPE_T: {
                "uri": type_uri,
                "typeof": "integer",
                "minimum_value": 0,
            },
        },
    }
    classes = {
        CLASS_D1: {
            "attributes": {
                SLOT_S3: {
                    "range": "string",
                }
            },
        },
        CLASS_D: {
            "is_a": CLASS_C,
            "class_uri": class_d_uri,
            "slots": [SLOT_S2],
        },
    }
    slots = {
        SLOT_S2: {
            "range": CLASS_D1,
            "alias": slot_2_alias,
            "slot_uri": slot_2_uri,
        },
    }
    expected_jsonld_context = {}
    if not SKIP_JSONLD_CONTEXT:
        if slot_1_alias:
            expected_jsonld_context[slot_1_alias] = {
                "@type": "xsd:integer",
                "@id": slot_1_uri if slot_1_uri else f"{SCHEMA_M1}:{SLOT_S2}",  # TODO
            }
    mappings = {
        JSONLD_CONTEXT: expected_jsonld_context,
    }
    schema_name = (
        f"S1A{slot_1_alias}_S2A{slot_2_alias}"
        f"_SU1{slot_1_uri}_SU2{slot_2_uri}_CUC{class_c_uri}_CUD{class_d_uri}"
        f"_TU{type_uri}"
    ).replace(":", "_")
    schema = validated_schema(
        test_import,
        schema_name,
        framework,
        imports=["linkml:types", SCHEMA_M1],
        imported_schemas=[imported_schema],
        classes=classes,
        slots=slots,
        prefixes={"schema": "http://schema.org/"},
        core_elements=["alias", "class_uri", "slot_uri"],
        mappings=mappings,
        merge_type_imports=False,
    )
    if data_name == "conflict_s2":
        pytest.skip("Behavior TBD")
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework == PANDERA_POLARS_CLASS:
        expected_behavior = ValidationBehavior.INCOMPLETE
    check_data(
        schema,
        data_name,
        framework,
        instance,
        is_valid,
        target_class=CLASS_D,
        expected_behavior=expected_behavior,
        description="alias",
        exclude_rdf=True,
    )


@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.skip("Not yet implemented")
def test_import_name_clash(framework):
    """
    Tests import with clashing names.


    :return:
    """
    imported_schema = {
        "id": f"http://example.org/{SCHEMA_M1}",
        "name": SCHEMA_M1,
        "imports": ["linkml:types"],
        "prefixes": {
            "linkml": "https://w3id.org/linkml/",
            SCHEMA_M1: f"http://example.org/{SCHEMA_M1}/",
        },
        "default_prefix": SCHEMA_M1,
        "description": "Test imported schema",
        "classes": {
            CLASS_C: {
                "slots": [SLOT_S1],
            }
        },
        "slots": {
            SLOT_S1: {
                "range": TYPE_T,
            },
        },
        "types": {
            TYPE_T: {
                "minimum_value": 0,
            },
        },
    }
    slots = {
        SLOT_S1: {
            "range": "string",
        },
    }
    classes = {
        CLASS_C: {
            # "is_a": CLASS_C,
            "slots": [SLOT_S1],
        },
    }

    schema_name = "name_clash"
    schema = validated_schema(
        test_import_name_clash,
        schema_name,
        framework,
        imports=["linkml:types", SCHEMA_M1],
        imported_schemas=[imported_schema],
        classes=classes,
        slots=slots,
        prefixes={"schema": "http://schema.org/"},
        core_elements=["import"],
        merge_type_imports=False,
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    data_name = "t"
    instance = {SLOT_S1: "x"}
    check_data(
        schema,
        data_name,
        framework,
        instance,
        True,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description="alias",
        exclude_rdf=True,
    )


@pytest.mark.network
@pytest.mark.slow
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
@pytest.mark.parametrize("valid", [True, False])
def test_import_metamodel(framework, valid):
    """
    Tests importing the metamodel works.
    :return:
    """
    root_class_name = "DerivedSchema"
    slots = {
        SLOT_S1: {
            "range": "string",
            "required": True,
        },
    }
    classes = {
        root_class_name: {
            "is_a": "schema_definition",
            "slots": [SLOT_S1],
        },
    }

    schema_name = "default"
    if framework == SHACL:
        pytest.skip("https://github.com/linkml/linkml/pull/2014")
    schema = validated_schema(
        test_import_metamodel,
        schema_name,
        framework,
        imports=["linkml:meta", "linkml:meta"],
        classes=classes,
        slots=slots,
        prefixes={"schema": "http://schema.org/"},
        core_elements=["import"],
        merge_type_imports=False,
    )
    if framework == SQL_DDL_SQLITE:
        pytest.skip("sqla issue")
    expected_behavior = ValidationBehavior.IMPLEMENTS
    if framework == PANDERA_POLARS_CLASS:
        expected_behavior = ValidationBehavior.INCOMPLETE
    data_name = f"my_derived_schema_{valid}"
    instance = {
        "id": f"http://example.org/my-derived-schema-{valid}",
        "name": data_name,
    }
    if valid:
        instance[SLOT_S1] = "x"
    check_data(
        schema,
        data_name,
        framework,
        instance,
        valid,
        target_class=root_class_name,
        expected_behavior=expected_behavior,
        description="alias",
        exclude_rdf=True,
    )
