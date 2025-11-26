import psycopg2
import pytest

DB = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def test_store_procedure_registrar_pedido():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    #Llama al procedure
    cur.execute("CALL registrar_pedido(1, '2025-06-01', 2, 3);")
    conn.commit()

    #Verifica que existe el pedido
    cur.execute("SELECT id_pedido FROM pedidos WHERE fecha='2025-06-01';")
    pedido = cur.fetchone()
    assert pedido is not None

    pedido_id = pedido[0]

    cur.execute("SELECT cantidad FROM detalle_pedido WHERE id_pedido=%s;", (pedido_id,))
    detalle = cur.fetchone()

    assert detalle is not None
    assert detalle[0] == 3  # cantidad correcta

    conn.close()
