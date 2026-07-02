"""Integration tests for TypeDBGenerator against a live TypeDB 3.x instance.

These tests require:
- A running TypeDB 3.x server at localhost:1729
- The typedb-driver package installed (``pip install typedb-driver``)
- Python <=3.13 (typedb-driver native extension segfaults on Python 3.14)

Run with::

    uv run --python 3.12 pytest tests/linkml/test_generators/test_typedbgen_integration.py -m integration -v
"""

import socket
import uuid
from pathlib import Path

import pytest

from linkml.generators.typedbgen import TypeDBGenerator

typedb = pytest.importorskip("typedb.driver", reason="typedb-driver not installed")

from typedb.driver import Credentials, DriverOptions, TransactionType, TypeDB  # noqa: E402

TYPEDB_HOST = "localhost:1729"


def _typedb_available() -> bool:
    """Return True if a TypeDB server is listening on localhost:1729."""
    host, port = TYPEDB_HOST.split(":")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex((host, int(port))) == 0


pytestmark = pytest.mark.skipif(
    not _typedb_available(),
    reason=f"TypeDB server not available at {TYPEDB_HOST}",
)

_INPUT_DIR = Path(__file__).parent / "input"

TYPEDB_CREDENTIALS = Credentials("admin", "password")
TYPEDB_OPTIONS = DriverOptions(is_tls_enabled=False)


@pytest.fixture(scope="module")
def typedb_driver():
    """Open a TypeDB driver connection for the test module, close when done."""
    driver = TypeDB.driver(TYPEDB_HOST, TYPEDB_CREDENTIALS, TYPEDB_OPTIONS)
    yield driver
    driver.close()


@pytest.fixture()
def temp_db(typedb_driver):
    """Create a temporary TypeDB database and drop it after the test."""
    db_name = f"linkml-test-{uuid.uuid4().hex[:8]}"
    typedb_driver.databases.create(db_name)
    yield db_name
    typedb_driver.databases.get(db_name).delete()


@pytest.mark.integration
def test_schema_loads_without_errors(typedb_driver, temp_db):
    """Generated TypeQL schema is accepted by TypeDB without errors."""
    schema = TypeDBGenerator(_INPUT_DIR / "organization.yaml").serialize()

    with typedb_driver.transaction(temp_db, TransactionType.SCHEMA) as tx:
        tx.query(schema).resolve()
        tx.commit()


@pytest.mark.integration
def test_entity_types_defined_in_db(typedb_driver, temp_db):
    """After loading the schema, the expected entity types are queryable."""
    schema = TypeDBGenerator(_INPUT_DIR / "organization.yaml").serialize()

    with typedb_driver.transaction(temp_db, TransactionType.SCHEMA) as tx:
        tx.query(schema).resolve()
        tx.commit()

    # Query back the defined types: ask for subtypes of each expected type
    # (in TypeDB 3.x, `entity`/`relation`/`attribute` are kind keywords, not root type names)
    with typedb_driver.transaction(temp_db, TransactionType.READ) as tx:
        org_result = list(tx.query('match $t sub organization; fetch { "t": $t };').resolve())
        emp_result = list(tx.query('match $t sub employee; fetch { "t": $t };').resolve())

    assert len(org_result) >= 1, "organization type not found in schema"
    assert len(emp_result) >= 1, "employee type not found in schema"
    # manager is a sub of employee — should appear in employee subtypes
    emp_labels = {r["t"]["label"] for r in emp_result}
    assert "manager" in emp_labels


@pytest.mark.integration
def test_attribute_types_defined_in_db(typedb_driver, temp_db):
    """After loading the schema, the expected attribute types are queryable."""
    schema = TypeDBGenerator(_INPUT_DIR / "organization.yaml").serialize()

    with typedb_driver.transaction(temp_db, TransactionType.SCHEMA) as tx:
        tx.query(schema).resolve()
        tx.commit()

    with typedb_driver.transaction(temp_db, TransactionType.READ) as tx:
        name_result = list(tx.query('match $t sub name; fetch { "t": $t };').resolve())
        id_result = list(tx.query('match $t sub id; fetch { "t": $t };').resolve())

    assert len(name_result) >= 1, "name attribute type not found"
    assert len(id_result) >= 1, "id attribute type not found"


@pytest.mark.integration
def test_relation_types_defined_in_db(typedb_driver, temp_db):
    """Object-ranged slots produce queryable relation types."""
    schema = TypeDBGenerator(_INPUT_DIR / "organization.yaml").serialize()

    with typedb_driver.transaction(temp_db, TransactionType.SCHEMA) as tx:
        tx.query(schema).resolve()
        tx.commit()

    with typedb_driver.transaction(temp_db, TransactionType.READ) as tx:
        boss_result = list(tx.query('match $t sub has-boss; fetch { "t": $t };').resolve())
        emp_result = list(tx.query('match $t sub has-employees; fetch { "t": $t };').resolve())

    assert len(boss_result) >= 1, "has-boss relation type not found"
    assert len(emp_result) >= 1, "has-employees relation type not found"


@pytest.mark.integration
def test_schema_is_idempotent(typedb_driver, temp_db):
    """Applying the same define block twice does not error (TypeDB define is idempotent)."""
    schema = TypeDBGenerator(_INPUT_DIR / "organization.yaml").serialize()

    with typedb_driver.transaction(temp_db, TransactionType.SCHEMA) as tx:
        tx.query(schema).resolve()
        tx.commit()

    # Apply again — should be a no-op, not an error
    with typedb_driver.transaction(temp_db, TransactionType.SCHEMA) as tx:
        tx.query(schema).resolve()
        tx.commit()
