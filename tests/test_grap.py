
import psycopg2
from .conftest import db_connection 

def test_rutas_desde_san_luis_potosi():
    """Verifica que todas las rutas desde SLP estén registradas."""
    conn = db_connection()
    cur = conn.cursor()
    
    query = """
    SELECT c_destino.nombre
    FROM rutas r
    JOIN ciudades c_origen ON r.id_origen = c_origen.id
    JOIN ciudades c_destino ON r.id_destino = c_destino.id
    WHERE c_origen.nombre = 'San Luis Potosí';
    """
    cur.execute(query)
    resultados = [row[0] for row in cur.fetchall()]
    
    rutas_esperadas = {'Querétaro', 'CDMX'}
    
    assert set(resultados) == rutas_esperadas
    assert len(resultados) == 2
    
    cur.close()
    conn.close()
