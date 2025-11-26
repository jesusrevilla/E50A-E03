
def test_graph(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM rutas WHERE id_origen = 1;")
    assert cur.fetchall() != []

    rutas_esperadas = {'Querétaro', 'CDMX'}
    
    assert set(resultados) == rutas_esperadas
    assert len(resultados) == 2
    
    cur.close()
    conn.close()
