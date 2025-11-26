import psycopg2
import pytest

DB_CONFIG = { "dbname": "test_db", "user": "postgres", "password": "postgres", "host": "localhost", "port": 5432 }

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    yield conn
    conn.close()

def test_vista_detalle(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT * FROM vista_detalle_pedidos WHERE cliente = 'Ana Torres'")
        results = cur.fetchall()
        assert len(results) == 2
