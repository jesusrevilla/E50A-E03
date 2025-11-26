import psycopg2

def test_trigger_auditoria():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-22') RETURNING id_pedido;")
    nuevo = cur.fetchone()[0]
    conn.commit()

    cur.execute("SELECT id_cliente FROM auditoria_pedidos ORDER BY id_auditoria DESC LIMIT 1;")
    audit_cliente = cur.fetchone()[0]

    assert audit_cliente == 1

    conn.close()
