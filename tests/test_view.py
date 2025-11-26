import os
import psycopg2
from decimal import Decimal

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )

def test_vista_detalle_pedidos():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM vista_detalle_pedidos;")
    total_filas = cur.fetchone()[0]
    assert total_filas == 3

    cur.execute("""
        SELECT total_linea
        FROM vista_detalle_pedidos
        WHERE nombre_cliente = 'Ana Torres'
          AND nombre_producto = 'Laptop';
    """)
    total_linea = cur.fetchone()[0]
    assert Decimal(total_linea) == Decimal("1200.00")

    cur.close()
    conn.close()
