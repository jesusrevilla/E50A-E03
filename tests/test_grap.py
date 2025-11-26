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

def test_rutas_desde_slp():
    result = run_query("""
        SELECT c2.nombre
        FROM rutas r
        JOIN ciudades c2 ON r.id_destino = c2.id
        WHERE r.id_origen = 1;
    """)
    nombres = {r[0] for r in result}
    assert "Querétaro" in nombres
    assert "CDMX" in nombres
    assert len(nombres) == 2

