import psycopg2
import pytest

def test_index_creation():
    # Conexión a la base de datos
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
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

