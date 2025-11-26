import psycopg2
import pytest

@pytest.fixture
def db():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="test_db",
        user="postgres",
        password="postgres"
    )
    yield conn
    conn.rollback()
    conn.close()


def test_insert(db):
    cur = db.cursor()
    cur.execute("""
        INSERT INTO productos(nombre, precio)
        VALUES ('Test Cola', 11)
        RETURNING id;
    """)
    pk = cur.fetchone()[0]
    db.commit()

    cur.execute("SELECT nombre FROM productos WHERE id=%s;", (pk,))
    assert cur.fetchone()[0] == "Test Cola"


def test_update(db):
    cur = db.cursor()
    cur.execute("""
        INSERT INTO productos(nombre, precio)
        VALUES ('Test Gansito', 20)
        RETURNING id;
    """)
    pk = cur.fetchone()[0]
    db.commit()

    cur.execute("UPDATE productos SET precio=25 WHERE id=%s;", (pk,))
    db.commit()

    cur.execute("SELECT precio FROM productos WHERE id=%s;", (pk,))
    assert cur.fetchone()[0] == 25


def test_delete(db):
    cur = db.cursor()
    cur.execute("""
        INSERT INTO productos(nombre, precio)
        VALUES ('Test Sprite', 10)
        RETURNING id;
    """)
    pk = cur.fetchone()[0]
    db.commit()

    cur.execute("DELETE FROM productos WHERE id=%s;", (pk,))
    db.commit()

    cur.execute("SELECT * FROM productos WHERE id=%s;", (pk,))
    assert cur.fetchone() is None

