def test_consulta_jsonb_atributos(cursor):
    cursor.execute("SELECT nombre FROM productos_json WHERE atributos ->> 'marca' = 'Dell'")
    nombre = cursor.fetchone()
    assert nombre is not None
    assert nombre[0] == 'Laptop'

def test_consulta_jsonb_historial(cursor):
    cursor.execute("SELECT nombre, correo FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]'")
    usuarios = [row[0] for row in cursor.fetchall()]
    assert 'Laura Gómez' in usuarios
    assert 'Pedro Ruiz' in usuarios
    assert len(usuarios) == 2
