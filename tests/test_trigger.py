import psycopg2
import pytest

def test_trigger_auditoria():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-07-01');")
    
    cur.execute("SELECT id_cliente, fecha_pedido FROM auditoria_pedidos ORDER BY id_auditoria DESC LIMIT 1;")
    res = cur.fetchone()
    
    assert res is not None
    assert res[0] == 2
    assert str(res[1]) == '2025-07-01'
    
    cur.close()
    conn.close()
