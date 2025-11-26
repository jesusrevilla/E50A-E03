from app.db import run_query


def test_productos_json():
    result = run_query("SELECT * FROM productos_json WHERE atributos ->> 'marca' = 'Dell';")
    assert len(result) > 0

def test_usuarios_json():
    result = run_query("SELECT nombre FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]';")
    assert len(result) > 0

