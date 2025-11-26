import psycopg2

def test_trigger_created_at():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO pedidos(cliente) VALUES ('x') RETURNING id;")
    pid = cur.fetchone()[0]
    conn.commit()

    cur.execute("SELECT created_at FROM pedidos WHERE id=%s;", (pid,))
    ts = cur.fetchone()[0]
    assert ts is not None
