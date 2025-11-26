import psycopg2
import pytest

DB_CONFIG = { "dbname": "test_db", "user": "postgres", "password": "postgres", "host": "localhost", "port": 5432 }

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    yield conn
    conn.close()

def test_json_query(db_connection):
    with db_connection.cursor() as cur:
        # Buscar producto marca Dell dentro del JSON
        cur.execute("SELECT nombre FROM productos_json WHERE atributos->>'marca' = 'Dell'")
        result = cur.fetchone()
        assert result[0] == 'Laptop'
