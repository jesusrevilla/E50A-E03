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

def test_registrar_pedido():
    query = """
        CALL registrar_pedido(1, '2025-05-10', 3, 2);
    """
    run_query(query)
    
    query_pedido = """
        SELECT * FROM pedidos WHERE id_cliente = 1 AND fecha = '2025-05-10';
    """
    pedido_result = run_query(query_pedido)

    query_detalle = """
        SELECT * FROM detalle_pedido WHERE id_pedido = %s;
    """
    detalle_result = run_query(query_detalle % (pedido_result[0][0],))

    expected_detalle = [(pedido_result[0][0], 3, 2)]  

    assert len(pedido_result) == 1
    assert detalle_result == expected_detalle
