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

    # Crear tablas
    with open(sql_dir / "01_create_tables.sql", "r") as f:
        with conn.cursor() as cur:
            cur.execute(f.read())

    # Insertar datos iniciales
    with open(sql_dir / "02_insert_data.sql", "r") as f:
        with conn.cursor() as cur:
            cur.execute(f.read())

    # Crear funciones, vistas, triggers, procedimiento, etc.
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


def test_procedimiento_registrar_pedido(db):

    query = """
    SELECT COUNT(*) 
    FROM detalle_pedido
    WHERE id_pedido IN (
        SELECT id_pedido 
        FROM pedidos 
        WHERE fecha = '2025-05-20'
    );
    """
    result = run_query(db, query)

    assert result[0][0] >= 1

