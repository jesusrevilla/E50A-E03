import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_connection():
    # Los detalles de la conexión coinciden con el YAML de GitHub Actions
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",  # Corregir la base de datos a test_db
        user="postgres",
        password="postgres"
    )
    yield conn
    conn.close()
