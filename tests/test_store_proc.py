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

def test_procedimiento_registrar_pedido():
    init_db()
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute("CALL registrar_pedido(1, '2025-06-01', 2, 3);")

        cur.execute("SELECT COUNT(*) FROM pedidos WHERE fecha = '2025-06-01';")
        (count_pedidos,) = cur.fetchone()
        assert count_pedidos == 1

        cur.execute("""
            SELECT cantidad FROM detalle_pedido 
            WHERE id_producto = 2 ORDER BY id_detalle DESC LIMIT 1;
        """)
        (cantidad,) = cur.fetchone()
        assert cantidad == 3  

    finally:
        cur.close()
        conn.close()
