import psycopg2
import pytest

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

def test_index_exists(db_connection):
    """
    Verifica que el índice 'idx_cliente_producto' haya sido creado
    en la tabla 'detalle_pedido'.
    """
    with db_connection.cursor() as cur:
        # Consultamos la tabla del sistema pg_indexes
        cur.execute("SELECT indexname FROM pg_indexes WHERE indexname = 'idx_cliente_producto'")
        result = cur.fetchone()
        
        # Si result no es None, significa que el índice existe
        assert result is not None, "El índice 'idx_cliente_producto' no se encontró en la base de datos"
        assert result[0] == 'idx_cliente_producto'
