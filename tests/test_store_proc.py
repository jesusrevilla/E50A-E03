import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )

def test_registrar_pedido_crea_pedido_y_detalle():
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("CALL registrar_pedido(1, '2025-05-20', 2, 3);")

    cur.execute("""
        SELECT p.id_pedido
        FROM pedidos p
        JOIN detalle_pedido d ON d.id_pedido = p.id_pedido
        WHERE p.id_cliente = 1
          AND p.fecha = '2025-05-20'
          AND d.id_producto = 2
          AND d.cantidad = 3;
    """)
    row = cur.fetchone()
    assert row is not None

    cur.close()
    conn.close()
