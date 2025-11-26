
# tests/test_view.py
from conftest import fetch_all, fetch_one

def test_view_exists(cur):
    row = fetch_one(cur, """
        SELECT 1
        FROM information_schema.views
        WHERE table_schema = 'public'
          AND table_name = 'vista_detalle_pedidos';
    """)
    assert row is not None, "La vista 'vista_detalle_pedidos' no existe."

def test_view_columns(cur):
    cols = fetch_all(cur, """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema='public'
          AND table_name='vista_detalle_pedidos'
        ORDER BY ordinal_position;
    """)
    names = [c[0] for c in cols]
    assert names == ["nombre_cliente", "nombre_producto", "cantidad", "total_por_linea"], \
        f"Columnas inesperadas en la vista: {names}"

def test_view_content_minimum_rows(cur):
    # Verificamos que existan al menos las filas base del README:
    # Ana: Laptop (1*1200=1200), Mouse (2*25.5=51), Luis: Teclado (1*45=45)
    rows = fetch_all(cur, "SELECT nombre_cliente, nombre_producto, cantidad, total_por_linea FROM vista_detalle_pedidos;")
    assert rows, "La vista está vacía."

    # Normalizamos para búsqueda
    data = {(r[0], r[1], int(r[2])) for r in rows}

    assert ("Ana Torres", "Laptop", 1) in data, "Falta la línea de Ana - Laptop x1."
    assert ("Ana Torres", "Mouse", 2) in data, "Falta la línea de Ana - Mouse x2."
    assert ("Luis Pérez", "Teclado", 1) in data, "Falta la línea de Luis - Teclado x1."

