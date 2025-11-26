import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture para establecer la conexión a la base de datos de prueba.
    El scope="module" asegura que la conexión se abre una vez por módulo de prueba.
    """
    try:
        # Los detalles de la conexión coinciden con el archivo postgresql_workflow.yml
        conn = psycopg2.connect(
            host="localhost",
            database="test_db",
            user="postgres",
            password="postgres"
        )
        conn.autocommit = True  # Permite que las operaciones de DDL/DML sean inmediatas
        
    except psycopg2.Error as e:
        # Si la conexión falla, se lanza una excepción para que pytest falle inmediatamente
        pytest.fail(f"Fallo al conectar con la base de datos PostgreSQL: {e}")
        return

    # 'yield' entrega la conexión a la función de prueba
    yield conn
    
    # Esta parte se ejecuta después de que todas las pruebas en el módulo han terminado
    if conn:
        conn.close()
