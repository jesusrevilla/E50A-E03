import psycopg2

def test_index_exists():
    conn = psycopg2.connect("dbname=test_db user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("""
        SELECT indexname 
        FROM pg_indexes 
        WHERE indexname='idx_cliente_producto';
    """)
    index = cur.fetchone()

    assert index is not None
    conn.close()

