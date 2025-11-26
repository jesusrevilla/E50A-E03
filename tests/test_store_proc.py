import psycopg2

from .conftest import db_connection 

def test_registrar_pedido_exitoso():
    conn = db_connection()
    cur = conn.cursor()
    
    id_cliente_prueba = 1
    fecha_prueba = '2025-12-01'
    id_producto_prueba = 2  # Mouse
    cantidad_prueba = 5

    cur.execute(f"SELECT registrar_pedido({id_cliente_prueba}, '{fecha_prueba}', {id_producto_prueba}, {cantidad_prueba});")
    
    
    cur.execute("SELECT id_pedido, id_cliente, fecha FROM pedidos ORDER BY id_pedido DESC LIMIT 1;")
    new_pedido = cur.fetchone()
    
    assert new_pedido is not None
    assert new_pedido[1] == id_cliente_prueba # El cliente debe ser el ID 1

    new_pedido_id = new_pedido[0]

   
    cur.execute("SELECT id_producto, cantidad FROM detalle_pedido WHERE id_pedido = %s;", (new_pedido_id,))
    detalle = cur.fetchone()
    
    assert detalle is not None
    assert detalle[0] == id_producto_prueba
    assert detalle[1] == cantidad_prueba

    conn.rollback() # Revertir cambios después de la prueba
    cur.close()
    conn.close()
