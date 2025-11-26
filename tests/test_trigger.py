import psycopg2
import pytest

def test_trigger_auditoria():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM auditoria_pedidos")
    count_antes = cur.fetchone()[0]

    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-25')")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM auditoria_pedidos")
    count_despues = cur.fetchone()[0]

    assert count_despues == count_antes + 1

    cur.close()
    conn.close()
