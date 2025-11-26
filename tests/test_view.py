import psycopg2

def test_view_select():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM vista_clientes LIMIT 1;")
    row = cur.fetchone()
    assert row is not None


def test_view_logic():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("SELECT total FROM vista_ventas WHERE id_cliente = 1;")
    result = cur.fetchone()
    assert result is not None


