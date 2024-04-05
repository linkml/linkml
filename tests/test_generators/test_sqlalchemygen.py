import logging
import re
from collections import Counter

import pytest
from linkml_runtime.linkml_model import SlotDefinition
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from linkml.generators.sqlalchemygen import SQLAlchemyGenerator, TemplateEnum
from linkml.generators.sqltablegen import SQLTableGenerator
from linkml.utils.schema_builder import SchemaBuilder


@pytest.fixture
def schema(input_path):
    return str(input_path("personinfo.yaml"))


def test_sqla_basic_imperative(schema):
    """
    Test generation of DDL for imperative mode

    Imperative mode assumes a pre-existing object model,
    and only mappings are generated

    This test will check the generated python, but does not include a compilation step
    """
    gen = SQLAlchemyGenerator(schema)
    code = gen.generate_sqla()  # default is imperative
    tables = []
    for item in code.splitlines():
        match = re.search(r"Table\('(.*?)',", item)
        if match:
            tables.append(match.group(1))

    expected_tables = [
        "NamedThing",
        "Person",
        "Organization",
        "Place",
        "Address",
        "Event",
        "Concept",
        "DiagnosisConcept",
        "ProcedureConcept",
        "Relationship",
        "FamilialRelationship",
        "EmploymentEvent",
        "MedicalEvent",
    ]
    for expected in expected_tables:
        assert expected in tables


def test_sqla_basic_declatative(schema):
    """
    Test generation of DDL for declarative mode

    With declarative mode, there is no pre-existing data model,
    and the generator creates classes from the schema

    This test will check the generated python, but does not include a compilation step
    """
    gen = SQLAlchemyGenerator(schema)
    code = gen.generate_sqla(template=TemplateEnum.DECLARATIVE)
    tables = []
    for item in code.splitlines():
        match = re.search(r"class\s(.*?)\(", item)
        if match:
            tables.append(match.group(1))

    expected_tables = [
        "NamedThing",
        "Person",
        "Organization",
        "Place",
        "Address",
        "Event",
        "Concept",
        "DiagnosisConcept",
        "ProcedureConcept",
        "Relationship",
        "FamilialRelationship",
        "EmploymentEvent",
        "MedicalEvent",
    ]
    for expected in expected_tables:
        assert expected in tables


def test_mixin():
    b = SchemaBuilder()
    b.add_slot(SlotDefinition("ref_to_c1", range="my_class1", multivalued=True))
    b.add_class("my_mixin", slots=["my_mixin_slot"], mixin=True)
    b.add_class("my_abstract", slots=["my_abstract_slot"], abstract=True)
    b.add_class("my_class1", is_a="my_abstract", mixins=["my_mixin"])
    b.add_class("my_class2", slots=["ref_to_c1"])
    gen = SQLAlchemyGenerator(b.schema)
    mod = gen.compile_sqla(template=TemplateEnum.DECLARATIVE)
    i1 = mod.MyClass1(my_mixin_slot="v1", my_abstract_slot="v2")
    i2 = mod.MyClass2(ref_to_c1=[i1])
    assert i2.ref_to_c1[0] == i1


def test_sqla_compile_imperative(schema):
    """
    tests compilation of generated imperative mappings
    """
    gen = SQLAlchemyGenerator(schema)
    # use standard python generation for classes and sqlagen for mappings
    personinfo_module = gen.compile_sqla(compile_python_dataclasses=True)
    p1 = personinfo_module.Person(id="P1", name="John Doe", age_in_years=22)

    # test three attributes with values supplied above
    assert hasattr(p1, "id"), f"'id' attribute not found in {p1}"
    assert hasattr(p1, "name"), f"'name' attribute not found in {p1}"
    assert hasattr(p1, "age_in_years"), f"'age_in_years' attribute not found in {p1}"

    # test one or more attributes without values supplied during initialization
    assert hasattr(p1, "description"), f"'description' attribute not found in {p1}"


def test_sqla_imperative_dataclasses_exec(schema):
    """
    combined test:

    - generate DDL from schema
    - load DDL into a fresh sqlite database
    - generate standard python object model and db mappings (i.e. IMPERATIVE mode)
    - test insertion into database using SQLA
    - test querying results
    """
    engine = create_engine("sqlite://")
    ddl = SQLTableGenerator(schema).generate_ddl()
    with engine.connect() as connection:
        cur = connection.connection.cursor()
        cur.executescript(ddl)

    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()
    gen = SQLAlchemyGenerator(schema)
    mod = gen.compile_sqla(template=TemplateEnum.IMPERATIVE, compile_python_dataclasses=True)
    p1 = mod.Person(id="P1", name="a b", age_in_years=22)
    session.add(p1)
    q = session.query(mod.Person).where(mod.Person.name == p1.name)
    persons = q.all()
    assert len(persons) == 1
    assert p1 in persons
    p1 = persons[0]
    assert p1.name == "a b"
    assert p1.age_in_years == 22
    session.commit()
    dc = mod.DiagnosisConcept(id="C001", name="cough")
    e1 = mod.MedicalEvent(duration=100.0, diagnosis=dc)
    address = mod.Address(street="1 a street", city="big city", postal_code="ZZ1 ZZ2")
    p2 = mod.Person(
        id="P2",
        name="p2 name",
        aliases=["foo"],
        has_medical_history=[e1],
        current_address=address,
    )
    session.add(p2)
    session.commit()
    q = session.query(mod.Person).where(mod.Person.id == p2.id)
    persons = q.all()
    assert len(persons) == 1
    p2_recap = persons[0]
    p2mh = p2_recap.has_medical_history
    assert p2mh[0].duration == e1.duration
    assert len(p2_recap.aliases) == 1
    assert p2_recap.aliases[0] == "foo"
    assert p2_recap.current_address.city == "big city"
    session.close()
    engine.dispose()


@pytest.mark.skip("Mixing sqla imperative and pydantic classes that extend from BaseModel may not play well together")
def test_sqla_imperative_pydantic_exec(schema):
    """
    https://github.com/tiangolo/fastapi/issues/214
    https://fastapi.tiangolo.com/tutorial/sql-databases/

    combined test:

    - generate DDL from schema
    - load DDL into a fresh sqlite database
    - generate standard python object model and db mappings (i.e. IMPERATIVE mode)
    - test insertion into database using SQLA
    - test querying results
    """
    engine = create_engine("sqlite://")
    ddl = SQLTableGenerator(schema).generate_ddl()
    with engine.connect() as connection:
        cur = connection.connection.cursor()
        cur.executescript(ddl)

    SessionClass = sessionmaker(bind=engine)
    session = SessionClass()
    gen = SQLAlchemyGenerator(schema)
    mod = gen.compile_sqla(
        template=TemplateEnum.IMPERATIVE,
        compile_python_dataclasses=True,
        pydantic=True,
    )
    # p1 = mod.NamedThing()
    p1 = mod.Person(id="P1", name="a b", age_in_years=22)
    session.add(p1)
    # SessionClass = sessionmaker(bind=engine)
    # session = SessionClass()
    q = session.query(mod.Person).where(mod.Person.name == p1.name)
    # q = session.query(mod.Person)
    persons = q.all()
    assert len(persons) == 1
    assert p1 in persons
    p1 = persons[0]
    assert p1.name == "a b"
    assert p1.age_in_years == 22
    session.commit()
    e1 = mod.MedicalEvent(duration=100.0)
    p2 = mod.Person(id="P2", name="p2 name", aliases=["foo"], has_medical_history=[e1])
    session.add(p2)
    session.commit()
    q = session.query(mod.Person).where(mod.Person.id == p2.id)
    persons = q.all()
    assert len(persons) == 1
    p2_recap = persons[0]
    p2mh = p2_recap.has_medical_history
    assert p2mh[0].duration == e1.duration
    session.close()
    engine.dispose()


def test_sqla_declarative_exec(schema):
    """
    combined test:

    - generate DDL from schema
    - load DDL into a fresh sqlite database
    - generate combined python and mappings (i.e. DECLARATIVE mode)
    - test insertion into database using SQLA
    - test querying results
    """
    engine = create_engine("sqlite://")
    ddl = SQLTableGenerator(schema).generate_ddl()
    with engine.connect() as connection:
        cur = connection.connection.cursor()
        cur.executescript(ddl)

    session_class = sessionmaker(bind=engine)
    session = session_class()
    gen = SQLAlchemyGenerator(schema)
    # declarative: bypasses standard LinkML dataclass generation
    mod = gen.compile_sqla(template=TemplateEnum.DECLARATIVE)
    # test adding by ID
    session.add(mod.DiagnosisConcept(id="C999", name="rash"))
    # test insertion of objects with no surrogate key; uses auto-increment ID
    e1 = mod.MedicalEvent(duration=100.0, diagnosis_id="C999")
    # test adding by inline
    dc = mod.DiagnosisConcept(id="C001", name="cough")
    e2 = mod.MedicalEvent(duration=200.0, diagnosis=dc)
    # add person - inlined medical events will be translated to backrefs
    # aliases =['x']
    # aliases = []
    address = mod.Address(street="1 a street", city="big city", postal_code="ZZ1 ZZ2")
    # p1 = mod.Person(id='P1', name='a b', aliases=aliases, age_in_years=22,
    #                 has_medical_history=[e1, e2], current_address=address)
    p1 = mod.Person(id="P1", name="a b", age_in_years=22, has_medical_history=[e1, e2])
    p1.aliases = ["Anne"]
    # p1.aliases_rel = [mod.Person_alias(alias='zzz')]
    p1.aliases.append("Fred")
    p1.has_familial_relationships.append(mod.FamilialRelationship(related_to="P2", type="SIBLING_OF"))
    news_event = mod.NewsEvent(headline="foo")
    p1.has_news_events.append(news_event)
    p1.current_address = address
    session.add(p1)
    session.add(mod.Person(id="P2", aliases=["Fred"], has_news_events=[news_event]))
    # session.add(mod.Person(id='P3', has_familial_relationships=[{"related_to": "P4"}]))
    session.commit()
    q = session.query(mod.NewsEvent)
    all_news = q.all()
    # ensure news object is shared between persons
    assert len(all_news) == 1
    q = session.query(mod.Person).where(mod.Person.name == p1.name)
    persons = q.all()
    for person in persons:
        assert isinstance(person, mod.NamedThing)
        logging.info(f"Person={person}")
        for a in person.aliases:
            logging.info(f"  ALIAS={a}")
        for e in person.has_medical_history:
            assert e.duration > 0
            assert isinstance(e, mod.Event)
    assert len(persons) == 1
    p1_from_query = persons[0]
    assert p1.age_in_years == 22
    assert Counter(p1.aliases) == Counter(["Anne", "Fred"])
    assert len(p1_from_query.has_medical_history) == 2
    assert p1 in persons
    # assert any(e for e in persons[0].has_medical_history if e.diagnosis.id == 'C999')
    p1_medical_history = p1_from_query.has_medical_history
    p1_famrels = p1_from_query.has_familial_relationships
    p1_news = p1_from_query.has_news_events
    assert any(e for e in p1_medical_history if e.diagnosis_id == "C999")
    assert any(e for e in p1_medical_history if e.diagnosis_id == "C001")
    assert any(e for e in p1_medical_history if (e.diagnosis.id == "C001" and e.diagnosis.name == "cough"))
    assert any(e for e in p1_medical_history if (e.diagnosis.id == "C999" and e.diagnosis.name == "rash"))
    assert any(r for r in p1_famrels if (r.related_to == "P2" and r.type == "SIBLING_OF"))
    assert any(n for n in p1_news if (n.headline == "foo"))
    session.commit()
    session.close()
    engine.dispose()
