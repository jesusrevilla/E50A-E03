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

def test_indice_compuesto_existe():
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        query = "SELECT indexname FROM pg_indexes WHERE indexname = 'idx_cliente_producto';"
        cur.execute(query)
        resultado = cur.fetchone()
        
        assert resultado is not None, "El índice 'idx_cliente_producto' no fue encontrado en la base de datos."
        assert resultado[0] == 'idx_cliente_producto'
        
    finally:
        cur.close()
        conn.close()
