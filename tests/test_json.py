import psycopg2
import pytest

DB = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def test_json_productos():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT nombre FROM productos_json
        WHERE atributos ->> 'marca' = 'Dell';
    """)
    producto = cur.fetchone()
    assert producto is not None
    assert producto[0] == "Laptop"

    conn.close()


def test_json_historial():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT nombre FROM usuarios
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)
    rows = cur.fetchall()

    #checa que Laura y Pedro si tienen inicio_sesion
    assert len(rows) == 2

    conn.close()
