
# tests/test_grap.py
from conftest import fetch_one, fetch_all

def test_ciudades_y_rutas_existen(cur):
    c = fetch_one(cur, "SELECT 1 FROM information_schema.tables WHERE table_name='ciudades';")
    r = fetch_one(cur, "SELECT 1 FROM information_schema.tables WHERE table_name='rutas';")
    assert c is not None, "La tabla 'ciudades' no existe."
    assert r is not None, "La tabla 'rutas' no existe."

def test_rutas_desde_san_luis(cur):
    # Soportar nombres con/ sin acentos según script
    city = fetch_one(cur, """
        SELECT id, nombre
        FROM ciudades
        WHERE nombre IN ('San Luis Potosí', 'San Luis Potosi')
        LIMIT 1;
    """)
    assert city is not None, "No se encontró 'San Luis Potosí/Potosi' en ciudades."
    id_origen, nombre_origen = city

    res = fetch_all(cur, """
        SELECT d.nombre AS destino, r.distancia_km
        FROM rutas r
        JOIN ciudades d ON r.id_destino = d.id
        WHERE r.id_origen = %s
        ORDER BY d.nombre;
    """, (id_origen,))
    assert res, f"No se encontraron rutas desde {nombre_origen}."

    # Aceptar variantes con/ sin acentos
    destinos = {row[0] for row in res}
    distmap = {row[0]: int(row[1]) for row in res}
    assert ("Querétaro" in destinos) or ("Queretaro" in destinos), "Falta ruta a Querétaro/Queretaro."
    assert "CDMX" in destinos, "Falta ruta a CDMX."
    # Distancias esperadas
    if "Querétaro" in distmap:
        assert distmap["Querétaro"] == 180, "Distancia a Querétaro debe ser 180 km."
    if "Queretaro" in distmap:
        assert distmap["Queretaro"] == 180, "Distancia a Queretaro debe ser 180 km."

