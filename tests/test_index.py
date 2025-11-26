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

def test_index_cliente_producto_existe():
    """Verifica la existencia del índice compuesto idx_cliente_producto."""

    query = """
    SELECT 1 
    FROM pg_indexes 
    WHERE tablename = 'detalle_pedido' 
      AND indexname = 'idx_cliente_producto';
    """

    result = execute_query(query)

    # Si el resultado no está vacío, el índice existe
    assert len(result) == 1, "El índice compuesto 'idx_cliente_producto' no fue encontrado."
