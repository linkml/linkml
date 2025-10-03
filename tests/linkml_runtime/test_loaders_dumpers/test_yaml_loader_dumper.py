import os

import pytest
import yaml.constructor

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader
from tests.test_loaders_dumpers import INPUT_DIR
from tests.test_loaders_dumpers.models.model_817 import Container, Person, PersonNoId, VitalStatusEnum


def test_normalise_inline_as_list() -> None:
    # see https://github.com/linkml/linkml/issues/817
    person = Person(id="x", name="x", vital_status=VitalStatusEnum("LIVING"))
    person2 = Person(id="y", name="y", vital_status=VitalStatusEnum("DEAD"))
    thing = PersonNoId(name="z", vital_status=VitalStatusEnum("LIVING"))
    c = Container(
        persons_as_list=[person, person2],
        persons_as_dict={person.id: person, person2.id: person2},
        single_person_inlined=person,
        noidobj_as_list=[thing],
        single_noidobj_inlined=thing,
    )
    s = yaml_dumper.dumps(c)
    c2 = yaml_loader.loads(s, Container)
    assert c2.persons_as_list == c.persons_as_list
    assert c2.persons_as_dict == c.persons_as_dict
    assert c2.noidobj_as_list == c.noidobj_as_list


def test_yaml_loader_error_includes_file_name() -> None:
    """Ensure the filename is reported when loading fails.

    see https://github.com/linkml/linkml/issues/1040

    issue_1040.yaml has a parsing error is confusing as all getout when accompanied by a stack
    trace.  We use this to make sure that the file name gets in correctly."""
    schema_file = os.path.join(INPUT_DIR, "issue_1040.yaml")

    with pytest.raises(yaml.constructor.ConstructorError, match='"issue_1040.yaml"'):
        yaml_loader.load(schema_file, SchemaDefinition)
