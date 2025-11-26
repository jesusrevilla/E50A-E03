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
    """Se deben obtener los productos con la marca 'Dell'."""
    query = """
        SELECT * FROM productos_json
        WHERE atributos ->> 'marca' = 'Dell';
    """
    result = run_query(query)

    expected_result = [
        (1, 'Laptop', '{"marca": "Dell", "ram": "16GB", "procesador": "Intel i7"}')
    ]

    assert result == expected_result



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
