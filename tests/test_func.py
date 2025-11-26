import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    yield conn
    conn.close()

def test_function_exists(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT proname
        FROM pg_proc
        WHERE proname = 'total_gastado_por_cliente'
          AND prokind = 'f';   -- 'f' = function
    """)

    result = cursor.fetchone()

    assert result is not None, "La función 'total_gastado_por_cliente' no existe"
    assert result[0] == 'total_gastado_por_cliente'

