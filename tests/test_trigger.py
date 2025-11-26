import pytest

def test_trigger_auditoria(db_cursor):
    # Setup
    db_cursor.execute("INSERT INTO clientes (nombre, correo) VALUES ('Audit User', 'audit@test.com') RETURNING id_cliente")
    cid = db_cursor.fetchone()[0]
    
    # Acción: Insertar pedido (esto debería disparar el trigger)
    db_cursor.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (%s, '2025-12-01')", (cid,))
    
    # Validar: Revisar tabla auditoria_pedidos
    db_cursor.execute("SELECT id_cliente, fecha_pedido FROM auditoria_pedidos WHERE id_cliente = %s", (cid,))
    audit_row = db_cursor.fetchone()
    
    assert audit_row is not None
    assert audit_row[0] == cid
