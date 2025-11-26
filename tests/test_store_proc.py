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


def test_store_procedure(db):
    """
    CALL sp_add_product('Galleta', 5)
    """
    cur = db.cursor()
    cur.execute("CALL sp_add_product('Test Galleta', 5);")
    db.commit()

    cur.execute("SELECT id FROM productos WHERE nombre='Test Galleta';")
    assert cur.fetchone() is not None

