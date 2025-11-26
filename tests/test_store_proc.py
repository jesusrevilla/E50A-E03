import pytest
# ... (incluir fixture db_connection) ...

def test_auditoria_trigger(db_connection):
    """Verifica que el trigger inserta un registro en auditoria_pedidos al crear un nuevo pedido."""
    cursor = db_connection.cursor()
    initial_audit_count = 0

    # 1. Contar registros iniciales de auditoría
    cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos;")
    initial_audit_count = cursor.fetchone()[0]

    # 2. Insertar un nuevo pedido (esto debe activar el trigger)
    cursor.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-11-26');")
    db_connection.commit()

    # 3. Contar registros finales de auditoría
    cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos;")
    final_audit_count = cursor.fetchone()[0]
    
    # 4. Verificar que se insertó una fila en la tabla de auditoría
    assert final_audit_count == initial_audit_count + 1, "El trigger no insertó el registro de auditoría."

    cursor.close()
