import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture de pytest para establecer una conexión de módulo a la base de datos de prueba.
    """
    try:
        # Detalles que coinciden con el archivo postgresql_workflow.yml
        conn = psycopg2.connect(
            host="localhost",
            database="test_db",
            user="postgres",
            password="postgres"
        )
        # Habilitar autocommit para operaciones de DDL/DML simples
        conn.autocommit = True

    except psycopg2.Error as e:
        pytest.fail(f"Fallo al conectar con PostgreSQL: {e}")
        return

    # Entrega la conexión a las funciones de prueba
    yield conn

    # Cierra la conexión después de que todas las pruebas en el módulo han terminado
    if conn:
        conn.close()
