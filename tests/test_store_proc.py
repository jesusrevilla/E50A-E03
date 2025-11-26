import pytest
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def test_procedure_registrar_pedido():
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        cliente_id = 1
        producto_id = 1
        cantidad = 5
        fecha = '2025-06-01'
        
        cur.execute("CALL registrar_pedido(%s, %s, %s, %s)", (cliente_id, fecha, producto_id, cantidad))
        conn.commit()
        
        cur.execute("SELECT id_pedido FROM pedidos WHERE fecha = %s AND id_cliente = %s ORDER BY id_pedido DESC LIMIT 1", (fecha, cliente_id))
        nuevo_pedido = cur.fetchone()
        assert nuevo_pedido is not None
        id_pedido_generado = nuevo_pedido[0]
        
        cur.execute("SELECT cantidad FROM detalle_pedido WHERE id_pedido = %s AND id_producto = %s", (id_pedido_generado, producto_id))
        detalle = cur.fetchone()
        
        assert detalle is not None
        assert detalle[0] == cantidad
        
    finally:
        cur.close()
        conn.close()
