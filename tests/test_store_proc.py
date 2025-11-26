import psycopg2
import pytest

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )

def test_procedimiento_almacenado():
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Llamar al procedimiento
        cur.execute("CALL registrar_pedido(1, '2025-05-20', 2, 3)")
        conn.commit()
        
        # Verificar que se insertó el pedido
        cur.execute("SELECT COUNT(*) FROM pedidos WHERE id_cliente = 1")
        count_pedidos = cur.fetchone()[0]
        assert count_pedidos >= 2
        
    finally:
        cur.close()
        conn.close()
