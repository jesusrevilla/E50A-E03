import psycopg2
import pytest

def test_trigger_auditoria():
    # Conexión a la base de datos
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()
    
    # Insertar un nuevo pedido
    cur.execute("""
        INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '2025-05-20');
    """)
    
    # Verificar si la auditoría se registró correctamente
    cur.execute("""
        SELECT * FROM auditoria_pedidos WHERE id_cliente = 1 AND fecha_pedido = '2025-05-20';
    """)
    result = cur.fetchone()
    
    # Comprobar que el registro de auditoría existe
    assert result is not None
    
    cur.close()
    conn.close()

