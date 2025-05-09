from linkml.generators.owlgen import OwlSchemaGenerator


def test_cardinalities(input_path, snapshot):
    output = OwlSchemaGenerator(input_path("owl1.yaml")).serialize()
    assert output == snapshot("owl1.owl")


def test_pred_types(input_path, snapshot):
    output = OwlSchemaGenerator(input_path("owl2.yaml")).serialize()
    assert output == snapshot("owl2.owl")
