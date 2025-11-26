
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
        run_sql_file(cur, "01_create_tables.sql")
        run_sql_file(cur, "02_insert_data.sql")
        run_sql_file(cur, "script.sql")
    finally:
        cur.close()
        conn.close()


def test_productos_json_marca_dell():
    init_db()

    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT nombre
            FROM productos_json
            WHERE atributos ->> 'marca' = 'Dell';
            """
        )
        rows = cur.fetchall()
        assert len(rows) == 1
        (nombre,) = rows[0]
        assert nombre == "Laptop"
    finally:
        cur.close()
        conn.close()


def test_usuarios_con_inicio_sesion():
    init_db()

    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT nombre
            FROM usuarios
            WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
            """
        )
        rows = cur.fetchall()
        nombres = sorted(r[0] for r in rows)
        # De acuerdo a los INSERT de ejemplo:
        assert nombres == ["Laura Gómez", "Pedro Ruiz"]
    finally:
        cur.close()
        conn.close()