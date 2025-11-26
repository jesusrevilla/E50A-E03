
def test_total_gastado_por_cliente(func_conn):
    cur = func_conn.cursor()

    cur.execute("SELECT total_gastado_por_cliente(1);")
    total = cur.fetchone()[0]

    # Debe ser un número decimal sin errores
    assert total is not None
    assert total >= 0
