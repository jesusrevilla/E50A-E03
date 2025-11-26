import psycopg2

def test_register_order():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Test inserting a new order
    cursor.callproc("registrar_pedido", (1, '2025-05-20', 2, 3))
    conn.commit()
    
    # Check if the order was inserted
    cursor.execute("SELECT * FROM pedidos WHERE id_cliente = 1 AND fecha = '2025-05-20';")
    order = cursor.fetchone()
    assert order is not None, "The new order was not inserted successfully."
    
    cursor.close()
    conn.close()

