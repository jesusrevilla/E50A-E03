import psycopg2

def test_index_exists():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT indexname
        FROM pg_indexes
        WHERE tablename = 'clientes';
    """)
    indexes = [r[0] for r in cur.fetchall()]

    assert 'idx_clientes_nombre' in indexes


def test_index_used_in_query():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("EXPLAIN SELECT * FROM clientes WHERE nombre = 'juan';")
    plan = "\n".join(row[0] for row in cur.fetchall())

    assert "Index Scan" in plan or "Bitmap Index Scan" in plan
