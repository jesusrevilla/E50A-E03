import psycopg2

def test_total_gastado_por_cliente():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT total_gastado_por_cliente(1);")
    total = cur.fetchone()[0]

    assert float(total) == 1251.0

    conn.close()
