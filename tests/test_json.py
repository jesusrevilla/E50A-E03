import psycopg2

def test_json_query():
    conn = psycopg2.connect("dbname=test_db user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("SELECT * FROM productos_json WHERE atributos->>'marca'='Dell';")
    rows = cur.fetchall()

    assert len(rows) == 1
    conn.close()

