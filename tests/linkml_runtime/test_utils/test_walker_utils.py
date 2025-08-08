import os
from copy import deepcopy

from jsonasobj2 import as_dict

from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.walker_utils import traverse_object_tree
from linkml_runtime.utils.yamlutils import YAMLRoot
from tests.test_utils import INPUT_DIR

SCHEMA = os.path.join(INPUT_DIR, "kitchen_sink_noimports.yaml")
INSERTED_COMMENT = "INSERTED COMMENT"

yaml_loader = YAMLLoader()


def count_classes(obj: YAMLRoot) -> int:
    """
    An example utility function

    :param obj:
    :return: count
    """
    n_classes = 0

    def collect(in_obj: YAMLRoot):
        nonlocal n_classes
        if isinstance(in_obj, ClassDefinition):
            n_classes += 1
        return in_obj

    traverse_object_tree(obj, collect)
    return n_classes


def test_collector():
    """
    Tests using a transformer to collect statistics on an object
    """
    # use the schema as a data object
    obj = yaml_loader.load(SCHEMA, target_class=SchemaDefinition)
    orig = deepcopy(obj)
    n_classes = 0

    def collect(in_obj: YAMLRoot):
        nonlocal n_classes
        if isinstance(in_obj, ClassDefinition):
            n_classes += 1
        return in_obj

    obj_tr = traverse_object_tree(obj, collect)
    assert n_classes > 1
    # test object is not mutated
    assert orig == obj
    # test transformed object is same as input
    assert obj_tr == obj
    assert count_classes(obj) == n_classes


def test_mutating_transformer():
    """
    Tests using transform_object_tree to apply changes
    """
    # use the schema as a data object
    obj = yaml_loader.load(SCHEMA, target_class=SchemaDefinition)
    orig = deepcopy(obj)
    n_changes = 0

    def tr(in_obj: YAMLRoot):
        nonlocal n_changes
        if isinstance(in_obj, ClassDefinition):
            in_obj.comments.append(INSERTED_COMMENT)
            n_changes += 1
        return in_obj

    obj_tr = traverse_object_tree(obj, tr)
    assert n_changes > 1
    assert orig != obj
    assert obj_tr == obj
    obj = SchemaDefinition(**as_dict(obj))
    assert INSERTED_COMMENT in obj.classes["Person"].comments


def test_non_mutating_transformer():
    """
    Tests using transform_object_tree to apply changes
    """
    # use the schema as a data object
    obj = yaml_loader.load(SCHEMA, target_class=SchemaDefinition)
    orig = deepcopy(obj)
    n_changes = 0

    def tr(in_obj: YAMLRoot):
        nonlocal n_changes
        if isinstance(in_obj, ClassDefinition):
            in_obj.comments.append(INSERTED_COMMENT)
            n_changes += 1
        return in_obj

    obj_tr = traverse_object_tree(obj, tr, mutate=False)
    assert n_changes > 1
    # check does not mutate
    assert orig == obj
    # check new object is different
    assert obj_tr != orig
    assert obj_tr != obj
    obj_tr = SchemaDefinition(**as_dict(obj_tr))
    assert INSERTED_COMMENT in obj_tr.classes["Person"].comments
