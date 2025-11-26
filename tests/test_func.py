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

def test_total_gastado_por_cliente():
    """La función 'total_gastado_por_cliente' debe devolver el total gastado correctamente."""
    query = """
        SELECT total_gastado_por_cliente(1);
    """
    result = run_query(query)

    expected_total = 1200.00 + 51.00

    assert result[0][0] == expected_total
