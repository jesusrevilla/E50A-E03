import psycopg2
import pytest

def test_vista_detalle_pedidos():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM vista_detalle_pedidos WHERE cliente = 'Ana Torres';")
    resultados = cur.fetchall()
    
    assert len(resultados) == 2
    assert resultados[0][3] == 1200.00 or resultados[1][3] == 1200.00
    
    cur.close()
    conn.close()
