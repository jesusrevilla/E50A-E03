def test_view(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM vista_detalle_pedidos;")
    assert cur.fetchall() != []

