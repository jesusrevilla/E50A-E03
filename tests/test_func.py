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

def test_total_gastado_por_cliente():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT total_gastado_por_cliente(1);")
    total = cur.fetchone()[0]

    assert Decimal(total) == Decimal("1251.00")

    cur.close()
    conn.close()

