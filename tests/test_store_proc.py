import pytest
from conftest import db_cursor, db_connection

class TestStoredProcedure:
    def test_registrar_pedido_creates_records(self, db_cursor, db_connection):
        """Prueba que 'registrar_pedido' inserte en pedidos y detalle_pedido."""
        initial_pedidos_count = 0
        initial_detalle_count = 0
        
        # 1. Conteo inicial
        db_cursor.execute("SELECT COUNT(*) FROM pedidos;")
        initial_pedidos_count = db_cursor.fetchone()[0]
        db_cursor.execute("SELECT COUNT(*) FROM detalle_pedido;")
        initial_detalle_count = db_cursor.fetchone()[0]
        
        # 2. Ejecutar el procedimiento almacenado
        # Cliente 1 (Ana), fecha nueva, Producto 3 (Teclado), Cantidad 5
        db_cursor.execute("CALL registrar_pedido(1, '2025-10-15', 3, 5);")
        db_connection.commit()

        # 3. Conteo final
        db_cursor.execute("SELECT COUNT(*) FROM pedidos;")
        final_pedidos_count = db_cursor.fetchone()[0]
        db_cursor.execute("SELECT COUNT(*) FROM detalle_pedido;")
        final_detalle_count = db_cursor.fetchone()[0]
        
        assert final_pedidos_count == initial_pedidos_count + 1, "No se insertó el nuevo pedido."
        assert final_detalle_count == initial_detalle_count + 1, "No se insertó el nuevo detalle_pedido."
        
        # 4. Verificar contenido del detalle (se asume que el nuevo pedido tiene ID max)
        db_cursor.execute("SELECT id_pedido FROM pedidos ORDER BY id_pedido DESC LIMIT 1;")
        new_pedido_id = db_cursor.fetchone()[0]
        
        db_cursor.execute(f"SELECT id_producto, cantidad FROM detalle_pedido WHERE id_pedido = {new_pedido_id};")
        new_detalle = db_cursor.fetchone()
        
        assert new_detalle == (3, 5), "El detalle del pedido insertado es incorrecto."
