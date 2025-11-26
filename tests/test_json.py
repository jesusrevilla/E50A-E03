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
    conn.close()


def test_json_field(db):
    cur = db.cursor()
    cur.execute("""
        INSERT INTO clientes(data)
        VALUES ('{"nombre": "Luis", "edad": 22}')
        RETURNING id;
    """)
    pk = cur.fetchone()[0]
    db.commit()

    cur.execute("SELECT data->>'nombre' FROM clientes WHERE id=%s;", (pk,))
    assert cur.fetchone()[0] == "Luis"

