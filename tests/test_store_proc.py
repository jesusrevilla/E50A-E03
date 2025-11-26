import psycopg2

def test_stored_procedure():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("CALL sp_crear_cliente('marcela');")

    cur.execute("SELECT COUNT(*) FROM clientes WHERE nombre='marcela';")
    count = cur.fetchone()[0]
    assert count == 1
