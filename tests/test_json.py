def test_json(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos_json WHERE atributos ->> 'marca' = 'Dell';")
    assert cur.fetchall() != []

