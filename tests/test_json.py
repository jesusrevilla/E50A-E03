import psycopg2
import pytest

def test_json_queries():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT nombre FROM productos_json WHERE atributos ->> 'marca' = 'Dell';")
    res_prod = cur.fetchone()
    assert res_prod[0] == 'Laptop'
    
    cur.execute("SELECT nombre FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]';")
    res_users = cur.fetchall()
    
    assert len(res_users) >= 2
    
    cur.close()
    conn.close()
