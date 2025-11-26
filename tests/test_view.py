import psycopg2
import pytest

def test_vista_detalle_pedidos():
    # Conexión a la base de datos
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    cur = conn.cursor()
    
    # Ejecutar la consulta a la vista
    cur.execute("SELECT * FROM vista_detalle_pedidos;")
    result = cur.fetchall()
    
    # Verificar que los datos sean correctos
    assert result == [('Ana Torres', 1, 1, 1200.00), 
                      ('Ana Torres', 2, 2, 51.00), 
                      ('Luis Pérez', 3, 1, 45.00)]
    
    cur.close()
    conn.close()

