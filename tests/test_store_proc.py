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
        SELECT id_pedido, id_cliente, fecha FROM pedidos 
        WHERE id_cliente = %s AND fecha = %s;
    """
    pedido_result = run_query(query_pedido, params=(1, '2025-05-10'), fetchone=True)

    assert pedido_result is not None 
    assert pedido_result[1] == 1 
    assert pedido_result[2] == '2025-05-10'  
    
    id_pedido = pedido_result[0]

    query_detalle = """
        SELECT id_pedido, id_producto, cantidad FROM detalle_pedido 
        WHERE id_pedido = %s;
    """
    detalle_result = run_query(query_detalle, params=(id_pedido,), fetchall=True)

    expected_detalle = [(id_pedido, 3, 2)]  

    assert len(detalle_result) == 1  
    assert detalle_result == expected_detalle
