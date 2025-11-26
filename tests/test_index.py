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

def test_indice_compuesto():
    result = run_query("""
        SELECT indexname
        FROM pg_indexes
        WHERE indexname = 'idx_cliente_producto';
    """)

    # Debe existir al menos una fila con ese nombre de índice
    assert result is not None
    assert len(result) >= 1
    assert result[0][0] == 'idx_cliente_producto'
