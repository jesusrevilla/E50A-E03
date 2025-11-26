import psycopg2
import pytest

DB_HOST = "localhost"
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASS = "postgres"

def execute_query(query, fetch=True):
    
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute(query)
        if fetch:
            result = cur.fetchall()
            return result
        else:
            conn.commit()
            return None
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        raise
    finally:
        if conn:
            conn.close()

def test_rutas_desde_san_luis_potosi():
    """Verifica la consulta de todas las rutas que parten de 'San Luis Potosí'."""
    
    query = """
    SELECT
        c_origen.nombre AS ciudad_origen,
        c_destino.nombre AS ciudad_destino,
        r.distancia_km
    FROM
        rutas r
    JOIN
        ciudades c_origen ON r.id_origen = c_origen.id
    JOIN
        ciudades c_destino ON r.id_destino = c_destino.id
    WHERE
        c_origen.nombre = 'San Luis Potosí'
    ORDER BY
        r.distancia_km;
    """
    
    result = execute_query(query)
    
    # SLP → Querétaro (180 km)
    # SLP → CDMX (410 km)
    expected_routes = [
        ('San Luis Potosí', 'Querétaro', 180),
        ('San Luis Potosí', 'CDMX', 410)
    ]
    
    assert len(result) == 2, "Deben encontrarse 2 rutas desde San Luis Potosí."
    assert result == expected_routes, "Las rutas y distancias no coinciden con las esperadas."
