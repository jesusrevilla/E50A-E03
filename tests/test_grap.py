import pytest
import psycopg2

def test_rutas_ciudades():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT c1.nombre as origen, c2.nombre as destino, r.distancia_km
        FROM rutas r
        JOIN ciudades c1 ON r.id_origen = c1.id
        JOIN ciudades c2 ON r.id_destino = c2.id
        WHERE c1.nombre = 'San Luis Potosí'
    """)
    results = cur.fetchall()
    assert len(results) >= 2
    cur.close()
    conn.close()
