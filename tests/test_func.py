
# tests/test_func.py
from decimal import Decimal, ROUND_HALF_UP
from conftest import fetch_one

def test_function_exists(cur):
    row = fetch_one(cur, """
        SELECT 1
        FROM pg_proc
        WHERE proname = 'total_gastado_por_cliente';
    """)
    assert row is not None, "No existe la función 'total_gastado_por_cliente'."

def test_function_matches_manual_sum(cur):
    cliente_id = 1  # Ana Torres
    # Resultado de la función
    func_val = fetch_one(cur, "SELECT total_gastado_por_cliente(%s);", (cliente_id,))[0]
    assert func_val is not None, "La función devolvió NULL."

    # Suma manual en SQL (coincide con lo que la función debe hacer)
    manual = fetch_one(cur, """
        SELECT COALESCE(SUM(p.precio * dp.cantidad), 0)
        FROM pedidos pe
        JOIN detalle_pedido dp ON pe.id_pedido = dp.id_pedido
        JOIN productos p ON dp.id_producto = p.id_producto
        WHERE pe.id_cliente = %s;
    """, (cliente_id,))[0]

    # Normalizamos a 2 decimales
    func_q = Decimal(func_val).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    man_q = Decimal(manual).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    assert func_q == man_q, f"Total no coincide: función={func_q} vs manual={man_q}"

