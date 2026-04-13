"""Smoke tests: insert 5 dismech disorders into a live TypeDB 3.x instance.

These tests verify that the generated TypeQL schema accepts real data by:
1. Loading the full dismech LinkML schema via TypeDBGenerator
2. Inserting 5 Disease entities (scalar attributes only) into the database
3. Querying back to confirm insertion

Requirements:
- Running TypeDB 3.x at localhost:1729
- typedb-driver installed (pip install typedb-driver)
- Python <= 3.13
- dismech repo at /Users/gullyburns/Documents/GitHub/dismech

Run with::

    python3.12 -m pytest tests/linkml/test_generators/test_typedbgen_dismech_smoke.py \\
        -m integration -v
"""

import uuid
from pathlib import Path

import pytest
import yaml

from linkml.generators.typedbgen import TypeDBGenerator

typedb = pytest.importorskip("typedb.driver", reason="typedb-driver not installed")

from typedb.driver import Credentials, DriverOptions, TransactionType, TypeDB  # noqa: E402

# ── Paths ─────────────────────────────────────────────────────────────────────

DISMECH_SCHEMA = Path(
    "/Users/gullyburns/Documents/GitHub/dismech/src/dismech/schema/dismech.yaml"
)
DISORDERS_DIR = Path("/Users/gullyburns/Documents/GitHub/dismech/kb/disorders")

# Five smallest non-history YAML files — representative of real data, minimal complexity.
SMOKE_DISORDERS = [
    "Gastric_Ulcer.yaml",
    "Urticaria.yaml",
    "Dorsalgia.yaml",
    "Secondary_Hypertension.yaml",
    "Lichen_Simplex_Chronicus.yaml",
]

TYPEDB_HOST = "localhost:1729"
TYPEDB_CREDENTIALS = Credentials("admin", "password")
TYPEDB_OPTIONS = DriverOptions(is_tls_enabled=False)


# ── Helpers ───────────────────────────────────────────────────────────────────


def _escape(s: str) -> str:
    """Escape backslashes and double-quotes for use inside TypeQL string literals."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _make_disease_insert(data: dict) -> str:
    """Build a TypeQL insert statement for scalar Disease attributes.

    Inserts ``name`` (required @key) and ``category`` (if present).
    Datetime fields (creation-date, updated-date) are intentionally omitted to
    avoid timezone-format edge cases in this smoke test.

    :param data: parsed YAML dict for a single disorder
    :return: TypeQL insert statement string
    """
    attrs = [f'has name "{_escape(data["name"])}"']
    if data.get("category"):
        attrs.append(f'has category "{_escape(str(data["category"]))}"')
    return "insert $d isa disease, " + ", ".join(attrs) + ";"


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def typedb_driver():
    """Open a TypeDB driver connection for the whole test module."""
    driver = TypeDB.driver(TYPEDB_HOST, TYPEDB_CREDENTIALS, TYPEDB_OPTIONS)
    yield driver
    driver.close()


@pytest.fixture(scope="module")
def loaded_db(typedb_driver):
    """Create a temp TypeDB database, load dismech schema, insert 5 disorders.

    Module-scoped so the expensive schema load happens once for all tests.
    The database is dropped in teardown regardless of test outcomes.
    """
    db_name = f"linkml-dismech-smoke-{uuid.uuid4().hex[:6]}"
    typedb_driver.databases.create(db_name)
    try:
        # Load schema
        schema = TypeDBGenerator(str(DISMECH_SCHEMA)).serialize()
        with typedb_driver.transaction(db_name, TransactionType.SCHEMA) as tx:
            tx.query(schema).resolve()
            tx.commit()

        # Insert 5 Disease entities
        for fname in SMOKE_DISORDERS:
            data = yaml.safe_load((DISORDERS_DIR / fname).read_text())
            insert_q = _make_disease_insert(data)
            with typedb_driver.transaction(db_name, TransactionType.WRITE) as tx:
                tx.query(insert_q).resolve()
                tx.commit()

        yield db_name
    finally:
        typedb_driver.databases.get(db_name).delete()


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.integration
def test_schema_loads(loaded_db):
    """Dismech schema loads into TypeDB without errors (fixture performs the load)."""
    assert loaded_db is not None


@pytest.mark.integration
def test_five_diseases_inserted(typedb_driver, loaded_db):
    """All 5 smoke-test diseases are present in the database after insertion.

    TypeDB 3.x does not allow fetching entity variables directly; use attribute
    projection (``has name $n``) instead.
    """
    with typedb_driver.transaction(loaded_db, TransactionType.READ) as tx:
        results = list(
            tx.query('match $d isa disease, has name $n; fetch {"name": $n};').resolve()
        )
    assert len(results) == 5, (
        f"Expected 5 disease instances, got {len(results)}"
    )


@pytest.mark.integration
@pytest.mark.parametrize("fname", SMOKE_DISORDERS)
def test_disease_exists_by_name(typedb_driver, loaded_db, fname):
    """Each disorder can be retrieved individually by its name attribute."""
    data = yaml.safe_load((DISORDERS_DIR / fname).read_text())
    name = data["name"]
    escaped = _escape(name)
    with typedb_driver.transaction(loaded_db, TransactionType.READ) as tx:
        # Fetch the name attribute of the matched entity (not the entity itself)
        results = list(
            tx.query(
                f'match $d isa disease, has name "{escaped}"; fetch {{"name": $d.name}};'
            ).resolve()
        )
    assert len(results) == 1, (
        f"Expected exactly 1 result for disease '{name}', got {len(results)}"
    )
