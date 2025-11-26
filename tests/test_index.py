import psycopg2

def test_index_exists():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT indexname
        FROM pg_indexes
        WHERE tablename='detalle_pedido';
    """)
    indices = [i[0] for i in cur.fetchall()]

    assert "idx_cliente_producto" in indices

    conn.close()
