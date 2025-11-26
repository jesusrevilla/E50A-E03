import psycopg2
import pytest

def test_funcion_total_gastado():
    conn = psycopg2.connect(
        host="localhost",
        database="exercises",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT total_gastado_por_cliente(1)")
    total = cur.fetchone()[0]
    
    assert total >= 0
    
    cur.close()
    conn.close()
