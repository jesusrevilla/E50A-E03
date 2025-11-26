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
def test_json_inicio_sesion():
    result = run_query("""
        SELECT nombre FROM usuarios
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)

    nombres = [r[0] for r in result]

    assert "Laura Gómez" in nombres
    assert "Pedro Ruiz" in nombres
    assert len(nombres) == 2

