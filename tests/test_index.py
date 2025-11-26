import psycopg2
import pytest

DB = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def test_index_exists():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT indexname
        FROM pg_indexes
        WHERE indexname = 'idx_cliente_producto';
    """)
    index = cur.fetchone()
    assert index is not None  #checa que el indice si debe existir
    conn.close()

