def test_trigger(conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO pedidos(id_cliente, fecha) VALUES (1, '2025-05-21');")
    conn.commit()

    cur.execute("SELECT * FROM auditoria_pedidos ORDER BY id_auditoria DESC LIMIT 1;")
    row = cur.fetchone()
    assert row is not None

