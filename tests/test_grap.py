import psycopg2
import pytest

def test_graph_queries():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()
    
    query = """
    SELECT c_destino.nombre 
    FROM rutas r
    JOIN ciudades c_origen ON r.id_origen = c_origen.id
    JOIN ciudades c_destino ON r.id_destino = c_destino.id
    WHERE c_origen.nombre = 'San Luis Potosí';
    """
    cur.execute(query)
    destinos = [row[0] for row in cur.fetchall()]
    
    assert 'Querétaro' in destinos
    assert 'CDMX' in destinos
    
    cur.close()
    conn.close()
