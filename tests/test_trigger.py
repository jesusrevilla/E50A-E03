import psycopg2

def test_trigger():
    conn = psycopg2.connect("dbname=test_db user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-30');")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM auditoria_pedidos WHERE fecha_pedido='2025-05-30';")
    count = cur.fetchone()[0]

    assert count >= 1
    conn.close()

