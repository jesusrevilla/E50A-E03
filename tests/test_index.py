import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )

def test_indice_idx_cliente_producto_existe():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT indexname
        FROM pg_indexes
        WHERE tablename = 'pedidos'
          AND indexname = 'idx_cliente_producto';
    """)
    row = cur.fetchone()
    assert row is not None 

    cur.close()
    conn.close()
