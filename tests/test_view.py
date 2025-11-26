
import psycopg2

def test_vista_detalle_pedidos(view_conn):
    cur = view_conn.cursor()
    cur.execute("SELECT * FROM vista_detalle_pedidos;")
    rows = cur.fetchall()

    # Debe existir al menos 1 fila si 02_insert_data.sql insertó datos
    assert len(rows) > 0

    # Validar columnas esperadas
    colnames = [desc[0] for desc in cur.description]
    assert "id_pedido" in colnames
    assert "cliente" in colnames
    assert "producto" in colnames
    assert "total_linea" in colnames
