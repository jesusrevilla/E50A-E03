
# tests/test_json.py
from conftest import fetch_all, fetch_one

def test_productos_json_query_by_marca(cur):
    rows = fetch_all(cur, """
        SELECT nombre, atributos->>'marca' AS marca
        FROM productos_json
        WHERE atributos->>'marca' = 'Dell';
    """)
    assert rows, "No se encontró producto con marca 'Dell'."
    nombres = [r[0] for r in rows]
    assert "Laptop" in nombres, f"Se esperaba 'Laptop' con marca 'Dell', obtuve: {nombres}"

def test_usuarios_historial_contains_inicio_sesion(cur):
    rows = fetch_all(cur, """
        SELECT nombre, correo
        FROM usuarios
        WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]';
    """)
    assert rows, "Ningún usuario con 'inicio_sesion' en historial_actividad."
    # Validamos que al menos los nombres existan como strings
    assert all(isinstance(r[0], str) for r in rows)

def test_extract_acciones_for_one_user(cur):
    # Tomamos cualquier usuario existente para evitar dependencia de nombres
    any_user = fetch_one(cur, "SELECT nombre FROM usuarios LIMIT 1;")
    assert any_user is not None, "No hay usuarios para probar."
    nombre = any_user[0]

    acciones = fetch_all(cur, """
        SELECT jsonb_array_elements(historial_actividad)->>'accion' AS accion
        FROM usuarios
        WHERE nombre = %s;
    """, (nombre,))
    assert acciones, f"El usuario '{nombre}' no tiene acciones en historial."
    accs = {a[0] for a in acciones}
    # Al menos alguna acción común esperada
    assert ("inicio_sesion" in accs) or ("subio_archivo" in accs) or ("cerró_sesion" in accs) or ("comentó_publicación" in accs), \
        f"Acciones poco comunes: {accs}"

