def test_consulta_rutas_slp(cursor):
    slp_id = 1
    
    # Consulta la ruta SLP -> Querétaro
    cursor.execute("""
        SELECT 
            c_destino.nombre
        FROM
            rutas r
        JOIN
            ciudades c_origen ON r.id_origen = c_origen.id
        JOIN
            ciudades c_destino ON r.id_destino = c_destino.id
        WHERE
            c_origen.nombre = 'San Luis Potosí'
        ORDER BY
            r.distancia_km
    """)
    
    rutas = [row[0] for row in cursor.fetchall()]
    assert 'Querétaro' in rutas
    assert 'CDMX' in rutas
    assert len(rutas) == 2
