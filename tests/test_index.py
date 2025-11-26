import pytest
import psycopg2

def test_index_exists():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) 
        FROM pg_indexes 
        WHERE indexname = 'idx_cliente_producto'
    """)
    exists = cur.fetchone()[0]
    assert exists == 1
    cur.close()
    conn.close()
