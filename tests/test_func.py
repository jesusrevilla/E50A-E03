import psycopg2

def test_total_spent_by_client():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Test cliente 1 gasto total
    cursor.execute("SELECT total_gastado_por_cliente(1);")
    result = cursor.fetchone()
    assert result[0] == 1296.00  # Se actualizó el valor esperado al total correcto
    
    cursor.close()
    conn.close()


