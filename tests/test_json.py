import psycopg2
import pytest

# Configuración de conexión (ajústala si usas conftest.py)
DB_HOST = "localhost"
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASS = "postgres"

def execute_query(query, fetch=True):
    # Función auxiliar para ejecutar consultas
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute(query)
        if fetch:
            result = cur.fetchall()
            return result
        else:
            conn.commit()
            return None
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        raise
    finally:
        if conn:
            conn.close()

def test_consulta_productos_por_atributo_especifico():
    """Verifica la consulta de productos con 'marca' = 'Dell'."""

    query = """
    SELECT nombre FROM productos_json
    WHERE atributos ->> 'marca' = 'Dell';
    """

    result = execute_query(query)

    # Esperamos solo 'Laptop'
    assert len(result) == 1, "Debe retornar un solo producto con marca 'Dell'."
    assert result[0][0] == 'Laptop', "El producto debe ser 'Laptop'."

def test_consulta_usuarios_por_accion_jsonb():
    """Verifica la consulta de usuarios que realizaron 'inicio_sesion'."""

    query = """
    SELECT nombre
    FROM usuarios
    WHERE historial_actividad @> '[{"accion": "inicio_sesion"}]'
    ORDER BY nombre;
    """

    result = execute_query(query)

    # Esperamos 'Laura Gómez' y 'Pedro Ruiz'
    expected_users = [('Laura Gómez',), ('Pedro Ruiz',)]

    assert len(result) == 2, "Deben retornar 2 usuarios con la acción 'inicio_sesion'."
    assert result == expected_users, "Los nombres de usuario no coinciden con los esperados."

def test_extraer_acciones_de_un_usuario():
    """Verifica la extracción de todas las acciones de un usuario específico."""

    query = """
    SELECT a.accion
    FROM usuarios u, jsonb_to_recordset(u.historial_actividad) AS a(fecha DATE, accion TEXT)
    WHERE u.nombre = 'Laura Gómez'
    ORDER BY a.fecha;
    """

    result = execute_query(query)

    # Esperamos las 3 acciones en orden de fecha: inicio_sesion, subio_archivo, cerró_sesion
    expected_actions = [('inicio_sesion',), ('subio_archivo',), ('cerró_sesion',)]

    assert len(result) == 3, "Deben retornar 3 acciones para Laura Gómez."
    assert result == expected_actions, "Las acciones o el orden no son correctos."
