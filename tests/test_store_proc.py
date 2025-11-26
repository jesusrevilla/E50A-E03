from db import run_query

def test_registrar_pedido():
    # Inserta un pedido
    run_query("CALL registrar_pedido(1, '2025-05-20', 2, 3);")
    result = run_query("SELECT * FROM detalle_pedido WHERE id_pedido = (SELECT MAX(id_pedido) FROM pedidos);")
    assert result[0][2] == 2  # id_producto
    assert result[0][3] == 3  # cantidad

def test_total_gastado():
    result = run_query("SELECT total_gastado_por_cliente(1);")
    assert result[0][0] > 0
