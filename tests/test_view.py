import pytest

DB_CONFIG = "dbname=tu_base_datos user=tu_usuario password=tu_password host=localhost"

def test_vista_detalle():
    """
    1. Vista: Valida que 'vista_detalle_pedidos' traiga la información unida
    (Cliente, Producto, Total Linea).
    """
    try:
        conn = psycopg2.connect(DB_CONFIG)
        cur = conn.cursor()
        
        # Consultamos la vista para el pedido 1
        cur.execute("SELECT nombre_cliente, nombre_producto, total_linea FROM vista_detalle_pedidos WHERE id_pedido = 1;")
        filas = cur.fetchall()
        
        assert len(filas) >= 1, "La vista está vacía o no trae datos del pedido 1"
        
        # Verificamos cálculo de total linea (Cantidad * Precio)
        # Laptop: 1 * 1200 = 1200
        # Mouse: 2 * 25.50 = 51
        totales = [float(f[2]) for f in filas]
        assert 1200.0 in totales, "No se encontró el cálculo correcto para la Laptop"
        assert 51.0 in totales, "No se encontró el cálculo correcto para los Mouse"
        
        print("✅ Test Vista: PASÓ")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Error en test_view: {e}")

if __name__ == "__main__":
    test_vista_detalle()
