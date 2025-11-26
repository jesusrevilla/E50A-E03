def test_trigger_auditoria_funciona(cursor):
    cliente_id = 2
    
    cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos")
    auditorias_antes = cursor.fetchone()[0]
    
    # El trigger se activa al insertar en la tabla 'pedidos'
    cursor.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (%s, '2025-06-05')", (cliente_id,))
    
    cursor.execute("SELECT COUNT(*) FROM auditoria_pedidos")
    auditorias_despues = cursor.fetchone()[0]

    assert auditorias_despues == auditorias_antes + 1

    cursor.execute("SELECT id_cliente, fecha_pedido FROM auditoria_pedidos ORDER BY id_auditoria DESC LIMIT 1")
    auditoria_registro = cursor.fetchone()
    
    assert auditoria_registro[0] == cliente_id
    assert str(auditoria_registro[1]) == '2025-06-05'
