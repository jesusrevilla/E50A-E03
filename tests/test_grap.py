import psycopg2
import pytest

DB_CONFIG = "dbname=tu_base_datos user=tu_usuario password=tu_password host=localhost"

def test_grafo_rutas():
    """
    6. Grafos: Valida la conexión entre nodos (ciudades).
    Busca una ruta de 2 saltos: SLP(1) -> CDMX(5) -> Monterrey(4).
    """
    try:
        conn = psycopg2.connect(DB_CONFIG)
        cur = conn.cursor()
        
        # Query de grafo para buscar conexión indirecta
        query = """
        SELECT c1.nombre, c2.nombre, c3.nombre
        FROM rutas r1
        JOIN rutas r2 ON r1.id_destino = r2.id_origen
        JOIN ciudades c1 ON r1.id_origen = c1.id
        JOIN ciudades c2 ON r1.id_destino = c2.id
        JOIN ciudades c3 ON r2.id_destino = c3.id
        WHERE c1.nombre = 'San Luis Potosí' AND c3.nombre = 'Monterrey';
        """
        cur.execute(query)
        ruta = cur.fetchone()
        
        assert ruta is not None, "No se encontró la ruta SLP -> CDMX -> Monterrey"
        assert ruta[1] == 'CDMX', "La escala debería ser CDMX"
        
        print("✅ Test Grafos: PASÓ")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Error en test_grap: {e}")

if __name__ == "__main__":
    test_grafo_rutas()
