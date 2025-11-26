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

def test_trigger_auditoria_pedidos():
    conn = get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO pedidos (id_cliente, fecha)
        VALUES (2, '2025-06-15')
        RETURNING id_pedido;
    """)
    _ = cur.fetchone()[0]

    cur.execute("""
        SELECT id_auditoria
        FROM auditoria_pedidos
        WHERE id_cliente = 2
          AND fecha_pedido = '2025-06-15';
    """)
    row = cur.fetchone()
    assert row is not None

    cur.close()
    conn.close()

