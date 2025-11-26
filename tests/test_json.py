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

def test_json_query_marca_dell(db_connection):
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT nombre
        FROM productos_json
        WHERE atributos ->> 'marca' = 'Dell';
    """)

    result = cursor.fetchall()

    assert len(result) > 0, "La consulta no encontro productos marca 'Dell'"

    nombres = [fila[0] for fila in result]
    assert "Laptop" in nombres, "No se encontro el producto 'Laptop' con marca Dell"

