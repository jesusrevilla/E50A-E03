import psycopg2

def test_registrar_pedido():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("CALL registrar_pedido(1, '2025-05-20', 2, 3);")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM pedidos WHERE fecha='2025-05-20';")
    cantidad = cur.fetchone()[0]

    assert cantidad >= 1

