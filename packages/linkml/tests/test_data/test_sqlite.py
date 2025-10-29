import csv

import pytest
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.loaders import csv_loader, yaml_loader
from sqlalchemy.orm import sessionmaker

from linkml.utils.schema_builder import SchemaBuilder
from linkml.utils.schema_fixer import SchemaFixer
from linkml.utils.sqlutils import SQLStore
from tests.utils.dict_comparator import compare_objs, compare_yaml


def test_sqlite_store(person, person_python, tmp_outputs):
    """
    tests a complete end-to-end example with a dump-load cycle
    """
    # step 1: setup
    # TODO: currently it is necessary to pass the actual yaml rather than a schema object
    # endpoint = SQLiteEndpoint(sv.schema, database_path=DB, include_schema_in_database=False)
    endpoint = SQLStore(person["schema"], database_path=tmp_outputs["db"], include_schema_in_database=False)
    endpoint.compile()
    endpoint.native_module = person_python
    endpoint.db_exists(force=True)
    # step 2: load data from file and store in SQLStore
    container = yaml_loader.load(person["data"], target_class=person_python.Container)
    endpoint.dump(container)

    # step 3: test query using SQL Alchemy
    session_class = sessionmaker(bind=endpoint.engine)
    session = session_class()
    q = session.query(endpoint.module.Person)
    all_objs = q.all()
    assert 2 == len(all_objs)
    session.close()

    # step 4: test loading from SQLStore
    # 4a: first test load_all, diff to original data should be empty
    x = endpoint.load_all(target_class=person_python.Container)
    y = yaml_dumper.dumps(x[0])
    with open(tmp_outputs["data"], "w") as stream:
        stream.write(y)
    diff = compare_yaml(person["data"], tmp_outputs["data"])
    assert diff == ""

    # 4b: next test load implicit object, diff to original data should be empty
    container_loaded = endpoint.load()
    endpoint.engine.dispose()
    yaml_dumper.dump(container_loaded, to_file=tmp_outputs["data"])
    diff = compare_yaml(person["data"], tmp_outputs["data"])
    assert diff == ""


def test_mixin(tmp_outputs):
    b = SchemaBuilder()
    b.add_defaults()
    b.add_slot(SlotDefinition("ref_to_c1", range="my_class1", multivalued=True))
    b.add_class("my_mixin", slots=["my_mixin_slot"], mixin=True)
    b.add_class("my_abstract", slots=["my_abstract_slot"], abstract=True)
    b.add_class("my_class1", is_a="my_abstract", mixins=["my_mixin"])
    b.add_class("my_class2", slots=["ref_to_c1"])
    endpoint = SQLStore(b.schema, database_path=tmp_outputs["db"])
    endpoint.db_exists(force=True)
    mod = endpoint.compile_native()
    i1 = mod.MyClass1(my_mixin_slot="v1", my_abstract_slot="v2")
    i2 = mod.MyClass2(ref_to_c1=i1)
    endpoint.dump(i2)
    i2_recap = endpoint.load(target_class=mod.MyClass2)
    diff = compare_objs(i2, i2_recap)
    assert diff == ""


@pytest.mark.parametrize("diff", [1, -1])
@pytest.mark.parametrize("size", [20, 200000])
def test_csv_limit(tmp_outputs, diff, size):
    """
    Tests https://github.com/linkml/linkml/issues/815
    """
    b = SchemaBuilder()
    b.add_class("Person", ["name"]).add_defaults()
    schema = b.schema
    sf = SchemaFixer()
    sf.add_container(schema)
    csv.field_size_limit(size)
    name = "N" * (size + diff)
    endpoint = SQLStore(schema, database_path=tmp_outputs["db"])
    endpoint.db_exists(force=True)
    mod = endpoint.compile_native()

    with open(tmp_outputs["tsv"], "w", encoding="UTF-8") as file:
        file.write("name\n")
        file.write(name)
        file.write("\n")

    if diff == -1:
        obj = csv_loader.load(
            str(tmp_outputs["tsv"]),
            target_class=mod.Container,
            index_slot="Person_index",
            schema=schema,
        )
        endpoint.dump(obj)
        obj2 = endpoint.load(target_class=mod.Container)
        person = getattr(obj2, "Person_index")[0]
        name2 = getattr(person, "name")
        assert name == name2
    else:
        with pytest.raises(Exception):
            csv_loader.load(
                tmp_outputs["tsv"],
                target_class=mod.Container,
                index_slot="Person_index",
                schema=schema,
            )

    # mod holds a reference to sqlite that prevents file closing
    del mod
    # dispose engine to allow creating of a new engine of same name
    endpoint.engine.dispose()
