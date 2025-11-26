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

def test_vista_detalle_pedidos():
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM vista_detalle_pedidos ORDER BY id_detalle;")
        rows = cur.fetchall()

        assert rows[0][1] == "Laptop"
        assert rows[0][3] == "Ana Torres"

        assert rows[1][1] == "Mouse"
        assert rows[2][3] == "Luis Pérez"

    finally:
        cur.close()
        conn.close()

