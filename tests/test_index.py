import psycopg2
import pytest

def test_indice_compuesto():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    # Verificar que el índice existe
    cur.execute("""
        SELECT COUNT(*) FROM pg_indexes 
        WHERE indexname = 'idx_cliente_producto'
    """)
    assert cur.fetchone()[0] == 1
    
    cur.close()
    conn.close()
