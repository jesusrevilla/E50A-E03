import os
from pathlib import Path
import psycopg2


ROOT = Path(__file__).resolve().parents[1]


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )


def run_sql_file(cur, filename: str) -> None:
    path = ROOT / filename
    with path.open(encoding="utf-8") as f:
        cur.execute(f.read())


def init_db():
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")

        run_sql_file(cur, "01_create_tables.sql")
        run_sql_file(cur, "02_insert_data.sql")
        run_sql_file(cur, "script.sql")
    finally:
        cur.close()
        conn.close()

def test_json_historial_pedro_ruiz():
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT ha.value->>'accion' 
            FROM usuarios u,
                 LATERAL jsonb_array_elements(u.historial_actividad) AS ha
            WHERE u.nombre = 'Pedro Ruiz';
        """)

        acciones = [row[0] for row in cur.fetchall()]
        assert "inicio_sesion" in acciones
        assert "comentó_publicación" in acciones

    finally:
        cur.close()
        conn.close()
