import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "test_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )

def test_rutas_desde_slp():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c1.nombre AS origen, c2.nombre AS destino, r.distancia_km
        FROM rutas r
        JOIN ciudades c1 ON c1.id = r.id_origen
        JOIN ciudades c2 ON c2.id = r.id_destino
        WHERE c1.nombre = 'San Luis Potosí'
        ORDER BY destino;
    """)

    rows = cur.fetchall()
    destinos = [r[1] for r in rows]
    distancias = [r[2] for r in rows]

    assert len(rows) == 2
    assert 'Querétaro' in destinos
    assert 'CDMX' in destinos
    assert 180 in distancias
    assert 410 in distancias

    cur.close()
    conn.close()

