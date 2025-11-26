import psycopg2
from .conftest import db_connection 

def test_index_optimiza_consulta():
    """
    Verifica si el índice compuesto 'idx_cliente_producto' es utilizado
    por PostgreSQL para una consulta que lo favorece.
    
    El índice es: ON detalle_pedido (id_producto, cantidad).
    La prueba verifica si la consulta utiliza un 'Index Scan' o 'Bitmap Index Scan'.
    """
    conn = db_connection()

    conn.autocommit = True 
    cur = conn.cursor()
    
    
    consulta_a_testear = """
    EXPLAIN ANALYZE
    SELECT *
    FROM detalle_pedido
    WHERE id_producto = 1 AND cantidad = 1;
    """
    
    cur.execute(consulta_a_testear)
    explicacion = cur.fetchall()
    
   
    plan_ejecucion = ' '.join([row[0] for row in explicacion])
    
  
    assert "Index Scan" in plan_ejecucion or "Bitmap Index Scan" in plan_ejecucion, \
        f"Fallo: La consulta no utilizó el índice 'idx_cliente_producto'. Plan: {plan_ejecucion}"

   
    assert "idx_cliente_producto" in plan_ejecucion, \
        f"Advertencia: El plan de ejecución no menciona explícitamente 'idx_cliente_producto'. Plan: {plan_ejecucion}"
        
    cur.close()
    conn.close()
