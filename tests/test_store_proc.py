
import psycopg2
import pytest

def test_registrar_pedido():
    # Conexión a la base de datos
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()
    
    # Ejecutar el procedimiento almacenado
    cur.execute("""
        CALL registrar_pedido(1, '2025-05-20', 2, 3);
    """)
    
    # Verificar si el pedido se ha insertado
    cur.execute("SELECT * FROM pedidos WHERE id_cliente = 1 AND fecha = '2025-05-20';")
    result = cur.fetchone()
    
    assert result is not None
    
    cur.close()
    conn.close()
