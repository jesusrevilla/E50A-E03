import psycopg2

def test_registrar_pedido():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM pedidos;")
    antes = cur.fetchone()[0]

    cur.execute("CALL registrar_pedido(2, '2025-05-21', 3, 5);")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM pedidos;")
    despues = cur.fetchone()[0]
    assert despues == antes + 1

    cur.execute("""
        SELECT d.cantidad, p.nombre
        FROM detalle_pedido d
        JOIN productos p ON d.id_producto=p.id_producto
        ORDER BY id_detalle DESC LIMIT 1;
    """)
    cant, prod = cur.fetchone()
    assert cant == 5
    assert prod == "Teclado"

    conn.close()
