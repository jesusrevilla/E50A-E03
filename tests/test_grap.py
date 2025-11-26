

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


def test_rutas_desde_san_luis_potosi():
    init_db()

    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT c_origen.nombre AS ciudad_origen,
                   c_destino.nombre AS ciudad_destino,
                   r.distancia_km
            FROM rutas r
            JOIN ciudades c_origen  ON r.id_origen  = c_origen.id
            JOIN ciudades c_destino ON r.id_destino = c_destino.id
            WHERE c_origen.nombre = 'San Luis Potosí'
            ORDER BY ciudad_destino;
            """
        )
        rows = cur.fetchall()

   
        assert len(rows) == 2
        destinos = [r[1] for r in rows]
        distancias = [r[2] for r in rows]

        assert sorted(destinos) == ["CDMX", "Querétaro"]
        assert sorted(distancias) == [180, 410]
    finally:
        cur.close()
        conn.close()
