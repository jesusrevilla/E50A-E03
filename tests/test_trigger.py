import pytest


def test_auditoria_trigger(db_connection):
    """Verifica que el trigger inserta un registro en auditoria_pedidos al crear un nuevo pedido."""
    cursor = db_connection.cursor()
    initial_audit_count = 0


    cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos;")
    initial_audit_count = cursor.fetchone()[0]


    cursor.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (2, '2025-11-26');")
    db_connection.commit()


    cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos;")
    final_audit_count = cursor.fetchone()[0]


    assert final_audit_count == initial_audit_count + 1, "El trigger no insertó el registro de auditoría."

    cursor.close()
