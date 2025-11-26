import pytest
from datetime import date

def test_vista_detalle_pedidos(db_cursor):

    db_cursor.execute("INSERT INTO clientes (nombre, correo) VALUES ('Test User', 'test@test.com') RETURNING id_cliente")
    id_cliente = db_cursor.fetchone()[0]
    
    db_cursor.execute("INSERT INTO productos (nombre, precio) VALUES ('Test Prod', 100.00) RETURNING id_producto")
    id_producto = db_cursor.fetchone()[0]
    
    db_cursor.execute("INSERT INTO pedidos (id_cliente, fecha) VALUES (%s, %s) RETURNING id_pedido", (id_cliente, date.today()))
    id_pedido = db_cursor.fetchone()[0]
    
    db_cursor.execute("INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad) VALUES (%s, %s, 2)", (id_pedido, id_producto))
    
    db_cursor.execute("SELECT * FROM vista_detalle_pedidos WHERE nombre_cliente = 'Test User'")
    resultado = db_cursor.fetchone()
    
    assert resultado is not None
    assert resultado[0] == 'Test User'   
    assert resultado[1] == 'Test Prod'   
    assert resultado[2] == 2             
    assert resultado[3] == 200.00        
