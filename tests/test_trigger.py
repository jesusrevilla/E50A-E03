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

def test_auditoria_pedidos_trigger():
    """Verifica que al insertar un pedido, se cree un registro en auditoria_pedidos."""

    ID_CLIENTE = 1
    FECHA = '2025-06-01'

    # 1. Obtener conteo inicial de auditoría
    initial_auditoria_count = execute_query("SELECT COUNT(*) FROM auditoria_pedidos;")[0][0]

    # 2. Insertar un nuevo pedido que debería disparar el trigger
    insert_pedido = f"INSERT INTO pedidos (id_cliente, fecha) VALUES ({ID_CLIENTE}, '{FECHA}');"
    execute_query(insert_pedido, fetch=False)

    # 3. Verificar conteo final
    final_auditoria_count = execute_query("SELECT COUNT(*) FROM auditoria_pedidos;")[0][0]

    assert final_auditoria_count == initial_auditoria_count + 1, "El trigger no insertó el registro de auditoría."

    # 4. Verificar los datos específicos del registro de auditoría
    query_check = f"""
    SELECT id_cliente, fecha_pedido 
    FROM auditoria_pedidos
    ORDER BY id_auditoria DESC
    LIMIT 1;
    """
    new_record = execute_query(query_check)[0]

    # psycopg2 recupera la fecha como datetime.date
    import datetime

    assert new_record[0] == ID_CLIENTE
    assert new_record[1] == datetime.date(2025, 6, 1)
