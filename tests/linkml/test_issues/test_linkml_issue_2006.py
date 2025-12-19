from linkml.generators import SQLTableGenerator

schema_yaml = """
id: https://examples.org/my-schema
prefixes:
  linkml: https://w3id.org/linkml/
  myschema: https://examples.org/my-schema
imports:
  - linkml:types
default_prefix: myschema
default_range: string

classes:
  MyClass:
    slots:
      - my_slot
    unique_keys:
      identifier:
        unique_key_slots:
          - my_slot

slots:
  my_slot:
    multivalued: true
    range: string
"""


def test_uniqueness_constraint_on_multivalued():
    """See https://github.com/linkml/linkml/issues/2006"""
    gen = SQLTableGenerator(schema_yaml)
    output = gen.serialize()
    assert "MyClass_my_slot" in output, "expected backref for multivalued"
    # the uniqueness constraint is necessarily dropped since it can't
    # be directly represented in SQL after relmodel transformation
    assert "unique" not in output.lower(), "expected MV uniqueness constraint to be dropped"
