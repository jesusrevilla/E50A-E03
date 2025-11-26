import psycopg2

def test_vista_detalle_pedidos():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT cliente, producto, cantidad, subtotal FROM vista_detalle_pedidos WHERE id_pedido = 1;")
    rows = cur.fetchall()

    assert len(rows) == 2 

    assert ("Ana Torres", "Laptop", 1, 1200.00) in rows

    assert ("Ana Torres", "Mouse", 2, 51.00) in rows

    conn.close()
