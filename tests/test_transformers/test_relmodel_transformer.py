from linkml_runtime import SchemaView

from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from linkml.utils.schema_builder import SchemaBuilder


def test_nested_key():
    """
    Test that the nested key is correctly handled

    Expected:

    ```yaml
    ExamResult:
        attributes:
          name:
            key: true
            range: string
            required: true
          score:
            range: integer
          additional_info:
            range: string
          Student_id:
            annotations:
              backref:
                tag: backref
                value: 'true'
              rdfs:subPropertyOf:
                tag: rdfs:subPropertyOf
                value: rdf:subject
              primary_key:
                tag: primary_key
                value: 'true'
              foreign_key:
                tag: foreign_key
                value: Student.id
            description: Autocreated FK slot
            slot_uri: rdf:subject
            range: Student
        unique_keys:
          Student_name:
            unique_key_slots:
            - Student_id
            - name
    """
    sb = SchemaBuilder()
    sb.add_slot("id", identifier=True)
    sb.add_slot("full_name")
    sb.add_slot("exam_results", range="ExamResult", multivalued=True, inlined=True)
    sb.add_slot("name", key=True)
    sb.add_slot("score", range="integer")
    sb.add_class("Student", ["id", "full_name", "exam_results"])
    sb.add_class("ExamResult", ["name", "score", "additional_info"])
    sb.add_defaults()
    schema = sb.schema
    rmt = RelationalModelTransformer()
    rmt.schemaview = SchemaView(schema)
    result = rmt.transform("test")
    rel_schema = result.schema
    exam_result = rel_schema.classes["ExamResult"]
    assert exam_result
    exam_result_atts = exam_result.attributes
    student_id = exam_result_atts["Student_id"]
    assert student_id.range == "Student"
    assert not student_id.multivalued
    unique_keys = list(exam_result.unique_keys.values())
    assert len(unique_keys) == 1
    unique_key = unique_keys[0]
    assert sorted(unique_key.unique_key_slots) == ["Student_id", "name"]
