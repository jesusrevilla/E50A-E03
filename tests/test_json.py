import pytest
import psycopg2

def test_productos_json():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos_json WHERE atributos ->> 'marca' = 'Dell'")
    results = cur.fetchall()
    assert len(results) >= 1
    cur.close()
    conn.close()

def test_usuarios_json():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT nombre, correo FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]'")
    results = cur.fetchall()
    assert len(results) >= 2
    cur.close()
    conn.close()
