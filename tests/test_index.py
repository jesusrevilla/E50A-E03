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
            
def test_indice_cliente_producto():
    """Verifica que el índice compuesto 'idx_cliente_producto' exista en la tabla 'detalle_pedido'."""
    query = """
        SELECT indexname
        FROM pg_indexes
        WHERE tablename = 'detalle_pedido' AND indexname = 'idx_cliente_producto';
    """
    result = run_query(query)

    assert len(result) == 1
    assert result[0][0] == 'idx_cliente_producto'
