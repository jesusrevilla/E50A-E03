def test_graph(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM rutas WHERE id_origen = 1;")
    assert cur.fetchall() != []

