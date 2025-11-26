import psycopg2
import pytest

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="exercises", 
        user="postgres",
        password="postgres"
    )

def test_vista_detalle_pedidos():
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT COUNT(*) FROM information_schema.views 
            WHERE table_name = 'vista_detalle_pedidos'
        """)
        assert cur.fetchone()[0] == 1
        
        cur.execute("SELECT COUNT(*) FROM vista_detalle_pedidos")
        count = cur.fetchone()[0]
        assert count >= 3
        
    finally:
        cur.close()
        conn.close()
