import psycopg2

def test_grafo():
    conn = psycopg2.connect("dbname=test_db user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("SELECT * FROM rutas WHERE id_origen=1;")
    rows = cur.fetchall()

    assert len(rows) >= 1
    conn.close()

