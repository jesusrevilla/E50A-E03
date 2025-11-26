import psycopg2

def test_total_gastado_por_cliente():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("SELECT total_gastado_por_cliente(1);")
    total = cur.fetchone()[0]

    assert total >= 0

