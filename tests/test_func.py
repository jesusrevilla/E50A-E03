import psycopg2
import pytest

# Configuración de conexión (Ajusta estos valores)
DB_CONFIG = "dbname=tu_base_datos user=tu_usuario password=tu_password host=localhost"

def test_total_gastado_por_cliente():
    """
    3. Función: Valida que total_gastado_por_cliente devuelva el monto correcto.
    Según los datos semilla:
    Ana (ID 1) compró: 1 Laptop (1200) + 2 Mouse (51) = 1251.00
    """
    try:
        conn = psycopg2.connect(DB_CONFIG)
        cur = conn.cursor()
        
        # Ejecutamos la función
        cur.execute("SELECT total_gastado_por_cliente(1);")
        resultado = cur.fetchone()[0]
        
        # Validamos
        assert float(resultado) == 1251.00, f"Se esperaba 1251.00, pero se obtuvo {resultado}"
        
        print("✅ Test Función: PASÓ")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Error en test_func: {e}")

if __name__ == "__main__":
    test_total_gastado_por_cliente()
