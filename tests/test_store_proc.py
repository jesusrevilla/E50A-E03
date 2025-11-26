import psycopg2
import pytest

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )

def test_procedimiento_almacenado():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL registrar_pedido(1, '2025-05-20', 2, 3)")

        cur.execute("SELECT COUNT(*) FROM pedidos WHERE id_cliente = 1")
        count_pedidos = cur.fetchone()[0]
        assert count_pedidos >= 2

    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()
