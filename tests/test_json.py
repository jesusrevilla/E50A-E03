import psycopg2

def test_json_producto_por_marca():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT nombre FROM productos_json
        WHERE atributos ->> 'marca' = 'Dell';
    """)
    prod = cur.fetchone()[0]
    assert prod == "Laptop"

    conn.close()


def test_json_usuario_historial():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT nombre FROM usuarios
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)
    rows = cur.fetchall()

    assert ("Laura Gómez",) in rows
    assert ("Pedro Ruiz",) in rows

    conn.close()


def test_json_array_elements():
    conn = psycopg2.connect(
        dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT jsonb_array_elements(historial_actividad)->>'accion'
        FROM usuarios
        WHERE id = 1;
    """)
    acciones = [a[0] for a in cur.fetchall()]

    assert "inicio_sesion" in acciones
    assert "subio_archivo" in acciones
    assert "cerro_sesion" in acciones

    conn.close()
