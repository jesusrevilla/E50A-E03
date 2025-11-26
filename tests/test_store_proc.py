def test_store_proc(conn):
    cur = conn.cursor()
    cur.execute("CALL registrar_pedido(1, '2025-05-20', 1, 2);")
    conn.commit()

    cur.execute("SELECT * FROM pedidos ORDER BY id_pedido DESC LIMIT 1;")
    assert cur.fetchone() is not None

