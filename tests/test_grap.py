import psycopg2
import pytest

DB = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def test_rutas_from_slp():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    #ve que SLP es ciudad con id 1
    cur.execute("SELECT id_destino FROM rutas WHERE id_origen=1 ORDER BY id_destino;")
    destinos = [r[0] for r in cur.fetchall()]
    assert destinos == [2, 5] 

    conn.close()

