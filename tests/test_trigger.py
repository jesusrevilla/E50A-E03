import psycopg2
import pytest
from datetime import date

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(query, params=None):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            try:
                return cur.fetchall()
            except psycopg2.ProgrammingError:
                return None

def test_trigger_auditoria_pedidos():
    
    run_query("INSERT INTO pedidos (id_cliente, fecha) VALUES (%s, %s);", (1, date(2025, 11, 25)))

    result = run_query("SELECT id_cliente, fecha_pedido FROM auditoria_pedidos ORDER BY id_auditoria DESC LIMIT 1;")


    assert result[0][0] == 1
    assert str(result[0][1]) == "2025-11-25"

