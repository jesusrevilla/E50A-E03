import psycopg2
import pytest

def test_registrar_pedido_procedure():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute("CALL registrar_pedido(2, '2025-06-01', 2, 5);")
    
    cur.execute("SELECT cantidad FROM detalle_pedido WHERE cantidad = 5 ORDER BY id_detalle DESC LIMIT 1;")
    res = cur.fetchone()
    
    assert res is not None
    assert res[0] == 5
    
    cur.close()
    conn.close()
