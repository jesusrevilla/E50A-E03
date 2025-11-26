import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def run_query(q):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(q)
            try:
                return cur.fetchall()
            except:
                return None

def test_trigger_auditoria():
    # Ejecutar inserción en pedidos
    run_query("""
        INSERT INTO pedidos (id_cliente, fecha)
        VALUES (1, '2025-06-01');
    """)

    # Verificar que la auditoría registró el evento
    result = run_query("""
        SELECT id_cliente, fecha_pedido
        FROM auditoria_pedidos
        ORDER BY id_auditoria DESC
        LIMIT 1;
    """)

    assert result is not None
    assert len(result) == 1
    assert result[0][0] == 1
    assert str(result[0][1]) == '2025-06-01'
