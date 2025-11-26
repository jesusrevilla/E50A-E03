def test_tablas_existen(index_conn):
    cur = index_conn.cursor()

    for table in ["clientes", "productos", "pedidos", "detalle_pedido"]:
        cur.execute(f"SELECT to_regclass('{table}');")
        assert cur.fetchone()[0] == table

