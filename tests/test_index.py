from app.db import run_query


def test_index_cliente_producto():
    result = run_query("EXPLAIN SELECT * FROM detalle_pedido WHERE id_pedido=1 AND id_producto=2;")
    assert any("Index Scan" in str(r) for r in result)

