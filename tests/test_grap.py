import psycopg2
import pytest

# Configuración de conexión 
DB_CONFIG = {
    "dbname": "test_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    yield conn
    conn.close()

def test_busqueda_arrays(db_connection):
    """
    Prueba para validar el uso de Arrays en PostgreSQL.
    """
    with db_connection.cursor() as cur:
        # Consulta usando el operador ANY() para buscar en el array
        cur.execute("SELECT nombre FROM productos WHERE 'tecnología' = ANY(etiquetas) ORDER BY nombre;")
        resultados = cur.fetchall()
        
        # Esperamos 3 productos: Laptop, Monitor, Teclado (Orden alfabético)
        assert len(resultados) == 3
        assert results[0][0] == "Laptop Gamer"
        assert results[1][0] == "Monitor 4K"
        assert results[2][0] == "Teclado Mecánico"

def test_grafo_cte_recursiva(db_connection):
    """
    Prueba para validar CTE Recursiva.
    """
    query_cte = """
    WITH RECURSIVE ruta_viaje AS (
        -- Caso Base: Ciudad de origen (ID 1 - Ciudad A)
        SELECT id, nombre, 0 as distancia_total
        FROM ciudades
        WHERE id = 1
        
        UNION ALL
        
        -- Parte Recursiva: Buscar destinos conectados
        SELECT c.id, c.nombre, rv.distancia_total + r.distancia_km
        FROM ciudades c
        INNER JOIN rutas r ON c.id = r.id_destino
        INNER JOIN ruta_viaje rv ON r.id_origen = rv.id
    )
    SELECT nombre FROM ruta_viaje ORDER BY nombre;
    """
    
    with db_connection.cursor() as cur:
        cur.execute(query_cte)
        resultados = cur.fetchall()
        
        # Esperamos encontrar Ciudad A, B y C (A->B->C)
        # Ciudad D está aislada y no debe aparecer.
        nombres = [fila[0] for fila in resultados]
        
        assert "Ciudad A" in nombres
        assert "Ciudad B" in nombres
        assert "Ciudad C" in nombres
        assert "Ciudad D" not in nombres
