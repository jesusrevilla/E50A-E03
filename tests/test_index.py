import pytest
from conftest import db_cursor

class TestIndex:
    def test_idx_cliente_producto_exists(self, db_cursor):
        """
        Prueba que el índice compuesto 'idx_cliente_producto' exista
        en la tabla 'detalle_pedido'.
        """
        db_cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_cliente_producto' AND tablename = 'detalle_pedido');"
        )
        exists = db_cursor.fetchone()[0]
        assert exists is True, "El índice 'idx_cliente_producto' no existe en detalle_pedido."

    def test_idx_cliente_producto_is_composite_on_correct_columns(self, db_cursor):
        """
        Prueba que el índice 'idx_cliente_producto' sea compuesto y esté definido
        sobre las columnas 'id_pedido' e 'id_producto'.
        """
        db_cursor.execute(
            """
            SELECT array_agg(a.attname ORDER BY array_position(i.indkey, a.attnum))
            FROM pg_index i
            JOIN pg_class c ON c.oid = i.indrelid
            JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(i.indkey)
            WHERE c.relname = 'detalle_pedido' 
              AND i.indisvalid 
              AND i.indexrelid::regclass::text = 'idx_cliente_producto';
            """
        )
        column_names = db_cursor.fetchone()[0]
        expected_columns = ['id_pedido', 'id_producto']
        
        assert column_names == expected_columns, f"El índice no incluye las columnas esperadas en el orden correcto. Columnas encontradas: {column_names}"
