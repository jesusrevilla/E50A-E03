import psycopg2
import pytest

@pytest.fixture(scope="module")
def db_connection():
   
    conn = psycopg2.connect(
        host="localhost",
        database="test_db",  
        user="postgres",
        password="postgres"
    )
    yield conn
    conn.close()
