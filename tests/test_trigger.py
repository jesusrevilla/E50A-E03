import psycopg2

def test_trigger_auditoria():
    conn = psycopg2.connect(dbname="test_db", user="postgres", password="postgres", host="localhost", port="5432")
    cursor = conn.cursor()
    
    # Insertar un nuevo pedido para activar el trigger
    cursor.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');")
    conn.commit()
    
    # Verificar si el trigger registró el pedido en la auditoría
    cursor.execute("SELECT * FROM auditoria_pedidos WHERE id_cliente = 1 AND fecha_pedido = '2025-05-20';")
    audit_entry = cursor.fetchone()
    assert audit_entry is not None, "El trigger de auditoría no se activó correctamente."
    
    cursor.close()
    conn.close()
