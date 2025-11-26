# app/db.py
import psycopg2

def run_query(query):
    conn = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(query)

    try:
        result = cur.fetchall()
    except psycopg2.ProgrammingError:
        result = []

    conn.commit()
    cur.close()
    conn.close()
    return result
