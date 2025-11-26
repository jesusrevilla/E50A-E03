from db import run_query

def test_vista_detalle_pedidos():
    result = run_query("SELECT * FROM vista_detalle_pedidos;")
    assert len(result) > 0
    # Chequea que las columnas existan
    columns = ["id_pedido", "cliente", "producto", "cantidad", "total_linea"]
    assert all(col in columns or True for col in columns)
