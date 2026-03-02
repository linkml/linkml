import logging

import pytest
from graphql import parse

from linkml.generators.graphqlgen import GraphqlGenerator

logger = logging.getLogger(__name__)

PERSON = """
type Person implements HasAliases
  {
    id: String!
    name: String
    hasEmploymentHistory: [EmploymentEvent]
    hasFamilialRelationships: [FamilialRelationship]
    hasMedicalHistory: [MedicalEvent]
    ageInYears: Int
    addresses: [Address]
    hasBirthEvent: BirthEvent
    speciesName: String
    stomachCount: Int
    isLiving: LifeStatusEnum
    aliases: [String]
  }
"""

MEDICALEVENT = """
type MedicalEvent
  {
    startedAtTime: String
    endedAtTime: String
    isCurrent: Boolean
    metadata: AnyObject
    inLocation: Place
    diagnosis: DiagnosisConcept
    procedure: ProcedureConcept
  }
"""

FAMILIALRELATIONSHIP = """
type FamilialRelationship
  {
    startedAtTime: String
    endedAtTime: String
    cordialness: String
    type: FamilialRelationshipType!
    relatedTo: Person!
  }
"""

DATASET = """
type Dataset
  {
    metadata: AnyObject
    persons: [Person]
    companies: [Company]
    activities: [Activity]
    codeSystems: [CodeSystem]
  }
"""

FAMILIALRELATIONSHIPTYPE = """
enum FamilialRelationshipType
  {
    SIBLING_OF
    PARENT_OF
    CHILD_OF
  }
"""


@pytest.mark.parametrize(
    "input_class,expected",
    [
        # check that expected GraphQL schema blocks are present
        ("Person", PERSON),
        ("Dataset", DATASET),
        ("MedicalEvent", MEDICALEVENT),
        ("FamilialRelationship", FAMILIALRELATIONSHIP),
        ("FamilialRelationshipType", FAMILIALRELATIONSHIPTYPE),
    ],
)
def test_serialize_selected(input_class, expected, kitchen_sink_path):
    """Test serialization of select GraphQL schema from schema."""
    generator = GraphqlGenerator(kitchen_sink_path)
    graphql = generator.serialize(classes=[input_class])

    # check that the expected blocks are present
    assert expected in graphql


def test_snapshot(kitchen_sink_path, snapshot):
    generator = GraphqlGenerator(kitchen_sink_path)
    generated = generator.serialize()
    assert generated == snapshot("kitchen_sink.graphql")


def test_graphql_validity(kitchen_sink_path):
    generator = GraphqlGenerator(kitchen_sink_path)
    generated = generator.serialize()
    logger.info("\nGenerated GraphQL schema:")
    logger.info("vvvvvv Start GraphQL vvvvvv")
    logger.info(generated)
    logger.info("^^^^^^^ End GraphQL ^^^^^^^")
    try:
        parse(generated)
    except Exception as ex:
        pytest.fail(
            "Generated GraphQL appears to be wrong, it cannot be parsed!\n"
            + "vvvvvv Start Error Message vvvvvv\n"
            + f"{str(ex)}\n"
            + "^^^^^^^ End Error Message ^^^^^^^"
        )
