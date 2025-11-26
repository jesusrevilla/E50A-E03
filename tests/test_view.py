import psycopg2
import pytest

DB = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def test_view_detalle_pedidos():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM vista_detalle_pedidos ORDER BY id_pedido, producto;")
    rows = cur.fetchall()

  #Se evaluan 3 lineas
    assert len(rows) == 3

  # Ve una línea
    # Pedido 1 Laptop
    assert rows[0][1] == "Ana Torres"  # cliente
    assert rows[0][2] == "Laptop"
    assert rows[0][3] == 1              # cantidad
    assert float(rows[0][4]) == 1200.00 # total

    conn.close()
