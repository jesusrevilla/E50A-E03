import pytest
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def test_vista_detalle_pedidos_existencia():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM vista_detalle_pedidos;")
    fila = cur.fetchall()
    
    assert len(fila) > 0
  
    cur.close()
    conn.close()
