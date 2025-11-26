import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(query):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def test_trigger_auditoria_pedido():
    query_insert = """
        INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-05-15');
    """
    run_query(query_insert)

    query_auditoria = """
        SELECT * FROM auditoria_pedidos WHERE id_cliente = 2 AND fecha_pedido = '2025-05-15';
    """
    auditoria_result = run_query(query_auditoria)

    assert len(auditoria_result) == 1  


