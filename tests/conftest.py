import psycopg2
import pytest

DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="module")
def conn():
    connection = psycopg2.connect(**DB_CONFIG)
    yield connection
    connection.close()
