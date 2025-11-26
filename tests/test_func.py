
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
    for file in ["01_create_tables.sql", "02_insert_data.sql"]:
        with open(sql_dir / file, "r") as f:
            with conn.cursor() as cur:
                cur.execute(f.read())

    with open(sql_dir / "script.sql", "r") as f:
        raw_queries = f.read()

    yield conn, raw_queries
    conn.close()

def run_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        try:
            return cur.fetchall()
        except:
            return None

def extract_query(raw_sql, index):
    parts = [q.strip() for q in raw_sql.split(";") if q.strip() != ""]
    return parts[index] + ";"

def test_productos_tecnologia(db):
    conn, raw_queries = db
    query = extract_query(raw_queries, 0)
    result = run_query(conn, query)
    nombres = [row[0] for row in result]
    assert "Laptop" in nombres
    assert "Mouse" in nombres
    assert "Teclado" in nombres

def test_usuarios_acciones(db):
    conn, raw_queries = db
    query = extract_query(raw_queries, 1)
    result = run_query(conn, query)
    acciones = [row[2] for row in result]  # columna 'accion'
    assert "inicio_sesion" in acciones
    assert "subio_archivo" in acciones
    assert "comentó_publicación" in acciones

def test_ciudades_alcanzables(db):
    conn, raw_queries = db
    query = extract_query(raw_queries, 2)
    result = run_query(conn, query)
    nombres = [row[0] for row in result]
    assert "San Luis Potosí" in nombres
    assert "Querétaro" in nombres
    assert "Guadalajara" in nombres
    assert "Monterrey" in nombres
    assert "CDMX" in nombres
    assert len(nombres) > 1
