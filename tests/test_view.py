def test_vista_detalle_pedidos_existencia(cursor):
    cursor.execute("SELECT viewname FROM pg_views WHERE viewname = 'vista_detalle_pedidos'")
    result = cursor.fetchone()
    assert result is not None, "La vista 'vista_detalle_pedidos' debe existir."

def test_vista_detalle_pedidos_contenido(cursor):
    cursor.execute("SELECT nombre_cliente, nombre_producto, cantidad, total_linea FROM vista_detalle_pedidos WHERE nombre_cliente = 'Ana Torres' AND nombre_producto = 'Laptop'")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == 'Ana Torres'
    assert result[1] == 'Laptop'
    assert result[2] == 1
    assert result[3] == 1200.00
