import pytest
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def test_ruta_slp_queretaro():
    conn = get_connection()
    try:
        cur = conn.cursor()
        
        query = """
        SELECT c_destino.nombre, r.distancia_km
        FROM rutas r
        JOIN ciudades c_origen ON r.id_origen = c_origen.id
        JOIN ciudades c_destino ON r.id_destino = c_destino.id
        WHERE c_origen.nombre = 'San Luis Potosí';
        """
        cur.execute(query)
        rutas = cur.fetchall()

        rutas_dict = {r[0]: r[1] for r in rutas}
        
        assert 'Querétaro' in rutas_dict
        assert rutas_dict['Querétaro'] == 180
        assert 'CDMX' in rutas_dict
        
    finally:
        cur.close()
        conn.close()
