import psycopg2
import pytest

def test_procedimiento_almacenado():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    cur.execute("CALL registrar_pedido(1, '2025-05-20', 2, 3)")
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM pedidos WHERE id_cliente = 1")
    count_pedidos = cur.fetchone()[0]
    assert count_pedidos >= 2
    
    cur.execute("""
        SELECT COUNT(*) FROM detalle_pedido dp
        JOIN pedidos p ON dp.id_pedido = p.id_pedido
        WHERE p.id_cliente = 1 AND dp.id_producto = 2 AND dp.cantidad = 3
    """)
    count_detalle = cur.fetchone()[0]
    assert count_detalle >= 1
    
    cur.close()
    conn.close()
