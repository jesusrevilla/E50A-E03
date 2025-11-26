import psycopg2

def test_index_exists():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Verificar si el índice compuesto existe
    cursor.execute("SELECT * FROM pg_indexes WHERE indexname = 'idx_cliente_producto';")
    index = cursor.fetchone()
    assert index is not None, "El índice idx_cliente_producto no existe."
    
    cursor.close()
    conn.close()


