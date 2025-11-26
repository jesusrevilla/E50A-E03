
# tests/test_index.py
from conftest import fetch_one

def test_compound_index_exists(cur):
    row = fetch_one(cur, """
        SELECT indexname
        FROM pg_indexes
        WHERE schemaname='public'
          AND tablename='detalle_pedido'
          AND indexname='idx_cliente_producto';
    """)
    assert row is not None, "No existe el índice compuesto 'idx_cliente_producto' en 'detalle_pedido'."

