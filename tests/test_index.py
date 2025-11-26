import psycopg2
import pytest
import os

def test_index_creation():
    # Conexión a la base de datos usando las variables de entorno
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cur = conn.cursor()

    # Verificar si el índice existe
    cur.execute("""
        SELECT * FROM pg_indexes
        WHERE indexname = 'idx_cliente_producto';
    """)
    result = cur.fetchone()

    # Verificar que el índice exista
    assert result is not None

    cur.close()
    conn.close()

