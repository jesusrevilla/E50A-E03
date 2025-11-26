import pytest
from conftest import db_cursor

class TestNoSQLJSONB:
    def test_query_productos_by_attribute(self, db_cursor):
        """Prueba la consulta de productos_json por un atributo JSONB ('marca' = 'Dell')."""
        db_cursor.execute("SELECT nombre FROM productos_json WHERE atributos ->> 'marca' = 'Dell';")
        resultados = [row[0] for row in db_cursor.fetchall()]
        
        assert len(resultados) == 1, "Debe haber 1 producto con marca 'Dell'."
        assert 'Laptop' in resultados, "El producto 'Laptop' no fue encontrado."

    def test_query_usuarios_by_action_presence(self, db_cursor):
        """Prueba la consulta de usuarios que realizaron una acción específica ('inicio_sesion')."""
        # Se busca usuarios con historial_actividad @> '[{"accion": "inicio_sesion"}]'
        db_cursor.execute("SELECT nombre FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]';")
        resultados = [row[0] for row in db_cursor.fetchall()]
        
        assert len(resultados) == 2, "Debe haber 2 usuarios que iniciaron sesión."
        assert 'Laura Gómez' in resultados
        assert 'Pedro Ruiz' in resultados
        
    def test_extract_user_actions_function(self, db_cursor):
        """Prueba la función que extrae todas las acciones de un usuario."""
        db_cursor.execute("SELECT accion FROM get_acciones_usuario('Laura Gómez');")
        acciones = [row[0] for row in db_cursor.fetchall()]
        
        expected_actions = ['inicio_sesion', 'subio_archivo', 'cerró_sesion']
        
        assert len(acciones) == 3, "Debe haber 3 acciones para Laura Gómez."
        assert sorted(acciones) == sorted(expected_actions), "Las acciones de Laura Gómez son incorrectas."
