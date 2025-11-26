import pytest

def test_procedure_registrar_pedido(db_cursor):
    db_cursor.execute("INSERT INTO clientes (nombre, correo) VALUES ('Proc User', 'proc@test.com') RETURNING id_cliente")
    id_cliente = db_cursor.fetchone()[0]
    
    db_cursor.execute("INSERT INTO productos (nombre, precio) VALUES ('Proc Prod', 50.00) RETURNING id_producto")
    id_producto = db_cursor.fetchone()[0]
    
    db_cursor.execute(f"CALL registrar_pedido({id_cliente}, '2025-10-10', {id_producto}, 5)")
    
    db_cursor.execute("SELECT * FROM pedidos WHERE id_cliente = %s", (id_cliente,))
    pedido = db_cursor.fetchone()
    assert pedido is not None
    
    db_cursor.execute("SELECT cantidad FROM detalle_pedido WHERE id_pedido = %s", (pedido[0],))
    detalle = db_cursor.fetchone()
    assert detalle[0] == 5
