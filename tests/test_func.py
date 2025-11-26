import psycopg2
import pytest

def test_total_gastado_funcion():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT total_gastado_por_cliente(1);")
    res = cur.fetchone()
    
    assert float(res[0]) == 1251.00
    
    cur.close()
    conn.close()
