
import psycopg2

def test_registrar_pedido(proc_conn):
    cur = proc_conn.cursor()

    # Llamar procedimiento
    cur.execute("CALL registrar_pedido(1, '2025-05-21', 2, 4);")

    # Verificar que se creó el pedido
    cur.execute("SELECT COUNT(*) FROM pedidos WHERE fecha='2025-05-21';")
    count = cur.fetchone()[0]

    assert count == 1

    # Verificar que también se creó el detalle
    cur.execute("""
        SELECT COUNT(*) FROM detalle_pedido dp
        JOIN pedidos p ON dp.id_pedido = p.id_pedido
        WHERE p.fecha='2025-05-21';
    """)
    detail_count = cur.fetchone()[0]

    assert detail_count == 1
