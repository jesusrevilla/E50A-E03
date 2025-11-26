import psycopg2
import pytest

DB_CONFIG = "dbname=tu_base_datos user=tu_usuario password=tu_password host=localhost"

def test_indice_existe():
    """
    3.1 Índice: Valida que el índice 'idx_cliente_producto' exista en la base de datos.
    """
    try:
        conn = psycopg2.connect(DB_CONFIG)
        cur = conn.cursor()
        
        # Consultamos el catálogo de índices de Postgres
        query = "SELECT indexname FROM pg_indexes WHERE indexname = 'idx_cliente_producto';"
        cur.execute(query)
        res = cur.fetchone()
        
        assert res is not None, "El índice 'idx_cliente_producto' no fue encontrado."
        assert res[0] == 'idx_cliente_producto'
        
        print("✅ Test Índice: PASÓ")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Error en test_index: {e}")

if __name__ == "__main__":
    test_indice_existe()
