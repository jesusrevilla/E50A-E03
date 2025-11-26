def test_rutas_grafos(graph_conn):
    cur = graph_conn.cursor()

    cur.execute("""
        SELECT 
            c1.nombre AS origen,
            c2.nombre AS destino,
            r.distancia_km
        FROM rutas r
        JOIN ciudades c1 ON r.id_origen = c1.id
        JOIN ciudades c2 ON r.id_destino = c2.id
        WHERE c1.nombre = 'San Luis Potosí';
    """)

    rows = cur.fetchall()

    assert len(rows) > 0

