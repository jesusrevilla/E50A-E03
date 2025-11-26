import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        dbname="testdb",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    yield conn
    conn.close()

def test_procedure_exists(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT proname
        FROM pg_proc
        WHERE proname = 'registrar_pedido'
          AND prokind = 'p';   -- 'p' = procedure
    """)

    result = cursor.fetchone()

    assert result is not None, "El procedimiento 'registrar_pedido' no existe"
    assert result[0] == 'registrar_pedido'

