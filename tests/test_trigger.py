import psycopg2
import pytest
from time import sleep

@pytest.fixture
def db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="test_db",
        user="postgres",
        password="postgres"
    )
    yield conn
    conn.close()


def test_trigger_updated_at(db):
    cur = db.cursor()

    cur.execute("""
        INSERT INTO productos(nombre, precio)
        VALUES ('Topo Chico', 19)
        RETURNING id, updated_at;
    """)
    pk, ts_before = cur.fetchone()
    db.commit()

    sleep(1)

    cur.execute("UPDATE productos SET precio=21 WHERE id=%s;", (pk,))
    db.commit()

    cur.execute("SELECT updated_at FROM productos WHERE id=%s;", (pk,))
    ts_after = cur.fetchone()[0]

    assert ts_after > ts_before

