import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(query):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def test_indice_cliente_producto_existe():
    result = run_query("""
        SELECT indexname, tablename, indexdef
        FROM pg_indexes
        WHERE tablename = 'detalle_pedido' AND indexname = 'idx_cliente_producto';
    """)
    assert len(result) == 1 
