import yaml
from linkml_runtime.dumpers import yaml_dumper
from pydantic.version import VERSION
from sqlalchemy.orm import sessionmaker

from linkml.utils.sqlutils import SQLStore
from tests.utils.dict_comparator import compare_yaml


def test_enums(person_pydantic):
    """
    Tests that enum objects can be constructed inlined.

    See https://github.com/linkml/linkml/issues/817
    """
    person_pydantic.FamilialRelationship(type="SIBLING_OF", related_to="x")
    p = person_pydantic.Person(id="x", gender=person_pydantic.GenderType("cisgender_man"))
    assert isinstance(p.gender, str)


def test_sqlite_store(person, person_pydantic, tmp_outputs):
    """
    tests a complete end-to-end example with a dump-load cycle
    """
    # step 1: setup
    # TODO: currently it is necessary to pass the actual yaml rather than a schema object
    # endpoint = SQLiteEndpoint(sv.schema, database_path=DB, include_schema_in_database=False)
    mod = person_pydantic
    endpoint = SQLStore(person["schema"], database_path=tmp_outputs["db"], include_schema_in_database=False)
    endpoint.native_module = mod
    endpoint.db_exists(force=True)

    # step 2: load data from file and store in SQLStore
    # TODO: use yaml_loader once this supports pydantic
    with open(person["data"]) as file:
        dict_obj = yaml.safe_load(file)
    container = mod.Container(**dict_obj)
    endpoint.dump(container)

    # step 3: test query using SQL Alchemy
    session_class = sessionmaker(bind=endpoint.engine)
    session = session_class()
    q = session.query(endpoint.module.Person)
    all_objs = q.all()
    assert 2 == len(all_objs)
    q = session.query(endpoint.module.FamilialRelationship)

    # step 4: test loading from SQLStore
    # 4a: first test load_all, diff to original data should be empty
    [returned_container] = endpoint.load_all(target_class=mod.Container)

    if VERSION[0] == "1":
        returned_dict = returned_container.dict(exclude_none=True)
    else:
        returned_dict = returned_container.model_dump(exclude_none=True)

    # Fix when this is fixed https://github.com/linkml/linkml/issues/999
    with open(tmp_outputs["data"], "w") as stream:
        yaml.dump(returned_dict, stream)
    diff = compare_yaml(person["data"], tmp_outputs["data"], remove_empty=True)
    assert diff == ""

    # 4b: next test load implicit object, diff to original data should be empty
    container_loaded = endpoint.load()
    yaml_dumper.dump(container_loaded, to_file=tmp_outputs["data"])
    yaml_dumper.dumps(container_loaded)
    diff = compare_yaml(person["data"], tmp_outputs["data"], remove_empty=True)
    assert diff == ""
