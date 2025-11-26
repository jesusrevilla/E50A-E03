import pytest
# ... (incluir fixture db_connection) ...

def test_index_existence(db_connection):
    """Verifica que el índice compuesto idx_pedido_producto existe."""
    cursor = db_connection.cursor()
    index_name = 'idx_pedido_producto'

    # Consulta para verificar la existencia de un índice por nombre
    cursor.execute(f"""
        SELECT EXISTS (
            SELECT 1 
            FROM pg_class c 
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relname = '{index_name}' 
            AND n.nspname = 'public'
        );
    """)
    index_exists = cursor.fetchone()[0]
    assert index_exists is True, f"El índice '{index_name}' no existe."

    cursor.close()
