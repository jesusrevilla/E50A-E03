import pytest
import psycopg2

DB_CONFIG = {
    "dbname": "test_db", 
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="function")
def db_cursor():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    conn.autocommit = False 
    
    yield cursor
    
    conn.rollback()
    cursor.close()
    conn.close()
