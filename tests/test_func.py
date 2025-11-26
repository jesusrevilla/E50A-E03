import psycopg2

def test_function_basic():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()
    cur.execute("SELECT mi_funcion(5);")
    result = cur.fetchone()[0]
    assert result == 25 

def test_function_null_case():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()
    cur.execute("SELECT mi_funcion(NULL);")
    result = cur.fetchone()[0]
    assert result is None
