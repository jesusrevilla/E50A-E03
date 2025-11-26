import psycopg2

def test_routes_between_cities():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Test routes from San Luis Potosí
    cursor.execute("SELECT id_destino, distancia_km FROM rutas WHERE id_origen = 1;")
    routes = cursor.fetchall()
    assert len(routes) == 2  # Expected two routes from San Luis Potosí
    
    cursor.close()
    conn.close()

