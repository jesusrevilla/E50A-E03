import psycopg2

def test_total_spent_by_client():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Test client 1 spending
    cursor.execute("SELECT total_gastado_por_cliente(1);")
    result = cursor.fetchone()
    assert result[0] == 2450.50  # assuming the expected total for client 1 is 2450.50
    
    cursor.close()
    conn.close()

