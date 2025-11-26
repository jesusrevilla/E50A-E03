import psycopg2
import pytest

DB = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def test_trigger_auditoria():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    #inserta pedido para activar el trigger
    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-06-02') RETURNING id_pedido;")
    pedido_new = cur.fetchone()
    conn.commit()

    #ver la auditoría
    cur.execute("SELECT id_cliente, fecha_pedido FROM auditoria_pedidos WHERE fecha_pedido='2025-06-02';")
    auditoria = cur.fetchone()

    assert auditoria is not None
    assert auditoria[0] == 2  # cliente 2 es (Luis)

    conn.close()
