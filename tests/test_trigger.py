
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


def test_trigger_auditoria_pedidos_inserta_registro():
    init_db()

    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        # Insertamos un pedido "manual" para disparar el trigger
        cur.execute(
            "INSERT INTO pedidos (id_cliente, fecha) VALUES (1, DATE '2025-05-20');"
        )

        # Debe haberse insertado algo en auditoria_pedidos
        cur.execute(
            """
            SELECT id_cliente, fecha_pedido, fecha_registro
            FROM auditoria_pedidos
            ORDER BY id_auditoria DESC
            LIMIT 1;
            """
        )
        row = cur.fetchone()
        assert row is not None

        id_cliente, fecha_pedido, fecha_registro = row
        assert id_cliente == 1
        assert str(fecha_pedido) == "2025-05-20"
        assert fecha_registro is not None
    finally:
        cur.close()
        conn.close()
