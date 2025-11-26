import pytest
from conftest import db_cursor

class TestFunction:
    def test_total_gastado_por_cliente(self, db_cursor):
        """Prueba la función 'total_gastado_por_cliente' con datos iniciales."""
        db_cursor.execute("SELECT total_gastado_por_cliente(1);")
        total_ana = db_cursor.fetchone()[0]

        db_cursor.execute("SELECT total_gastado_por_cliente(2);")
        total_luis = db_cursor.fetchone()[0]

        db_cursor.execute("SELECT total_gastado_por_cliente(99);")
        total_inexistente = db_cursor.fetchone()[0]
        
        assert total_ana == 1251.00, "El total gastado por Ana es incorrecto."
        assert total_luis == 45.00, "El total gastado por Luis es incorrecto."
        assert total_inexistente == 0.00, "El total para cliente inexistente debería ser 0.00."

    def test_index_exists(self, db_cursor):
        """Prueba que el índice compuesto 'idx_cliente_producto' exista."""
        db_cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_cliente_producto' AND tablename = 'detalle_pedido');"
        )
        assert db_cursor.fetchone()[0] is True, "El índice 'idx_cliente_producto' no existe."
