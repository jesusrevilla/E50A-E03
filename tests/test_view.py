import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(q):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(q)
            try:
                return cur.fetchall()
            except:
                return None

def test_vista_detalle():
    result = run_query("""
        SELECT DISTINCT cliente, producto, cantidad
        FROM vista_detalle_pedidos
        ORDER BY cliente, producto;
    """)

    assert ("Ana Torres", "Laptop", 1) in result
    assert ("Ana Torres", "Mouse", 2) in result
    assert ("Luis Pérez", "Teclado", 1) in result


