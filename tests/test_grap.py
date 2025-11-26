import psycopg2

def test_grafo_rutas():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT c1.nombre, c2.nombre, distancia_km
        FROM rutas r
        JOIN ciudades c1 ON r.id_origen = c1.id
        JOIN ciudades c2 ON r.id_destino = c2.id
        WHERE r.id_origen = 1;
    """)
    rows = cur.fetchall()

    assert ("San Luis Potosí", "Querétaro", 180) in rows

    assert ("San Luis Potosí", "CDMX", 410) in rows

    conn.close()
