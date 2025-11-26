

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
        sql = f.read()
    cur.execute(sql)


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


def test_vista_detalle_pedidos_datos_correctos():
    init_db()

    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT id_pedido,
                   fecha,
                   id_cliente,
                   nombre_cliente,
                   correo,
                   id_producto,
                   nombre_producto,
                   precio,
                   cantidad,
                   total_linea
            FROM vista_detalle_pedidos
            ORDER BY id_pedido, id_producto;
            """
        )
        rows = cur.fetchall()

        # Debe haber 3 filas: 2 de Ana, 1 de Luis
        assert len(rows) == 3

     
        r1 = rows[0]
        assert r1[0] == 1              # id_pedido
        assert r1[2] == 1              # id_cliente
        assert r1[3] == "Ana Torres"
        assert r1[5] == 1              # id_producto Laptop
        assert r1[6] == "Laptop"
        assert float(r1[7]) == 1200.00
        assert r1[8] == 1              # cantidad
        assert float(r1[9]) == 1200.00 # total_linea

        # 2) Ana compra 2 Mouse
        r2 = rows[1]
        assert r2[0] == 1
        assert r2[2] == 1
        assert r2[5] == 2              # id_producto Mouse
        assert r2[6] == "Mouse"
        assert float(r2[7]) == 25.50
        assert r2[8] == 2
        assert float(r2[9]) == 51.00

        # 3) Luis compra 1 Teclado
        r3 = rows[2]
        assert r3[0] == 2
        assert r3[2] == 2
        assert r3[3] == "Luis Pérez"
        assert r3[5] == 3              # id_producto Teclado
        assert r3[6] == "Teclado"
        assert float(r3[7]) == 45.00
        assert r3[8] == 1
        assert float(r3[9]) == 45.00
    finally:
        cur.close()
        conn.close()
