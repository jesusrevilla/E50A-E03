import pytest
import psycopg2

def test_trigger_auditar_pedido():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-25')")
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM auditoria_pedidos WHERE id_cliente = 1")
    count = cur.fetchone()[0]
    assert count >= 1
    cur.close()
    conn.close()
