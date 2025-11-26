import psycopg2
import pytest
import time

DB_CONFIG = "dbname=tu_base_datos user=tu_usuario password=tu_password host=localhost"

def test_trigger_auditoria():
    """
    4. Trigger: Valida que al insertar un pedido, se cree un registro en auditoria_pedidos.
    """
    try:
        conn = psycopg2.connect(DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        fecha_test = '2025-12-31'
        
        # Insertamos pedido (esto dispara el trigger)
        cur.execute(f"INSERT INTO pedidos (id_cliente, fecha) VALUES (1, '{fecha_test}');")
        
        # Verificamos tabla de auditoría
        cur.execute(f"SELECT * FROM auditoria_pedidos WHERE fecha_pedido = '{fecha_test}' AND id_cliente = 1;")
        audit = cur.fetchone()
        
        assert audit is not None, "El trigger no insertó el registro de auditoría"
        
        print("✅ Test Trigger: PASÓ")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Error en test_trigger: {e}")

if __name__ == "__main__":
    test_trigger_auditoria()
