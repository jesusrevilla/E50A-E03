def test_productos_json(json_conn):
    cur = json_conn.cursor()

    # Producto marca Dell debe existir según tus inserts
    cur.execute("""
        SELECT * FROM productos_json
        WHERE atributos ->> 'marca' = 'Dell';
    """)

    assert len(cur.fetchall()) > 0


def test_historial_actividad(json_conn):
    cur = json_conn.cursor()

    cur.execute("""
        SELECT nombre, correo
        FROM usuarios
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)

    rows = cur.fetchall()
    assert len(rows) > 0

