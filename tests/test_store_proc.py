import psycopg2

def test_registrar_pedido():
    conn = psycopg2.connect("dbname=test_db user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("CALL registrar_pedido(1, '2025-05-25', 1, 1);")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM pedidos WHERE fecha='2025-05-25';")
    count = cur.fetchone()[0]

    assert count >= 1
    conn.close()

