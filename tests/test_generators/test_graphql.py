import pytest

from linkml.generators.graphqlgen import GraphqlGenerator

PERSON = """
type Person implements HasAliases
  {
    id: String!
    name: String
    hasEmploymentHistory: [EmploymentEvent]
    hasFamilialRelationships: [FamilialRelationship]
    hasMedicalHistory: [MedicalEvent]
    ageInYears: Integer
    addresses: [Address]
    hasBirthEvent: BirthEvent
    speciesName: String
    stomachCount: Integer
    isLiving: LifeStatusEnum
    aliases: [String]
  }
"""

MEDICALEVENT = """
type MedicalEvent
  {
    startedAtTime: Date
    endedAtTime: Date
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
    startedAtTime: Date
    endedAtTime: Date
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
