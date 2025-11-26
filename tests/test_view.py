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

def test_vista_detalle_pedidos():
    """La vista 'vista_detalle_pedidos' debe devolver los resultados correctos."""
    query = """
        SELECT * FROM vista_detalle_pedidos;
    """
    result = run_query(query)

    expected_result = [
        ('Ana Torres', 'Laptop', 1, 1200.00),
        ('Ana Torres', 'Mouse', 2, 51.00),
        ('Luis Pérez', 'Teclado', 1, 45.00)
    ]

    assert result == expected_result
