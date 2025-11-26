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

def test_total_cliente1():
    result = run_query("SELECT total_gastado_por_cliente(1);")
    total = float(result[0][0])
    print(f"Total gastado por cliente 1: {total}")
    assert total == 1251.00

