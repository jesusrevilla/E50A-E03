import psycopg2

def test_grafo_rutas():
    conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
    cur = conn.cursor()

    cur.execute("SELECT * FROM rutas WHERE id_origen = 1;")
    rutas = cur.fetchall()

    assert len(rutas) >= 1

