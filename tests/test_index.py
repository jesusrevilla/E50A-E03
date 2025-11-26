import psycopg2
import pytest

def test_index_exists():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT indexname FROM pg_indexes WHERE tablename = 'detalle_pedido' AND indexname = 'idx_cliente_producto';")
    res = cur.fetchone()
    
    assert res is not None
    assert res[0] == 'idx_cliente_producto'
    
    cur.close()
    conn.close()
