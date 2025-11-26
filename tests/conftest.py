import pytest
import psycopg2
import os

@pytest.fixture(scope="session")
def db_conn():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
        database=os.environ.get("DB_NAME", "exercises")
    )
    yield conn
    conn.close()

@pytest.fixture(scope="function", autouse=True)
def cursor(db_conn):
    cursor = db_conn.cursor()
    yield cursor
    db_conn.rollback()
    cursor.close()
