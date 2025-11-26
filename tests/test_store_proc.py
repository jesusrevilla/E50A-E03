import pytest
import psycopg2

def test_registrar_pedido():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("CALL registrar_pedido(1, '2025-05-20', 2, 3)")
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM detalle_pedido WHERE id_producto = 2")
    count = cur.fetchone()[0]
    assert count >= 1
    cur.close()
    conn.close()
