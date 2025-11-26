import psycopg2
import pytest
from pathlib import Path

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="module")
def db():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True

    sql_dir = Path(".")

    with open(sql_dir / "create_tables.sql", "r") as f:
        with conn.cursor() as cur:
            cur.execute(f.read())

    with open(sql_dir / "insert_data.sql", "r") as f:
        with conn.cursor() as cur:
            cur.execute(f.read())

    with open(sql_dir / "script.sql", "r") as f:
        with conn.cursor() as cur:
            cur.execute(f.read())

    yield conn

    conn.close()


def run_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        try:
            return cur.fetchall()
        except:
            return None

def test_funcion_total_gastado_por_cliente(db):
    query = "SELECT total_gastado_por_cliente(1);"
    result = run_query(db, query)
    esperado = 1251.00

    assert float(result[0][0]) == esperado

