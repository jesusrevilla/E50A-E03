import psycopg2
import pytest

def test_consultas_json():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM productos_json WHERE atributos ->> 'marca' = 'Dell'")
    count_dell = cur.fetchone()[0]
    assert count_dell >= 1
    
    cur.execute("SELECT COUNT(*) FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]'")
    count_usuarios = cur.fetchone()[0]
    assert count_usuarios >= 2
    
    cur.close()
    conn.close()
