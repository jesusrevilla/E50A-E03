import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(query):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def test_productos_con_marca_dell():
    json_data = '{"marca": "Dell", "color": "Rojo"}'
    run_query(f"INSERT INTO productos_json (nombre, atributos) VALUES ('TestItem', '{json_data}');")

    query = "SELECT nombre FROM productos_json WHERE atributos ->> 'color' = 'Rojo';"
    res = run_query(query, fetchone=True)

    assert res is not None  
    assert res[0] == 'TestItem'  



def test_usuarios_con_inicio_sesion():
    query = """
        SELECT nombre, correo
        FROM usuarios
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """
    result = run_query(query)

    expected_result = [
        ('Laura Gómez', 'laura@example.com'),
        ('Pedro Ruiz', 'pedro@example.com')
    ]

    assert result == expected_result
