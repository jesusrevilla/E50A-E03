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

def test_trigger_exists(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT tgname
        FROM pg_trigger
        WHERE tgname = 'trg_registrar_auditoria_pedido'
          AND NOT tgisinternal;   -- evitar triggers internos del sistema
    """)

    result = cursor.fetchone()

    assert result is not None, "El trigger 'trg_registrar_auditoria_pedido' no existe"
    assert result[0] == 'trg_registrar_auditoria_pedido'

