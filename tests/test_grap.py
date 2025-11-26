import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(query):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def test_rutas_desde_san_luis_potosi():
    """Se deben obtener las rutas desde San Luis Potosí."""
    query = """
        SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
        FROM rutas r
        JOIN ciudades c1 ON r.id_origen = c1.id
        JOIN ciudades c2 ON r.id_destino = c2.id
        WHERE c1.nombre = 'San Luis Potosí';
    """
    result = run_query(query)

    expected_result = [
        ('San Luis Potosí', 'Querétaro', 180),
        ('San Luis Potosí', 'CDMX', 410)
    ]

    assert result == expected_result
