import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(q):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(q)
            try:
                return cur.fetchall()
            except:
                return None
def test_registrar_pedido():
    run_query("CALL registrar_pedido(1, '2025-06-01', 2, 5);")
    result = run_query("SELECT cantidad FROM detalle_pedido ORDER BY id_detalle DESC LIMIT 1;")
    assert result[0][0] == 5

