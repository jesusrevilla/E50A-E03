import pytest

def test_func_total_gastado(db_cursor):
    db_cursor.execute("INSERT INTO clientes (nombre, correo) VALUES ('Rich User', 'rich@test.com') RETURNING id_cliente")
    cid = db_cursor.fetchone()[0]
    
    db_cursor.execute("INSERT INTO productos (nombre, precio) VALUES ('Gold', 50.00) RETURNING id_producto")
    pid = db_cursor.fetchone()[0]
    
    db_cursor.execute(f"CALL registrar_pedido({cid}, '2025-01-01', {pid}, 2)")
    
    db_cursor.execute("SELECT total_gastado_por_cliente(%s)", (cid,))
    total = db_cursor.fetchone()[0]
    
    assert float(total) == 100.00
