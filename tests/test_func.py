import psycopg2
import pytest

DB = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def test_total_gastado_func():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    #Checa que Ana compró en total 1251
    cur.execute("SELECT total_gastado_por_cliente(1);")
    total = float(cur.fetchone()[0])
    assert total == 1251.00

    conn.close()
