import psycopg2

def test_insert_row():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO clientes(nombre) VALUES ('pato') RETURNING id;")
    new_id = cur.fetchone()[0]
    conn.commit()

    cur.execute("SELECT nombre FROM clientes WHERE id = %s;", (new_id,))
    result = cur.fetchone()[0]
    assert result == 'pato'


def test_update_row():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO clientes(nombre) VALUES ('viejo') RETURNING id;")
    cid = cur.fetchone()[0]

    cur.execute("UPDATE clientes SET nombre = 'nuevo' WHERE id = %s;", (cid,))
    conn.commit()

    cur.execute("SELECT nombre FROM clientes WHERE id = %s;", (cid,))
    result = cur.fetchone()[0]
    assert result == 'nuevo'
