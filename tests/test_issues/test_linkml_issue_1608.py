import importlib
import os

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators import PythonGenerator
from linkml.validators import JsonSchemaDataValidator

schema_file = "input/linkml_issue_1608_schema.yaml"
data_file = "input/linkml_issue_1608_data.yaml"
# output_dir = "../output"
schema_python_source_file_name = "linkml_issue_1608_schema.py"
model_dir = "model"
schema_python_source_file_path = os.path.join(model_dir, schema_python_source_file_name)


def test_heterogeneous_collection():
    # read a schema YAML file and prepare for compilation to python
    pg = PythonGenerator(schema_file)
    # compile the YAML to python, in a string
    python_source_text = pg.serialize()
    # write the generated python string to a file
    with open(schema_python_source_file_path, 'w') as f:
        f.write(python_source_text)
    # dynamically import the generated python module into this namespace
    database_class = getattr(importlib.import_module("tests.test_issues.model.linkml_issue_1608_schema"), "Database")

    # read a YAML data file and instantiate it against the dynamically loaded Database class
    # this performs SOME validation
    database_instance = yaml_loader.loads(data_file, target_class=database_class)

    print("\n")
    print(yaml_dumper.dumps(database_instance))

    # additional validation if necessary
    jv = JsonSchemaDataValidator(schema_file)
    jv.validate_object(database_instance, target_class=database_class)
