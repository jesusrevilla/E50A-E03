
def test_func(conn):
    cur = conn.cursor()
    cur.execute("SELECT total_gastado_por_cliente(1);")
    total = cur.fetchone()[0]
    assert total >= 0

