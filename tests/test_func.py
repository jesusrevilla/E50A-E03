import psycopg2
import pytest
import decimal

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

def test_total_gastado_por_cliente_ana():
    """Verifica el total gastado por Ana Torres (ID 1)."""

    expected_total = decimal.Decimal('1251.00')

    query = "SELECT total_gastado_por_cliente(1);"
    result = execute_query(query)

    actual_total = result[0][0]

    assert actual_total == expected_total, f"Total para Cliente 1 debe ser {expected_total}, pero fue {actual_total}"

def test_total_gastado_por_cliente_luis():
    """Verifica el total gastado por Luis Pérez (ID 2)."""
    # Luis compró: 1 Teclado (45.00)
    # Total esperado: 45.00
    expected_total = decimal.Decimal('45.00')

    query = "SELECT total_gastado_por_cliente(2);"
    result = execute_query(query)

    actual_total = result[0][0]

    assert actual_total == expected_total, f"Total para Cliente 2 debe ser {expected_total}, pero fue {actual_total}"

def test_total_gastado_cliente_inexistente():
    """Verifica que devuelva 0.00 para un cliente sin pedidos (o inexistente)."""
    expected_total = decimal.Decimal('0.00')

    # Asumiendo que el ID 999 no existe
    query = "SELECT total_gastado_por_cliente(999);"
    result = execute_query(query)

    actual_total = result[0][0]

    assert actual_total == expected_total, f"Total para cliente inexistente debe ser {expected_total}, pero fue {actual_total}"
