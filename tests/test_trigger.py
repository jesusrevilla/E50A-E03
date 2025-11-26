
# tests/test_trigger.py
from datetime import date
from conftest import fetch_one

def test_trigger_on_pedidos(cur):
    # Insertamos un pedido para disparar el trigger
    test_date = date(2025, 5, 22)
    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (%s, %s) RETURNING id_pedido;", (1, test_date))
    id_pedido = fetch_one(cur, "SELECT %s;", (None, ))  # dummy to keep structure

    # Verificamos que auditoría registró la inserción
    row = fetch_one(cur, """
        SELECT id_cliente, fecha_pedido
        FROM auditoria_pedidos
        WHERE id_cliente = %s AND fecha_pedido = %s;
    """, (1, test_date))
    assert row is not None, "El trigger no insertó registro en 'auditoria_pedidos'."

    # Cleanup
    # El pedido insertado no tiene detalle, borramos auditoría y pedido
    cur.execute("DELETE FROM auditoria_pedidos WHERE id_cliente = %s AND fecha_pedido = %s;", (1, test_date))
    cur.execute("DELETE FROM pedidos WHERE id_cliente = %s AND fecha = %s;", (1, test_date))

