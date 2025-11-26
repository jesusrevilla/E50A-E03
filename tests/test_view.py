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

    with open(sql_dir / "01_create_tables.sql", "r") as f:
        with conn.cursor() as cur:
            cur.execute(f.read())

    with open(sql_dir / "02_insert_data.sql", "r") as f:
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


# ============================================================
# 1. Test de vista vista_detalle_pedidos
# ============================================================

def test_vista_detalle_pedidos(db):
    query = """
    SELECT cliente, producto, cantidad, total_linea
    FROM vista_detalle_pedidos
    ORDER BY cliente, producto;
    """
    result = run_query(db, query)

    assert ("Ana Torres", "Laptop", 1, 1200.00) in result
    assert ("Ana Torres", "Mouse", 2, 51.00) in result
    assert ("Luis Pérez", "Teclado", 1, 45.00) in result

