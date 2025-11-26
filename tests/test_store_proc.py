
# tests/test_store_proc.py
from datetime import date
from conftest import fetch_one, fetch_all

def test_procedure_exists(cur):
    row = fetch_one(cur, """
        SELECT 1
        FROM pg_proc
        WHERE proname = 'registrar_pedido';
    """)
    assert row is not None, "No existe el procedimiento 'registrar_pedido'."

def test_procedure_inserts_pedido_and_detalle(cur):
    # Insertamos un pedido limpio y verificamos
    test_date = date(2025, 5, 21)
    # Cliente 2, producto 3, cantidad 2 (según datos base del README)
    cur.execute("CALL registrar_pedido(%s, %s, %s, %s);", (2, test_date, 3, 2))

    # Buscar el pedido recién insertado
    ped = fetch_one(cur, """
        SELECT id_pedido
        FROM pedidos
        WHERE id_cliente = %s AND fecha = %s
        ORDER BY id_pedido DESC
        LIMIT 1;
    """, (2, test_date))
    assert ped is not None, "El procedimiento no insertó el pedido."
    id_pedido = ped[0]

    # Buscar detalle
    det = fetch_one(cur, """
        SELECT id_producto, cantidad
        FROM detalle_pedido
        WHERE id_pedido = %s;
    """, (id_pedido,))
    assert det is not None, "El procedimiento no insertó el detalle del pedido."
    assert det[0] == 3 and int(det[1]) == 2, "Detalle no coincide (producto 3, cantidad 2)."

    # Cleanup (detalle, auditoría y pedido)
    cur.execute("DELETE FROM detalle_pedido WHERE id_pedido = %s;", (id_pedido,))
    cur.execute("DELETE FROM auditoria_pedidos WHERE id_cliente = %s AND fecha_pedido = %s;", (2, test_date))

