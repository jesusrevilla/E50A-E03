from app.db import run_query


def test_trigger_auditoria():
    # Inserta un pedido para activar trigger
    run_query("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-05-21');")
    result = run_query("SELECT * FROM auditoria_pedidos WHERE id_cliente = 2 ORDER BY id_auditoria DESC LIMIT 1;")
    assert result[0][1] == 2  # id_cliente

