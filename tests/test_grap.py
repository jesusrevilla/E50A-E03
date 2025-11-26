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

def test_grafo_rutas_desde_slp():
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        WITH RECURSIVE grafos AS (
            SELECT 
                c.id AS ciudad_id,
                c.nombre AS ciudad,
                r.id_destino,
                r.distancia_km,
                c.nombre::TEXT AS ruta
            FROM ciudades c
            JOIN rutas r ON c.id = r.id_origen
            WHERE c.id = 1
            
            UNION ALL
            
            SELECT
                c2.id AS ciudad_id,
                c2.nombre AS ciudad,
                r2.id_destino,
                r2.distancia_km,
                rd.ruta || ' - ' || c2.nombre
            FROM grafos rd
            JOIN rutas r2 ON rd.id_destino = r2.id_origen
            JOIN ciudades c2 ON r2.id_destino = c2.id
        )
        SELECT ciudad FROM grafos;
        """)

        ciudades = {row[0] for row in cur.fetchall()}

        assert "Guadalajara" in ciudades
        assert "CDMX" in ciudades
        assert "Monterrey" in ciudades

    finally:
        cur.close()
        conn.close()

