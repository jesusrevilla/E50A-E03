import psycopg2
import pytest
import json

DB_CONFIG = "dbname=tu_base_datos user=tu_usuario password=tu_password host=localhost"

def test_json_attributes():
    """
    5. NoSQL: Valida consultas sobre campos JSONB.
    1. Buscar producto por atributo 'marca' -> 'Dell'
    2. Buscar usuario por elemento en array 'historial_actividad' -> 'inicio_sesion'
    """
    try:
        conn = psycopg2.connect(DB_CONFIG)
        cur = conn.cursor()
        
        # Prueba 1: Atributo simple
        cur.execute("SELECT nombre FROM productos_json WHERE atributos ->> 'marca' = 'Dell';")
        prod = cur.fetchone()
        assert prod is not None
        assert prod[0] == 'Laptop'
        
        # Prueba 2: Array de objetos (búsqueda de contención @>)
        cur.execute("SELECT count(*) FROM usuarios WHERE historial_actividad @> '[{\"accion\": \"inicio_sesion\"}]';")
        count = cur.fetchone()[0]
        assert count >= 2, "Debería haber al menos 2 usuarios que iniciaron sesión"
        
        print("✅ Test JSON: PASÓ")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Error en test_json: {e}")

if __name__ == "__main__":
    test_json_attributes()
