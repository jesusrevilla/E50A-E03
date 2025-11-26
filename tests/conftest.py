import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture de pytest para establecer una conexión de módulo a la base de datos de prueba.
    """
    try:
        
        conn = psycopg2.connect(
            host="localhost",
            database="exercises",
            user="postgres",
            password="postgres"
        )
       
        conn.autocommit = True

    except psycopg2.Error as e:
        pytest.fail(f"Fallo al conectar con PostgreSQL: {e}")
        return

   
    yield conn

    
    if conn:
        conn.close()
