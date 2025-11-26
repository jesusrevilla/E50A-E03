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

def test_productos_json_por_marca_dell():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT nombre
        FROM productos_json
        WHERE atributos ->> 'marca' = 'Dell';
    """)
    row = cur.fetchone()
    assert row is not None
    assert row[0] == 'Laptop'

    cur.close()
    conn.close()

def test_usuarios_con_inicio_sesion():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT nombre
        FROM usuarios
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)
    nombres = {r[0] for r in cur.fetchall()}

    assert 'Laura Gómez' in nombres
    assert 'Pedro Ruiz' in nombres

    cur.close()
    conn.close()
