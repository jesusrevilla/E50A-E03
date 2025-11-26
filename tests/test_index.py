import psycopg2
import pytest

@pytest.fixture
def db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="test_db",
        user="postgres",
        password="postgres"
    )
    yield conn
    conn.close()


def test_index_exists(db):
    """
    Reemplaza productos_nombre_idx por el nombre real
    """
    cur = db.cursor()
    cur.execute("""
        SELECT indexname
        FROM pg_indexes
        WHERE indexname='productos_nombre_idx';
    """)
    assert cur.fetchone() is not None

