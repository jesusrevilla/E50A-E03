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

def test_graph_tables_exist(db_connection):
    cursor = db_connection.cursor()

    expected_tables = [
        'ciudades',
        'rutas'
    ]

    for table in expected_tables:
        cursor.execute(f"SELECT to_regclass('{table}');")
        result = cursor.fetchone()
        assert result[0] == table, f"La tabla '{table}' no existe"

