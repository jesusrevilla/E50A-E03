import psycopg2
import pytest

DB_CONFIG = { "dbname": "test_db", "user": "postgres", "password": "postgres", "host": "localhost", "port": 5432 }

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    yield conn
    conn.close()

def test_trigger_auditoria(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-07-01');")
        cur.execute("SELECT * FROM auditoria_pedidos WHERE fecha_pedido = '2025-07-01'")
        result = cur.fetchall()
        assert len(result) > 0
