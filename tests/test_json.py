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

def test_json_historial_actividad(db):
    query = """
    SELECT actividad->>'accion'
    FROM usuarios,
         jsonb_array_elements(historial_actividad) AS actividad
    WHERE id = 1;
    """
    result = run_query(db, query)

    acciones = [row[0] for row in result]

    assert "inicio_sesion" in acciones
    assert "subio_archivo" in acciones
    assert "cerró_sesion" in acciones

