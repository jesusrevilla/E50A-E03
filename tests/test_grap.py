from app.db import run_query


def test_rutas_ciudades():
    result = run_query("""
        WITH RECURSIVE conexiones AS (
            SELECT id_origen, id_destino, distancia_km FROM rutas WHERE id_origen = 1
            UNION ALL
            SELECT r.id_origen, r.id_destino, r.distancia_km
            FROM rutas r
            INNER JOIN conexiones c ON r.id_origen = c.id_destino
        )
        SELECT * FROM conexiones;
    """)
    assert len(result) > 0

