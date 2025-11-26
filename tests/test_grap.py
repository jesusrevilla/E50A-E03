import pytest

def test_grafo_rutas_desde_slp(db_connection):
    """Verifica la consulta de rutas de grafo desde San Luis Potosí."""
    cursor = db_connection.cursor()

    
    cursor.execute("""
        SELECT
            destino.nombre
        FROM
            rutas r
        JOIN
            ciudades origen ON r.id_origen = origen.id
        JOIN
            ciudades destino ON r.id_destino = destino.id
        WHERE
            origen.nombre = 'San Luis Potosí';
    """)

    results = cursor.fetchall()
    destinos = sorted([r[0] for r in results])

   
    expected_destinations = ['CDMX', 'Querétaro']

    assert destinos == expected_destinations, "La consulta de grafo no devolvió los destinos correctos."

    cursor.close()
