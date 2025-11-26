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
        SELECT * FROM vista_detalle_pedidos LIMIT 1;
    """)
    rows = cur.fetchall()

    assert isinstance(rows, list)

