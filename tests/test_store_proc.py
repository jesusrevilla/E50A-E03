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


def test_registrar_pedido_total():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("CALL registrar_pedido(1, '2025-11-25', 1, 3);")
            conn.commit()

 
    result = run_query("""
        SELECT SUM(total_linea) 
        FROM vista_detalle_pedidos 
        WHERE id_cliente = 1;
    """)
    assert float(result[0][0]) == 1251.00

