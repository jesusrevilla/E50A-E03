import psycopg2

def test_json_attribute_query():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Query products with brand Dell
    cursor.execute("SELECT * FROM productos_json WHERE atributos ->> 'marca' = 'Dell';")
    products = cursor.fetchall()
    assert len(products) == 1  # Assuming only one Dell product
    
    cursor.close()
    conn.close()

