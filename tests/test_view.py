import psycopg2

def test_view_exists():
    conn = psycopg2.connect("dbname=test_db user=postgres password=postgres host=localhost")
    cur = conn.cursor()
    cur.execute("SELECT * FROM vista_detalle_pedidos;")
    rows = cur.fetchall()
    assert len(rows) > 0
    conn.close()

