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


def test_view_exists(db):
    cur = db.cursor()
    cur.execute("""
        SELECT * FROM vista_productos_activos LIMIT 1;
    """)
    rows = cur.fetchall()

    # No debe tirar error
    assert isinstance(rows, list)

