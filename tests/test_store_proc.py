import psycopg2
import pytest

DB_CONFIG = "dbname=tu_base_datos user=tu_usuario password=tu_password host=localhost"

def test_registrar_pedido_sp():
    """
    2. Procedimiento Almacenado: Valida 'registrar_pedido'.
    Debe insertar en 'pedidos' y 'detalle_pedido' atómicamente.
    """
    try:
        conn = psycopg2.connect(DB_CONFIG)
        conn.autocommit = True # Necesario para CALL
        cur = conn.cursor()
        
        # Datos de prueba
        cliente_id = 2
        fecha = '2025-06-15'
        prod_id = 3
        cant = 10
        
        # Llamamos al SP
        cur.execute(f"CALL registrar_pedido({cliente_id}, '{fecha}', {prod_id}, {cant});")
        
        # Verificamos inserción
        cur.execute(f"SELECT id_pedido FROM pedidos WHERE fecha = '{fecha}' AND id_cliente = {cliente_id};")
        pedido = cur.fetchone()
        assert pedido is not None, "El pedido no se registró en la tabla padre"
        
        id_pedido = pedido[0]
        cur.execute(f"SELECT cantidad FROM detalle_pedido WHERE id_pedido = {id_pedido} AND id_producto = {prod_id};")
        detalle = cur.fetchone()
        assert detalle is not None, "El detalle no se registró"
        assert detalle[0] == cant
        
        print("✅ Test Store Proc: PASÓ")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Error en test_store_proc: {e}")

if __name__ == "__main__":
    test_registrar_pedido_sp()
