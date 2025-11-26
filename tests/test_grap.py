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

def test_rutas_desde_slp(db):
    query = """
    SELECT d.nombre
    FROM rutas r
    JOIN ciudades o ON r.id_origen = o.id
    JOIN ciudades d ON r.id_destino = d.id
    WHERE o.nombre = 'San Luis Potosí';
    """
    result = run_query(db, query)

    ciudades = [row[0] for row in result]

    assert "Querétaro" in ciudades
    assert "CDMX" in ciudades
    assert len(ciudades) == 2

