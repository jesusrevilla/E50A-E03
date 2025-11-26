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

def test_tables_exist(db_connection):
    cursor = db_connection.cursor()

    expected_tables = [
        'clientes',
        'productos',
        'pedidos',
        'detalle_pedido'
    ]

    for table in expected_tables:
        cursor.execute(f"SELECT to_regclass('{table}');")
        result = cursor.fetchone()
        assert result[0] == table, f"La tabla '{table}' no existe"

def test_view_exists(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT table_name 
        FROM information_schema.views
        WHERE table_name = 'vista_detalle_pedidos';
    """)

    result = cursor.fetchone()

    assert result is not None, "La vista 'vista_detalle_pedidos' no existe"
    assert result[0] == 'vista_detalle_pedidos'
