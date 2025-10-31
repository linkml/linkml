from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators import PythonGenerator
from linkml.validators import JsonSchemaDataValidator


def test_heterogeneous_collection(input_path):
    # read a schema YAML file and prepare for compilation to python
    # pg = PythonGenerator(schema_file)
    pg = PythonGenerator(input_path("linkml_issue_1608_schema.yaml"))

    # compile the YAML to python, in a string
    python_source_text = pg.serialize()

    module = compile_python(python_source_text)

    # read a YAML data file and instantiate it against the generated/serialized/compiled Database class
    # this performs SOME validation
    database_instance = yaml_loader.loads(input_path("linkml_issue_1608_data.yaml"), target_class=module.Database)

    # print("\n")
    # print(yaml_dumper.dumps(database_instance))

    # additional validation if necessary
    jv = JsonSchemaDataValidator(input_path("linkml_issue_1608_schema.yaml"))
    jv.validate_object(database_instance, target_class=module.Database)
