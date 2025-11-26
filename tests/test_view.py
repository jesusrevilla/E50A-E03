
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

def test_columnas_vista():
    result = run_query("SELECT column_name FROM information_schema.columns WHERE table_name = 'vista_detalle_pedidos';")
    columnas = {row[0] for row in
