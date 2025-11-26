def test_trigger_auditoria(trigger_conn):
    cur = trigger_conn.cursor()

    # Insertar un nuevo pedido
    cur.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-22');")

    # Comprobar auditoría
    cur.execute("SELECT * FROM auditoria_pedidos WHERE fecha_pedido='2025-05-22';")
    rows = cur.fetchall()

    assert len(rows) == 1

