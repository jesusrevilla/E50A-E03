import psycopg2
import pytest

@pytest.fixture
def db():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="test_db",
        user="postgres",
        password="postgres"
    )
    yield conn
    conn.close()


def test_function_example(db):
    """
    Ejemplo para función:
    SELECT total_price(100, 3) => 300
    """
    cur = db.cursor()
    cur.execute("SELECT total_price(100, 3);")
    result = cur.fetchone()[0]
    assert result == 300
