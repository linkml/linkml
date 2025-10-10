import os

import pytest

import tests.test_index.model.container_test as src_dm
from linkml_runtime.index.object_index import ObjectIndex, ProxyObject
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.inference_utils import Config, infer_slot_value
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_index import INPUT_DIR

SCHEMA = os.path.join(INPUT_DIR, "container_test.yaml")
DATA = os.path.join(INPUT_DIR, "object-indexer-data.yaml")


@pytest.fixture
def schema_view():
    """SchemaView instance for container test schema."""
    return SchemaView(SCHEMA)


@pytest.fixture
def container():
    """Load container test data."""
    return yaml_loader.load(DATA, target_class=src_dm.Container)


@pytest.fixture
def object_index(container, schema_view):
    """ObjectIndex instance for testing."""
    return ObjectIndex(container, schemaview=schema_view)


def test_object_index(schema_view, container, object_index):
    """Test object indexing functionality."""
    # Test domain object
    frt = container.persons[0].has_familial_relationships[0].type
    assert isinstance(frt, src_dm.FamilialRelationshipType)

    # Test index initialization
    oix = object_index
    assert oix.proxy_object_cache_size == 0
    assert oix.source_object_cache_size > 4

    # Test basic lookups
    proxy_obj = oix.bless(container)
    # Proxy objects mock the domain object class, plus they also instantiate ProxyObject
    assert isinstance(proxy_obj, ProxyObject)
    assert isinstance(proxy_obj, src_dm.Container)

    proxy_obj = oix.bless(container.persons[0])
    assert isinstance(proxy_obj, ProxyObject)
    assert isinstance(proxy_obj, src_dm.Person)

    # Test basic attributes
    v = proxy_obj.name
    assert v == "fred bloggs"
    assert proxy_obj.age_in_years == 33
    assert sorted(proxy_obj.aliases) == sorted(["a", "b"])

    # Test address proxy
    addr = proxy_obj.current_address
    assert isinstance(addr, ProxyObject)
    assert isinstance(addr, src_dm.Address)
    assert addr.street == "1 oak street"

    # Test familial relationships
    assert isinstance(proxy_obj.has_familial_relationships, list)
    fr = proxy_obj.has_familial_relationships[0]
    assert isinstance(fr, ProxyObject)

    # Test automatic dereferencing - related_to is *not* inlined in the schema
    assert fr.related_to.name == "Alison Wu"
    assert isinstance(fr.type, src_dm.FamilialRelationshipType)
    assert fr.related_to.age_in_years is None
    assert isinstance(fr.related_to, ProxyObject)
    assert len(proxy_obj.has_medical_history) == 2

    # Test recursive relationships
    fr2 = fr.related_to.has_familial_relationships[0]
    assert fr2.related_to.name == "fred bloggs"
    assert fr2.related_to.age_in_years == 33
    assert isinstance(fr2.related_to, ProxyObject)

    fr3 = fr2.related_to.has_familial_relationships[0]
    assert isinstance(fr3.related_to, ProxyObject)
    assert fr3.related_to.name == "Alison Wu"

    # Test cache behavior
    assert oix.proxy_object_cache_size > 1
    assert oix.proxy_object_cache_size < 9
    oix.clear_proxy_object_cache()
    assert oix.proxy_object_cache_size == 0

    # Test that attributes are closed
    with pytest.raises(ValueError):
        v = proxy_obj.fake_attribute

    # Test setting attributes affects shadowed object
    proxy_obj.age_in_years = 44
    assert proxy_obj.age_in_years == 44
    assert container.persons[0].age_in_years == 44

    # Test evaluation of expressions
    assert oix.eval_expr("5") == 5
    assert oix.eval_expr("2*2+1") == 5
    assert oix.eval_expr("persons", container)[0].id == "P:001"
    assert oix.eval_expr("persons[0].id", container) == "P:001"
    assert oix.eval_expr("persons", container) == oix.eval_expr("persons")

    person = oix.eval_expr("persons")[0]
    assert isinstance(oix.bless(container).persons[0], ProxyObject)
    assert isinstance(person, ProxyObject)
    assert oix.eval_expr("current_address.street", person) == "1 oak street"
    assert oix.eval_expr("has_familial_relationships[0].related_to.name", person) == "Alison Wu"

    # Test experimental reverse direction
    assert oix.eval_expr("persons[0]._parents[0][1].persons[0].id") == "P:001"
    assert oix.eval_expr("persons[0].persons__inverse[0].persons[0].id") == "P:001"

    # Test inference
    config = Config(use_expressions=True)
    infer_slot_value(person, "description", schemaview=schema_view, class_name="Person", config=config)
    assert person.description == "name: fred bloggs address: 1 oak street"
