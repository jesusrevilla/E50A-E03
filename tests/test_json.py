import psycopg2
from .conftest import db_connection # Asume configuración de conexión

def test_consulta_productos_por_marca():
    """Verifica la consulta con el operador ->> en la tabla productos_json."""
    conn = db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT nombre FROM productos_json WHERE atributos ->> 'marca' = 'Samsung';")
    resultado = cur.fetchone()
    
    assert resultado is not None
    assert resultado[0] == 'Smartphone'
    
    cur.close()
    conn.close()

def test_consulta_usuarios_por_accion():
    """Verifica la consulta de un elemento dentro del arreglo JSONB usando el operador @>."""
    conn = db_connection()
    cur = conn.cursor()
    
    # Debe encontrar a Laura Gómez y Pedro Ruiz
    cur.execute("SELECT COUNT(*) FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"comentó_publicación\"}]';")
    count = cur.fetchone()[0]
    
    assert count == 1
    
    cur.close()
    conn.close()
