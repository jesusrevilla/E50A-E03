import pytest

def test_jsonb_productos(db_cursor):
    json_data = '{"marca": "TestBrand", "color": "Rojo"}'
    db_cursor.execute("INSERT INTO productos_json (nombre, atributos) VALUES (%s, %s)", ('TestItem', json_data))
    
    db_cursor.execute("SELECT nombre FROM productos_json WHERE atributos ->> 'color' = 'Rojo'")
    res = db_cursor.fetchone()
    
    assert res is not None
    assert res[0] == 'TestItem'

def test_jsonb_usuarios_array(db_cursor):
    historial = '[{"accion": "login"}, {"accion": "logout"}]'
    db_cursor.execute("INSERT INTO usuarios (nombre, historial_actividad) VALUES (%s, %s)", ('JsonUser', historial))
    
    db_cursor.execute("SELECT nombre FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"login\"}]'")
    res = db_cursor.fetchone()
    
    assert res[0] == 'JsonUser'
