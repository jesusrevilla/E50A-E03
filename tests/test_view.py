import psycopg2
from decimal import Decimal # Para manejar números decimales con precisión
from .conftest import db_connection # Asume configuración de conexión a DB

def test_vista_detalle_pedidos_funcionalidad():
    """
    Verifica que la vista 'vista_detalle_pedidos' devuelva los datos correctos
    y que el cálculo del total sea preciso.
    """
    conn = db_connection()
    cur = conn.cursor()
    
    # 1. Consulta la vista
    cur.execute("SELECT nombre_cliente, nombre_producto, cantidad, precio, total_linea FROM vista_detalle_pedidos ORDER BY id_pedido, nombre_producto;")
    resultados = cur.fetchall()
    
    # 2. Definición de los datos esperados (basados en 02_insert_data.sql)
    # Ana Torres: 1 Laptop (1200.00) y 2 Mouse (25.50)
    # Luis Pérez: 1 Teclado (45.00)
    
    datos_esperados = [
        ('Ana Torres', 'Laptop', 1, Decimal('1200.00'), Decimal('1200.00')),
        ('Ana Torres', 'Mouse', 2, Decimal('25.50'), Decimal('51.00')), # 2 * 25.50 = 51.00
        ('Luis Pérez', 'Teclado', 1, Decimal('45.00'), Decimal('45.00')),
    ]
    
    # 3. Verificación de resultados
    
    # Debe tener el número correcto de líneas
    assert len(resultados) == len(datos_esperados), f"Esperado {len(datos_esperados)} filas, pero se obtuvieron {len(resultados)}"
    
    # Verifica que cada fila coincida con los datos esperados, incluyendo el cálculo total
    for i, fila in enumerate(resultados):
        assert fila[0] == datos_esperados[i][0], f"Fila {i}: Cliente incorrecto"
        assert fila[1] == datos_esperados[i][1], f"Fila {i}: Producto incorrecto"
        assert fila[2] == datos_esperados[i][2], f"Fila {i}: Cantidad incorrecta"
        
        # Uso de Decimal para asegurar la precisión en las comparaciones de moneda
        assert fila[3] == datos_esperados[i][3], f"Fila {i}: Precio incorrecto"
        assert fila[4] == datos_esperados[i][4], f"Fila {i}: Total de línea incorrecto"

    cur.close()
    conn.close()

def test_vista_detalle_pedidos_calculo():
    """Verifica el cálculo de total_linea para una línea específica."""
    conn = db_connection()
    cur = conn.cursor()
    
    # Buscamos la línea del Mouse para verificar el cálculo: 2 * 25.50 = 51.00
    cur.execute("SELECT total_linea FROM vista_detalle_pedidos WHERE nombre_producto = 'Mouse';")
    total_calculado = cur.fetchone()[0]
    
    assert total_calculado == Decimal('51.00'), f"Cálculo fallido: Esperado 51.00, obtenido {total_calculado}"
    
    cur.close()
    conn.close()
