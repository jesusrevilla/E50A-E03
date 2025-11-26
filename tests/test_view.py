import psycopg2

def test_view_detalle_pedidos():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Verificar si la vista existe
    cursor.execute("SELECT * FROM vista_detalle_pedidos;")
    result = cursor.fetchall()
    
    # Verificar que la vista devuelva los resultados esperados
    assert len(result) > 0, "La vista 'vista_detalle_pedidos' no devuelve resultados."
    
    cursor.close()
    conn.close()

