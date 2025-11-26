import pytest


def test_grafo_rutas(db_cursor):
    db_cursor.execute("INSERT INTO ciudades (nombre) VALUES ('A'), ('B') RETURNING id")
    ids = db_cursor.fetchall()
    id_a, id_b = ids[0][0], ids[1][0]
    
    db_cursor.execute("INSERT INTO rutas (id_origen, id_destino, distancia_km) VALUES (%s, %s, 100)", (id_a, id_b))
    
    query = """
        SELECT c2.nombre 
        FROM rutas r
        JOIN ciudades c1 ON r.id_origen = c1.id
        JOIN ciudades c2 ON r.id_destino = c2.id
        WHERE c1.nombre = 'A'
    """
    db_cursor.execute(query)
    destino = db_cursor.fetchone()[0]
    
    assert destino == 'B'
