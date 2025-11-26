import pytest
import psycopg2

def test_vista_detalle_pedidos():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM vista_detalle_pedidos")
    results = cur.fetchall()
    assert len(results) >= 3
    cur.close()
    conn.close()
