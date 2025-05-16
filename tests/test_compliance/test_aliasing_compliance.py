"""
Tests for aliasing compliance.

Aliases include:

- the ``alias`` metaslot
- uri aliases for RDF translation: class_uri, slot_uri
"""

import pytest
import rdflib
from rdflib import URIRef

from linkml.reporting.model import RDF, RDFS
from tests.test_compliance.helper import (
    JSONLD_CONTEXT,
    OWL,
    PYDANTIC,
    PYTHON_DATACLASSES,
    ValidationBehavior,
    check_data,
    validated_schema,
)
from tests.test_compliance.test_compliance import (
    CLASS_C,
    CORE_FRAMEWORKS,
    ENUM_E,
    PV_1,
    PV_2,
    SLOT_S1,
    TYPE_T,
)

SDO_C = "schema:C"
SDO_S1 = "schema:s1"
ALIAS_S1 = "s1alias"
SDO_T = "schema:T"
SDO_E = "schema:E"
SDO_PV1 = "schema:pv1"

EX = rdflib.Namespace("http://example.org/")
SCHEMA = rdflib.Namespace("http://schema.org/")
OWLNS = rdflib.Namespace("http://www.w3.org/2002/07/owl#")


@pytest.mark.parametrize(
    "class_uri,slot_uri,slot_alias,type_uri,data_name,instance,is_valid",
    [
        (None, None, None, None, "empty", {}, True),
        (None, None, None, None, "basic", {SLOT_S1: 1}, True),
        (None, None, ALIAS_S1, None, "aliased", {ALIAS_S1: 1}, True),
        (SDO_C, SDO_S1, None, None, "uri_aliases_CS", {SLOT_S1: 1}, True),
        (None, None, None, SDO_T, "uri_aliases_T", {SLOT_S1: 1}, True),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_alias(framework, class_uri, slot_uri, slot_alias, type_uri, data_name, instance, is_valid):
    """
    Tests ability to alias slots.

    The alias metaslot allows for a different name to be used for a slot than the name of the slot.
    It is not to be confused with `aliases`.

    This test generates a class C, with a slot s1, aliased to `slot_alias`.
    s1 is of type T, which is an integer.

    Known issues:

    - PydanticGenerator does not yet support aliasing

    :param framework: framework to test
    :param class_uri: optional class URI for C
    :param slot_uri: optional slot URI for s1
    :param slot_alias: optional slot alias for s1
    :param type_uri: optional type URI for type T
    :param data_name: name of the test data
    :param instance: instance data to test
    :param is_valid: whether the instance is expected to validate
    :return:
    """
    prop_uriref = SCHEMA.s1 if slot_uri else EX.s1
    class_uriref = SCHEMA.C if class_uri else EX.C
    type_uriref = SCHEMA.T if type_uri else EX.T
    expected_slot_name = slot_alias if slot_alias else SLOT_S1
    expected_class_name = CLASS_C
    dc_type_expected = "class T(Integer):"
    if type_uri:
        dc_type_expected += "    type_class_uri = SCHEMA.T"
    else:
        dc_type_expected += "    type_class_uri = XSD.integer"
    expected_class_jsonld_context = {
        expected_class_name: {
            "@id": expected_class_name,
        },
    }
    if class_uri:
        expected_class_jsonld_context[expected_class_name]["@id"] = class_uri
    classes = {
        CLASS_C: {
            "class_uri": class_uri,
            "slots": [SLOT_S1],
            "_mappings": {
                OWL: [(class_uriref, RDF.type, OWLNS.Class)],
                PYDANTIC: f"{expected_slot_name}: Optional[int]",
                PYTHON_DATACLASSES: f"{expected_slot_name}: Optional[Union[int, T]]",
                JSONLD_CONTEXT: expected_class_jsonld_context,
            },
        },
    }
    # TODO: add typeof inference to ContextGenerator
    expected_slot_jsonld_context = {
        expected_slot_name: {
            "@id": expected_slot_name,
            "@type": type_uri if type_uri else "xsd:integer",
        },
    }
    if slot_uri:
        expected_slot_jsonld_context[expected_slot_name]["@id"] = slot_uri
    slots = {
        SLOT_S1: {
            "alias": slot_alias,
            "slot_uri": slot_uri,
            "range": TYPE_T,
            "_mappings": {
                OWL: [(prop_uriref, RDF.type, OWLNS.DatatypeProperty)],
                JSONLD_CONTEXT: expected_slot_jsonld_context,
            },
        },
    }
    types = {
        TYPE_T: {
            "uri": type_uri,
            "typeof": "integer",
            "minimum_value": 0,
            "_mappings": {
                OWL: [(type_uriref, RDF.type, RDFS.Datatype)],
            },
        }
    }

    schema = validated_schema(
        test_alias,
        f"A{slot_alias}_SU{slot_uri}_CU{class_uri}_TU{type_uri}".replace(":", "_"),
        framework,
        classes=classes,
        slots=slots,
        types=types,
        prefixes={"schema": "http://schema.org/"},
        core_elements=["alias", "class_uri", "slot_uri"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    check_data(
        schema,
        data_name,
        framework,
        instance,
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description="alias",
        exclude_rdf=slot_alias is not None,
    )


@pytest.mark.parametrize(
    "enum_uri,pv_meaning,data_name,instance,is_valid",
    [
        (None, None, "empty", {}, True),
        (None, None, "valid1", {SLOT_S1: PV_1}, True),
        (None, None, "invalid1", {SLOT_S1: "x"}, False),
        (None, SDO_PV1, "valid1", {SLOT_S1: PV_1}, True),
        (None, SDO_PV1, "invalid1", {SLOT_S1: "x"}, False),
        (SDO_E, SDO_PV1, "valid1", {SLOT_S1: PV_1}, True),
        (SDO_E, SDO_PV1, "invalid1", {SLOT_S1: "x"}, False),
    ],
)
@pytest.mark.parametrize("framework", CORE_FRAMEWORKS)
def test_enum_alias(framework, enum_uri, pv_meaning, data_name, instance, is_valid):
    """
    Tests alias metaslot on EnumDefinitions and PermissibleValues.

    :param framework:
    :param enum_uri:
    :param pv_meaning:
    :param data_name:
    :param instance:
    :param is_valid:
    :return:
    """
    enum_uriref = SCHEMA.E if enum_uri else EX.E
    pv_uriref = SCHEMA.pv1 if pv_meaning else URIRef("http://example.org/E#pv1")
    classes = {
        CLASS_C: {
            "slots": [SLOT_S1],
        },
    }
    slots = {
        SLOT_S1: {
            "range": ENUM_E,
        },
    }
    enums = {
        ENUM_E: {
            "enum_uri": enum_uri,
            "permissible_values": {
                PV_1: {
                    "meaning": pv_meaning,
                },
                PV_2: {},
            },
            "_mappings": {
                OWL: [
                    (enum_uriref, RDF.type, OWLNS.Class),
                    (pv_uriref, RDF.type, OWLNS.Class),  # May change
                ],
            },
        }
    }

    schema = validated_schema(
        test_enum_alias,
        f"E{enum_uri}_PV{pv_meaning}".replace(":", "_"),
        framework,
        classes=classes,
        slots=slots,
        enums=enums,
        prefixes={"schema": "http://schema.org/"},
        core_elements=["alias", "class_uri", "slot_uri"],
    )
    expected_behavior = ValidationBehavior.IMPLEMENTS
    check_data(
        schema,
        data_name,
        framework,
        instance,
        is_valid,
        target_class=CLASS_C,
        expected_behavior=expected_behavior,
        description="alias_enum",
        # exclude_rdf=pv_meaning is not None, ## TODO
    )
