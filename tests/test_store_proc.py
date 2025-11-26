import psycopg2
import pytest

# Configuración de conexión (ajústala si usas conftest.py)
DB_HOST = "localhost"
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASS = "postgres"

def execute_query(query, fetch=True):
    # Función auxiliar para ejecutar consultas
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute(query)
        if fetch:
            result = cur.fetchall()
            return result
        else:
            conn.commit()
            return None
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        raise
    finally:
        if conn:
            conn.close()

def test_registrar_pedido():
    """Verifica que el procedimiento almacenado inserte un pedido y su detalle."""
    
    # Valores a insertar
    ID_CLIENTE = 2
    FECHA = '2025-05-20'
    ID_PRODUCTO = 2 # Mouse
    CANTIDAD = 5
    
    initial_pedidos_count = execute_query("SELECT COUNT(*) FROM pedidos;")[0][0]
    initial_detalle_count = execute_query("SELECT COUNT(*) FROM detalle_pedido;")[0][0]
    
    # 2. Ejecutar el procedimiento
    call_proc = f"CALL registrar_pedido({ID_CLIENTE}, '{FECHA}', {ID_PRODUCTO}, {CANTIDAD});"
    execute_query(call_proc, fetch=False)
    
    # 3. Verificar conteo final
    final_pedidos_count = execute_query("SELECT COUNT(*) FROM pedidos;")[0][0]
    final_detalle_count = execute_query("SELECT COUNT(*) FROM detalle_pedido;")[0][0]

    assert final_pedidos_count == initial_pedidos_count + 1, "Debe insertarse un nuevo pedido."
    assert final_detalle_count == initial_detalle_count + 1, "Debe insertarse un nuevo detalle de pedido."

    # 4. Verificar los datos específicos del nuevo detalle
    query_check = f"""
    SELECT p.id_cliente, dp.id_producto, dp.cantidad 
    FROM pedidos p
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    ORDER BY p.id_pedido DESC
    LIMIT 1;
    """
    new_record = execute_query(query_check)[0]
    
    assert new_record[0] == ID_CLIENTE
    assert new_record[1] == ID_PRODUCTO
    assert new_record[2] == CANTIDAD
  
