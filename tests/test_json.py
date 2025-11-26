import psycopg2
import json

def test_json_insert_and_select():
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cur = conn.cursor()

    data = {"os": "android", "ram": 8}
    cur.execute(
        "INSERT INTO devices(info) VALUES (%s) RETURNING id;",
        (json.dumps(data),)
    )
    did = cur.fetchone()[0]
    conn.commit()

    cur.execute("SELECT info->>'os' FROM devices WHERE id=%s;", (did,))
    result = cur.fetchone()[0]
    assert result == "android"
