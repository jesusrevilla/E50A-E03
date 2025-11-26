
# tests/conftest.py
import os
import psycopg2
import pytest

def get_db_params():
    return {
        "dbname": os.getenv("POSTGRES_DB", "test_db"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
    }

@pytest.fixture(scope="session")
def conn():
    params = get_db_params()
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    yield conn
    conn.close()

@pytest.fixture
def cur(conn):
    cur = conn.cursor()
    yield cur
    cur.close()

def fetch_one(cur, sql, args=None):
    cur.execute(sql, args or ())
    return cur.fetchone()

def fetch_all(cur, sql, args=None):
    cur.execute(sql, args or ())
    return cur.fetchall()
