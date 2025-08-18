from linkml_runtime.loaders import yaml_loader

from linkml.validator.validator import Validator
from tests.test_generators.test_pythongen import make_python


def test_validate_person_instance_from_personinfo(input_path, personinfo_path):
    personinfo_python = make_python(personinfo_path)

    # Path to instance YAML file which contains one instance of Person class
    # from personinfo schema
    instance_path = input_path("personinfo_person_inst_01.yaml")

    # Load Person instance
    instance_data = yaml_loader.load(instance_path, target_class=personinfo_python.Person)

    # Initialize validator with personinfo schema
    validator = Validator(personinfo_path)

    # Validate Person instance against personinfo schema using validator
    validation_results = validator.validate(instance_data, target_class=personinfo_python.Person)

    # Check that no errors are captured in the returned ValidationReport
    assert validation_results.results == []
