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


def test_registrar_pedido_inserta_pedido_y_detalle():
    init_db()

    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        # Llamamos al procedimiento:
        # cliente 1, fecha 2025-05-20, producto 2, cantidad 3
        cur.execute("CALL registrar_pedido(1, '2025-05-20', 2, 3);")

        # Debe existir al menos un pedido con esa fecha y cliente
        cur.execute(
            """
            SELECT id_pedido
            FROM pedidos
            WHERE id_cliente = 1 AND fecha = DATE '2025-05-20';
            """
        )
        pedidos = cur.fetchall()
        assert len(pedidos) >= 1

        # Tomamos los ids de los pedidos nuevos
        ids_pedidos = [p[0] for p in pedidos]

        # En detalle_pedido debe haber registro(s) correspondientes
        cur.execute(
            """
            SELECT SUM(cantidad)
            FROM detalle_pedido
            WHERE id_pedido = ANY(%s) AND id_producto = 2;
            """,
            (ids_pedidos,),
        )
        total_cant, = cur.fetchone()
        # Debe sumar al menos 3 (por la llamada que hicimos)
        assert total_cant is not None
        assert total_cant >= 3
    finally:
        cur.close()
        conn.close()
