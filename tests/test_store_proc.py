import pytest

def test_registrar_pedido(db_connection):
    """Verifica que el procedimiento almacenado inserta un nuevo pedido y su detalle."""
    cursor = db_connection.cursor()
    initial_pedidos_count = 0
    initial_detalle_count = 0

    
    cursor.execute("SELECT COUNT(*) FROM pedidos;")
    initial_pedidos_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM detalle_pedido;")
    initial_detalle_count = cursor.fetchone()[0]

    cursor.execute("CALL registrar_pedido(1, '2025-11-25', 1, 5);")
    db_connection.commit()

      cursor.execute("SELECT COUNT(*) FROM pedidos;")
    final_pedidos_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM detalle_pedido;")
    final_detalle_count = cursor.fetchone()[0]

      assert final_pedidos_count == initial_pedidos_count + 1, "No se insertó el pedido correctamente."
    assert final_detalle_count == initial_detalle_count + 1, "No se insertó el detalle correctamente."

    cursor.close()
