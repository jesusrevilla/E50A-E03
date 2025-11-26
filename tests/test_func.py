import psycopg2
import pytest

DB_CONFIG = { "dbname": "test_db", "user": "postgres", "password": "postgres", "host": "localhost", "port": 5432 }

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    yield conn
    conn.close()

def test_func_total_gastado(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT total_gastado_por_cliente(1);")
        result = cur.fetchone()[0]
        assert float(result) == 1251.00
