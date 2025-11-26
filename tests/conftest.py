# tests/conftest.py
import pytest
import psycopg2

DB_CONFIG = dict(
    host="localhost",
    port=5432,
    database="test_db",
    user="postgres",
    password="postgres"
)

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# ------ FIXTURES POR CADA GRUPO DE TESTS (según tus nombres) -------

@pytest.fixture
def func_conn():
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def graph_conn():
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def index_conn():
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def json_conn():
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def proc_conn():
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def trigger_conn():
    conn = get_connection()
    yield conn
    conn.close()

@pytest.fixture
def view_conn():
    conn = get_connection()
    yield conn
    conn.close()
