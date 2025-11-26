import psycopg2
import pytest

def test_consultas_grafo():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM rutas r
        JOIN ciudades c1 ON r.id_origen = c1.id
        WHERE c1.nombre = 'San Luis Potosí'
    """)
    count_rutas = cur.fetchone()[0]
    assert count_rutas >= 2

    cur.close()
    conn.close()
