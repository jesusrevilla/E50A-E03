import psycopg2
import pytest

DB_HOST = "localhost"
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASS = "postgres"

def execute_query(query, fetch=True):
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

def test_vista_detalle_pedidos_existe_y_es_correcta():
    """Verifica que la vista devuelva la estructura y datos correctos."""
    
    query_count = "SELECT COUNT(*) FROM vista_detalle_pedidos;"
    count_result = execute_query(query_count)
    assert count_result[0][0] == 3, "La vista debe retornar 3 líneas de pedido."

   
    query_data = """
    SELECT 
        nombre_cliente, 
        nombre_producto, 
        cantidad, 
        precio_unitario, 
        total_linea 
    FROM vista_detalle_pedidos 
    WHERE nombre_cliente = 'Ana Torres' AND nombre_producto = 'Laptop';
    """
    data_result = execute_query(query_data)
    
    assert len(data_result) == 1, "Debe haber una línea para Laptop de Ana Torres."
    
    
    import decimal
    
    record = data_result[0]
    assert record[0] == 'Ana Torres'
    assert record[1] == 'Laptop'
    assert record[2] == 1
    assert record[3] == decimal.Decimal('1200.00')
    assert record[4] == decimal.Decimal('1200.00')

