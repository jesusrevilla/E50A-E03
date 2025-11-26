def test_index(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT indexname FROM pg_indexes
        WHERE indexname = 'idx_cliente_producto';
    """)
    assert cur.fetchone() is not None

