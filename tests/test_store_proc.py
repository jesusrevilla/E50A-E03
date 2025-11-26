import psycopg2
import pytest

DB_CONFIG = { "dbname": "test_db", "user": "postgres", "password": "postgres", "host": "localhost", "port": 5432 }

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    yield conn
    conn.close()

def test_proc_registrar_pedido(db_connection):
    with db_connection.cursor() as cur:
        # Llamamos al procedimiento
        cur.execute("CALL registrar_pedido(2, '2025-06-01', 3, 5);") 
        
        # Verifico que se haya insertado en detalle_pedido
        cur.execute("SELECT cantidad FROM detalle_pedido WHERE cantidad = 5")
        result = cur.fetchone()
        assert result is not None
        assert result[0] == 5
