import psycopg2

def test_vista_detalle_pedidos():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("SELECT * FROM vista_detalle_pedidos;")
    filas = cur.fetchall()

    assert len(filas) >= 1

