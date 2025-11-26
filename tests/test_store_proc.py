def test_registrar_pedido_funciona(cursor):
    cliente_id = 2
    producto_id = 1
    cantidad = 5
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos_antes = cursor.fetchone()[0]

    cursor.callproc("registrar_pedido", (cliente_id, '2025-06-01', producto_id, cantidad))
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos_despues = cursor.fetchone()[0]

    assert pedidos_despues == pedidos_antes + 1
    
    cursor.execute("SELECT p.id_pedido FROM pedidos p WHERE p.id_cliente = %s ORDER BY p.id_pedido DESC LIMIT 1", (cliente_id,))
    nuevo_pedido_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id_producto, cantidad FROM detalle_pedido WHERE id_pedido = %s", (nuevo_pedido_id,))
    detalle = cursor.fetchone()
    
    assert detalle[0] == producto_id
    assert detalle[1] == cantidad
