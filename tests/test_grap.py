import psycopg2
import pytest

def test_rutas():
    # Conexión a la base de datos
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()
    
    # Ejecutar consulta de rutas desde San Luis Potosí
    cur.execute("""
        SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
        FROM rutas r
        JOIN ciudades c1 ON r.id_origen = c1.id
        JOIN ciudades c2 ON r.id_destino = c2.id
        WHERE r.id_origen = 1;
    """)
    result = cur.fetchall()
    
    # Verificar el resultado
    assert result == [('San Luis Potosí', 'Querétaro', 180), 
                      ('San Luis Potosí', 'CDMX', 410)]
    
    cur.close()
    conn.close()

